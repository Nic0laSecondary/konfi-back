FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY . .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]