# 数据模型定义

## 1. 核心模型

### 1.1 Project (项目)
```python
class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(default=ProjectStatus.DRAFT)
    
    # 关联
    script: Mapped["Script"] = relationship(back_populates="project", uselist=False)
    storyboard: Mapped["Storyboard"] = relationship(back_populates="project", uselist=False)
    assets: Mapped[List["Asset"]] = relationship(back_populates="project")
    timeline: Mapped["Timeline"] = relationship(back_populates="project", uselist=False)
    
    # 元数据
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by: Mapped[str] = mapped_column(nullable=True)
```

### 1.2 Script (脚本)
```python
class Script(Base):
    __tablename__ = "scripts"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="script")
    
    title: Mapped[str]
    content: Mapped[str]
    segments: Mapped[List["ScriptSegment"]] = relationship(back_populates="script", cascade="all, delete-orphan")
    
    # 脚本元数据
    tone: Mapped[str] = mapped_column(default="neutral")  # 语气
    style: Mapped[str] = mapped_column(default="informative")  # 风格
    target_duration: Mapped[int] = mapped_column(default=300)  # 目标时长(秒)
```

### 1.3 ScriptSegment (脚本片段)
```python
class ScriptSegment(Base):
    __tablename__ = "script_segments"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    script_id: Mapped[str] = mapped_column(ForeignKey("scripts.id"))
    script: Mapped["Script"] = relationship(back_populates="segments")
    
    sequence: Mapped[int]  # 顺序
    type: Mapped[SegmentType]  # 类型: narration, dialogue, scene_description
    speaker: Mapped[str] = mapped_column(nullable=True)  # 说话人
    content: Mapped[str]  # 内容
    duration: Mapped[float] = mapped_column(default=0)  # 预估时长(秒)
    
    # 视觉提示
    visual_hint: Mapped[str] = mapped_column(nullable=True)
    audio_hint: Mapped[str] = mapped_column(nullable=True)
```

### 1.4 Storyboard (分镜)
```python
class Storyboard(Base):
    __tablename__ = "storyboards"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="storyboard")
    
    # 视觉风格
    visual_style: Mapped[JSON] = mapped_column(default=dict)
    color_palette: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    # 场景列表
    scenes: Mapped[List["Scene"]] = relationship(back_populates="storyboard", cascade="all, delete-orphan", order_by="Scene.sequence")
    
    # 转场定义
    transitions: Mapped[List["Transition"]] = relationship(back_populates="storyboard", cascade="all, delete-orphan")
```

### 1.5 Scene (场景)
```python
class Scene(Base):
    __tablename__ = "scenes"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    storyboard_id: Mapped[str] = mapped_column(ForeignKey("storyboards.id"))
    storyboard: Mapped["Storyboard"] = relationship(back_populates="scenes")
    
    sequence: Mapped[int]  # 场景顺序
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    
    # 镜头配置
    shot_type: Mapped[ShotType] = mapped_column(default=ShotType.MEDIUM)
    camera_movement: Mapped[CameraMovement] = mapped_column(default=CameraMovement.STATIC)
    camera_angle: Mapped[CameraAngle] = mapped_column(default=CameraAngle.EYE_LEVEL)
    
    # 时长
    duration: Mapped[float] = mapped_column(default=5)  # 秒
    
    # 视觉和音频
    visual_prompt: Mapped[str] = mapped_column(nullable=True)  # 图像生成提示词
    audio_prompt: Mapped[str] = mapped_column(nullable=True)  # 音频生成提示词
    
    # 关联素材
    assets: Mapped[List["SceneAsset"]] = relationship(back_populates="scene", cascade="all, delete-orphan")
    
    # 对应的脚本片段
    script_segment_id: Mapped[str] = mapped_column(ForeignKey("script_segments.id"), nullable=True)
```

### 1.6 Asset (素材)
```python
class Asset(Base):
    __tablename__ = "assets"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="assets")
    
    type: Mapped[AssetType]  # image, video, audio, subtitle
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    
    # 文件信息
    file_path: Mapped[str]
    file_size: Mapped[int] = mapped_column(nullable=True)
    mime_type: Mapped[str] = mapped_column(nullable=True)
    duration: Mapped[float] = mapped_column(nullable=True)  # 音视频时长
    width: Mapped[int] = mapped_column(nullable=True)  # 图像/视频宽度
    height: Mapped[int] = mapped_column(nullable=True)  # 图像/视频高度
    
    # 生成元数据
    generation_prompt: Mapped[str] = mapped_column(nullable=True)
    generation_model: Mapped[str] = mapped_column(nullable=True)
    generation_params: Mapped[JSON] = mapped_column(default=dict, nullable=True)
    
    status: Mapped[AssetStatus] = mapped_column(default=AssetStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

### 1.7 Timeline (时间轴)
```python
class Timeline(Base):
    __tablename__ = "timelines"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="timeline")
    
    # 轨道
    tracks: Mapped[List["Track"]] = relationship(back_populates="timeline", cascade="all, delete-orphan", order_by="Track.order")
    
    # 总时长
    total_duration: Mapped[float] = mapped_column(default=0)
