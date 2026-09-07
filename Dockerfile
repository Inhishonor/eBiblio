FROM zauberzeug/nicegui:latest

WORKDIR /app

COPY requirements.txt .

# Thi
RUN /usr/local/bin/pip --python /opt/venv/bin/python3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/opt/venv/bin/python3", "main.py"]
