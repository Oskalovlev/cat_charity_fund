from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation, BaseModel
# from app.core.config import settings


def close_donation_for_obj(
    target: Union[CharityProject, Donation]
) -> None:
    target.fully_invested = True
    target.close_date = datetime.now()


def investing(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]],
) -> List[BaseModel]:

    target.invested_amount = 0
    new_target = []
    for source in sources:
        donation = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for new_source in source, target:
            new_source.invested_amount += donation
            if new_source.full_amount == new_source.invested_amount:
                close_donation_for_obj(new_source)
        new_target.append(source)
    return new_target
