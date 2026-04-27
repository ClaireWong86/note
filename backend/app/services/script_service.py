from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid

from ..models.models import Project, Script, ScriptSegment
from ..models.enums import ProjectStatus, SegmentType
from ..schemas.script import (
    ScriptCreate,
    ScriptUpdate,
    ScriptSegmentCreate,
    ScriptSegmentUpdate,
)


class ScriptService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_project_script(self, project_id: str) -> Optional[Script]:
        result = await self.db.execute(
            select(Script)
            .where(Script.project_id == project_id)
        )
        return result.scalar_one_or_none()
    
    async def create_script(
        self,
        project_id: str,
        script_data: ScriptCreate
    ) -> Script:
        script_id = str(uuid.uuid4())
        
        script = Script(
            id=script_id,
            project_id=project_id,
            title=script_data.title,
            content=script_data.content,
            tone=script_data.tone,
            style=script_data.style,
            target_duration=script_data.target_duration,
        )
        
        self.db.add(script)
        
        if script_data.segments:
            for idx, segment_data in enumerate(script_data.segments):
                segment = ScriptSegment(
                    id=str(uuid.uuid4()),
                    script_id=script_id,
                    sequence=idx,
                    type=segment_data.type,
                    speaker=segment_data.speaker,
                    content=segment_data.content,
                    duration=segment_data.duration,
                    visual_hint=segment_data.visual_hint,
                    audio_hint=segment_data.audio_hint,
                )
                self.db.add(segment)
        
        await self.db.commit()
        await self.db.refresh(script)
        
        return script
    
    async def update_script(
        self,
        project_id: str,
        script_data: ScriptUpdate
    ) -> Optional[Script]:
        script = await self.get_project_script(project_id)
        if not script:
            return None
        
        if script_data.title is not None:
            script.title = script_data.title
        if script_data.content is not None:
            script.content = script_data.content
        if script_data.tone is not None:
            script.tone = script_data.tone
        if script_data.style is not None:
            script.style = script_data.style
        if script_data.target_duration is not None:
            script.target_duration = script_data.target_duration
        
        await self.db.commit()
        await self.db.refresh(script)
        
        return script
    
    async def get_script_segments(self, project_id: str) -> List[ScriptSegment]:
        script = await self.get_project_script(project_id)
        if not script:
            return []
        
        result = await self.db.execute(
            select(ScriptSegment)
            .where(ScriptSegment.script_id == script.id)
            .order_by(ScriptSegment.sequence)
        )
        return list(result.scalars().all())
    
    async def add_script_segment(
        self,
        project_id: str,
        segment_data: ScriptSegmentCreate
    ) -> Optional[ScriptSegment]:
        script = await self.get_project_script(project_id)
        if not script:
            return None
        
        segments = await self.get_script_segments(project_id)
        next_sequence = len(segments)
        
        segment = ScriptSegment(
            id=str(uuid.uuid4()),
            script_id=script.id,
            sequence=next_sequence,
            type=segment_data.type,
            speaker=segment_data.speaker,
            content=segment_data.content,
            duration=segment_data.duration,
            visual_hint=segment_data.visual_hint,
            audio_hint=segment_data.audio_hint,
        )
        
        self.db.add(segment)
        await self.db.commit()
        await self.db.refresh(segment)
        
        return segment
    
    async def update_script_segment(
        self,
        segment_id: str,
        segment_data: ScriptSegmentUpdate
    ) -> Optional[ScriptSegment]:
        result = await self.db.execute(
            select(ScriptSegment).where(ScriptSegment.id == segment_id)
        )
        segment = result.scalar_one_or_none()
        if not segment:
            return None
        
        if segment_data.type is not None:
            segment.type = segment_data.type
        if segment_data.speaker is not None:
            segment.speaker = segment_data.speaker
        if segment_data.content is not None:
            segment.content = segment_data.content
        if segment_data.duration is not None:
            segment.duration = segment_data.duration
        if segment_data.visual_hint is not None:
            segment.visual_hint = segment_data.visual_hint
        if segment_data.audio_hint is not None:
            segment.audio_hint = segment_data.audio_hint
        
        await self.db.commit()
        await self.db.refresh(segment)
        
        return segment
    
    async def delete_script_segment(self, segment_id: str) -> bool:
        result = await self.db.execute(
            select(ScriptSegment).where(ScriptSegment.id == segment_id)
        )
        segment = result.scalar_one_or_none()
        if not segment:
            return False
        
        await self.db.delete(segment)
        await self.db.commit()
        
        return True
