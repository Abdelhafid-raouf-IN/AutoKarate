from swagger_fetcher import fetch_swagger_data
from file_manager import create_directory, write_to_file
from test_generator import generate_tests

swagger_url = "http://localhost:9090/v3/api-docs/unibank-service-pilot"
output_dir = "unibank.service-testing"
api_name = "unibank.service-testing"
api_version = "v1"

swagger_data = fetch_swagger_data(swagger_url)

create_directory(output_dir)

generate_tests(swagger_data, api_name, output_dir)

print(f"Scénarios de test générés dans le dossier {output_dir}")
