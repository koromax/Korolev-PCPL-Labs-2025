from behave import given, when, then
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "lab3", "lab_python_fp"))
from gen_random import gen_random

@given("I want to generate numbers")
def step_given_gen(context):
    pass

@given("I want to generate negative numbers")
def step_given_gen(context):
    pass

@when('I generate {n} numbers ranging between {mn} and {mx}')
def step_when_gen(context, n, mn, mx):
    context.result = gen_random(int(n), int(mn), int(mx))

@when('I generate {n} negative numbers')
def step_when_filter_unique_ignore_case(context, n):
    context.result = gen_random(int(n), -10, -1)

@then("I should get {n} numbers ranging between {mn} and {mx}")
def step_then_get_list(context, n, mn, mx):
    for e in context.result:
        assert int(mn) <= e <= int(mx)
    assert len(context.result) == int(n)

@then("I should get {n} negative numbers")
def step_then_get_list_ignore_case(context, n):
    for e in context.result:
        assert e < 0
