"""Page 'A propos' du TP 3."""

from __future__ import annotations

import streamlit as st


st.set_page_config(page_title="A propos", page_icon=":information_source:")
st.title("A propos")

st.markdown(
    """
    ## Role pedagogique - TP 3

    Cette application Streamlit fait partie du **TP 3** du cours
    « Terraform avec LocalStack ». Elle ajoute une **file SQS** a
    l'infrastructure validee dans le TP 2.

    ### Ressources validees

    | Service | Ressource Terraform | Page Streamlit |
    |---|---|---|
    | S3 | `aws_s3_bucket.documents` | S3 |
    | DynamoDB | `aws_dynamodb_table.students` | DynamoDB |
    | SQS | `aws_sqs_queue.notifications` | SQS |

    ### Principe

    1. Terraform declare les ressources.
    2. `terraform apply` les cree dans LocalStack.
    3. `terraform output` expose leurs identifiants.
    4. `.env` reprend ces valeurs.
    5. Streamlit + boto3 les utilisent pour valider et manipuler.

    Si une ressource n'est pas declaree dans Terraform, elle ne doit pas
    apparaitre dans Streamlit.
    """
)
