FROM 54.207.180.218:5000/python_cx:v.0.0.1

WORKDIR /app

RUN mkdir -p /root/.pip/

RUN pwd
COPY pip.conf /root/.pip/pip.conf
COPY . .

RUN mkdir -p /opt/envs/heimdall.lionx.com.br/
RUN touch /opt/envs/heimdall.lionx.com.br/.env

RUN pip3 install -r requirements.txt --trusted-host 54.207.180.218
RUN apt-get update
RUN apt-get -y install wkhtmltopdf

EXPOSE 8000

ENTRYPOINT ["python3", "run.py"]