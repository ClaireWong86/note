# 快速测试指南

本指南将帮助你快速启动和测试视频生成系统的API。

## 🚀 快速启动

### 1. 启动后端服务

```bash
cd /workspace/backend

# 方式一：使用启动脚本 (推荐)
./start.sh

# 方式二：手动启动
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main_sqlite:app --reload --host 0.0.0.0 --port 8000
```

### 2. 访问API文档

服务启动后，在浏览器中访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📝 API 测试流程

### 步骤1: 创建一个新项目

在 Swagger UI 中找到 `POST /projects` 端点，点击 "Try it out"，然后输入以下JSON：

```json
{
  "title": "我的第一个视频项目",
  "description": "这是一个测试项目，用于演示视频生成流程",
  "created_by": "测试用户"
}
```

点击 "Execute"，你会得到一个项目ID，复制这个ID备用。

### 步骤2: 查看项目列表

使用 `GET /projects` 端点查看所有项目。

### 步骤3: 创建脚本

使用 `POST /projects/{project_id}/script` 端点创建脚本：

```json
{
  "title": "人工智能介绍",
  "content": "这是一个关于人工智能的介绍视频。",
  "tone": "professional",
  "style": "informative",
  "target_duration": 300,
  "segments": [
    {
      "type": "narration",
      "speaker": "主持人",
      "content": "大家好，欢迎来到今天的视频。",
      "duration": 5,
      "visual_hint": "主持人出镜，微笑面对镜头",
      "audio_hint": "温暖友好的声音"
    },
    {
      "type": "narration",
      "speaker": "主持人",
      "content": "人工智能正在改变我们的生活。",
      "duration": 5,
      "visual_hint": "展示AI相关的图像和图表",
      "audio_hint": "专业的解说语调"
    }
  ]
}
```

### 步骤4: 查看脚本

使用 `GET /projects/{project_id}/script` 查看刚才创建的脚本。

## 🔄 使用 curl 测试

如果你喜欢使用命令行，这里有一些示例：

### 创建项目
```bash
curl -X POST "http://localhost:8000/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试项目",
    "description": "通过curl创建的测试项目"
  }'
```

### 获取项目列表
```bash
curl -X GET "http://localhost:8000/projects"
```

## 📊 项目状态

项目有以下状态：
- `draft`: 草稿
- `planning`: 规划中
- `producing`: 制作中
- `reviewing`: 审核中
- `published`: 已发布
- `failed`: 失败

你可以使用 `PATCH /projects/{project_id}/status` 来更新项目状态。

## 🎯 下一步

现在你已经了解了基础API的使用，接下来可以：

1. 继续完善项目架构
2. 添加分镜设计功能
3. 集成AI服务
4. 开发前端界面

查看 [ARCHITECTURE.md](../ARCHITECTURE.md) 了解更多关于系统架构的信息。

## 💡 提示

- 数据库文件会自动创建在 `backend/video_gen.db`
- 可以随时删除 `video_gen.db` 来重置数据库
- API支持热重载，修改代码后会自动重启
