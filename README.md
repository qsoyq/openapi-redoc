# openapi-redoc

拉取多个服务的 `openapi.json`文件, 合并`paths`项和`components`项.

其余部分可通过环境变量配置.

## 通过环境变量配置

接口在被请求时, 会读取环境变量中所有匹配`openapi_url_*`的值作为需要收集的目标.

```sh
docker network create my_bridge
docker run -d --network my_bridge  -e openapi_url_pywhoami=http://openapi_pywhoami:8000/openapi.json  -p 8888:8000  clpy9793/openapi-redoc
docker run  -d --network my_bridge --name openapi_pywhoami  clpy9793/pywhoami
```

## 通过 docker label 配置

在启动服务时, 设置环境变量`label_name`和`label_value`.

需要暴露 API 文档的容器需要配置相应的 docker label 键值.

```sh
docker network create my_bridge
docker run -d --network my_bridge -v /var/run/docker.sock:/var/run/docker.sock  -e label_name=openapi-redoc -e label_value=test -p 8888:8000  clpy9793/openapi-redoc
docker run  -d --network my_bridge  --label openapi-redoc=test clpy9793/pywhoami
```

## 本地运行

```sh
pip install poetry
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true
poetry install
poetry shell
pre-commit install
python src/main.py
```
