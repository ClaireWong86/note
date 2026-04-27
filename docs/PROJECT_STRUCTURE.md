# 项目文件结构

本文档详细展示了智能视频生成系统的完整文件结构。

## 📁 完整结构

```
/workspace
├── 📄 README.md                      # 项目说明文档
├── 📄 .gitignore                     # Git忽略文件配置
├── 📄 ARCHITECTURE.md                # 系统架构设计文档
│
├── 📂 backend/                       # 后端服务目录
│   ├── 📄 requirements.txt            # Python依赖包
│   ├── 📄 start.sh                   # 快速启动脚本
│   ├── 📄 .env.example               # 环境变量示例
│   │
│   └── 📂 app/                       # 应用主目录
│       ├── 📄 __init__.py
│       ├── 📄 main.py                # PostgreSQL版本主入口
│       ├── 📄 main_sqlite.py         # SQLite版本主入口(测试用)
│       │
│       ├── 📂 core/                  # 核心模块
│       │   ├── 📄 __init__.py
│       │   ├── 📄 config.py          # 配置管理
│       │   ├── 📄 database.py        # PostgreSQL数据库连接
│       │   └── 📄 database_sqlite.py # SQLite数据库连接
│       │
│       ├── 📂 models/                # 数据模型
│       │   ├── 📄 __init__.py
│       │   ├── 📄 base.py            # 基础模型
│       │   ├── 📄 enums.py           # 枚举类型定义
│       │   └── 📄 models.py          # 核心数据模型
│       │
│       ├── 📂 schemas/               # Pydantic schemas
│       │   ├── 📄 __init__.py
│       │   ├── 📄 project.py         # 项目相关schemas
│       │   └── 📄 script.py          # 脚本相关schemas
│       │
│       ├── 📂 services/              # 业务逻辑层
│       │   ├── 📄 __init__.py
│       │   ├── 📄 project_service.py # 项目服务
│       │   └── 📄 script_service.py  # 脚本服务
│       │
│       ├── 📂 api/                   # API路由
│       │   ├── 📄 __init__.py
│       │   ├── 📄 projects.py        # 项目API
│       │   └── 📄 scripts.py         # 脚本API
│       │
│       ├── 📂 workflows/             # 工作流引擎 (待实现)
│       │   └── 📄 __init__.py
│       │
│       └── 📂 utils/                 # 工具函数 (待实现)
│           └── 📄 __init__.py
│
├── 📂 frontend/                      # 前端应用 (待实现)
│   └── 📂 src/
│       ├── 📂 components/
│       ├── 📂 pages/
│       ├── 📂 store/
│       └── 📂 utils/
│
├── 📂 docs/                          # 文档目录
│   ├── 📄 ARCHITECTURE.md            # 架构设计 (链接到根目录)
│   ├── 📄 DATA_MODELS.md             # 数据模型定义
│   ├── 📄 QUICKSTART.md              # 快速测试指南
│   ├── 📄 ROADMAP.md                 # 开发路线图
│   └── 📄 PROJECT_STRUCTURE.md       # 本文档
│
├── 📂 scripts/                       # 工具脚本 (待实现)
├── 📂 docker/                        # Docker配置 (待实现)
└── 📂 tests/                         # 测试代码 (待实现)
```

## 📂 核心目录说明

### backend/app/core/
核心配置和基础设施模块
- `config.py`: 应用配置管理
- `database*.py`: 数据库连接和会话管理

### backend/app/models/
数据模型定义
- `base.py`: SQLAlchemy基类
- `enums.py`: 枚举类型定义
- `models.py`: 核心数据模型

### backend/app/schemas/
Pydantic模型定义
- API请求/响应数据结构
- 数据验证规则

### backend/app/services/
业务逻辑层
- 包含所有的业务逻辑处理
- 封装数据访问操作

### backend/app/api/
API路由层
- RESTful API端点定义
- 请求/响应处理

## 📄 核心模型清单

### 已实现的模型
1. **Project** - 项目模型
2. **Script** - 脚本模型
3. **ScriptSegment** - 脚本片段模型
4. **Storyboard** - 分镜模型 (结构已定义)
5. **Scene** - 场景模型 (结构已定义)
6. **Asset** - 素材模型 (结构已定义)
7. **Timeline** - 时间轴模型 (结构已定义)
8. **Track** - 轨道模型 (结构已定义)
9. **Clip** - 片段模型 (结构已定义)
10. **WorkflowTask** - 工作流任务模型 (结构已定义)

### 待完善的模型
- 特效模型
- 发布目标模型
- 用户模型
- 模板模型

## 🔗 文件依赖关系

```
main.py 
  ├─> core/config.py
  ├─> core/database*.py
  ├─> api/projects.py
  │   └─> services/project_service.py
  │       └─> models/models.py
  │
  └─> api/scripts.py
      └─> services/script_service.py
          └─> models/models.py
```

## 🎯 下一步创建建议

按优先级排序：

1. **高优先级**
   - `backend/app/services/storyboard_service.py`
   - `backend/app/api/storyboards.py`
   - `backend/app/schemas/storyboard.py`

2. **中优先级**
   - `backend/app/services/asset_service.py`
   - `backend/app/api/assets.py`
   - `backend/app/schemas/asset.py`

3. **低优先级**
   - 前端应用文件
   - 测试文件
   - Docker配置文件
