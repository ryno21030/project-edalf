FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY modules/ modules/
COPY notify.py get_token.py ./

CMD ["python", "notify.py"]
