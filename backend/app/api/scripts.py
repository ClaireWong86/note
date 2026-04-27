from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Try to import sqlite version first, fallback to postgres
try:
    from ..core.database_sqlite import get_db
except ImportError:
    from ..core.database import get_db
from ..schemas.script import (
    ScriptCreate,
    ScriptUpdate,
    ScriptResponse,
    ScriptSegmentCreate,
    ScriptSegmentUpdate,
    ScriptSegmentResponse,
)
from ..services.script_service import ScriptService


router = APIRouter(prefix="/projects/{project_id}/script", tags=["scripts"])


@router.get("", response_model=ScriptResponse)
async def get_project_script(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = ScriptService(db)
    script = await service.get_project_script(project_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    segments = await service.get_script_segments(project_id)
    return ScriptResponse(
        id=script.id,
        project_id=script.project_id,
        title=script.title,
        content=script.content,
        tone=script.tone,
        style=script.style,
        target_duration=script.target_duration,
        created_at=script.created_at,
        updated_at=script.updated_at,
        segments=segments,
    )


@router.post("", response_model=ScriptResponse, status_code=201)
async def create_script(
    project_id: str,
    script_data: ScriptCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ScriptService(db)
    return await service.create_script(project_id, script_data)


@router.put("", response_model=ScriptResponse)
async def update_script(
    project_id: str,
    script_data: ScriptUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ScriptService(db)
    script = await service.update_script(project_id, script_data)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return script


@router.get("/segments", response_model=List[ScriptSegmentResponse])
async def get_script_segments(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = ScriptService(db)
    return await service.get_script_segments(project_id)


@router.post("/segments", response_model=ScriptSegmentResponse, status_code=201)
async def add_script_segment(
    project_id: str,
    segment_data: ScriptSegmentCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ScriptService(db)
    segment = await service.add_script_segment(project_id, segment_data)
    if not segment:
        raise HTTPException(status_code=404, detail="Script not found")
    return segment


@router.put("/segments/{segment_id}", response_model=ScriptSegmentResponse)
async def update_script_segment(
    project_id: str,
    segment_id: str,
    segment_data: ScriptSegmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ScriptService(db)
    segment = await service.update_script_segment(segment_id, segment_data)
    if not segment:
        raise HTTPException(status_code=404, detail="Script segment not found")
    return segment


@router.delete("/segments/{segment_id}", status_code=204)
async def delete_script_segment(
    project_id: str,
    segment_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = ScriptService(db)
    success = await service.delete_script_segment(segment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Script segment not found")
    return None
