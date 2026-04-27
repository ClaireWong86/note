from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import uuid
from datetime import datetime

from ..models.models import Project, Script, Storyboard, Timeline
from ..models.enums import ProjectStatus
from ..schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_project(self, project_id: str) -> Optional[Project]:
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()
    
    async def get_projects(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ProjectStatus] = None
    ) -> List[Project]:
        query = select(Project)
        
        if status:
            query = query.where(Project.status == status)
        
        query = query.order_by(Project.updated_at.desc()).offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def create_project(self, project_data: ProjectCreate) -> Project:
        project_id = str(uuid.uuid4())
        
        project = Project(
            id=project_id,
            title=project_data.title,
            description=project_data.description,
            status=ProjectStatus.DRAFT,
            created_by=project_data.created_by,
        )
        
        self.db.add(project)
        
        script = Script(
            id=str(uuid.uuid4()),
            project_id=project_id,
            title=project_data.title,
            content="",
        )
        self.db.add(script)
        
        storyboard = Storyboard(
            id=str(uuid.uuid4()),
            project_id=project_id,
        )
        self.db.add(storyboard)
        
        timeline = Timeline(
            id=str(uuid.uuid4()),
            project_id=project_id,
        )
        self.db.add(timeline)
        
        await self.db.commit()
        await self.db.refresh(project)
        
        return project
    
    async def update_project(
        self,
        project_id: str,
        project_data: ProjectUpdate
    ) -> Optional[Project]:
        project = await self.get_project(project_id)
        if not project:
            return None
        
        if project_data.title is not None:
            project.title = project_data.title
        if project_data.description is not None:
            project.description = project_data.description
        if project_data.status is not None:
            project.status = project_data.status
        
        project.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(project)
        
        return project
    
    async def delete_project(self, project_id: str) -> bool:
        project = await self.get_project(project_id)
        if not project:
            return False
        
        await self.db.delete(project)
        await self.db.commit()
        
        return True
    
    async def update_project_status(
        self,
        project_id: str,
        status: ProjectStatus
    ) -> Optional[Project]:
        project = await self.get_project(project_id)
        if not project:
            return None
        
        project.status = status
        project.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(project)
        
        return project
