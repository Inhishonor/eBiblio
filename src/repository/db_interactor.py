from src import models


async def get_books_by_tab(tab_name):
    if tab_name == "All":
        books = await get_books_by_genre(None)
    elif tab_name == "Checked Out":
        books = await get_books_by_checkout()
    else:
        books = await get_books_by_genre(tab_name)
    return books


async def get_books_by_genre(genre):
    if not genre:
        books: list[models.Book] = await models.Book.all()
    else:
        books: list[models.Book] = await models.Book.filter(
            genre=models.genres.Genres(genre)
        )
    return books


async def get_books_by_checkout():
    books: list[models.Book] = await models.Book.filter(checked_out=True)
    return books


async def save_book(book):
    await book.save()


def get_field_default(model, field_name):
    default = model._meta.fields_map[field_name].default
    return default() if callable(default) else default
