"""
Author: Jeremy Roland
Purpose: A template for using pytest, a tool that, at it's simplest level, can do some checking to check the logic
    of your code to make sure everything works as it should
Note: run pip install -U pytest in your python console to install. You can run pytest via the console by typing pytest
    Pytest will run any file that follows this naming format: test_*.py or *_test.py
"""


# A basic function to return a value
def func(x):
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
