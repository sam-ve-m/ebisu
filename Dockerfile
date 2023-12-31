FROM python:3.8 AS builder

ARG oci_nexus_password

COPY requirements.txt requirements.txt

RUN mkdir -p ~/.pip/
RUN touch ~/.pip/pip.conf

RUN echo "[global]" >> ~/.pip/pip.conf
RUN echo "timeout = 60" >> ~/.pip/pip.conf
RUN echo "extra-index-url =" >> ~/.pip/pip.conf
RUN echo "    https://backend:${oci_nexus_password}@nexus.sigame.com.br/repository/pypi/simple" >> ~/.pip/pip.conf

RUN pip install --user -r requirements.txt

FROM nexus.sigame.com.br/python-cx:0.0.1
COPY --from=builder /root/.local /root/.local

RUN mkdir -p /opt/envs/heimdall.lionx.com.br/
RUN mkdir -p /opt/envs/ebisu.lionx.com.br/
RUN mkdir -p /opt/envs/etria.lionx.com.br/
RUN mkdir -p /opt/envs/mist.lionx.com.br/
RUN mkdir -p /opt/envs/mepho.lionx.com.br/
RUN mkdir -p /opt/envs/persephone.client.python.lionx.com.br/
RUN mkdir -p /opt/envs/floki_client.lionx.com.br/
RUN mkdir -p /opt/envs/caronte.lionx.com.br/
RUN mkdir -p /opt/envs/halberd.lionx.com.br/
RUN mkdir -p /opt/envs/bifrost.client.python.lionx.com.br/

RUN touch /opt/envs/heimdall.lionx.com.br/.env
RUN touch /opt/envs/ebisu.lionx.com.br/.env
RUN touch /opt/envs/etria.lionx.com.br/.env
RUN touch /opt/envs/mist.lionx.com.br/.env
RUN touch /opt/envs/mepho.lionx.com.br/.env
RUN touch /opt/envs/persephone.client.python.lionx.com.br/.env
RUN touch /opt/envs/floki_client.lionx.com.br/.env
RUN touch /opt/envs/caronte.lionx.com.br/.env
RUN touch /opt/envs/halberd.lionx.com.br/.env
RUN touch /opt/envs/bifrost.client.python.lionx.com.br/.env

COPY . .

ENV PATH=/root/.local:$PATH

EXPOSE 8000

ENTRYPOINT ["python3", "run.py"]