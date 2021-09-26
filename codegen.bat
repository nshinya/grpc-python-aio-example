python -m grpc_tools.protoc -Iprotos --python_out=server --grpc_python_out=server protos/helloworld.proto
python -m grpc_tools.protoc -Iprotos --python_out=client --grpc_python_out=client protos/helloworld.proto

python -m grpc_tools.protoc -Iprotos --python_out=server --grpc_python_out=server protos/hellostreamingworld.proto
python -m grpc_tools.protoc -Iprotos --python_out=client --grpc_python_out=client protos/hellostreamingworld.proto