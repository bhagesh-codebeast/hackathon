FROM continuumio/miniconda3:latest

RUN conda update -n base -c defaults conda && \
    conda create -n ml python=3.11 && \
    echo "source activate ml" > ~/.bashrc

ENV PATH /opt/conda/envs/ml/bin:$PATH

RUN conda install -n ml -c conda-forge -c anaconda streamlit streamlit-extras pandas

ENV PORT = 8000

# COPY app/* /app


# Docker STuff
# pip install 'transformers[torch]'
# pip install sentencepiece
# pip install hf_transfer
# HF_HUB_ENABLE_HF_TRANSFER=1
