all: build

build:
	# base image
	docker build ubuntu-conda 	-f ./ubuntu-conda/Dockerfile	--network host -t momiji-conda


	docker build text-generator -f ./text-generator/Dockerfile	--network host -t momiji-text-generator

clean:
	@docker image rm momiji-conda      			2> /dev/null || true
	@docker image rm momiji-text-generator      2> /dev/null || true
