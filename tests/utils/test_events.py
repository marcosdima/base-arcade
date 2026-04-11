import pytest
from src.utils import Event


@pytest.fixture
def empty_callback():
	return lambda *_args, **_kwargs: None


@pytest.fixture
def empty_event():
	return Event()


@pytest.fixture
def event_with_validators() -> Event[[int, str]]:
	event = Event[[int, str]]()
	event.validators = [
		lambda value, label, **kw: value > 0, # Validator that checks if the value is positive.
		lambda _, label, **kw: len(label) > 0, # Validator that checks if the label is not empty.
	]
	return event


def test_suscribe_adds_callback(empty_event: Event, empty_callback: callable):
	empty_event.subscribe(empty_callback)
	assert empty_callback in empty_event.callbacks


def test_unsuscribe_removes_existing_callback(empty_event: Event, empty_callback: callable):
	empty_event.subscribe(empty_callback)

	empty_event.unsubscribe(empty_callback)

	assert empty_callback not in empty_event.callbacks


def test_unsuscribe_ignores_unknown_callback(empty_event: Event, empty_callback: callable):
	with pytest.raises(ValueError):
		empty_event.unsubscribe(empty_callback)


def test_trigger_calls_callback_when_validators_pass(event_with_validators: Event[[int, str]]):
    calls = []

    def callback(possitive_value, label):
        calls.append((possitive_value, label))

    event_with_validators.subscribe(callback)
    event_with_validators.trigger(10, "ok")

    assert calls == [(10, "ok")]


def test_trigger_does_not_call_callback_when_validator_fails(event_with_validators: Event[[int, str]]):
	calls = []

	def callback(possitive_value, label):
		calls.append((possitive_value, label))
	
	event_with_validators.subscribe(callback)

	# Trigger with wrong value type.
	with pytest.raises(ValueError):
		event_with_validators.trigger(-1, 'ok')

	# Trigger with wrong label type.
	with pytest.raises(ValueError):
		event_with_validators.trigger(10, '')


def test_clear_removes_all_callbacks(empty_event: Event, empty_callback: callable):
	empty_event.subscribe(empty_callback)
	empty_event.subscribe(lambda: None)  # Add another callback to ensure all are cleared.

	empty_event.clear()

	assert empty_event.callbacks == []


def test_event_param_specification():
	event = Event[[int, str]]()

	called = False

	def callback(value: int, label: str):
		nonlocal called
		called = True

	event.subscribe(callback)

	event.trigger(42, "test")

	assert called is True
