.PHONY: default refactor mypy image push


IMAGE_NAME := clpy9793/openapi-redoc

default: refactor pre-commit image push

refactor:
	@yapf -r -i . 
	@isort . 
	@pycln -a .

pre-commit:
	@pre-commit run --all-file

mypy:
	@mypy .

image:
	docker build --platform linux/amd64 -t $(IMAGE_NAME) .

push:
	docker push $(IMAGE_NAME)	