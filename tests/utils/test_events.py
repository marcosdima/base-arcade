import pytest

from src.utils import Event


@pytest.fixture
def event() -> Event:
	return Event()


def test_suscribe_adds_callback(event: Event):
	callback = lambda *_args, **_kwargs: None

	event.suscribe(callback)

	assert callback in event.callbacks


def test_unsuscribe_removes_existing_callback(event: Event):
	callback = lambda *_args, **_kwargs: None
	event.suscribe(callback)

	event.unsuscribe(callback)

	assert callback not in event.callbacks


def test_unsuscribe_ignores_unknown_callback(event: Event):
	callback = lambda *_args, **_kwargs: None

	event.unsuscribe(callback)

	assert event.callbacks == []


def test_trigger_calls_callback_when_validators_pass(event: Event):
	calls = []

	def callback(value, label, *, flag=False):
		calls.append((value, label, flag))

	event.validators = [lambda v: isinstance(v, int), lambda v: isinstance(v, str)]
	event.suscribe(callback)

	event.trigger(10, "ok", flag=True)

	assert calls == [(10, "ok", True)]


def test_trigger_does_not_call_callback_when_validator_fails(event: Event):
	called = False

	def callback(*_args, **_kwargs):
		nonlocal called
		called = True

	event.validators = [lambda v: isinstance(v, int)]
	event.suscribe(callback)

	event.trigger("invalid")

	assert called is False


def test_trigger_without_validators_still_calls_callback(event: Event):
	called = False

	def callback(*_args, **_kwargs):
		nonlocal called
		called = True

	event.suscribe(callback)

	event.trigger("anything")

	assert called is True


def test_clear_removes_all_callbacks(event: Event):
	event.suscribe(lambda *_args, **_kwargs: None)
	event.suscribe(lambda *_args, **_kwargs: None)

	event.clear()

	assert event.callbacks == []
