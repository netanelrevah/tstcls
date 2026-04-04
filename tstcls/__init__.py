from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

from pytest import fixture

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    import pytest

__all__ = ["TestClassBase"]


class TestClassBase:
    @classmethod
    def find_fixtures(cls, func: Callable[..., Any], request: pytest.FixtureRequest) -> dict[str, Any]:
        fixtures = {}
        arg_spec = inspect.getfullargspec(func)
        for index, arg in enumerate(arg_spec.args):
            if index == 0 and arg in ["self", "cls"]:
                continue
            fixtures[arg] = request.getfixturevalue(arg)

        return fixtures

    @fixture(autouse=True, scope="class")
    def init_class(self, request: pytest.FixtureRequest) -> Iterator[None]:
        setup_fixtures = self.find_fixtures(self.setup_test_class, request)
        teardown_fixtures = self.find_fixtures(self.teardown_test_class, request)

        self.__class__.setup_test_class(**setup_fixtures)
        yield
        self.__class__.teardown_test_class(**teardown_fixtures)

    @fixture(autouse=True)
    def init(self, request: pytest.FixtureRequest) -> Iterator[None]:
        setup_fixtures = self.find_fixtures(self.setup_test, request)
        teardown_fixtures = self.find_fixtures(self.teardown_test, request)

        self.setup_test(**setup_fixtures)
        yield
        self.teardown_test(**teardown_fixtures)

    def setup_test(self, **fixtures: Any) -> None:  # noqa: ANN401
        pass

    def teardown_test(self, **fixtures: Any) -> None:  # noqa: ANN401
        pass

    @classmethod
    def setup_test_class(cls, **fixtures: Any) -> None:  # noqa: ANN401
        pass

    @classmethod
    def teardown_test_class(cls, **fixtures: Any) -> None:  # noqa: ANN401
        pass
