"""Page 'A propos' du TP 5."""

from __future__ import annotations

import streamlit as st

from lib.aws_clients import render_env_selector


st.set_page_config(page_title="A propos", page_icon=":information_source:")
render_env_selector()

st.title("A propos")

st.markdown(
    """
    ## TP 5 - Multi-environnements (dev / test)

    Cette application Streamlit fait partie du **TP 5** du cours.
    Elle illustre comment isoler les ressources d'un meme projet selon
    l'environnement (`dev`, `test`, ...).

    ### Structure Terraform

    ```
    terraform/
    ├── modules/                     code reutilisable
    │   ├── s3/
    │   ├── dynamodb/
    │   └── sqs/
    └── environments/                instances de modules
        ├── dev/
        │   ├── main.tf              appelle les modules avec environment=dev
        │   ├── provider.tf
        │   ├── variables.tf
        │   ├── terraform.tfvars
        │   └── outputs.tf
        └── test/
            └── ...                  meme code, environment=test
    ```

    ### Pourquoi separer ?

    - **Donnees isolees** : un test destructif ne touche pas dev.
    - **Lifecycle distinct** : on peut detruire test sans toucher dev.
    - **Nommage clair** : `tp-localstack-dev-*` vs `tp-localstack-test-*`.
    - **Code unique** : le code Terraform reste DRY grace aux modules.

    ### Commandes

    ```bash
    # Lancer dev
    cd terraform/environments/dev
    terraform init
    terraform apply -auto-approve

    # Lancer test (depuis un autre terminal)
    cd ../test
    terraform init
    terraform apply -auto-approve

    # Detruire seulement test
    terraform destroy -auto-approve
    ```

    ### Selecteur dans Streamlit

    La barre laterale liste les sous-dossiers de `terraform/environments/`.
    L'application lit les outputs du dossier choisi et affiche les ressources
    de cet environnement uniquement.
    """
)
