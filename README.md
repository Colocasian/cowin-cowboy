# cowin-cowboy

Python utility to check for available COVID-19 vaccination slots.

Note, that this is just a hobby project I wrote to learn the ins-and-outs of
Python. But I do hope to keep the scripts up-to-date.

## Requirements

`cowin_cowboy` module requires Python>=3.5 for running. For running Black,
Python>=3.6.2 is required.

To install dependencies, it is first recommended that you create a virtualenv,
then install the dependencies.

```sh
# Setup venv, and source it
python -m venv venv
# For sourcing in *nix for bash/zsh
source ./venv/bin/activate
# For sourcing in Windows using cmd.exe
./venv/bin/activate.bat

# To install cowboy.py dependencies
python -m pip install -r requirements.txt

# Only if you want to contribute code
# To install dev dependencies (Black + pre-commit)
python -m pip install -r requirements-dev.txt
# Set up pre-commit hooks
pre-commit install
```

- `cowin_cowboy` module requires `requests-toolbelt`
- `cowboy.py` requires `cowin_cowboy` and `appdirs`

## Usage

To use the `cowboy.py` script, simply run `python3 ./cowboy.py`

Optionally, you can specify logging verbosity by `-l <log-level>`. You can
also point the script to a custom config file with `-c <path/to/config`.

To see all available options, do `python3 ./cowboy.py -h`

## Configuration

`cowboy.py` expects a json file (the default config path can be queried by
`python3 ./cowboy.py --config-path`), with the following structure:

- A `"locations"` table, with any combination of these three sub-keys:
  * `"pincodes"`: Array of PIN codes, as strings.
  * `"district_ids"`: Array of district IDs to query.
  * `"center_ids"`: Array of center IDs to query. Note: Although API endpoint
    exists to check for center ID, (atleast till now) it just returns error
    code 403. Thus, the center ID endpoint just exists for when they open up
    the CalendarByCenter API endpoint.

- A `"filters"` table, with any combination of the following fields:
  * `"capacity"`: Either an integer, or a table with fields `"dose1"` and
    `"dose2"` fields. If an integer, checks for total available slots. If
    separated into dose 1 and dose 2, check for each center having both dose 1
    capacity >= `"dose1"` and dose 2 capacity >= `"dose2"`.
  * `"age"`: Integer, specifying minimum age allowed.
  * `"vaccine"`: Array of (case-insensitive) strings, with all the wanted
    vaccine variants.
  * `"feeType"`: A string, saying whether free or paid

All the fields are optional, except atleast one location needs to be specified.

### Sample Configuration

```json
{
  "locations": {
    "pincodes": ["787349", "312244", "763257"],
    "district_ids": [591, 218]
  },
  "filters": {
    "capacity": {
      "dose1": 2,
      "dose2": 0
    },
    "age": 30,
    "vaccine": ["covaxin", "covishield", "sputnik"],
    "feeType": "Free"
  }
}
```

## TODO

- [x] Check for available centers for the given district and PIN code.
- [x] Filter available centers based on various criteria.
- [ ] Book vaccination appointments.

## Licensing

Licensed under the GNU General Public License v3.0, or any later version.
