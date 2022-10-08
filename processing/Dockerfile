FROM python:3
RUN python -m pip install --upgrade pip
COPY requirements.txt /
RUN python -m pip install -r requirements.txt
EXPOSE 5672
EXPOSE 15672
COPY test_producer.py /
COPY contracts_pb2.py /
COPY contracts_pb2_grpc.py /
COPY processor.py /
CMD ["python", "processor.py"]
