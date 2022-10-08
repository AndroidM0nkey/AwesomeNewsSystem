FROM python:3
RUN python -m pip install --upgrade pip
COPY requirements.txt /
RUN python -m pip install -r requirements.txt
COPY create_db.py /
CMD ["python", "create_db.py"]
