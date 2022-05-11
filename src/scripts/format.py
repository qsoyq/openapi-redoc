import inspect
import shlex
import subprocess

from pathlib import Path

import typer


def bad_message(message: str) -> str:
    return typer.style(message, fg=typer.colors.WHITE, bg=typer.colors.RED)


app = typer.Typer()
cwd = Path.cwd()


@app.command()
def install():
    """pre-commit对应的 hooks 需要单独安装. 其余命令通过`poetry install`安装.
    """
    cmd = 'pre-commit install'
    args = shlex.split(cmd)
    p = subprocess.run(args, capture_output=False, text=True, cwd=cwd.absolute())
    if p.returncode != 0:
        typer.echo(bad_message(f"{cmd} failed."))
        raise typer.Exit(p.returncode)


@app.command()
def mypy():
    """mypy static check"""
    _cwd = cwd / 'src'
    if not _cwd.exists() or not _cwd.is_dir():
        _cwd = cwd

    cmd = 'mypy .'
    args = shlex.split(cmd)
    p = subprocess.run(args, capture_output=False, text=True, cwd=_cwd.absolute())
    if p.returncode != 0:
        typer.echo(bad_message(f"{cmd} failed."))
        raise typer.Exit(p.returncode)


@app.callback(invoke_without_command=True)
def refactor(ctx: typer.Context):
    """代码格式化

    yapf -r -i . && isort . && pycln -a .
    """
    # 当前函数使用回调作为默认命令
    # 如果调用了其他子命令的情况, 退出当前函数处理流程
    if ctx.invoked_subcommand and ctx.invoked_subcommand != inspect.stack()[0].function:
        return

    cmds = [
        "yapf -r -i .",
        "isort .",
        "pycln -a .",
        "pre-commit run --all-file",
    ]
    for cmd in cmds:
        args = shlex.split(cmd)
        p = subprocess.run(args, capture_output=False, text=True, cwd=cwd.absolute())
        if p.returncode != 0:
            typer.echo(bad_message(f"{cmd} failed."))
            raise typer.Exit(p.returncode)


if __name__ == "__main__":
    app()
