FROM momiji-pytorch

SHELL ["conda", "run", "-n", "neuro", "--no-capture-output", "/bin/bash", "-c"]

WORKDIR /content

COPY src/ .

USER user

ENTRYPOINT conda run -n neuro --no-capture-output

CMD uvicorn app:app --host='0.0.0.0' --port='8080' --workers=1 --log-config=logging.yaml
