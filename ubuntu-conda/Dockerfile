FROM ubuntu:22.04

# Create non root user
RUN groupadd --gid 1000 user && \
    useradd --uid 1000 --gid 1000 -m user && \
    usermod --shell /bin/bash user

# Install conda

RUN apt-get update && \
    apt-get install curl -y && \
    rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR=/opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

RUN curl --silent https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh > ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh

RUN groupadd condagroup && \
    chgrp -R condagroup $CONDA_DIR && \
    chmod 770 -R $CONDA_DIR && \
    adduser user condagroup

COPY conda.bashrc conda.bashrc

RUN cat conda.bashrc >> /root/.bashrc && \
    rm conda.bashrc
