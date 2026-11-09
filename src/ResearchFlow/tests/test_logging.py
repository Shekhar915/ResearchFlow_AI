import logging

from ResearchFlow.config.logging_config import setup_logging


def test_log_level_is_read_from_environment(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "debug")
    monkeypatch.setattr(logging, "basicConfig", lambda **kw: kw)
    captured = {}
    monkeypatch.setattr(logging, "basicConfig", lambda **kw: captured.update(kw))

    setup_logging()

    assert captured["level"] == logging.DEBUG


def test_invalid_log_level_falls_back_to_info(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "nonsense")
    captured = {}
    monkeypatch.setattr(logging, "basicConfig", lambda **kw: captured.update(kw))

    setup_logging()

    assert captured["level"] == logging.INFO
