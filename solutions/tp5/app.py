"""Dashboard Streamlit du TP 5 (multi-environnements dev / test)."""

from __future__ import annotations

import requests
import streamlit as st

from lib.aws_clients import (
    bucket_name,
    current_env,
    localstack_endpoint,
    queue_name,
    render_env_selector,
    table_name,
)


st.set_page_config(
    page_title="TP 5 - Multi-environnements",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("TP 5 - Validation multi-environnements (dev / test)")

env = render_env_selector()
st.caption(f"Environnement Terraform selectionne : **{current_env()}**")

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
        st.error(f"Ne repond pas : {msg}")

with col2:
    st.subheader("Bucket S3")
    name = bucket_name()
    st.info(name) if name else st.warning("`terraform apply` non execute ?")

with col3:
    st.subheader("Table DynamoDB")
    name = table_name()
    st.info(name) if name else st.warning("`terraform apply` non execute ?")

with col4:
    st.subheader("File SQS")
    name = queue_name()
    st.info(name) if name else st.warning("`terraform apply` non execute ?")

st.divider()

st.markdown(
    f"""
    ### Principe du TP 5

    Un meme code Terraform (les modules `modules/s3`, `modules/dynamodb`,
    `modules/sqs`) est instancie deux fois, dans deux environnements :

    | Environnement | Dossier | Bucket S3 | Table DynamoDB | File SQS |
    |---|---|---|---|---|
    | dev  | `terraform/environments/dev/`  | `tp-localstack-dev-documents`  | `tp-localstack-dev-students`  | `tp-localstack-dev-notifications`  |
    | test | `terraform/environments/test/` | `tp-localstack-test-documents` | `tp-localstack-test-students` | `tp-localstack-test-notifications` |

    Choisissez `dev` ou `test` dans la barre laterale, puis naviguez vers les
    pages S3 / DynamoDB / SQS pour voir les ressources de cet environnement.

    > Selection actuelle : **{env}**
    """
)
