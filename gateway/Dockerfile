FROM python:3.9

WORKDIR /gateway

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/"

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7333"]