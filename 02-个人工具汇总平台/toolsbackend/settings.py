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
            "models": ["models.User", "aerich.models"],
            "default_connection": "mysql",  # 默认使用的数据库连接
        },
    },
}
