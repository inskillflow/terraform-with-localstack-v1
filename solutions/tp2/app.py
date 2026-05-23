"""Dashboard Streamlit - page d'accueil du TP 2.

Le but du dashboard est de valider visuellement que les ressources declarees
par Terraform existent reellement dans LocalStack.
"""

from __future__ import annotations

import requests
import streamlit as st

from lib.aws_clients import bucket_name, localstack_endpoint, table_name


st.set_page_config(
    page_title="TP 2 - Validation Terraform",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("TP 2 - Validation Terraform via Streamlit")
st.caption(
    "Terraform est la source de verite de l'infrastructure. "
    "Streamlit sert uniquement a verifier visuellement ce que Terraform a cree."
)

st.divider()


def _check_localstack(url: str) -> tuple[bool, str]:
    try:
        resp = requests.get(f"{url}/_localstack/info", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            edition = data.get("edition", "?")
            return True, f"LocalStack repond (edition: {edition})"
        return False, f"HTTP {resp.status_code}"
    except requests.RequestException as exc:
        return False, str(exc)


col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("LocalStack")
    ok, msg = _check_localstack(localstack_endpoint())
    if ok:
        st.success(msg)
    else:
        st.error(f"LocalStack ne repond pas : {msg}")
    st.code(localstack_endpoint())

with col2:
    st.subheader("Bucket S3 attendu")
    name = bucket_name()
    if name:
        st.info(name)
    else:
        st.warning("S3_BUCKET_NAME absent dans .env")

with col3:
    st.subheader("Table DynamoDB attendue")
    name = table_name()
    if name:
        st.info(name)
    else:
        st.warning("DYNAMODB_TABLE_NAME absent dans .env")

st.divider()

st.markdown(
    """
    ### Comment utiliser ce dashboard

    1. Utilisez la barre laterale pour naviguer entre les pages.
    2. **Terraform outputs** : compare `.env` avec les outputs Terraform.
    3. **S3** : verifie que le bucket existe, depose et liste des fichiers.
    4. **DynamoDB** : verifie que la table existe, ajoute et liste des items.

    > Si une page affiche une erreur, c'est que `terraform apply` n'a pas
    > encore ete execute, ou que LocalStack n'est pas demarre.
    """
)
