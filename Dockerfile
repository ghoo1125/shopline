FROM python:3.9

WORKDIR /app
COPY . /app 
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
