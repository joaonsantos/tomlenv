# TOMLenv

Environment wrapped TOML.

## Getting Started

### Install the library

Using pip:
```sh
$ pip install tomlenv
```

Using pipenv:
```sh
$ pipenv install tomlenv
```

Using poetry:
```sh
$ poetry add tomlenv
```

### Basic Usage

Assuming you have this TOML file:
```toml
token = "dev"
debug = false
```

And this environment set:
```sh
TOMLENV_DEBUG=true
```

Create your configuration dataclass and parse configuration into it:
```python
import tomlenv

class Config:
    token: str | None = ""
    enabled: bool = False

config = Config()
parser = tomlenv.Parser()

parser.load(config)

# You can now access the fields of your fully typed Config class
# that contains values from a TOML config file and the environment.
#
# For example:

token = config.token
debug = config.debug
print(token) # prints "dev"
print(debug) # prints True
```

## Tests

This project uses [Poetry](https://python-poetry.org/) and [GNU Make](https://www.gnu.org/software/make/).

Run tests from the project root with:
```sh
$ make test
```

To get a coverage report:
```sh
$ make cov
```