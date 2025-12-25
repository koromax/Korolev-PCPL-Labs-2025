Feature: Field extraction from dictionaries

    Scenario: Extract single field
        Given I have a list of dictionaries
        When I extract field "title" from the list
        Then I should get ["Ковер", "Диван для отдыха"]
    
    Scenario: Extract multiple fields
        Given I have a list of dictionaries
        When I extract fields "title" and "price" from the list
        Then I should get dictionaries with "title" and "price" fields
