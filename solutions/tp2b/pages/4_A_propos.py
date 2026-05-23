"""Page 'A propos' : explique le role pedagogique du dashboard."""

from __future__ import annotations

import streamlit as st


st.set_page_config(page_title="A propos", page_icon=":information_source:")
st.title("A propos")

st.markdown(
    """
    ## Role pedagogique de cette application

    Cette application Streamlit fait partie du **TP 2** du cours
    « Terraform avec LocalStack ». Son but est de **valider visuellement**
    une infrastructure declaree avec Terraform.

    ### Principes

    - **Terraform** est la source de verite de l'infrastructure.
    - **LocalStack** simule AWS localement (S3, DynamoDB, etc.).
    - **boto3** est le client Python officiel d'AWS.
    - **Streamlit** est l'interface de validation.

    ### Flux de donnees

    ```
    Etudiant
       v
    Streamlit (app.py + pages/)
       v
    boto3
       v
    LocalStack (http://localhost:4566)
       v
    S3 / DynamoDB simules
    ```

    ### Pages disponibles

    1. **Dashboard** : sante LocalStack + noms de ressources attendus.
    2. **Terraform outputs** : compare `.env` aux `terraform output`.
    3. **S3** : valide le bucket cree par Terraform, upload / list / delete.
    4. **DynamoDB** : valide la table creee par Terraform, ajoute / scan / delete.
    5. **A propos** : cette page.

    ### Ce que cette application ne fait PAS

    - Elle ne cree **pas** l'infrastructure (c'est le role de Terraform).
    - Elle ne modifie **pas** la configuration AWS / LocalStack.
    - Elle ne stocke **pas** de donnees en dehors de LocalStack.
    """
)
