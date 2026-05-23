"""Page S3 multi-env."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from botocore.exceptions import ClientError

from lib.aws_clients import bucket_name, current_env, render_env_selector, s3_client


st.set_page_config(page_title="S3 - Multi-env", page_icon=":package:")
render_env_selector()

st.title("S3 - Ressource Terraform")
st.caption(f"Environnement : **{current_env()}**")

bucket = bucket_name()
client = s3_client()

if not bucket:
    st.error("Pas de bucket pour cet environnement. Avez-vous applique `terraform apply` ?")
    st.stop()

st.write(f"Bucket cible : `{bucket}`")


def _bucket_exists(name: str) -> bool:
    try:
        client.head_bucket(Bucket=name)
        return True
    except ClientError:
        return False


col1, col2 = st.columns(2)
with col1:
    if _bucket_exists(bucket):
        st.success("Le bucket existe dans LocalStack.")
    else:
        st.error("Le bucket n'existe pas.")
        st.stop()

with col2:
    if st.button("Rafraichir"):
        st.rerun()

st.divider()

st.subheader("Uploader un fichier")
uploaded = st.file_uploader("Choisir un fichier")
if uploaded is not None:
    try:
        client.put_object(Bucket=bucket, Key=uploaded.name, Body=uploaded.getvalue())
        st.success(f"`{uploaded.name}` envoye dans `{bucket}`.")
    except ClientError as exc:
        st.error(f"Erreur : {exc}")

st.divider()

st.subheader("Contenu du bucket")
resp = client.list_objects_v2(Bucket=bucket)
contents = resp.get("Contents", [])

if not contents:
    st.info("Bucket vide.")
else:
    df = pd.DataFrame(
        [
            {"Key": obj["Key"], "Size (octets)": obj["Size"], "Last modified": obj["LastModified"]}
            for obj in contents
        ]
    )
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.subheader("Supprimer un objet")
    keys = [obj["Key"] for obj in contents]
    to_delete = st.selectbox("Selectionner un objet", options=keys)
    if st.button("Supprimer", type="primary"):
        client.delete_object(Bucket=bucket, Key=to_delete)
        st.success(f"`{to_delete}` supprime.")
        st.rerun()
