FROM 54.207.180.218:5000/python_cx:v.0.0.1

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3", "run.py"]