from typing import Literal

import httpx

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

    async def _send(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Базовый метод, отправляющий запросы
        :param method: str, GET/POST и прочие
        :param path: путь относительно BASE_URL
        :param kwargs:
        :return:
        """
        response = httpx.request(
            method=method,
            url=path,
            **kwargs
        )
        response.raise_for_status()
        return response

    async def _login(self) -> None:
        """
        Получение access токена и сохранение в классе
        :return:
        """
        response = await self._send(
            method="post",
            path=f"/{BASE_URL}/auth/login",
            params={
                "login": self.__login,
                "password": self.__password
            }
        )
        self.__access_token = response.json()["access_token"]

    async def request(
            self,
            method: Literal["GET", "POST"],
            path: str,
            **kwargs
    ) -> httpx.Response:
        """

        """
        try:
            response = await self._send(
                method=method,
                path=path,
                **kwargs
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code != 401:
                raise

            await self._login()

            response = await self._send(
                method,
                path,
                **kwargs
            )
        return response
