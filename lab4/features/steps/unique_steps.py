from behave import given, when, then
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "lab3", "lab_python_fp"))
from unique import Unique

@given("I have a list with duplicates ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']")
def step_given_list_of_dicts(context):
    context.data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']

@when('I filter unique values')
def step_when_filter_unique(context):
    context.result = list(Unique(context.data))

@when('I filter unique values ignoring case')
def step_when_filter_unique_ignore_case(context):
    context.result = list(Unique(context.data, ignore_case=True))

@then("I should get ['a', 'A', 'b', 'B']")
def step_then_get_list(context):
    assert context.result == ['a', 'A', 'b', 'B']

@then("I should get ['a', 'b']")
def step_then_get_list_ignore_case(context):
    assert context.result == ['a', 'b']
