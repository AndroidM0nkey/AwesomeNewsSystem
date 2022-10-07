import grpc
import contracts_pb2_grpc

from concurrent import futures
import logging


# GRPC server

GRPC_SERVER_MAX_WORKERS = 10
MODEL_SERVICE_PORT = 8000


class ModelService(contracts_pb2_grpc.ModelServiceServicer):

    def GetEmbeddings(self, request, context):
        request.Embeddings = calculate_embeddings(request)
        return request


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_SERVER_MAX_WORKERS))
    contracts_pb2_grpc.add_ModelServiceServicer_to_server(ModelService(), server)
    server.add_insecure_port('[::]:8000')
    server.start()
    server.wait_for_termination()



print('GRPC Model Service starting')
logging.basicConfig()
serve()


def calculate_embeddings(proto):
    # dummy output
    return [1.0, 0.1]
