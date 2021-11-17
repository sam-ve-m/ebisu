FROM 54.207.180.218:5000/sigame_python_cx_oracle:v0.0.1

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3", "run.py"]