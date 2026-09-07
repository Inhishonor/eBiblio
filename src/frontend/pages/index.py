from nicegui import app, ui

from src import models
from src.ebiblio import book_number_per_page, primary_color
from src.repository.db_interactor import get_books_by_tab, get_field_default, save_book
from src.search.search import search_db

from . import delete_dialog

app.colors(primary=primary_color)

tab_state = {
    "All": 1,
    "Checked Out": 1,
    **{genre.value: 1 for genre in models.genres.Genres},
}
PAGE_SIZE = book_number_per_page


def book_card(book):
    with (
        ui.card().classes("w-full md:max-w-9/10 items-center"),
        ui.row(align_items=True).classes(
            "items-center flex-wrap justify-center w-full"
        ),
    ):
        checked_out_button(book)
        ui.input("Name").bind_value(book, "name").on(
            "blur", lambda _, b=book: save_book(b)
        )
        ui.input("Author").bind_value(book, "author").on(
            "blur", lambda _, b=book: save_book(b)
        )
        ui.select(
            options=[item.value for item in models.genres.Genres],
            label="Genre",
        ).bind_value(book, "genre").on("blur", lambda _, b=book: save_book(b)).classes(
            "w-32 flex-shrink-0"
        )
        ui.input("Shelf").bind_value(book, "shelf").on(
            "blur", lambda _, b=book: save_book(b)
        )
        ui.input("Subject").bind_value(book, "subject").on(
            "blur", lambda _, b=book: save_book(b)
        )
        ui.input("Notes").bind_value(book, "notes").on(
            "blur", lambda _, b=book: save_book(b)
        )
        ui.input("Owner").bind_value(book, "owner").on(
            "blur", lambda _, b=book: save_book(b)
        )
        with ui.button(
            icon="delete",
            on_click=lambda _, b=book: delete_dialog.confirm_deletion(b),
        ).props("flat"):
            ui.tooltip("Delete this book")


async def toggle_checked_out(book):
    book.checked_out = not book.checked_out
    await book.save(update_fields=["checked_out"])
    list_of_books.refresh()


@ui.refreshable
def checked_out_button(book):
    with (
        ui.button(
            icon="assignment_return" if book.checked_out else "task_alt",
            on_click=lambda _, b=book: toggle_checked_out(b),
        )
        .classes("m-2")
        .props("flat")
    ):
        ui.tooltip("Return this book" if book.checked_out else "Checkout this book")


