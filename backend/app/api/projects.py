from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

# Try to import sqlite version first, fallback to postgres
try:
    from ..core.database_sqlite import get_db
except ImportError:
    from ..core.database import get_db
from ..schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)
from ..services.project_service import ProjectService
from ..models.enums import ProjectStatus


router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ProjectStatus] = None,
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    return await service.get_projects(skip=skip, limit=limit, status=status)


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    return await service.create_project(project_data)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    project = await service.update_project(project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    success = await service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return None


@router.patch("/{project_id}/status", response_model=ProjectResponse)
async def update_project_status(
    project_id: str,
    status: ProjectStatus,
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    project = await service.update_project_status(project_id, status)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
