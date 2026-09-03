from ..enums import MonthPoints
from .base import BaseResource

ATTENDANCE_PATH = "dashboard/chart/attendance"


class AttendanceResource(BaseResource):
    async def get(self):
        response = await self.client.request(
            "GET",
            ATTENDANCE_PATH,
        )
        print(response.json())
        # return MonthPoints(**response.json())
