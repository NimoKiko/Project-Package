from fastapi import FastAPI
# 导入处理跨域中间件
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# tortoise-orm 注册函数
# from tortoise.contrib.fastapi import register_tortoise
# 导入tortoise-orm配置
# from settings import TORTOISE_ORM
# 注册路由
from api.User.routes import user
from api.Audio.routes import audio
from api.Pdf.routes import pdf

app = FastAPI()

app.include_router(user, prefix="/user", tags=["用户模块"])
app.include_router(audio, prefix="/audio", tags=["音频处理模块"])
app.include_router(pdf, prefix="/pdf", tags=["PDF处理模块"])

# 处理跨域的中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# fastapi一旦运行，注册就运行了，实现监控
# register_tortoise(
#     app=app,
#     config=TORTOISE_ORM
# )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
