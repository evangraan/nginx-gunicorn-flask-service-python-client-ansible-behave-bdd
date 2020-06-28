Feature: API
  In order to record process lists received from client systems
  As a support engineer
  I want to verify that the service API is working

  Scenario: No configuration
    Given an API installation
    And no configuration file
    When the API is launched
    Then the API notifies 'configuration file does not exist'
    And the API exits

  Scenario: Unable to open configuration
    Given an API installation
    And a configuration file exists
    And the configuration file cannot be opened
    When the API is launched
    Then the API notifies 'Could not open configuration file'
    And the API exits

  Scenario: No storage directory configured
    Given an API installation
    And a configuration file exists
    And the configuration file does not have records_dir
    When the API is launched
    Then the API notifies 'Storage directory not configured'
    And the API exists

  Scenario: No storage directory
    Given an API installation
    And a configuration file exists
    And the configuration file is valid
    And the records_dir does not exist
    When the API is launched
    Then the API creates records_dir
    And the API continues to operate

  Scenario: No storage directory - fail to create
    Given an API installation
    And a configuration file exists
    And the configuration file is valid
    And the records_dir does not exist
    And the API fails to create records_dir
    When the API is launched
    Then the API notifies 'Could not create storage directory'
    And the API exits

  Scenario: Existing storage directory
    Given an API installation
    And a configuration file exists
    And the configuration file is valid
    And the records_dir does exist
    When the API is launched
    Then the API uses records_dir
    And the API continues to operate

  Scenario: Authentication success
    Given an API installation
    When the API receives a record
    And the client presents the correct bearer token
    Then the API stores the record in records_dir
    And the API responds with status code 200
    And the API responds with JSON containing the client uuid and client request timestamp

  Scenario: Authentication failure
    Given an API installation
    When the API receives a record
    And the client does not present the correct bearer token
    And the API responds with status code 401
    And the API responds with 'Unauthorized Access'

  Scenario: Receiving records
    Given an API installation
    And a configuration file exists
    And the configuration file is valid
    When the API receives a record
    Then the API stores the record in records_dir
    And the record contains the client uuid
    And the record contains the client timestamp
    And the API continues to operate

  Scenario: Receiving records - unable to write record
    Given an API installation
    And a configuration file exists
    And the configuration file is valid
    And the API cannot create a record
    When the API receives a record
    Then the API notifies 'Could not write'
    And the API continues to operate

