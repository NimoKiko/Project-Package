'''
用户模块接口
'''
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, field_validator
from models.User import *

user = APIRouter()


@user.get("/")
async def get_all_user():

    user = await User.all()  # 查询全部
    return user


@user.get("/{u_id}")
async def get_user(u_id: int):

    # 使用 filter() 若表中没有数据会返回空列表
    # 或者使用 get_or_none()：如果你查询的是 主键或唯一字段（如 id、username），并且希望代码更简洁，就用 get_or_none()。
    user = await User.get_or_none(id=u_id)
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return {
        "msg": "查询成功",
        "user": user
    }


class UserInfo(BaseModel):
    username: str | None = None
    password: str | None = None

    # 使用field_validator()做字段校验
    @field_validator("password")
    def password_rule(cls, value):
        if len(value) < 6:
            raise ValueError(" 密码必须大于6位")
        return value


@user.post("/")
async def add_user(user_info: UserInfo):

    user = await User.create(username=user_info.username, password=user_info.password)

    return user


@user.put("/{u_id}")
async def update_user(u_id: int, user_info: UserInfo):

    # 将需要更新的数据转换为字典
    # data = user_info.model_dump()
    '''
    字典推导式一般形式：
    {k: v for k, v in iterable if condition}
    '''
    data = {k: v for k, v in user_info.model_dump().items() if v is not None}

    print(data)

    update_result = await User.filter(id=u_id).update(**data)

    if update_result:
        return f"更新了ID为{u_id}的用户"
    else:
        # raise HTTPException(status_code=500, detail="Internal Server Error")
        return f"更新了{update_result}条记录"


@user.delete("/{u_id}")
async def delete_user(u_id: int):

    delete_result = await User.filter(id=u_id).delete()

    if not delete_result:
        raise HTTPException(status_code=404, detail=f"主键为{u_id}的用户不存在")

    return f"删除ID为{u_id}的用户成功！"
