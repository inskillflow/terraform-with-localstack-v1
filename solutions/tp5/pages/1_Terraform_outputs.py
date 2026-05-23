"""Page 'Terraform outputs' multi-env."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from lib.aws_clients import current_env, read_terraform_outputs, render_env_selector


st.set_page_config(page_title="Terraform outputs", page_icon=":memo:")
render_env_selector()

st.title("Terraform outputs")
st.caption(f"Environnement : **{current_env()}**")

outputs = read_terraform_outputs()

if "_error" in outputs:
    st.error("Impossible de lire `terraform output` pour cet environnement.")
    with st.expander("Detail de l'erreur"):
        st.code(outputs["_error"])
    st.stop()

if not outputs:
    st.warning("Aucun output Terraform. Avez-vous execute `terraform apply` ?")
    st.stop()

rows = [{"Output": k, "Valeur": v} for k, v in outputs.items()]
df = pd.DataFrame(rows)
st.dataframe(df, hide_index=True, use_container_width=True)

with st.expander("Outputs Terraform bruts"):
    st.json(outputs)
