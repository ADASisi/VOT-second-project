FROM python:3.12

WORKDIR /app

RUN pip install flask jwt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
