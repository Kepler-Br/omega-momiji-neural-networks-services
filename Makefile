all: build

build:
	# Base images
	docker build ubuntu-conda 		-f ./ubuntu-conda/Dockerfile		--network host -t momiji-conda
	docker build pytorch 			-f ./pytorch/Dockerfile				--network host -t momiji-pytorch

	# Services
	docker build text-generator 	-f ./text-generator/Dockerfile		--network host -t momiji-text-generator
	docker build speech-recognition -f ./speech-recognition/Dockerfile	--network host -t momiji-speech-recognition

clean:
	@docker image rm momiji-conda      			2> /dev/null || true
	@docker image rm momiji-pytorch      		2> /dev/null || true
	@docker image rm momiji-text-generator      2> /dev/null || true
	@docker image rm momiji-speech-recognition  2> /dev/null || true
