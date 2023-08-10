from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_fully_invested_obj(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:

    obj = await session.execute(
        select(obj_in).where(
            obj_in.fully_invested is not None
        ).order_by(obj_in.create_date)
    )
    return obj.scalars().all()


async def close_donation_for_obj(
    obj_in: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:

    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


async def invest_donation(
    obj_in: Union[CharityProject, Donation],
    obj_model: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:

    unalloted_amount = obj_in.full_amount - obj_in.invested_amount
    amount_in_model = obj_model.full_amount - obj_model.invested_amount

    if unalloted_amount > amount_in_model:
        obj_in.invested_amount += amount_in_model
        await close_donation_for_obj(obj_model)

    elif unalloted_amount == amount_in_model:
        await close_donation_for_obj(obj_in)
        await close_donation_for_obj(obj_model)

    else:
        obj_model.invested_amount += unalloted_amount
        await close_donation_for_obj(obj_in)

    return obj_in, obj_model


async def investing(
    obj_in: Union[CharityProject, Donation],
    model_add: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:

    obj_model = await get_not_fully_invested_obj(model_add, session)

    for model in obj_model:
        obj_in, model = await invest_donation(obj_in, model)
        session.add(obj_in)
        session.add(model)

    await session.commit()
    await session.refresh(obj_in)
    return obj_in
