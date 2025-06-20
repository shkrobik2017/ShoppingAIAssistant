from datetime import datetime

from tortoise import fields, models


class CommonModel(models.Model):
    id: int = fields.IntField(pk=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True