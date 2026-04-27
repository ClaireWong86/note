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


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
