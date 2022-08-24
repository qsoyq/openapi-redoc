from pydantic import AnyHttpUrl, BaseModel


class ServerSchema(BaseModel):

    url: AnyHttpUrl
    description: str = ''
