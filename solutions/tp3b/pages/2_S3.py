"""Page S3 : valide le bucket cree par Terraform."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from botocore.exceptions import ClientError

from lib.aws_clients import bucket_name, s3_client


st.set_page_config(page_title="S3 - Ressource Terraform", page_icon=":package:")
st.title("S3 - Ressource Terraform")

bucket = bucket_name()
client = s3_client()

if not bucket:
    st.error("`S3_BUCKET_NAME` est vide dans `.env`. Completez `.env` d'abord.")
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
        st.error("Le bucket n'existe pas. Avez-vous execute `terraform apply` ?")
        st.stop()

with col2:
    if st.button("Rafraichir la liste"):
        st.rerun()

st.divider()

st.subheader("Uploader un fichier")
uploaded = st.file_uploader("Choisir un fichier a envoyer dans S3")
if uploaded is not None:
    try:
        client.put_object(Bucket=bucket, Key=uploaded.name, Body=uploaded.getvalue())
        st.success(f"`{uploaded.name}` envoye dans `{bucket}`.")
    except ClientError as exc:
        st.error(f"Erreur a l'upload : {exc}")

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
        st.success(f"`{to_delete}` supprime du bucket.")
        st.rerun()
