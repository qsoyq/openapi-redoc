from typing import Optional

from pydantic import BaseSettings, HttpUrl


class InfoSettings(BaseSettings):
    title: str = 'OpenAPI'
    description: str = ''
    version: str = '0.1.0'


class ContactSettings(BaseSettings):

    contact_name: str = ''
    contact_url: Optional[HttpUrl] = None
    contact_email: str = ''


class AppSettings(BaseSettings):

    label_name: str = ''
    label_value: str = ''
