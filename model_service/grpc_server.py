import grpc
import contracts_pb2_grpc
from contracts_pb2 import ModelServiceAnswer, CategoryInfo

from concurrent import futures
import logging


# GRPC server

GRPC_SERVER_MAX_WORKERS = 10
MODEL_SERVICE_PORT = 8001


def calculate_embeddings(proto):
    # dummy output
    return [1.0, 0.1]


def calculate_categories(proto):
    # dummu output
    categoriesList = []
    for i in range(2):
        catInfo = CategoryInfo(Category=('Cat' + str(i)), Probability=(i + 1))
        categoriesList.append(catInfo)
    return categoriesList

class ModelService(contracts_pb2_grpc.ModelServiceServicer):

    def GetModelServiceAnswer(self, request, context):
        answer = ModelServiceAnswer(Categories=calculate_categories(request), Embeddings=calculate_embeddings(request))
        return answer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_SERVER_MAX_WORKERS))
    contracts_pb2_grpc.add_ModelServiceServicer_to_server(ModelService(), server)
    server.add_insecure_port('[::]:8001')
    server.start()
    server.wait_for_termination()



print('GRPC Model Service starting')
logging.basicConfig()
serve()

