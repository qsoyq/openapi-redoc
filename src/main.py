import logging

import httpx
import typer
import uvicorn

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse

from settings import ContactSettings, InfoSettings, RefSettigns, ServerSettings

cmd = typer.Typer()
app = FastAPI(openapi_url=None)


@app.get('/redoc', include_in_schema=False)
async def redoc_html(req: Request) -> HTMLResponse:
    openapi_url = '/openapi.json'
    return get_redoc_html(openapi_url=openapi_url, title=InfoSettings().title + " - ReDoc")


@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    paths = {}
    components = {}
    urls = [f'{ref}' for ref in RefSettigns().refs]
    cli = httpx.AsyncClient(timeout=1.0)
    for url in urls:
        try:
            data = (await cli.get(url)).json()
        except Exception as e:
            print(f'url: {url}, error: {e}')
            continue
        paths.update(data.get('paths', []))
        components.update(data.get("components", {}))

    contact = {
        "name": ContactSettings().contact_name,
        "url": ContactSettings().contact_url,
        "email": ContactSettings().contact_email,
    }
    info = InfoSettings()
    content = get_openapi(title=info.title, version=info.version, routes=app.routes, contact=contact)
    content['paths'] = paths
    content['servers'] = [x.dict() for x in ServerSettings().servers]
    content['components'] = components
    return JSONResponse(content)


@cmd.command()
def http(
    host: str = typer.Option("0.0.0.0",
                             '--host',
                             '-h',
                             envvar='http_host'),
    port: int = typer.Option(8000,
                             '--port',
                             '-p',
                             envvar='http_port'),
    debug: bool = typer.Option(False,
                               '--debug',
                               envvar='http_debug'),
    reload: bool = typer.Option(False,
                                '--debug',
                                envvar='http_reload'),
):
    """启动 http 服务"""
    logging.info(f"http server listening on {host}:{port}")
    uvicorn.run(app, host=host, port=port, debug=debug, reload=reload)


if __name__ == '__main__':
    cmd()
