FROM python:3.11

RUN wget -O - https://www.openssl.org/source/openssl-1.1.1u.tar.gz | tar zxf -
RUN cd openssl*/
RUN ./config --prefix=/usr/local
RUN make -j $(nproc)
RUN make install_sw install_ssldirs
RUN ldconfig -v
RUN export SSL_CERT_DIR=/etc/ssl/certs
RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
RUN apt-get update -y
RUN apt-get install build-essential libssl-dev wget
RUN python -m pip install azure-ai-vision
RUN pip install --no-cache-dir azure-core azure-ai-formrecognizer
RUN pip install --no-cache-dir streamlit streamlit-extras pandas

ENV PORT = 8000

WORKDIR /app/

COPY app/* .

CMD ["streamlit", "run", "/app/app.py", "--server.port", "8000"]