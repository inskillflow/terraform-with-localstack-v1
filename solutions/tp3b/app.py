"""Dashboard Streamlit du TP 3 (S3 + DynamoDB + SQS)."""

from __future__ import annotations

import requests
import streamlit as st

from lib.aws_clients import bucket_name, localstack_endpoint, queue_name, table_name


st.set_page_config(
    page_title="TP 3 - Validation Terraform (S3 + DynamoDB + SQS)",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("TP 3 - Validation Terraform via Streamlit")
st.caption("S3 + DynamoDB + SQS, cree avec Terraform, valide ici visuellement.")

st.divider()


def _check_localstack(url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{url}/_localstack/info", timeout=3)
        if resp.status_code == 200:
            edition = resp.json().get("edition", "?")
            return True, f"LocalStack repond (edition: {edition})"
        return False, f"HTTP {resp.status_code}"
    except requests.RequestException as exc:
        return False, str(exc)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("LocalStack")
    ok, msg = _check_localstack(localstack_endpoint())
    if ok:
        st.success(msg)
    else:
        st.error(f"LocalStack ne repond pas : {msg}")
    st.code(localstack_endpoint())

with col2:
    st.subheader("Bucket S3")
    name = bucket_name()
    st.info(name) if name else st.warning("Manque dans .env")

with col3:
    st.subheader("Table DynamoDB")
    name = table_name()
    st.info(name) if name else st.warning("Manque dans .env")

with col4:
    st.subheader("File SQS")
    name = queue_name()
    st.info(name) if name else st.warning("Manque dans .env")

st.divider()

st.markdown(
    """
    ### Pages disponibles

    - **Terraform outputs** : compare `.env` aux outputs Terraform.
    - **S3** : valide le bucket cree par Terraform.
    - **DynamoDB** : valide la table creee par Terraform.
    - **SQS** : valide la file creee par Terraform, envoie / recoit des messages.
    - **A propos** : explications pedagogiques.

    > Toutes les ressources doivent venir de `terraform apply`.
    > Streamlit ne cree jamais d'infrastructure.
    """
)
