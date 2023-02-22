all: build

build:
	docker build . -f ./ubuntu-conda/Dockerfile 	--network host	-t momiji-conda

clean:
	@docker image rm ./ubuntu-conda/Dockerfile      2> /dev/null || true
