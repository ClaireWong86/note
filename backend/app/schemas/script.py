from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from ..models.enums import SegmentType


class ScriptSegmentBase(BaseModel):
    type: SegmentType = SegmentType.NARRATION
    speaker: Optional[str] = Field(None, max_length=100)
    content: str = Field(..., min_length=1)
    duration: float = Field(default=0, ge=0)
    visual_hint: Optional[str] = None
    audio_hint: Optional[str] = None


class ScriptSegmentCreate(ScriptSegmentBase):
    pass


class ScriptSegmentUpdate(BaseModel):
    type: Optional[SegmentType] = None
    speaker: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None
    duration: Optional[float] = None
    visual_hint: Optional[str] = None
    audio_hint: Optional[str] = None


class ScriptSegmentResponse(ScriptSegmentBase):
    id: str
    script_id: str
    sequence: int
    
    class Config:
        from_attributes = True


class ScriptBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    tone: str = Field(default="neutral", max_length=50)
    style: str = Field(default="informative", max_length=50)
    target_duration: int = Field(default=300, ge=10)


class ScriptCreate(ScriptBase):
    segments: Optional[List[ScriptSegmentCreate]] = None


class ScriptUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    tone: Optional[str] = Field(None, max_length=50)
    style: Optional[str] = Field(None, max_length=50)
    target_duration: Optional[int] = None


class ScriptResponse(ScriptBase):
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
    segments: Optional[List[ScriptSegmentResponse]] = None
    
    class Config:
        from_attributes = True


class ScriptGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    tone: str = Field(default="neutral", max_length=50)
    style: str = Field(default="informative", max_length=50)
    target_duration: int = Field(default=300, ge=10)
    additional_instructions: Optional[str] = None
