import json
import os
from template_manager import background_template, rest_query_template
from file_manager import write_to_file

def format_request_body(request_body, swagger_data):
    request_body_content = request_body.get('content', {})
    request_body_json = request_body_content.get('application/json', {}).get('schema', {})
    if '$ref' in request_body_json:
        ref_path = request_body_json['$ref'].split('/')[-1]
        request_body_json = swagger_data.get('components', {}).get('schemas', {}).get(ref_path, {})
    request_body_example = json.dumps(request_body_json, separators=(',', ':')) if request_body_json else "{}"
    return f"  And request {request_body_example}"

def generate_tests(swagger_data, api_name, output_dir):
    paths = swagger_data['paths']
    for endpoint, methods in paths.items():
        for method, details in methods.items():
            summary = details.get('summary', 'No summary provided')

            responses = details.get('responses', {})
            response = responses.get('200', {}).get('content', {}).get('*/*', {}).get('schema', {})
            if '$ref' in response:
                response = swagger_data['components']['schemas'].get(response['$ref'].split('/')[-1], {})
            response_example = json.dumps(response, indent=2) if response else "{}"

            request_body = details.get('requestBody', {})
            request_body_line = format_request_body(request_body, swagger_data) if request_body else ""

            additional_params = ""
            if method == 'get' and '{id}' in endpoint:
                additional_params = "  And param id = 123"
            elif method == 'get':
                additional_params = "  And param includeDetails = true"

            if method.lower() == 'get':
                expected_status = '200'
            elif method.lower() == 'post':
                expected_status = '201'
            else:
                expected_status = '200'

            scenario_name = f"{method.upper()} {endpoint.replace('{id}', '123')}"
            scenario_name_clean = scenario_name.replace('/', '_').replace(' ', '_')

            scenario_content = background_template + rest_query_template.format(
                scenario_name=scenario_name,
                endpoint=endpoint,
                method=method.upper(),
                additional_params=additional_params,
                request_body=request_body_line,
                expected_status=expected_status
            )

            filename = os.path.join(output_dir, f"{api_name}_{scenario_name_clean}.feature")
            write_to_file(filename, scenario_content)
