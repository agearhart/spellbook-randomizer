import random

from collections import defaultdict
from logging import Logger
from typing import List, Set

class SpellbookSelector:
    """Class used to abstract out the random spell selection
    """

    logger: Logger = None

    def __init__(self, in_logger: Logger = None) -> None:
        if in_logger:
            self.logger = in_logger
        else:
            self.logger = Logger("SpellbookSelector")


    def generate_spellbook(self,
                           caster_level: int,
                           caster_class_spells: List[dict],
                           caster_class_progression: List[List[int]],
                           custom_allocation: List[int] = []) -> List[dict]:
        """Select spells for the spellbook based on the owning caster's class and level

        Args:
            caster_level (int): The level of the owning caster
            caster_class_spells (List[dict]): Spells available to the caster class
            caster_class_progression (List[List[int]]): Array of how many spells slots per level the caster has access
            custom_allocation (List[int]): A custom allocation of spells per level to choose

        Returns:
            List[dict]: _description_
        """

        spells_by_level = defaultdict(list)
        spells_for_level: List[int] = []
        randomly_selected_spells: List[dict] = []

        for spell in caster_class_spells:
            spells_by_level[spell['level'] - 1].append(spell)

        if not custom_allocation:
            progression_level: int = min([len(caster_class_progression), caster_level])

            if len(caster_class_progression) - 1 < progression_level:
                self.logger.error(f"pell progression list is smaller than {progression_level}")
                return []

            spells_for_level = caster_class_progression[progression_level]
        else:
            spells_for_level = custom_allocation

        # for each spell level we want to choose as many spells as can be memorized
        for spell_level, quantity in enumerate(spells_for_level):
            spells_in_level = len(spells_by_level[spell_level])
            if(quantity > spells_in_level):
                self.logger.info(f"Exhausted all spells of {spell_level + 1} level!")
                quantity = spells_in_level

            randomly_selected_spells += [spells_by_level[spell_level][spell_id] for spell_id in random.sample(range(spells_in_level), quantity)]

        return randomly_selected_spells

    def prety_print_spells(self, spellbook: List[dict]) -> List[str]:
        """Turn the spellbook dictionaries into descriptive lines

        Args:
            spellbook (List[dict]): The spells in the spellbook

        Returns:
            List[str]: Nicely formatted spells
        """

        spell_descriptions = [f"Level {spell['level']} {spell['name']}" if random.randint(0,1) else f"Level {spell['level']} {spell['name']} Reversed" for spell in spellbook if 'name' in spell and 'level' in spell]

        return sorted(spell_descriptions)