```

### 1.8 Track (轨道)
```python
class Track(Base):
    __tablename__ = "tracks"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    timeline_id: Mapped[str] = mapped_column(ForeignKey("timelines.id"))
    timeline: Mapped["Timeline"] = relationship(back_populates="tracks")
    
    type: Mapped[TrackType]  # video, audio, subtitle, effect
    name: Mapped[str]
    order: Mapped[int]  # 轨道顺序
    muted: Mapped[bool] = mapped_column(default=False)
    locked: Mapped[bool] = mapped_column(default=False)
    
    # 轨道上的片段
    clips: Mapped[List["Clip"]] = relationship(back_populates="track", cascade="all, delete-orphan")
```

### 1.9 Clip (片段)
```python
class Clip(Base):
    __tablename__ = "clips"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    track_id: Mapped[str] = mapped_column(ForeignKey("tracks.id"))
    track: Mapped["Track"] = relationship(back_populates="clips")
    
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), nullable=True)
    asset: Mapped["Asset"] = relationship()
    
    # 时间位置
    start_time: Mapped[float]  # 开始时间(秒)
    end_time: Mapped[float]  # 结束时间(秒)
    
    # 素材裁剪
    asset_start_time: Mapped[float] = mapped_column(default=0)  # 素材起始点
    asset_end_time: Mapped[float] = mapped_column(nullable=True)  # 素材结束点
    
    # 变换参数
    transform: Mapped[JSON] = mapped_column(default=dict)  # 缩放、旋转、位置
    opacity: Mapped[float] = mapped_column(default=1.0)  # 透明度
    
    # 特效
    effects: Mapped[List["Effect"]] = relationship(back_populates="clip", cascade="all, delete-orphan")
```

### 1.10 Effect (特效)
```python
class Effect(Base):
    __tablename__ = "effects"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    clip_id: Mapped[str] = mapped_column(ForeignKey("clips.id"))
    clip: Mapped["Clip"] = relationship(back_populates="effects")
    
    type: Mapped[str]  # 特效类型
    name: Mapped[str]
    params: Mapped[JSON] = mapped_column(default=dict)  # 特效参数
    
    # 应用时间范围
    start_offset: Mapped[float] = mapped_column(default=0)
    end_offset: Mapped[float] = mapped_column(nullable=True)
```

### 1.11 PublishingTarget (发布目标)
```python
class PublishingTarget(Base):
    __tablename__ = "publishing_targets"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    
    platform: Mapped[str]  # youtube, bilibili, etc.
    status: Mapped[PublishingStatus] = mapped_column(default=PublishingStatus.PENDING)
    
    # 平台特定配置
    config: Mapped[JSON] = mapped_column(default=dict)
    published_url: Mapped[str] = mapped_column(nullable=True)
    published_at: Mapped[datetime] = mapped_column(nullable=True)
```

## 2. 枚举类型

```python
from enum import Enum

class ProjectStatus(str, Enum):
    DRAFT = "draft"
    PLANNING = "planning"
    PRODUCING = "producing"
    REVIEWING = "reviewing"
    PUBLISHED = "published"
    FAILED = "failed"

class SegmentType(str, Enum):
    NARRATION = "narration"
    DIALOGUE = "dialogue"
    SCENE_DESCRIPTION = "scene_description"
    MUSIC = "music"
    SOUND_EFFECT = "sound_effect"

class ShotType(str, Enum):
    EXTREME_WIDE = "extreme_wide"
    WIDE = "wide"
    MEDIUM = "medium"
    CLOSEUP = "closeup"
    EXTREME_CLOSEUP = "extreme_closeup"

class CameraMovement(str, Enum):
    STATIC = "static"
    PAN = "pan"
    TILT = "tilt"
    DOLLY = "dolly"
    TRUCK = "truck"
    PEDESTAL = "pedestal"
    ZOOM = "zoom"
    FOLLOW = "follow"

class CameraAngle(str, Enum):
    LOW = "low"
    EYE_LEVEL = "eye_level"
    HIGH = "high"
    BIRDS_EYE = "birds_eye"
    DUTCH = "dutch"

class AssetType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    SUBTITLE = "subtitle"

class AssetStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    READY = "ready"
    FAILED = "failed"

class TrackType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    SUBTITLE = "subtitle"
    EFFECT = "effect"

class PublishingStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    UPLOADING = "uploading"
    PUBLISHED = "published"
    FAILED = "failed"
```

## 3. 工作流/任务模型

```python
class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    task_type: Mapped[str]  # script_generation, storyboard_generation, etc.
    
    status: Mapped[str] = mapped_column(default="pending")
    progress: Mapped[int] = mapped_column(default=0)  # 0-100
    
    # 依赖管理
    dependencies: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    # 参数和结果
    params: Mapped[JSON] = mapped_column(default=dict)
    result: Mapped[JSON] = mapped_column(default=dict, nullable=True)
    error: Mapped[str] = mapped_column(nullable=True)
    
    # 时间
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    started_at: Mapped[datetime] = mapped_column(nullable=True)
    completed_at: Mapped[datetime] = mapped_column(nullable=True)
```