@ui.refreshable
async def list_of_books(tab_name):
    books = await get_books_by_tab(tab_name)
    max_pages = max(1, (len(books) + PAGE_SIZE - 1) // PAGE_SIZE)

    tab_state[tab_name] = min(tab_state[tab_name], max_pages)

    start = (tab_state[tab_name] - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    def on_page_change(e):
        tab_state[tab_name] = e.value
        list_of_books.refresh()

    with ui.scroll_area().classes("w-full flex-grow").style("height: 75vh"):
        if not books:
            with (
                ui.column().classes("w-full items-center"),
                ui.card().classes("w-full md:max-w-2/3 items-center text-md"),
            ):
                ui.label("Sorry, no books in this genre!")
        else:
            with ui.column().classes("w-full items-center"):
                paginated_books = books[::-1][start:end]
                for book in paginated_books:
                    book_card(book)
        with ui.row().classes("w-full justify-center pb-4"):
            ui.pagination(
                1,
                max_pages,
                direction_links=True,
                value=tab_state[tab_name],
                on_change=on_page_change,
            )


@ui.page("/")
async def index():
    async def create() -> None:
        if any(
            not field.value for field in (owner, name, author, genre, shelf, subject)
        ):
            ui.notify("Please double check that all fields are filled in.")
            return
        await models.Book.create(
            owner=owner.value,
            name=name.value,
            author=author.value,
            genre=genre.value,
            shelf=shelf.value,
            subject=subject.value,
            notes=notes.value,
        )
        await list_of_books.refresh()
        owner.value = get_field_default(models.Book, "owner")
        name.value = ""
        author.value = ""
        genre.value = None
        shelf.value = ""
        subject.value = ""
        notes.value = ""

    with ui.tabs().classes("w-full") as tabs:
        all_tab = ui.tab("All")
        checked_out_tab = ui.tab("Checked Out")

        tab_elements = {genre: ui.tab(genre.value) for genre in models.genres.Genres}
        search_tab = ui.tab("Search")

    with ui.tab_panels(
        tabs,
        value=all_tab,
    ).classes("w-full"):
        with ui.tab_panel(all_tab):
            ui.separator().classes("bg-[#523211]")
            await list_of_books("All")

        with ui.tab_panel(checked_out_tab):
            ui.separator().classes("bg-[#523211]")
            await list_of_books("Checked Out")

        for genre in models.genres.Genres:
            with ui.tab_panel(tab_elements[genre]):
                ui.separator().classes("bg-[#523211]")
                await list_of_books(genre.value)

        with ui.tab_panel(search_tab):
            ui.separator().classes("bg-[#523211]")

            async def handle_search(event):
                query = event.value
                results_container.clear()

                if not query:
                    docs_container.visible = True
                    return
                docs_container.visible = False
                spinner.visible = True
                try:
                    results = await search_db(query)
                    with (
                        results_container,
                        ui.scroll_area()
                        .classes("w-full flex-grow")
                        .style("height: 75vh"),
                    ):
                        if not results:
                            with (
                                ui.column().classes("w-full items-center"),
                                ui.card().classes(
                                    "w-full md:max-w-2/3 items-center text-md"
                                ),
                            ):
                                ui.label("No books found.")
                        else:
                            with ui.column().classes("w-full items-center"):
                                for book in reversed(results):
                                    book_card(book)
                finally:
                    spinner.visible = False

            with ui.column().classes("w-full items-center gap-0"):
                with ui.row().classes("w-9/10 items-center gap-0"):
                    search_bar = (
                        ui.input(label="Search", on_change=handle_search)
                        .classes("w-9/10")
                        .props("borderless")
                    )
                    ui.button(
                        icon="close", on_click=lambda: search_bar.set_value("")
                    ).props("flat").classes("align-right")
                    ui.separator().classes("bg-[#523211]")
                spinner = ui.spinner(size="lg")
                spinner.visible = False

            results_container = ui.column().classes("w-full items-center")
            docs_container = ui.column().classes("w-full items-center")
            with docs_container, ui.card().classes("w-1/3 items-center"):
                ui.label("Search Operators").classes("text-xl font-medium")
                ui.label(
                    "In order to narrow down your search you have a few options:"
                ).classes("text-lg")
                ui.separator().classes("bg-[#523211]")
                with ui.row().classes("w-full items-center"):
                    ui.button(
                        "author:", on_click=lambda: search_bar.set_value("author: ")
                    ).classes("w-1/2")
                    ui.label("Search only for authors").classes("text-lg")
                with ui.row().classes("w-full items-center"):
                    ui.button(
                        "title:", on_click=lambda: search_bar.set_value("title: ")
                    ).classes("w-1/2")
                    ui.label("Search only for book titles").classes("text-lg")
                with ui.row().classes("w-full items-center"):
                    ui.button(
                        "subject:", on_click=lambda: search_bar.set_value("subject: ")
                    ).classes("w-1/2")
                    ui.label("Search only for subjects").classes("text-lg")
                with ui.row().classes("w-full items-center"):
                    ui.button(
                        "owner:", on_click=lambda: search_bar.set_value("owner: ")
                    ).classes("w-1/2")
                    ui.label("Search only for book owners").classes("text-lg")

    with (
        ui.column().classes("fixed bottom-0 w-full items-center p-8"),
        ui.row().classes("items-center px-4 bg-white"),
    ):
        name = ui.input(label="Name")
        author = ui.input(label="Author")
        genre = ui.select(
            options=[item.value for item in models.genres.Genres],
            with_input=True,
            label="Genre",
        )
        shelf = ui.input(label="Shelf")
        subject = ui.input(label="Subject")
        notes = ui.input(label="Notes")
        owner = ui.input(
            label="Owner",
            value=get_field_default(models.Book, "owner"),
        )
        ui.button("Add book", on_click=create)
