FROM momiji-pytorch

RUN apt-get update && \
    apt-get install ffmpeg -y && \
    rm -rf /var/lib/apt/lists/*

SHELL ["conda", "run", "-n", "neuro", "--no-capture-output", "/bin/bash", "-c"]

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /content

COPY src/ .

USER user

ENTRYPOINT conda run -n neuro --no-capture-output

CMD uvicorn app:app --host='0.0.0.0' --port='8080' --workers=1 --log-config=logging.yaml
