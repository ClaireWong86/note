from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Float, Integer, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import (
    ProjectStatus,
    SegmentType,
    ShotType,
    CameraMovement,
    CameraAngle,
    AssetType,
    AssetStatus,
    TrackType,
    PublishingStatus,
    TaskStatus,
)


class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(default=ProjectStatus.DRAFT)
    created_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # 关联
    script: Mapped[Optional["Script"]] = relationship(
        "Script", 
        back_populates="project", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    storyboard: Mapped[Optional["Storyboard"]] = relationship(
        "Storyboard", 
        back_populates="project", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    assets: Mapped[List["Asset"]] = relationship(
        "Asset", 
        back_populates="project",
        cascade="all, delete-orphan"
    )
    timeline: Mapped[Optional["Timeline"]] = relationship(
        "Timeline", 
        back_populates="project", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    publishing_targets: Mapped[List["PublishingTarget"]] = relationship(
        "PublishingTarget",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    tasks: Mapped[List["WorkflowTask"]] = relationship(
        "WorkflowTask",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Script(Base):
    __tablename__ = "scripts"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="script")
    
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    
    # 脚本元数据
    tone: Mapped[str] = mapped_column(String, default="neutral")
    style: Mapped[str] = mapped_column(String, default="informative")
    target_duration: Mapped[int] = mapped_column(Integer, default=300)
    
    segments: Mapped[List["ScriptSegment"]] = relationship(
        "ScriptSegment",
        back_populates="script",
        cascade="all, delete-orphan",
        order_by="ScriptSegment.sequence"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScriptSegment(Base):
    __tablename__ = "script_segments"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    script_id: Mapped[str] = mapped_column(String, ForeignKey("scripts.id"))
    script: Mapped["Script"] = relationship("Script", back_populates="segments")
    
    sequence: Mapped[int] = mapped_column(Integer)
    type: Mapped[SegmentType] = mapped_column(default=SegmentType.NARRATION)
    speaker: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(Text)
    duration: Mapped[float] = mapped_column(Float, default=0)
    
    visual_hint: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    audio_hint: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    scenes: Mapped[List["Scene"]] = relationship("Scene", back_populates="script_segment")


class Storyboard(Base):
    __tablename__ = "storyboards"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="storyboard")
    
    visual_style: Mapped[dict] = mapped_column(JSON, default=dict)
    color_palette: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    scenes: Mapped[List["Scene"]] = relationship(
        "Scene",
        back_populates="storyboard",
        cascade="all, delete-orphan",
        order_by="Scene.sequence"
    )
    transitions: Mapped[List["Transition"]] = relationship(
        "Transition",
        back_populates="storyboard",
        cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Scene(Base):
    __tablename__ = "scenes"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    storyboard_id: Mapped[str] = mapped_column(String, ForeignKey("storyboards.id"))
    storyboard: Mapped["Storyboard"] = relationship("Storyboard", back_populates="scenes")
    script_segment_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("script_segments.id"), nullable=True)
    script_segment: Mapped[Optional["ScriptSegment"]] = relationship("ScriptSegment", back_populates="scenes")
    
    sequence: Mapped[int] = mapped_column(Integer)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    shot_type: Mapped[ShotType] = mapped_column(default=ShotType.MEDIUM)
    camera_movement: Mapped[CameraMovement] = mapped_column(default=CameraMovement.STATIC)
    camera_angle: Mapped[CameraAngle] = mapped_column(default=CameraAngle.EYE_LEVEL)
    
    duration: Mapped[float] = mapped_column(Float, default=5)
    
    visual_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    audio_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    scene_assets: Mapped[List["SceneAsset"]] = relationship(
        "SceneAsset",
        back_populates="scene",
        cascade="all, delete-orphan"
    )


class SceneAsset(Base):
    __tablename__ = "scene_assets"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    scene_id: Mapped[str] = mapped_column(String, ForeignKey("scenes.id"))
    scene: Mapped["Scene"] = relationship("Scene", back_populates="scene_assets")
    asset_id: Mapped[str] = mapped_column(String, ForeignKey("assets.id"))
    asset: Mapped["Asset"] = relationship("Asset")
    
    role: Mapped[str] = mapped_column(String, default="main")  # main, background, etc.


class Transition(Base):
    __tablename__ = "transitions"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    storyboard_id: Mapped[str] = mapped_column(String, ForeignKey("storyboards.id"))
    storyboard: Mapped["Storyboard"] = relationship("Storyboard", back_populates="transitions")
    
    from_scene_sequence: Mapped[int] = mapped_column(Integer)
    to_scene_sequence: Mapped[int] = mapped_column(Integer)
    transition_type: Mapped[str] = mapped_column(String, default="cut")  # cut, fade, dissolve, etc.
    duration: Mapped[float] = mapped_column(Float, default=0.5)
    params: Mapped[dict] = mapped_column(JSON, default=dict)


class Asset(Base):
    __tablename__ = "assets"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="assets")
    
    type: Mapped[AssetType] = mapped_column()
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    file_path: Mapped[str] = mapped_column(String)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    generation_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    generation_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    generation_params: Mapped[dict] = mapped_column(JSON, default=dict)
    
    status: Mapped[AssetStatus] = mapped_column(default=AssetStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    scene_assets: Mapped[List["SceneAsset"]] = relationship("SceneAsset", back_populates="asset")
    clips: Mapped[List["Clip"]] = relationship("Clip", back_populates="asset")


class Timeline(Base):
    __tablename__ = "timelines"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="timeline")
    
    total_duration: Mapped[float] = mapped_column(Float, default=0)
    
    tracks: Mapped[List["Track"]] = relationship(
        "Track",
        back_populates="timeline",
        cascade="all, delete-orphan",
        order_by="Track.order"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Track(Base):
    __tablename__ = "tracks"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    timeline_id: Mapped[str] = mapped_column(String, ForeignKey("timelines.id"))
    timeline: Mapped["Timeline"] = relationship("Timeline", back_populates="tracks")
    
    type: Mapped[TrackType] = mapped_column()
    name: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)
    muted: Mapped[bool] = mapped_column(Boolean, default=False)
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    clips: Mapped[List["Clip"]] = relationship(
        "Clip",
        back_populates="track",
        cascade="all, delete-orphan"
    )


class Clip(Base):
    __tablename__ = "clips"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    track_id: Mapped[str] = mapped_column(String, ForeignKey("tracks.id"))
    track: Mapped["Track"] = relationship("Track", back_populates="clips")
    
    asset_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("assets.id"), nullable=True)
    asset: Mapped[Optional["Asset"]] = relationship("Asset", back_populates="clips")
    
    start_time: Mapped[float] = mapped_column(Float)
    end_time: Mapped[float] = mapped_column(Float)
    
    asset_start_time: Mapped[float] = mapped_column(Float, default=0)
    asset_end_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    transform: Mapped[dict] = mapped_column(JSON, default=dict)
    opacity: Mapped[float] = mapped_column(Float, default=1.0)
    
    effects: Mapped[List["Effect"]] = relationship(
        "Effect",
        back_populates="clip",
        cascade="all, delete-orphan"
    )


class Effect(Base):
    __tablename__ = "effects"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    clip_id: Mapped[str] = mapped_column(String, ForeignKey("clips.id"))
    clip: Mapped["Clip"] = relationship("Clip", back_populates="effects")
    
    type: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    params: Mapped[dict] = mapped_column(JSON, default=dict)
    
    start_offset: Mapped[float] = mapped_column(Float, default=0)
    end_offset: Mapped[Optional[float]] = mapped_column(Float, nullable=True)


class PublishingTarget(Base):
    __tablename__ = "publishing_targets"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="publishing_targets")
    
    platform: Mapped[str] = mapped_column(String)
    status: Mapped[PublishingStatus] = mapped_column(default=PublishingStatus.PENDING)
    
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    published_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    
    task_type: Mapped[str] = mapped_column(String)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.PENDING)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    
    dependencies: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    params: Mapped[dict] = mapped_column(JSON, default=dict)
    result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
