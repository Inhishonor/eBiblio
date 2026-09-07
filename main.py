from nicegui import app, ui
from tortoise.contrib.fastapi import register_tortoise

from src.ebiblio import db_name
from src.frontend.pages import index  # noqa: F401

register_tortoise(
    app,
    db_url=f"sqlite://db/{db_name}.sqlite3",
    modules={
        "models": ["src.models"],
    },
    generate_schemas=True,
)

ui.run(title="eBiblio", show=False, reload=True)
