from tortoise.queryset import Q

from src import models


async def search_db(query: str):
    if query.startswith("author: "):
        return await search_by_author(query.removeprefix("author: "))
    elif query.startswith("title: "):
        return await search_by_title(query.removeprefix("title: "))
    elif query.startswith("subject: "):
        return await search_by_subject(query.removeprefix("subject: "))
    elif query.startswith("owner: "):
        return await search_by_owner(query.removeprefix("owner: "))
    else:
        return await search_general(query)


async def search_general(query: str):
    return await models.Book.filter(
        Q(name__icontains=query)
        | Q(author__icontains=query)
        | Q(subject__icontains=query)
    )

async def search_by_author(query: str):
    return await models.Book.filter(Q(author__icontains=query)).all()


async def search_by_title(query: str):
    return await models.Book.filter(Q(name__icontains=query)).all()


async def search_by_subject(query: str):
    return await models.Book.filter(Q(subject__icontains=query)).all()


async def search_by_owner(query: str):
    return await models.Book.filter(Q(owner__icontains=query)).all()
