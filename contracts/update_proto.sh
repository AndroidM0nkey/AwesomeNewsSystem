sudo python3 -m grpc_tools.protoc -I. --python_out=./../processing/ --grpc_python_out=./../processing/ contracts.proto
sudo python3 -m grpc_tools.protoc -I. --python_out=./../model_service/ --grpc_python_out=./../model_service/ contracts.proto
