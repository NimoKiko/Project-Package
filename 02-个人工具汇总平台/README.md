# 个人工具汇总平台

一个简洁的个人实用工具平台，采用前后端分离架构，提供音频格式转换和 PDF 文件处理功能。

![技术栈](https://img.shields.io/badge/前端-Vue%203%20+%20TypeScript%20+%20Vite-blue)
![技术栈](https://img.shields.io/badge/后端-Python%20+%20FastAPI-green)
![UI](https://img.shields.io/badge/UI-Obsidian%20Command%20Dark-purple)

---

## 功能特性

| 工具 | 功能描述 |
|------|---------|
| **音频处理** | |
| ├─ 格式转换 | 支持 MP3、FLAC、OGG、WAV、MP4 格式互转 |
| └─ 音频提取 | 从视频文件（MP4/AVI/MOV/MKV/WEBM）中提取音频 |
| **PDF 处理** | |
| ├─ PDF 合并 | 将两个 PDF 文件按交替页码合并 |
| ├─ PDF 逆序 | 将 PDF 页面顺序反转 |
| ├─ PDF 权限解锁 | 移除 PDF 的复制/打印/编辑限制 |
| └─ PDF 转 Word | 将 PDF 转换为可编辑的 Word 文档 |

---

## 技术架构

### 前端 (`tools/`)
- **框架**: Vue 3 + Composition API
- **语言**: TypeScript 5.8
- **构建**: Vite 7
- **UI 库**: Element Plus (中文 locale)
- **状态管理**: Pinia
- **样式**: SCSS + CSS Variables
- **设计主题**: Obsidian Command — 深色专业工具风格
- **布局**: 左侧功能列表 + 右侧内容区（可扩展多工具）

### 后端 (`toolsbackend/`)
- **框架**: FastAPI 0.116
- **语言**: Python 3.11+
- **运行**: Uvicorn
- **包管理**: [uv](https://docs.astral.sh/uv/)
- **依赖**:
  - `pypdf2` — PDF 合并、逆序、权限解锁
  - `pdf2docx` — PDF 转 Word
  - `pydub` — 音频格式转换
  - `ffmpeg-python` — 视频音频提取（需系统安装 FFmpeg）
  - `pycryptodome` — PDF 加密处理
  - `fastapi` / `pydantic` v2 — API 框架
  - `tortoise-orm` — ORM（当前未启用）

---

## 快速开始

### 前端启动

```bash
cd tools
npm install
npm run dev
```

访问 http://localhost:5173

### 后端启动（使用 uv）

```bash
cd toolsbackend

# 首次运行：创建环境并安装依赖
uv sync

# 启动服务
uv run python main.py
```

**常用 uv 命令：**

```bash
# 添加新依赖
uv add package-name

# 移除依赖
uv remove package-name

# 更新所有依赖
uv sync --upgrade

# 仅安装生产依赖（不含 dev）
uv sync --no-dev
```

后端运行在 http://localhost:8000

### 配置

前端通过 `tools/public/config.json` 配置后端地址，默认：

```json
{
  "BASE_URL": "http://127.0.0.1:8000"
}
```

---

## 项目结构

```
.
├── tools/                    # 前端 Vue 3 项目
│   ├── src/
│   │   ├── components/       # 公共组件 (Header, Side)
│   │   ├── views/            # 页面视图
│   │   │   └── modules/      # 工具模块 (音频、PDF)
│   │   │       ├── audio/    # 音频处理工具（格式转换、音频提取）
│   │   │       └── pdf/      # PDF 工具（合并、逆序、解锁、转Word）
│   │   ├── api/              # API 接口封装
│   │   ├── stores/           # Pinia 状态管理
│   │   └── assets/scss/      # 样式文件
│   └── public/config.json    # 运行时配置
│
└── toolsbackend/             # 后端 FastAPI 项目
    ├── main.py               # 应用入口
    ├── pyproject.toml        # 项目配置与依赖（uv 管理）
    ├── uv.lock               # 依赖锁定文件
    ├── .python-version       # Python 版本指定
    └── api/                  # 路由模块
        ├── Audio/
        └── Pdf/
```

---

## 开发说明

- 前端使用 Element Plus 组件库，但已完全自定义主题样式
- **音频/PDF 模块**采用左侧功能列表 + 右侧内容区的可扩展布局（工具箱模式）
- 支持拖拽上传文件，转换后自动下载
- 后端 CORS 完全开放，仅限本地开发使用

### 添加新工具模块

参考现有音频/PDF模块的结构：

```
src/views/modules/yourModule/
├── yourModule.vue      # 主入口（工具箱布局）
├── feature1.vue        # 功能1组件
└── feature2.vue        # 功能2组件
```

主入口文件使用动态组件切换不同功能，便于扩展。

---

## 环境依赖

### 必需：FFmpeg（音频功能依赖）

**音频格式转换**和**视频音频提取**功能依赖 FFmpeg，请根据系统安装：

**Windows:**
```bash
# 使用 chocolatey
choco install ffmpeg

# 或手动下载：https://www.gyan.dev/ffmpeg/builds/
# 下载后解压并将 bin 目录添加到系统 PATH
```

**macOS:**
```bash
# 使用 Homebrew（推荐）
brew install ffmpeg

# 或手动下载：https://ffmpeg.org/download.html#build-mac
```

**验证安装：**
```bash
ffmpeg -version
```

---

## GitHub 部署流程

### 上传到 GitHub

1. **在 GitHub 创建仓库**（不勾选初始化 README）

2. **本地推送：**
```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M master
git push -u origin master
```

### 新电脑 Clone 部署

```bash
# 1. Clone 项目
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名

# 2. 安装 FFmpeg（见上文环境依赖）

# 3. 前端设置
cd tools
npm install
npm run dev

# 4. 后端设置（新终端）
cd toolsbackend

# 安装 uv（如未安装）
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建环境并安装依赖
uv sync

# 启动服务
uv run python main.py
```

### 配置注意事项

| 配置项 | 说明 |
|--------|------|
| `tools/public/config.json` | 修改 `BASE_URL` 匹配后端实际地址 |
| `toolsbackend/settings.py` | 如启用数据库，修改 MySQL 连接信息 |
| 数据库 | 当前 MySQL 功能被注释，无需安装 |

---

## License

个人学习项目