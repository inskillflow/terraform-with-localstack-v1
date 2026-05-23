"""Page DynamoDB multi-env."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from botocore.exceptions import ClientError

from lib.aws_clients import current_env, dynamodb_client, render_env_selector, table_name


st.set_page_config(page_title="DynamoDB - Multi-env", page_icon=":card_index_dividers:")
render_env_selector()

st.title("DynamoDB - Ressource Terraform")
st.caption(f"Environnement : **{current_env()}**")

table = table_name()
client = dynamodb_client()

if not table:
    st.error("Pas de table pour cet environnement. Avez-vous applique `terraform apply` ?")
    st.stop()

st.write(f"Table cible : `{table}`")


def _table_exists(name: str) -> bool:
    try:
        client.describe_table(TableName=name)
        return True
    except ClientError:
        return False


col1, col2 = st.columns(2)
with col1:
    if _table_exists(table):
        st.success("La table existe.")
    else:
        st.error("La table n'existe pas.")
        st.stop()

with col2:
    if st.button("Rafraichir"):
        st.rerun()

st.divider()

st.subheader("Ajouter un etudiant")
with st.form("add_student", clear_on_submit=True):
    student_id = st.text_input("student_id", value=f"{current_env().upper()}-S001")
    first_name = st.text_input("first_name", value="")
    last_name = st.text_input("last_name", value="")
    submitted = st.form_submit_button("Ajouter")
    if submitted and student_id:
        item: dict[str, dict[str, str]] = {"student_id": {"S": student_id}}
        if first_name:
            item["first_name"] = {"S": first_name}
        if last_name:
            item["last_name"] = {"S": last_name}
        try:
            client.put_item(TableName=table, Item=item)
            st.success(f"Etudiant `{student_id}` ajoute dans `{table}`.")
        except ClientError as exc:
            st.error(f"Erreur : {exc}")

st.divider()

st.subheader("Contenu de la table")
resp = client.scan(TableName=table)
items = resp.get("Items", [])

if not items:
    st.info("Table vide.")
else:
    rows = [{k: list(v.values())[0] for k, v in item.items()} for item in items]
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.subheader("Supprimer un etudiant")
    ids = [list(item["student_id"].values())[0] for item in items]
    to_delete = st.selectbox("Selectionner un student_id", options=ids)
    if st.button("Supprimer", type="primary"):
        client.delete_item(TableName=table, Key={"student_id": {"S": to_delete}})
        st.success(f"Etudiant `{to_delete}` supprime.")
        st.rerun()
