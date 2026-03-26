# 个人工具汇总平台

一个简洁的个人实用工具平台，采用前后端分离架构，提供音频格式转换和 PDF 文件处理功能。

![技术栈](https://img.shields.io/badge/前端-Vue%203%20+%20TypeScript%20+%20Vite-blue)
![技术栈](https://img.shields.io/badge/后端-Python%20+%20FastAPI-green)
![UI](https://img.shields.io/badge/UI-Obsidian%20Command%20Dark-purple)

---

## 功能特性

| 工具 | 功能描述 |
|------|---------|
| **音频转换** | 支持 MP3、FLAC、OGG、WAV 格式互转 |
| **PDF 合并** | 将两个 PDF 文件按交替页码合并 |
| **PDF 逆序** | 将 PDF 页面顺序反转 |

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

### 后端 (`toolsbackend/`)
- **框架**: FastAPI 0.116
- **语言**: Python 3
- **运行**: Uvicorn
- **依赖**: PyPDF2 (PDF 处理)、pydub (音频处理)、Pydantic v2

---

## 快速开始

### 前端启动

```bash
cd tools
npm install
npm run dev
```

访问 http://localhost:5173

### 后端启动

```bash
cd toolsbackend

# 首次运行需创建虚拟环境
python -m venv toolkitenv
source toolkitenv/Scripts/activate  # Windows
# 或: source toolkitenv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python main.py
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
│   │   ├── api/              # API 接口封装
│   │   ├── stores/           # Pinia 状态管理
│   │   └── assets/scss/      # 样式文件
│   └── public/config.json    # 运行时配置
│
└── toolsbackend/             # 后端 FastAPI 项目
    ├── main.py               # 应用入口
    ├── api/                  # 路由模块
    │   ├── Audio/
    │   └── Pdf/
    └── requirements.txt      # 依赖列表
```

---

## 开发说明

- 前端使用 Element Plus 组件库，但已完全自定义主题样式
- 所有业务逻辑保持完整，仅 UI 层重新设计
- 支持拖拽上传文件，转换后自动下载
- 后端 CORS 完全开放，仅限本地开发使用

---

## License

个人学习项目
