# 1 创建Python 虚拟环境
```shell
python -m venv myenv # 创建虚拟环境

myenv/Scripts/activate # 激活虚拟环境
```

# 2 安装FastAPI Tortoise-ORM 所需依赖
```shell
pip install fastapi uvicorn

pip install tortoise-orm aerich

pip install tomlkit

pip install aiomysql
```

# 3 创建合理的项目结构并配置数据库相关
- 创建数据库(以Mysql为例)
- 创建 tortoise-orm 配置文件 settings.py
```py
# 数据库配置
TORTOISE_ORM = {
    "connections": {
        # 定义数据库连接，使用MySQL为例
        "mysql": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "root",
                "database": "templateProject",
                "charset": "utf8mb4",
            }
        },
    },
    "apps": {
        # 定义应用模型，这里假设你的模型在`models`模块中
        "models": {
            # 如果有使用aerich进行迁移，需要包含 "aerich.models"
            "models": ["Models.*", "aerich.models"],
            "default_connection": "mysql",  # 默认使用的数据库连接
        },
    },
}

```
- 在main.py中 注册配置
```py
# fastapi一旦运行，注册就运行了，实现监控
register_tortoise(
    app=app,
    config=TORTOISE_ORM
)
```

- 初始化配置
```bash
# 初始化配置只需要使用一次
aerich init -t settings.TORTOISE_ORM

# 初始化数据库，真正迁移表的命令
aerich init-db

# 修改了模型之后需要重新迁移, 这一步会生成一个语句文件, 并没有直接将数据库的表修改
aerich migrate --name 行为 # --name这部分可以不加

# 执行upgrade可以更新表，如果执行downgrade可以将表回溯
aerich upgrade
aerich downgrade

```

# 生成依赖配置文件
```shell
pip freeze > requirements.txt # 生成依赖汇总文件
```