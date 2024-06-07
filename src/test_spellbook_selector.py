import json
import unittest

from pathlib import Path
from typing import List, Set

from spellbook_selector import SpellbookSelector

class SpellbookSelectorTests(unittest.TestCase):
    """Unit tests for the spellbook selector
    """

    spellbook_selector = SpellbookSelector()
    ose_spells: dict = {}
    cleric_spells: List[dict] = []
    cleric_progression: List[List[int]] = []

    def setUp(self):
        ose_spells_path: Path = Path.cwd().joinpath("./spells/ose.json")
        ose_spells_str = ose_spells_path.read_text()
        self.ose_spells = json.loads(ose_spells_str)

        self.cleric_spells = [spell for spell in self.ose_spells['spells'] if 'cleric' in spell['class']]
        cleric_progression = [p['spell_progression'] for p in self.ose_spells['classes'] if p['class'] == 'cleric']
        self.cleric_progression = cleric_progression[0]

    def test__ose_json_properly_formatted(self):
        """OSE.json should have the expected format
        """
        self.assertIn('classes', self.ose_spells)

        progression_classes: Set[str] = set()
        spell_classes: Set[str] = set()

        for clazz in self.ose_spells['classes']:
            self.assertIn('class', clazz)
            self.assertIn('spell_progression', clazz)

            self.assertIsInstance(clazz['class'], str)

            progression_classes.add(clazz['class'])

            for progression in clazz['spell_progression']:
                self.assertIsInstance(progression, list)

                for level in progression:
                    self.assertIsInstance(level, int)

        self.assertIn('spells', self.ose_spells)

        for spell in self.ose_spells['spells']:
            self.assertIn('name', spell)
            self.assertIsInstance(spell['name'], str)

            self.assertIn('reversable', spell)
            self.assertIsInstance(spell['reversable'], bool)

            self.assertIn('level', spell)
            self.assertIsInstance(spell['level'], int)

            self.assertIn('class', spell)
            self.assertIsInstance(spell['class'], list)

            for clazz in spell['class']:
                self.assertIsInstance(clazz, str)
                spell_classes.add(clazz)

        self.assertEqual(progression_classes, spell_classes)

    def test__golden_path__succeeds(self):
        """OSE level 4 Cleric should have 2 first level and 1 second level spell
        """

        cleric_level = 3

        spellbook = self.spellbook_selector.generate_spellbook(cleric_level, self.cleric_spells, self.cleric_progression)

        self.assertEqual(len(spellbook), sum(self.cleric_progression[cleric_level]))

        for spell_level, qty in enumerate(self.cleric_progression[cleric_level]):
            actual_spell_level = spell_level + 1
            level_spells = [s for s in spellbook if s['level'] == actual_spell_level]
            self.assertEqual(len(level_spells), qty, f"There should be {qty} spells of level {actual_spell_level}")

    def test__custom_allocation__returns__expected_spellbook(self):
        """When provided a custom allocation a spellbook is returned containing that allocation
        """
        custom_allocation = [3, 2, 1]
        spellbook = self.spellbook_selector.generate_spellbook(1, self.cleric_spells, self.cleric_progression, custom_allocation)

        self.assertEqual(len(spellbook), sum(custom_allocation))

        for spell_level, qty in enumerate(custom_allocation):
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

        spellbook = self.spellbook_selector.generate_spellbook(3, [], self.cleric_progression)

        self.assertFalse(spellbook)


if __name__ == '__main__':
    unittest.main()