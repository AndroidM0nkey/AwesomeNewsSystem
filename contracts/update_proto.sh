sudo python3 -m grpc_tools.protoc -I. --python_out=./../processing/ --grpc_python_out=./../processing/ contracts.proto
sudo python3 -m grpc_tools.protoc -I. --python_out=./../model_service/ --grpc_python_out=./../model_service/ contracts.proto
sudo python3 -m grpc_tools.protoc -I. --python_out=./../backend-api/ --grpc_python_out=./../backend-api/ contracts.proto
sudo python3 -m grpc_tools.protoc -I. --python_out=./../parser/forbes/ --grpc_python_out=./../parser/forbes/ contracts.proto
sudo python3 -m grpc_tools.protoc -I. --python_out=./../parser/rbc/ --grpc_python_out=./../parser/rbc/ contracts.proto
