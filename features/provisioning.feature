Feature: Provisioning
  In order to facilitate reporting of record process lists
  As a devops engineer
  I want to provision the client and server API

  # Manual
  Scenario: Client provisioning
    Given client credentials
    When I run automated client provisioning
    Then all necessary python packages are installed
    And a python venv is created
    And the client repository is cloned
    And the client is registered as a service
    And the client runs on reboot
    And the client is configured to communicate successfully with the API

  # Manual
  Scenario: Service API provisioning
    Given service API credentials
    When I run automated API provisioning
    Then all necessary python packages are installed
    And a python venv is created
    And the service repository is cloned
    And the service is registered as a service
    And the service runs on reboot
    And the service is configured to communicate successfully with clients
    And cron is configured to clear old records
    And SELinux is configured to support HTTPS and HTTP
    And the firewall is configured to open the necessary ports only
    And the service API is secured using SSL
    And the service API redirects HTTP to HTTPS
    And the service API is configured to handle load using gunicorn
    And the service API is proxied using nginx