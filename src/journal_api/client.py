from typing import Literal

import httpx
from .resources.attendance import AttendanceResource

BASE_URL = "https://msapi.top-academy.ru/api/v2"


class Client:
    def __init__(self, login: str, password: str):
        """
        Клиент журнала академии ТОП, все запросы происходят асинхронно
        :param login: Логин пользователя
        :param password: Пароль пользователя
        """
        self.__login = login
        self.__password = password
        self.__access_token = None
        self.__client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.__access_token}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
            }
        )

        self.attendance = AttendanceResource(client=self)

    async def _send(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Базовый метод, отправляющий запросы
        :param method: str, GET/POST и прочие
        :param path: путь относительно BASE_URL
        :param kwargs:
        :return:
        """
        print(path)
        response = await self.__client.request(method=method, url=path, **kwargs)
        response.raise_for_status()
        return response

    async def _login(self) -> None:
        """
        Получение access токена и сохранение в классе
        :return:
        """
        response = await self._send(
            method="post",
            path=f"{BASE_URL}/auth/login",
            params={"login": self.__login, "password": self.__password},
        )
        print(response.json())
        self.__access_token = response.json()["access_token"]

    async def request(
        self, method: Literal["GET", "POST"], path: str, **kwargs
    ) -> httpx.Response:
        """
        Метод, использующий _send() для запросов, с автоматическим логином. Используется в Resource-ах
        :param method: POST/GET
        :param path: относительный к BASE_URL путь, пример */auth/login*
        :param kwargs:
        :return:
        """
        try:
            response = await self._send(
                method=method, path=f"{BASE_URL}/{path}", **kwargs
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code != 401:
                raise

            await self._login()

            response = await self._send(method, path, **kwargs)
        return response
