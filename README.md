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