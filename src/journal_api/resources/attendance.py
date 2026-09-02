from .base import BaseResource

ATTENDANCE_PATH = "dashboard/chart/attendance"

class AttendanceResource(BaseResource):
    async def get(self):
        await self.client.request()