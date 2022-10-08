import grpc
import contracts_pb2_grpc
from contracts_pb2 import ModelServiceAnswer, CategoryInfo

from concurrent import futures
import logging

import torch
from torch import nn
from transformers import AutoTokenizer, AutoModel
from transformers import BertTokenizer
from transformers import BertModel


GRPC_SERVER_MAX_WORKERS = 10
MODEL_SERVICE_PORT = 8001

tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
labels = {'BUH':0, 'HR':1, 'BDG':2, 'GZ':3, 'MED':4, 'JUR':5 }

class BertClassifier(nn.Module):

    def __init__(self, dropout=0.5):

        super(BertClassifier, self).__init__()

        self.bert = AutoModel.from_pretrained("cointegrated/rubert-tiny")
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(312, 6)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):

        _, self.pooled_output = self.bert(input_ids= input_id, attention_mask=mask,return_dict=False)
        dropout_output = self.dropout(self.pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)
        

        return final_layer


use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
model_path = 'classifier_1.0.model'
model = BertClassifier()
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)


def calculate_embedding(proto):
    text = proto.Body
    title = proto.Title
    with torch.no_grad():
        model.eval()
        X = tokenizer(f"{title} [SEP] {text}", padding='max_length',
                       max_length=512, truncation=True, return_tensors="pt")
        # X = X.reshape(1, *X.shape)
        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")
        X = X.to(device)
        mask = X['attention_mask'].to(device)
        input_id = X['input_ids'].squeeze(1).to(device)
        pred = model(input_id, mask)
        embedding = model.pooled_output.to('cpu').numpy().tolist()
    
    return embedding


def calculate_categories(proto):
    text = proto.Body
    title = proto.Title
    with torch.no_grad():
        model.eval()
        X = tokenizer(f"{title} [SEP] {text}", padding='max_length',
                       max_length=512, truncation=True, return_tensors="pt")
        # X = X.reshape(1, *X.shape)
        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")
        X = X.to(device)
        mask = X['attention_mask'].to(device)
        input_id = X['input_ids'].squeeze(1).to(device)
        pred = model(input_id, mask)

    categoriesList = []
    for i in range(len(pred)):
        catInfo = CategoryInfo(Category=labels[i], Probability=(pred[i]))
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

