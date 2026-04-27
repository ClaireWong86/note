# 智能视频生成系统

一个**重流程、重逻辑、重视觉表现**的全流程视频生成平台，支持从内容策划到多平台发布的完整工作流。

## ✨ 特性

### 📋 完整工作流
- **内容策划**: AI辅助脚本生成，多语言支持
- **分镜设计**: 专业的镜头规划，视觉风格定义
- **素材制作**: 图像、音频、视频的AI生成
- **视频合成**: 多轨道编辑，特效叠加
- **质量审核**: 自动质量检查和人工审核
- **多平台发布**: 一键发布到YouTube、B站等

### 🎨 视觉表现
- 专业的分镜系统
- 多种视觉风格模板
- 灵活的转场效果
- 字幕自动生成和同步

### 🔧 技术特性
- 模块化架构设计
- 异步API服务
- 任务队列处理
- 插件化AI服务集成
- 完整的数据模型定义

## 🏗️ 项目架构

```
/workspace
├── backend/                 # 后端服务 (FastAPI)
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置和数据库
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # 业务逻辑
│   │   ├── workflows/      # 工作流引擎
│   │   └── utils/          # 工具函数
│   ├── tests/
│   └── requirements.txt
├── frontend/               # 前端应用 (React + TypeScript)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   └── utils/
│   └── package.json
├── docs/                   # 文档
│   ├── ARCHITECTURE.md    # 架构设计文档
│   └── DATA_MODELS.md     # 数据模型定义
├── scripts/                # 工具脚本
└── docker/                 # Docker配置
```

## 🚀 快速开始

### 前置要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- FFmpeg

### 后端启动

1. 克隆项目
```bash
cd /workspace
```

2. 配置环境变量
```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，配置数据库和AI服务
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 启动服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. 访问API文档
```
http://localhost:8000/docs
```

### 使用Docker (推荐)

```bash
# 待完善 - 将提供完整的docker-compose配置
```

## 📚 API 文档

启动后端服务后，访问以下地址查看API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 主要API端点

#### 项目管理
- `GET /projects` - 获取项目列表
- `POST /projects` - 创建新项目
- `GET /projects/{id}` - 获取项目详情
- `PUT /projects/{id}` - 更新项目
- `DELETE /projects/{id}` - 删除项目

#### 脚本管理
- `GET /projects/{id}/script` - 获取项目脚本
- `POST /projects/{id}/script` - 创建脚本
- `PUT /projects/{id}/script` - 更新脚本
- `GET /projects/{id}/script/segments` - 获取脚本片段
- `POST /projects/{id}/script/segments` - 添加脚本片段

更多API端点请参考 Swagger 文档。

## 📖 核心概念

### 项目状态流转
```
DRAFT → PLANNING → PRODUCING → REVIEWING → PUBLISHED
            ↓          ↓
          FAILED     FAILED
```

### 核心数据模型
- **Project**: 项目，包含脚本、分镜、素材、时间轴
- **Script**: 脚本，包含多个脚本片段
- **Storyboard**: 分镜，包含场景和转场定义
- **Asset**: 素材，图像、音频、视频等
- **Timeline**: 时间轴，包含轨道和片段

更多详细信息请参考 [架构设计文档](./ARCHITECTURE.md) 和 [数据模型文档](./docs/DATA_MODELS.md)。

## 🤝 开发指南

### 代码规范
- 后端: 使用 `black` 和 `isort` 格式化代码
- 前端: 使用 `eslint` 和 `prettier`

### 提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

### 贡献流程
1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 🙋‍♀️ 支持

如有问题，请创建 Issue 或发送邮件联系。

---

**注意**: 这是一个正在开发的项目，核心功能正在逐步完善中。
