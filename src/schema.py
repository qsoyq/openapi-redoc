from pydantic import BaseModel, HttpUrl


class ServerSchema(BaseModel):

    url: HttpUrl
    description: str = ''
