Feature: Client
  In order to record process lists on a client system
  As a support engineer
  I want to verify that the client app is working

  Scenario: No configuration
    Given a client installation
    And no configuration file
    When the client is launched
    Then the client notifies 'configuration file does not exist'
    And the client exits

  Scenario: Unable to open configuration
    Given a client installation
    And a configuration file exists
    And the configuration file cannot be opened
    When the client is launched
    Then the client notifies 'Could not open configuration file'
    And the client exits

  Scenario: No uuid configured
    Given a client installation
    And a configuration file exists
    And the configuration file does not include uuid
    When the client is launched
    Then the client notifies 'client uuid not configured'
    And the client exits

  Scenario: No service API URL configured
    Given a client installation
    And a configuration file exists
    And the configuration file does not include url
    When the client is launched
    Then the client notifies 'server url not configured'
    And the client exits

  Scenario: No bearer token configured
    Given a client installation
    And a configuration file exists
    And the configuration file does not include token
    When the client is launched
    Then the client notifies 'bearer token not configured'
    And the client exits

  Scenario: POST to service API fails
    Given a client installation
    And a configuration file exists
    And the configuration is valid
    And the client cannot POST to the service API
    When the client reports
    Then the client notifies 'POST failed'
    And the client continues to operate

  Scenario: Reporting
    Given a client installation
    And a configuration file exists
    And the configuration is valid
    When 5 seconds have passed
    Then the client obtains a list of processes
    And the client authenticates with the service API using its bearer token
    And the client identifies with the service API using its uuid
    And the client POSTs the list as JSON to the service API
    And the client notifies using the API response code
    And the client notifies using the API response body
    And the client continues to operate
