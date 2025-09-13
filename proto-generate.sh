#!bin/bash
# This file is used to generate the proto files for a module bith given paths
# eg: sh proto-generate.sh ./communication-api-service/proto/communication_proto/meter_text/meter_text.proto ./communication-api-service/proto/communication_proto ./communication-api-service/proto/communication_proto
# eg: sh proto-generate.sh ./invoice-api-service/proto/invoice_proto/invoices/invoice.proto ./invoice-api-service/proto/invoice_proto ./invoice-api-service/proto/invoice_proto
# eg: sh proto-generate.sh ./payment-api-service/proto/payments_proto/transactions/transactions.proto ./payment-api-service/proto/payments_proto ./payment-api-service/proto/payments_proto
# eg: sh proto-generate.sh ./survey-api-service/proto/survey_proto/survey/survey.proto ./survey-api-service/proto/survey_proto ./survey-api-service/proto/survey_proto
# eg: sh proto-generate.sh ./user-api-service/proto/user_proto/user_user/user_user.proto ./user-api-service/proto/user_proto ./user-api-service/proto/user_proto

DEFAULT_DIR="."
INPUT="${1:-$DEFAULT_DIR}"
IMPORT="${2:-$DEFAULT_DIR}"
OUTPUT="${3:-$DEFAULT_DIR}"

python3 -m grpc_tools.protoc -I$IMPORT --python_out=$OUTPUT --pyi_out=$OUTPUT --grpc_python_out=$OUTPUT $INPUT

