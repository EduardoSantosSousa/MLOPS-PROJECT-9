FROM python:3.11

WORKDIR /app

# Copiar tudo exceto o que está no .dockerignore
COPY . .

RUN pip install --no-cache-dir -e .

EXPOSE 5000

ENV FLASK_APP = application.py

CMD ["python", "application.py"]