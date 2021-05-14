# cowin-cowboy

Python utility to check for available COVID-19 vaccination slots.

Licensed under the GNU General Public License v3.0, or any later version.

## Requirements

`cowin_cowboy` module requires Python>=3.5 for running. For running Black,
Python>=3.6.2 is required.

To install dependencies, run:

```sh
# To install main.py dependencies
python -m pip install -r requirements.txt
# To install dev dependencies (Black + pre-commit)
python -m pip install -r requirements-dev.txt
```

- `cowin_cowboy` module requires `requests-toolbelt`
- `main.py` requires `cowin_cowboy` and `appdirs`

## TODO

- [x] Check for available centers for the given district and PIN code.
- [x] Filter available centers based on various criteria.
- [ ] Book vaccination appointments.
