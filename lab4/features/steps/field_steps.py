from behave import given, when, then
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "lab3", "lab_python_fp"))
from field import field

@given("I have a list of dictionaries")
def step_given_list_of_dicts(context):
    context.data = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'color': 'black'},
        {'color': 'blue'}
    ]

@when('I extract field "{field_name}" from the list')
def step_when_extract_single_field(context, field_name):
    context.result = field(context.data, field_name)

@when('I extract fields "{field_name1}" and "{field_name2}" from the list')
def step_when_extract_multiple_fields(context, field_name1, field_name2):
    context.result = field(context.data, field_name1, field_name2)

@then('I should get ["Ковер", "Диван для отдыха"]')
def step_then_get_list(context):
    assert context.result == ["Ковер", "Диван для отдыха"]

@then('I should get dictionaries with "title" and "price" fields')
def step_then_get_dicts(context):
    assert context.result == [
                {'title': 'Ковер', 'price': 2000},
                {'title': 'Диван для отдыха'}
            ]
