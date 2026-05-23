"""Clients boto3 et lecture multi-environnements (TP 5).

L'utilisateur choisit l'environnement (dev / test) dans la sidebar Streamlit.
La selection est stockee dans st.session_state['env'] et utilisee pour
lire les outputs Terraform du bon dossier `terraform/environments/<env>`.
"""

from __future__ import annotations

import json
import os
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any

import boto3
import streamlit as st
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_DIR = PROJECT_ROOT / "terraform" / "environments"


def load_dotenv_once() -> None:
    load_dotenv(PROJECT_ROOT / ".env")


def default_env() -> str:
    load_dotenv_once()
    return os.getenv("DEFAULT_TERRAFORM_ENV", "dev")


def available_environments() -> list[str]:
    if not ENV_DIR.exists():
        return []
    return sorted(p.name for p in ENV_DIR.iterdir() if p.is_dir())


def current_env() -> str:
    """Renvoie l'environnement actuellement selectionne dans la sidebar."""
    envs = available_environments()
    if not envs:
        return default_env()
    default = default_env() if default_env() in envs else envs[0]
    return st.session_state.get("env", default)


def localstack_endpoint() -> str:
    load_dotenv_once()
    return os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")


def _aws_creds() -> dict[str, str]:
    load_dotenv_once()
    return {
        "region_name": os.getenv("AWS_REGION", "us-east-1"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", "test"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    }


def _client(service: str):
    return boto3.client(service, endpoint_url=localstack_endpoint(), **_aws_creds())


def s3_client():
    return _client("s3")


def dynamodb_client():
    return _client("dynamodb")


def sqs_client():
    return _client("sqs")


@lru_cache(maxsize=4)
def _read_terraform_outputs_cached(env: str) -> dict[str, Any]:
    env_dir = ENV_DIR / env
    if not env_dir.exists():
        return {"_error": f"L'environnement '{env}' n'existe pas dans {ENV_DIR}."}
    try:
        result = subprocess.run(
            ["terraform", f"-chdir={env_dir}", "output", "-json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"_error": str(exc)}

    raw = json.loads(result.stdout or "{}")
    return {name: meta.get("value") for name, meta in raw.items()}


def read_terraform_outputs(env: str | None = None) -> dict[str, Any]:
    env = env or current_env()
    return _read_terraform_outputs_cached(env)


def bucket_name(env: str | None = None) -> str:
    outputs = read_terraform_outputs(env)
    return outputs.get("s3_bucket_name", "") or ""


def table_name(env: str | None = None) -> str:
    outputs = read_terraform_outputs(env)
    return outputs.get("dynamodb_table_name", "") or ""


def queue_name(env: str | None = None) -> str:
    outputs = read_terraform_outputs(env)
    return outputs.get("sqs_queue_name", "") or ""


def queue_url(env: str | None = None) -> str:
    outputs = read_terraform_outputs(env)
    return outputs.get("sqs_queue_url", "") or ""


def render_env_selector() -> str:
    """Affiche le selecteur d'environnement dans la sidebar et retourne le choix."""
    envs = available_environments()
    if not envs:
        st.sidebar.error(
            "Aucun environnement trouve dans `terraform/environments/`. "
            "Avez-vous cree les dossiers `dev/` et `test/` ?"
        )
        return ""

    default = default_env() if default_env() in envs else envs[0]
    if "env" not in st.session_state:
        st.session_state["env"] = default

    chosen = st.sidebar.selectbox(
        "Environnement Terraform",
        options=envs,
        index=envs.index(st.session_state["env"]),
        key="env_select",
    )
    if chosen != st.session_state["env"]:
        st.session_state["env"] = chosen
        _read_terraform_outputs_cached.cache_clear()
        st.rerun()
    return chosen
