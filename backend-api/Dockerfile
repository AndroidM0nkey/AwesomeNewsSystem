FROM python:3.7
RUN python -m pip install --upgrade pip
COPY requirements.txt /
RUN python -m pip install -r requirements.txt
COPY contracts_pb2.py /
COPY contracts_pb2_grpc.py /
COPY kmeans.pkl /
COPY server.py /
CMD ["python", "server.py"]
