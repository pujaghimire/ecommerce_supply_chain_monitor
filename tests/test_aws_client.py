import builtins
import io
import sys

from aws_utils.aws_client import AWSClient


def test_put_metric_prints_message(capsys):
    aw = AWSClient()
    # put_metric should not raise and will print a message
    aw.put_metric("test.metric", 42)
    captured = capsys.readouterr()
    assert "METRIC test.metric=42" in captured.out


def test_aws_client_falls_back_when_boto3_missing(monkeypatch, capsys):
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "boto3":
            raise ImportError("No module named boto3")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    aw = AWSClient()
    assert aw.boto3 is None
    assert aw.s3 is None
    assert aw.ddb is None
    # fallback put_metric should still work
    aw.put_metric("fallback.metric", 1)
    captured = capsys.readouterr()
    assert "METRIC fallback.metric=1" in captured.out
