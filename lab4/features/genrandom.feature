Feature: Generate Random Values

    Scenario: Correct generation
        Given I want to generate numbers
        When I generate 100 numbers ranging between 1 and 100
        Then I should get 100 numbers ranging between 1 and 100
    
    Scenario: Generation in negative range
        Given I want to generate negative numbers
        When I generate 5 negative numbers
        Then I should get 5 negative numbers
