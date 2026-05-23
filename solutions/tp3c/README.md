# Solution — TP 3c (TP 2c + SQS, sans token)

État de référence du projet à la fin du **TP 3 version `c`** : on ajoute SQS au TP 2c.

> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, basculez sur [`solutions/tp3/`](../tp3/) (avec token).
>
> Corrigé associé : [`../../03c-Chapitre3-Pratique-03-ajouter-sqs-terraform-validation-streamlit-hobby-no-token.md`](../../03c-Chapitre3-Pratique-03-ajouter-sqs-terraform-validation-streamlit-hobby-no-token.md)

## Différence avec `solutions/tp3/`

Identique sauf `.env.example` et `docker-compose.yml` (bypass au lieu de token). Terraform et Streamlit identiques.

## Démarrage rapide

```bash
cp .env.example .env

docker compose up -d

cd terraform
terraform init
terraform apply -auto-approve
terraform output sqs_queue_url   # copier dans .env
cd ..

python -m venv .venv
pip install -r requirements.txt

streamlit run app.py
```
