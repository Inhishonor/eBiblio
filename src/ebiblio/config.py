import os

import tomllib

from src.utils.file_utils import get_project_root

config_path = os.path.join(get_project_root(), "config.toml")
with open(config_path, "rb") as f:
    config = tomllib.load(f)

db_name = config["database"]["name"]
default_owner = config["books"]["owner"]
book_number_per_page = config["books"]["number"]
primary_color = config["style"]["primary_color"]
genre_list = config.get("genres", {}).get("list", [])
