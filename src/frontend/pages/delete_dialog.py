from nicegui import ui

from src import models

from . import index


async def confirm_deletion(book):
    with ui.dialog() as dialog, ui.card():
        ui.label("Are you sure?")

        with ui.row():
            ui.button("Yes", on_click=lambda: dialog.submit("Yes"))
            ui.button("No", on_click=lambda: dialog.submit("No"))

    dialog.open()
    result = await dialog

    if result == "Yes":
        await delete(book)
        ui.notify("Book deleted")
        index.list_of_books.refresh()
    else:
        ui.notify("Deletion cancelled")


async def delete(book: models.Book) -> None:
    await book.delete()
