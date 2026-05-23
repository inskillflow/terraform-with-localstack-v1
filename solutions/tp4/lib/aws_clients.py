"""Clients boto3 configures pour parler a LocalStack (TP 4 : meme interface que TP 3,
le Streamlit ne sait pas que Terraform a ete refactorise en modules)."""

from __future__ import annotations

import json
import os
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any

import boto3
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_env() -> dict[str, str]:
    load_dotenv(PROJECT_ROOT / ".env")
    keys = [
        "LOCALSTACK_ENDPOINT",
        "AWS_REGION",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "S3_BUCKET_NAME",
        "DYNAMODB_TABLE_NAME",
        "SQS_QUEUE_NAME",
        "SQS_QUEUE_URL",
    ]
    return {k: os.getenv(k, "") for k in keys}


@lru_cache(maxsize=1)
def _config() -> dict[str, str]:
    return load_env()


def _client(service: str):
    cfg = _config()
    return boto3.client(
        service,
        endpoint_url=cfg["LOCALSTACK_ENDPOINT"] or "http://localhost:4566",
        region_name=cfg["AWS_REGION"] or "us-east-1",
        aws_access_key_id=cfg["AWS_ACCESS_KEY_ID"] or "test",
        aws_secret_access_key=cfg["AWS_SECRET_ACCESS_KEY"] or "test",
    )


def s3_client():
    return _client("s3")


def dynamodb_client():
    return _client("dynamodb")


def sqs_client():
    return _client("sqs")


def localstack_endpoint() -> str:
    return _config()["LOCALSTACK_ENDPOINT"] or "http://localhost:4566"


def bucket_name() -> str:
    return _config()["S3_BUCKET_NAME"]


def table_name() -> str:
    return _config()["DYNAMODB_TABLE_NAME"]


def queue_name() -> str:
    return _config()["SQS_QUEUE_NAME"]


def queue_url() -> str:
    return _config()["SQS_QUEUE_URL"]


def read_terraform_outputs() -> dict[str, Any]:
    terraform_dir = PROJECT_ROOT / "terraform"
    try:
        result = subprocess.run(
            ["terraform", f"-chdir={terraform_dir}", "output", "-json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"_error": str(exc)}

    raw = json.loads(result.stdout or "{}")
    return {name: meta.get("value") for name, meta in raw.items()}
