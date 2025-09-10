from tortoise.models import Model
from tortoise import fields

# 用户类


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, description="昵称")
    password = fields.CharField(max_length=32, description="密码")
