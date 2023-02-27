FROM momiji-pytorch

SHELL ["conda", "run", "-n", "neuro", "--no-capture-output", "/bin/bash", "-c"]

RUN pip install clip_interrogator

WORKDIR /content

COPY src/ .

USER user
