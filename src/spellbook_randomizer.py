import random
import sys

from collections import defaultdict
from logging import Formatter, Logger, StreamHandler
from typing import List, Set

from spellbook_randomizer_args import SpellbookRandomizerArgs
from spellbook_selector import SpellbookSelector

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

    spellbook_selector:SpellbookSelector = SpellbookSelector(logger)

    spells: List[dict] = spellbook_selector.generate_spellbook(args.caster_level, args.caster_class_spells, args.caster_class_progression)
    pretty_spells: List[str] = spellbook_selector.prety_print_spells(spells)

    logger.info(f"Found {args.caster_class} {args.caster_level + 1} spellbook contains:")
    for spell in pretty_spells:
        logger.info(spell)

if __name__ == "__main__":
    main()