from typing import ClassVar

import pytest

from tstcls import TestClassBase


@pytest.fixture
def injected_value():
    return 42


@pytest.fixture(scope="class")
def class_injected_value():
    return "hello"


class TestSetupTest(TestClassBase):
    received = None

    def setup_test(self, injected_value):
        self.received = injected_value

    def test_fixture_injected_into_setup_test(self):
        assert self.received == 42


class TestTeardownTest(TestClassBase):
    calls: ClassVar[list[str]] = []

    def teardown_test(self):
        self.calls.append("teardown")

    def test_first(self):
        pass

    def test_teardown_was_called_after_previous_test(self):
        assert self.calls == ["teardown"]


class TestSetupTestClass(TestClassBase):
    call_count = 0

    @classmethod
    def setup_test_class(cls):
        cls.call_count += 1

    def test_setup_called_once_a(self):
        assert self.call_count == 1

    def test_setup_called_once_b(self):
        assert self.call_count == 1


class TestSetupTestClassWithFixture(TestClassBase):
    received = None

    @classmethod
    def setup_test_class(cls, class_injected_value):
        cls.received = class_injected_value

    def test_fixture_injected_into_setup_test_class(self):
        assert self.received == "hello"


class TestTeardownTestClass(TestClassBase):
    teardown_called = False

    @classmethod
    def teardown_test_class(cls):
        cls.teardown_called = True

    def test_teardown_not_yet_called(self):
        assert not self.teardown_called


class TestTeardownTestClassWasCalledAfterPrevious(TestClassBase):
    def test_previous_class_teardown_was_called(self):
        assert TestTeardownTestClass.teardown_called
