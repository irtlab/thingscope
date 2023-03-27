# dockerfile for a python application whose source is at flask_handler.py
# and whose dependencies are in requirements.txt
FROM python:3.7
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "flask_handler.py"]