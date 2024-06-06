import random
import sys

from collections import defaultdict
from logging import Formatter, Logger, StreamHandler
from typing import List, Set

from spellbook_randomizer_args import SpellbookRandomizerArgs

def generate_spellbook(args: SpellbookRandomizerArgs, logger: Logger) -> List[str]:
    """Generate a random spellbook from the given arguments

    Args:
        args (SpellbookRandomizerArgs): Parse command line parameters to generate the spellbook

    Returns:
        List[str]: The list of spells found in the book
    """

    spellbook: Set[str] = set()

    spells_by_level = defaultdict(list)

    for spell in args.caster_class_spells:
        spells_by_level[spell['level'] - 1].append(spell)

    progression_level: int = min([len(args.caster_class_progression), args.caster_level])
    spells_for_level: List[int] = args.caster_class_progression[progression_level]

    # for each spell level we want to choose as many spells as can be memorized

    for spell_level, quantity in enumerate(spells_for_level):
        for _ in range(quantity):
            if len(spells_by_level[spell_level]) < 1:
                logger.info(f"Exhausted all spells of {spell_level + 1} level!")
                break  # ran out of spells to choose from

            spell_id = random.randint(0, len(spells_by_level[spell_level]) - 1)
            random_spell_dict: dict = spells_by_level[spell_level][spell_id]

            random_spell: str = f"Level {random_spell_dict['level']}  {random_spell_dict['name']}"

            # if the spell is reversable, flip a coin to see if it's reversed
            if 'reversable' in random_spell_dict and random_spell_dict['reversable'] and random.randint(0,1):
                random_spell += " (Reversed)"

            spellbook.add(random_spell)

            spells_by_level[spell_level].pop(spell_id)

    return spellbook
    

def main():
    """Generate randomized spellbooks for TTRPGs
    """
    logFormatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler = StreamHandler(sys.stdout)
    streamHandler.setFormatter(logFormatter)

    logger: Logger = Logger("SpellbookRandomizer")
    logger.addHandler(streamHandler)

    args: SpellbookRandomizerArgs = SpellbookRandomizerArgs(logger)
    args.parse_args()

    spells: List[str] = generate_spellbook(args, logger)

    logger.info(f"Found {args.caster_class} {args.caster_level + 1} spellbook contains:")
    for spell in sorted(spells):
        logger.info(spell)

if __name__ == "__main__":
    main()