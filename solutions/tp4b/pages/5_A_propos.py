"""Page 'A propos' du TP 4."""

from __future__ import annotations

import streamlit as st


st.set_page_config(page_title="A propos", page_icon=":information_source:")
st.title("A propos")

st.markdown(
    """
    ## TP 4 - Modules Terraform

    Cette application Streamlit fait partie du **TP 4** du cours.
    Le code Terraform a ete refactorise en **modules reutilisables** :

    ```
    terraform/
    ├── main.tf            appelle les modules
    ├── outputs.tf         re-expose les outputs des modules
    ├── variables.tf       project_name, environment, owner_name
    ├── provider.tf
    └── modules/
        ├── s3/
        │   ├── main.tf
        │   ├── variables.tf
        │   └── outputs.tf
        ├── dynamodb/
        │   └── ...
        └── sqs/
            └── ...
    ```

    ### Pourquoi des modules ?

    - **Reutilisabilite** : un meme module peut creer plusieurs buckets.
    - **Lisibilite** : un seul fichier `main.tf` racine, court.
    - **Test** : on peut tester chaque module independamment.
    - **Convention** : tous les modules respectent la meme convention de nommage.

    ### Test important du TP 4

    Apres refactoring, **les noms des ressources doivent rester les memes** :

    ```
    tp-localstack-dev-documents
    tp-localstack-dev-students
    tp-localstack-dev-notifications
    ```

    Si Streamlit fonctionne sans changement, le refactoring a reussi.
    Si une ressource manque ou est renommee, il y a une regression.
    """
)
