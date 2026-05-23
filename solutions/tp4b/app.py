"""Dashboard Streamlit du TP 4 (modules Terraform : S3 + DynamoDB + SQS)."""

from __future__ import annotations

import requests
import streamlit as st

from lib.aws_clients import bucket_name, localstack_endpoint, queue_name, table_name


st.set_page_config(
    page_title="TP 4 - Modules Terraform + Streamlit",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("TP 4 - Validation modules Terraform")
st.caption(
    "Meme infrastructure que le TP 3, mais Terraform est maintenant organise en modules "
    "(modules/s3, modules/dynamodb, modules/sqs). Le dashboard ne devrait rien voir de different."
)

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
    ### Refactoring en modules

    Le code Terraform est maintenant decoupe en trois modules reutilisables :

    | Module | Role |
    |---|---|
    | `modules/s3` | Cree un bucket S3 avec convention de nommage |
    | `modules/dynamodb` | Cree une table DynamoDB avec convention de nommage |
    | `modules/sqs` | Cree une file SQS avec convention de nommage |

    Le `main.tf` racine appelle ces modules et leur passe `project_name`,
    `environment`, `owner_name` et un suffixe.

    **Resultat attendu** : les ressources cree(e)s gardent les memes noms,
    donc Streamlit fonctionne exactement comme avant.
    """
)
