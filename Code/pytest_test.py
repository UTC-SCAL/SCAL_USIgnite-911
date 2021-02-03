"""
Author: Jeremy Roland
Purpose: A template for using pytest, a tool that, at it's simplest level, can do some checking to check the logic
    of your code to make sure everything works as it should
Note: run pip install -U pytest in your python console to install. You can run pytest via the console by typing pytest
    Pytest will run any file that follows this naming format: test_*.py or *_test.py
"""
import pytest


# A basic function to return a value
def func(x):  # doesn't test this method since it doesn't start with test
    return x + 1


# Another basic function that uses assert to state something
# This is what pytest will be looking at to test
def test_answer():
    assert func(3) == 5  # This is the line that pytest catches as an error


# Grouping multiple tests in a class
class TestClass:
    """
    Benefits of grouping tests in a class: organization, sharing fixtures for tests, applying marks at class level
        and having them implicitly apply to all tests
    """
    def test_one(self):
        x = "this"
        assert "h" in x  # this assertion is true, so it'll pass

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")  # this assertion is false, so it won't pass


# Fixtures
class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


# By passing the fixtures in as arguments, we say that this method needs these variables/data
# Any future tests we run with this method, we won't have to worry about supplying those arguments, since now they're
# fixtures
def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket

