"""Page SQS multi-env."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from botocore.exceptions import ClientError

from lib.aws_clients import current_env, queue_url, render_env_selector, sqs_client


st.set_page_config(page_title="SQS - Multi-env", page_icon=":envelope:")
render_env_selector()

st.title("SQS - Ressource Terraform")
st.caption(f"Environnement : **{current_env()}**")

url = queue_url()
client = sqs_client()

if not url:
    st.error("Pas de file SQS pour cet environnement.")
    st.stop()

st.write(f"File cible : `{url}`")


def _queue_exists(queue_url_value: str) -> bool:
    try:
        client.get_queue_attributes(QueueUrl=queue_url_value, AttributeNames=["QueueArn"])
        return True
    except ClientError:
        return False


col1, col2 = st.columns(2)
with col1:
    if _queue_exists(url):
        st.success("La file existe.")
    else:
        st.error("La file n'existe pas.")
        st.stop()

with col2:
    if st.button("Rafraichir"):
        st.rerun()

st.divider()

st.subheader("Envoyer un message")
with st.form("send_message", clear_on_submit=True):
    body = st.text_area(
        "Corps du message",
        value=f"Message envoye dans {current_env()}",
    )
    submitted = st.form_submit_button("Envoyer")
    if submitted and body:
        try:
            resp = client.send_message(QueueUrl=url, MessageBody=body)
            st.success(f"Message envoye (MessageId: {resp.get('MessageId')}).")
        except ClientError as exc:
            st.error(f"Erreur : {exc}")

st.divider()

st.subheader("Recevoir des messages")

if st.button("Lire les messages"):
    try:
        resp = client.receive_message(
            QueueUrl=url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1,
        )
        messages = resp.get("Messages", [])
        if not messages:
            st.info("Aucun message en attente.")
        else:
            rows = [
                {"MessageId": m["MessageId"], "Body": m["Body"]}
                for m in messages
            ]
            df = pd.DataFrame(rows)
            st.dataframe(df, hide_index=True, use_container_width=True)
            st.session_state["last_messages"] = messages
    except ClientError as exc:
        st.error(f"Erreur : {exc}")

st.divider()

st.subheader("Supprimer les messages lus")
last = st.session_state.get("last_messages", [])
if not last:
    st.info("Lisez d'abord des messages.")
elif st.button("Supprimer les messages lus", type="primary"):
    deleted = 0
    for m in last:
        try:
            client.delete_message(QueueUrl=url, ReceiptHandle=m["ReceiptHandle"])
            deleted += 1
        except ClientError:
            pass
    st.success(f"{deleted} message(s) supprime(s).")
    st.session_state["last_messages"] = []
