import shlex

from pathlib import Path
from subprocess import Popen

import typer


def bad_message(message: str) -> str:
    return typer.style(message, fg=typer.colors.WHITE, bg=typer.colors.RED)


app = typer.Typer()
cwd = Path.cwd()


@app.command()
def build(
    name: str = typer.Argument(...,
                               help='镜像名称'),
    tag: str = typer.Option("latest",
                            '--tag',
                            '-t'),
    dockerfile: str = typer.Option("Dockerfile",
                                   '-f'),
):
    """构建镜像"""
    context = cwd
    build_path = cwd / dockerfile

    assert build_path.is_file(), f'需要在项目根目录下执行脚本, 当前工作目录: {cwd}'

    name = f'{name}:{tag}'
    cmd = f"docker build --platform linux/amd64 -t {name} -f {build_path.absolute()} {context.absolute()}"
    typer.echo(f'the command is: {cmd}')

    args = shlex.split(cmd)
    p = Popen(args)
    exitcode = p.wait()
    if exitcode != 0:
        typer.echo(bad_message(f"build image {name} failed."))
        raise typer.Exit(exitcode)

    typer.echo(f"build image {name} successed.")


@app.command()
def publish(
    name: str = typer.Argument(...,
                               help='镜像名称'),
    tag: str = typer.Option("latest",
                            '--tag',
                            '-t'),
):
    """推送镜像到仓库"""

    name = f'{name}:{tag}'
    cmd = f'docker push {name}'
    p = Popen(shlex.split(cmd))
    exitcode = p.wait()
    if exitcode != 0:
        typer.echo(bad_message(f"push image {name} failed."))
        raise typer.Exit(exitcode)

    typer.echo(f"push image {name} successed.")


if __name__ == "__main__":
    app()
