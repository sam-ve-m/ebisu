FROM nexus:5000/python_cx:v.0.0.1

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get -y install wkhtmltopdf

EXPOSE 8000

ENTRYPOINT ["python3", "run.py"]