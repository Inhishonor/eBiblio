from enum import Enum

from src.ebiblio import genre_list


def create_genre_enum(genres: list[str]) -> type[Enum]:
    enum_dict = {genre.upper().replace(" ", "_"): genre for genre in genres}
    return Enum("Genres", enum_dict, type=str)


Genres = create_genre_enum(genre_list)
