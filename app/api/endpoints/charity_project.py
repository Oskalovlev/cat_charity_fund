from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.api.validators import (
    check_name_duplicate, check_charity_project_exists,
    check_charity_project_already_invested,
    check_charity_project_closed_invested,
    check_charity_project_invested,
)
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.models import Donation, CharityProject
from app.api.manage.investment import investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Только для суперюзеров."""

    await check_name_duplicate(charity_project.name, session)
    await charity_project_crud.get_project_id_by_name(
        charity_project.name, session
    )
    new_project = await charity_project_crud.create(charity_project, session)
    obj = await charity_project_crud.get_underinvested_obj(session, Donation)
    if obj:
        session.add_all(investing(new_project, obj))
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
) -> List[CharityProject]:

    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    """Только для суперюзеров."""

    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_closed_invested(project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_charity_project_invested(project, obj_in.full_amount)

    update_project = await charity_project_crud.update(
        project, obj_in, session
    )
    return update_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Только для суперюзеров."""

    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_already_invested(project)
    delete_project = await charity_project_crud.remove(
        project, session
    )
    return delete_project
