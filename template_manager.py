background_template = """Feature:
  Background:
    * configure ssl = true
    * url 'http://localhost:9090/'
"""
rest_query_template = """
  Scenario: {scenario_name}
    Given path '{endpoint}'
    {additional_params}
    {request_body}
    When method {method}
    Then status {expected_status}
    And print 'Actual response:', response
    * def responseHeaders = responseHeaders
    * def responseBody = response
    * karate.log('Response Headers:', responseHeaders)
    * karate.log('Response Body:', responseBody)
"""
