# openapi-redoc

聚合多个服务对应的OpenAPI描述文件.

通过 http 请求拉取多个 `openapi.json`文件, 合并`paths`项和`components`项.

其余部分可通过环境变量配置.

## 使用注意

服务运行前需要传递指定的环境变量.

通过环境变量`refs`指定多个线上的 OpenAPI 描述文件访问链接.

通过环境变量`urls`指定多个服务器信息.

示例环境变量如下:

```sh
servers='[{"url": "https://host-01.com", "description":"生产环境"}, {"url": "https://host-02.com", "description":"测试环境"}]'

refs='["https://host-01.com/openapi.json", "https://host-02.com/openapi.json"]'
```

## 运行

```sh
pip install poetry
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true
poetry install
poetry shell
pre-commit install
python src/main.py
```

## 容器快捷部署

```sh
docker run -d -p 8888:8000 -e refs='["https://{host-01}/openapi.json", "https://{host-02}/openapi.json"]' clpy9793/openapi-redoc
```
