FROM momiji-conda

WORKDIR /content

COPY environment.yaml .

RUN CONDA_OVERRIDE_CUDA='11.7' \
    conda env create -f environment.yaml && \
    rm environment.yaml

SHELL ["conda", "run", "-n", "neuro", "--no-capture-output", "/bin/bash", "-c"]

RUN echo "conda activate neuro" >> /home/user/.bashrc && \
    echo "conda activate neuro" >> /root/.bashrc

COPY src/ .

USER user
