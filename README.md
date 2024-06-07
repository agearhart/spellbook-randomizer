# Spellbook Randomizer
Script used to generate randomized spellbooks for TTRPGs

## Using the Tool as a Non-Developer
Run the [Generate Spellbook](https://github.com/agearhart/spellbook-randomizer/actions/workflows/generate_spellbook.yml) Action and **refresh the page**.  The spellbook should be printed out at the end of the `Generate Spellbook` step.  It will look like:

```
2024-06-06 15:49:11,991 - SpellbookRandomizer - INFO - Found cleric 2 spellbook contains:
2024-06-06 15:49:11,992 - SpellbookRandomizer - INFO - Level 1  Detect Magic
```

## Installing Dependencies for Local Development
To install all dependencies for the project you must have:
* Python 3.8 or higher
* [pdm](https://pdm-project.org/en/latest/)

then run the command `pdm install` from the root folder.

## Calling from commandline
```
spellbook_randomizer.py [-h] --spells_folder SPELLS_FOLDER --system SYSTEM --caster_class CASTER_CLASS
                               [--caster_level CASTER_LEVEL] [--custom_allocation [CUSTOM_ALLOCATION ...]]

options:
  -h, --help            show this help message and exit
  --spells_folder SPELLS_FOLDER
                        Path or URL to the spells files
  --system SYSTEM       Which game system are we generating a spellbook for? System JSON file must exist in spells folder.
  --caster_class CASTER_CLASS
                        What is the owning caster's class? Must be a class found in System JSON file.
  --caster_level CASTER_LEVEL
                        What is the level of the owning caster? Default 3
  --custom_allocation [CUSTOM_ALLOCATION ...]
                        An array of spells to be found in spellbook per level. Ex: 2 0 1 would give 2 first level and 1 third level spells.
```

### Custom Allocation Example
This will give an elf spell book with 2 first level and 1 third level spells:
```
spellbook_randomizer.py --spells_folder "./spells" --system ose --caster_class elf --caster_level 1 --custom_allocation 2 0 1
```