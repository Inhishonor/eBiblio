from tortoise import fields, models

from src.ebiblio import default_owner

from .genres import Genres


class Book(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    author = fields.CharField(max_length=255)
    shelf = fields.CharField(max_length=10)
    subject = fields.CharField(max_length=255)
    genre = fields.CharEnumField(enum_type=Genres)
    checked_out = fields.BooleanField(default=False)
    owner = fields.CharField(max_length=255, default=default_owner)
    notes = fields.CharField(max_length=255)
