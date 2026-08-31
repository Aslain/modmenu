# Examples

Four mods, each one a step larger than the last.

| File | Shows |
| --- | --- |
| [01_minimal.py](01_minimal.py) | The whole contract in forty lines: register, read the saved values, run |
| [02_controls.py](02_controls.py) | One of every control type and what each stores |
| [03_layout.py](03_layout.py) | Tabs, a group behind a master switch, and options that appear or grey out |
| [04_highlights.py](04_highlights.py) | Marking options as new, and getting the flares back to look at them |

Copy one into `res_mods/<game version>/scripts/client/gui/mods/` as
`mod_<something>.py` and call its `init()` from your own startup.

Only the first one guards the import. The others assume the menu is there so the code
stays readable, but a mod you ship should do what the first one does and run on its own
defaults when nobody has the menu installed.

The guide is in [../docs/api.md](../docs/api.md) and the full list of everything is in
[../docs/reference.md](../docs/reference.md).
