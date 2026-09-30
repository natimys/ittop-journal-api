"""Получить расписание на сегодня и вывести ответ API в консоль."""

import asyncio
import json
from datetime import date

from ittop_journal import JournalClient


# Заполните своими данными перед запуском.
USERNAME = "Tarab_ko06"
PASSWORD = "Wh4zr978"
APPLICATION_KEY = "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6"


async def main() -> None:
    async with JournalClient() as journal:
        await journal.auth.login(USERNAME, PASSWORD, APPLICATION_KEY)
        lessons = await journal.schedule.get_by_date(date.today())

    print(json.dumps(
        [lesson.model_dump(mode="json") for lesson in lessons],
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    asyncio.run(main())
