Feature: Reporting
  In order to record process lists on a client system
  As a client app
  I want to report to a service API
  Using a process list I obtained

  Scenario: Integration
    Given a client running
    And a service API running
    And client credentials
    And service API credentials
    And enough time for records to have been reported
    When I check the service API records repository
    Then I see the correct amount of records
    And the records have the client uuid
    And the records are timestamped
    And the records contain JSON process lists
