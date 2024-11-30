# chess-rating
tool to store and modify ELO chess ratings

## Installation

This project uses the [poetry](https://python-poetry.org/) build tool.

First, `git clone` the project and `cd` into the project root folder

Then, install the project with all dependencies in a virtual environment using `poetry install`

Enter a new shell using `poetry shell` (optionally set environment variable `VIRTUAL_ENV_DISABLE_PROMPT=1` to disable the prompt prefix).


## Usage

Follow the steps outlined in the [Installation](#installation) section.

Run the script using `poetry run chess_rating` followed by command line arguments.

### Command line usage

```text
usage: chess_rating.cmd [-h] (-n | -o) [-p PLAYER_NAMES] [-d] [-r] dir

Chess rating program to store, access and modify chess rating scores for players. Note: Autosave is on by default, ie, all changes will be saved automatically. To discard changes,       
choose exit and then choose not save. Alternatively, turn off for that session by passing `-d` switch. Then, to save changes, choose exit and then choose save.

positional arguments:
  dir                   directory to store results in / retrieve results from

options:
  -h, --help            show this help message and exit
  -n, --new             make a new game
  -o, --open            open an existing game
  -p PLAYER_NAMES, --player-names PLAYER_NAMES
                        single string of space seperated single-word player names for a new game
  -d, --dont-save       turn off autosave. will require manually saving changes before exiting
  -r, --repl            drop into REPL instead of interactive menu (for advanced users)
```

### Examples

## Developing

1. Download the source code.
2. Open up a terminal.
3. `cd` into the project root †.
4. Install the project using steps outlined in [Installation](#installation)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Notes

See [https://en.wikipedia.org/wiki/Elo_rating_system?oldformat=true#Combating_deflation](https://en.wikipedia.org/wiki/Elo_rating_system?oldformat=true#Combating_deflation)

## License

[MIT](https://choosealicense.com/licenses/mit/)

---

† Project root is the folder named "chess-rating" at the top level, i.e., it is shalloww

†† Source root is the folder named "chess_rating" inside another folder named "chess-rating", i.e., it is deep (nested)

