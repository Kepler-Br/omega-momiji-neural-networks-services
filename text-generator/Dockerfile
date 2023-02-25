FROM momiji-pytorch

SHELL ["conda", "run", "-n", "neuro", "--no-capture-output", "/bin/bash", "-c"]

RUN pip install transformers==4.26.1

WORKDIR /content

COPY src/ .

USER user
