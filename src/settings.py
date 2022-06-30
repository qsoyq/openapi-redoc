from typing import List, Optional

from pydantic import BaseSettings, HttpUrl

from schema import ServerSchema


class InfoSettings(BaseSettings):
    title: str = 'OpenAPI'
    description: str = ''
    version: str = '0.1.0'


class ContactSettings(BaseSettings):

    contact_name: str = ''
    contact_url: Optional[HttpUrl] = None
    contact_email: str = ''


class RefSettigns(BaseSettings):

    # 需要线上可访问的 openapi 文档地址
    refs: List[HttpUrl] = []


class ServerSettings(BaseSettings):
    servers: List[ServerSchema] = []
