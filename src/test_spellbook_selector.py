import json
import unittest

from pathlib import Path

from spellbook_selector import SpellbookSelector

class SpellbookSelectorTests(unittest.TestCase):
    """Unit tests for the spellbook selector
    """

    spellbook_selector = SpellbookSelector()
    ose_spells: dict = {}

    def setUp(self):
        ose_spells_path: Path = Path.cwd().joinpath("./spells/ose.json")
        ose_spells_str = ose_spells_path.read_text()
        self.ose_spells = json.loads(ose_spells_str)

    def test__golden_path__succeeds(self):
        """OSE level 4 Cleric should have 2 first level and 1 second level spell
        """
        cleric_spells = [spell for spell in self.ose_spells['spells'] if 'cleric' in spell['class']]
        cleric_progression = [p['spell_progression'] for p in self.ose_spells['classes'] if p['class'] == 'cleric']
        cleric_progression = cleric_progression[0]
        cleric_level = 3

        spellbook = self.spellbook_selector.generate_spellbook(cleric_level, cleric_spells, cleric_progression)

        self.assertEqual(len(spellbook), sum(cleric_progression[cleric_level]))

        for spell_level, qty in enumerate(cleric_progression[cleric_level]):
            actual_spell_level = spell_level + 1
            level_spells = [s for s in spellbook if s['level'] == actual_spell_level]
            self.assertEqual(len(level_spells), qty, f"There should be {qty} spells of level {actual_spell_level}")

    def test__empty_progression__returns__empty_spellbook(self):
        """When the progression level has no spells the spellbook should have no spells
        """

        spellbook = self.spellbook_selector.generate_spellbook(3, self.ose_spells['spells'], [])

        self.assertFalse(spellbook)

    def test__empty_spells__returns__empty_spellbook(self):
        """When the progression level has no spells the spellbook should have no spells
        """

        spellbook = self.spellbook_selector.generate_spellbook(3, [], self.ose_spells['classes'][0]['spell_progression'])

        self.assertFalse(spellbook)



if __name__ == '__main__':
    unittest.main()