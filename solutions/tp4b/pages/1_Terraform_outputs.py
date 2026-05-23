"""Page 'Terraform outputs' : compare .env avec terraform output -json."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from lib.aws_clients import (
    bucket_name,
    localstack_endpoint,
    queue_name,
    queue_url,
    read_terraform_outputs,
    table_name,
)


st.set_page_config(page_title="Terraform outputs", page_icon=":memo:")
st.title("Terraform outputs")
st.caption("Comparaison entre les outputs Terraform (issus des modules) et le fichier .env.")

outputs = read_terraform_outputs()

if "_error" in outputs:
    st.error(
        "Impossible de lire `terraform output`. "
        "Verifiez que `terraform apply` a ete execute dans le dossier `terraform/`."
    )
    with st.expander("Detail de l'erreur"):
        st.code(outputs["_error"])
    st.stop()

env_values = {
    "s3_bucket_name": bucket_name(),
    "dynamodb_table_name": table_name(),
    "sqs_queue_name": queue_name(),
    "sqs_queue_url": queue_url(),
    "localstack_endpoint": localstack_endpoint(),
}

rows = []
for key, env_val in env_values.items():
    tf_val = outputs.get(key, "")
    rows.append(
        {
            "Variable": key,
            "Terraform output": tf_val,
            ".env": env_val,
            "Statut": "OK" if tf_val and tf_val == env_val else "Divergence",
        }
    )

df = pd.DataFrame(rows)
st.dataframe(df, hide_index=True, use_container_width=True)

divergences = df[df["Statut"] == "Divergence"]
if divergences.empty:
    st.success("Tout est coherent entre Terraform et .env.")
else:
    st.warning(
        f"{len(divergences)} divergence(s) detectee(s). "
        "Mettez `.env` a jour pour qu'il corresponde aux outputs Terraform."
    )

with st.expander("Outputs Terraform bruts"):
    st.json(outputs)
