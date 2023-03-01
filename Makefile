all: build

build:
	# Base images
	docker build base-images/ubuntu-conda 		-f ./base-images/ubuntu-conda/Dockerfile		--network host -t momiji-conda
	docker build base-images/pytorch 			-f ./base-images/pytorch/Dockerfile				--network host -t momiji-pytorch

	# Services
	docker build text-generator 	-f ./text-generator/Dockerfile		--network host -t momiji-text-generator
	docker build speech-recognition -f ./speech-recognition/Dockerfile	--network host -t momiji-speech-recognition
	docker build image-caption		-f ./image-caption/Dockerfile		--network host -t momiji-image-caption
	docker build image-caption		-f ./image-generator/Dockerfile		--network host -t momiji-image-generator

clean:
	@docker image rm momiji-conda				2> /dev/null || true
	@docker image rm momiji-pytorch				2> /dev/null || true

	@docker image rm momiji-text-generator		2> /dev/null || true
	@docker image rm momiji-speech-recognition	2> /dev/null || true
	@docker image rm momiji-image-caption		2> /dev/null || true
	@docker image rm momiji-image-generator		2> /dev/null || true
