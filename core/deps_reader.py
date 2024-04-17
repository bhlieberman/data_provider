import tomllib
from pathlib import Path
from core.data_provider import Deps

toml_data = None
with open(Path("./config/html.toml"), "rb") as f:
    toml_data = tomllib.load(f)

deps = Deps(**toml_data)

deps.meta