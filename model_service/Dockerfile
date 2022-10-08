FROM python:3
RUN python -m pip install --upgrade pip
COPY requirements.txt /
RUN python -m pip install -r requirements.txt
EXPOSE 8000
COPY classifier_1.0.model /
COPY contracts_pb2.py /
COPY contracts_pb2_grpc.py /
COPY grpc_server.py /
CMD ["python", "grpc_server.py"]
