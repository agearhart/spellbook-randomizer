import argparse
import json
import requests
import validators

from logging import Logger
from pathlib import Path
from typing import List

class SpellbookRandomizerArgs:
    """Arguments for creating randomized spellbooks"""

    logger: Logger = None

    spells_folder: str = None
    spells_folder_is_url: bool = False
    system: str = None
    caster_level: int = 3
    caster_class: str = None

    caster_class_spells: List[dict] = []
    caster_class_progression: List[List[int]] = []


    def __init__(self, inLogger: Logger = None) -> None:
        if inLogger:
            self.logger = inLogger
        else:
            self.logger = Logger("SpellbookRandomizerArgs")

    def __validate(self) -> bool:
        """Validates the passed in parameters

        Returns:
            bool: True if the parameters are valid; False otherwise
        """
        spells_path_str = self.get_spells_path()

        spells_raw: str = None

        if validators.url(spells_path_str):
            # get the JSON text from the URL
            response = requests.get(spells_path_str, verify=False)

            if response.ok:
                spells_raw = response.text
            else:
                self.logger.error(f"Cannot find spells at [{spells_path_str}]!")
                return False
        else:
            # should be a folder path
            spells_path: Path = Path(spells_path_str)

            if not spells_path.exists():
                self.logger.error(f"Cannot find spells at [{spells_path_str}]!")
                return False
            
            spells_raw = spells_path.read_text()

        spells_dict: dict = json.loads(spells_raw)

        classes:List[dict] = spells_dict['classes'] if 'classes' in spells_dict else []
        spells:List[dict] = spells_dict['spells'] if 'spells' in spells_dict else []

        self.caster_class_progression = [x['spell_progression'] for x in classes if 'class' in x and x['class'] == self.caster_class and 'spell_progression' in x]
        self.caster_class_progression = self.caster_class_progression[0]  # I'm not sure why this above isn't giving me this already
        self.caster_class_spells = [x for x in spells if 'class' in x and x['class'] == self.caster_class]

        if len(self.caster_class_progression) < 1:
            self.logger.error(f"Cannot find spell progression for class [{self.caster_class}] in [{spells_path_str}]!")
            return False
        
        if len(self.caster_class_spells) < 1:
            self.logger.error(f"Cannot find spells for class [{self.caster_class}] in [{spells_path_str}]!")
            return False
        
        return True

    def get_spells_path(self)-> str:
        """Generate the path to the spells JSON file

        Returns:
            str: the path to the spells JSON file
        """

        spells_path:str = f"{self.spells_folder}/{self.system}.json"

        return spells_path

    def parse_args(self):
        """Parse the commandline parameters passed in
        """

        arg_parser = argparse.ArgumentParser()

        arg_parser.add_argument("--spells_folder", required=True, help="Path or URL to the spells files")
        arg_parser.add_argument("--system", required=True, help="Which game system are we generating a spellbook for?  System JSON file must exist in spells folder.")
        arg_parser.add_argument("--caster_class", required=True, help="What is the owning caster's class?  Must be a class found in System JSON file.")
        arg_parser.add_argument("--caster_level", type=int, default=self.caster_level, help=f"What is the level of the owning caster? Default {self.caster_level}")

        args = arg_parser.parse_args()

        self.spells_folder = args.spells_folder
        self.system = args.system
        self.caster_level = args.caster_level - 1 
        self.caster_class = args.caster_class

        if not self.__validate():
            self.logger.error("Invalid parameters detected!")
            raise ValueError("Invalid parameters detected!")
