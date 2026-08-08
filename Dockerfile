FROM python:3.10-slim

WORKDIR /app

# Instalar FFmpeg para el procesamiento de video
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p downloads

CMD ["python", "bot.py"]
