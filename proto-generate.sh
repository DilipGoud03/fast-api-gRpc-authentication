#!bin/bash
# This file is used to generate the proto files for a module bith given paths
# eg: sh proto-generate.sh ./user-api-service/proto/user_proto/user_user/user_user.proto ./user-api-service/proto/user_proto ./user-api-service/proto/user_proto

DEFAULT_DIR="."
INPUT="${1:-$DEFAULT_DIR}"
IMPORT="${2:-$DEFAULT_DIR}"
OUTPUT="${3:-$DEFAULT_DIR}"

python3 -m grpc_tools.protoc -I$IMPORT --python_out=$OUTPUT --pyi_out=$OUTPUT --grpc_python_out=$OUTPUT $INPUT

