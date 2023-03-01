FROM momiji-pytorch

RUN apt-get update && \
    apt-get install ffmpeg -y && \
    rm -rf /var/lib/apt/lists/*

SHELL ["conda", "run", "-n", "neuro", "--no-capture-output", "/bin/bash", "-c"]

RUN pip install openai-whisper pyyaml numpy setuptools-rust==1.5.2

WORKDIR /content

COPY src/ .

USER user

ENTRYPOINT conda run -n neuro --no-capture-output

CMD uvicorn app:app --host='0.0.0.0' --port='8080' --workers=1 --log-config=logging.yaml
