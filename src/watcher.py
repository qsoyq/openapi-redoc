"""
通过 Docker events 监听容器变化, 并获得所有容器的主机和端口信息
"""
import itertools

from dataclasses import dataclass

from docker import DockerClient, from_env
from docker.models.containers import Container


@dataclass
class Address:
    ip: str
    port: str

    def __repr__(self) -> str:
        return f"{self.ip}:{self.port}"


class DockerWatcher:
    """监听事件
    """

    def __init__(self):
        self.api: DockerClient = from_env()
        self._state = 0

    def containers_by_label(self, label_key: str, label_val: str) -> list[Container]:
        filter_ = {"label": f"{label_key}={label_val}"}
        return self.api.containers.list(filters=filter_)  # type: ignore

    def get_ipaddress(self, container: Container) -> list[Address]:
        ports: list[str] = []
        ips: list[str] = []
        for key in container.ports.keys():
            if isinstance(key, str) and key.endswith('/tcp'):
                p, _, _ = key.partition('/')
                ports.append(p)

        assert container.attrs
        networks = container.attrs.get("NetworkSettings", {}).get("Networks", [])
        for bridge in networks:
            ips.append(networks[bridge]["IPAddress"])

        return [Address(ip, port) for ip, port in itertools.product(ips, ports)]
