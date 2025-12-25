Feature: Unique

    Scenario: Filter copies
        Given I have a list with duplicates ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
        When I filter unique values
        Then I should get ['a', 'A', 'b', 'B']
    
    Scenario: Filter copies with ignore case
        Given I have a list with duplicates ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
        When I filter unique values ignoring case
        Then I should get ['a', 'b']
