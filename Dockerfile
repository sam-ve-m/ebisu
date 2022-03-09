FROM python:3.8 AS builder

ARG oci_nexus_password
ARG aws_nexus_password

WORKDIR /app

COPY requirements.txt requirements.txt

RUN mkdir -p ~/.pip/
RUN touch ~/.pip/pip.conf

RUN echo "[global]" >> ~/.pip/pip.conf
RUN echo "timeout = 60" >> ~/.pip/pip.conf
RUN echo "extra-index-url =" >> ~/.pip/pip.conf
RUN echo "    https://backend:${oci_nexus_password}@nexus.sigame.com.br/repository/pypi/simple" >> ~/.pip/pip.conf
RUN echo "    http://nexus:${aws_nexus_password}@54.207.180.218:80/repository/pypi/simple/" >> ~/.pip/pip.conf

RUN pip install --user -r requirements.txt --trusted-host 54.207.180.218

FROM 54.207.180.218:5000/python_cx:v.0.0.1
COPY --from=builder /root/.local /root/.local

RUN mkdir -p /opt/envs/heimdall.lionx.com.br/
RUN mkdir -p /opt/envs/ebisu.lionx.com.br/

RUN touch /opt/envs/heimdall.lionx.com.br/.env
RUN touch /opt/envs/ebisu.lionx.com.br/.env

COPY . .

RUN apt-get update
RUN apt-get -y install wkhtmltopdf

ENV PATH=/root/.local:$PATH

RUN pip install --upgrade pip
RUN python -m pip install --upgrade pip

EXPOSE 8000

ENTRYPOINT ["python3", "run.py"]