# Solution — TP 2c (Terraform + Streamlit dashboard, sans token)

État de référence du projet à la fin du **TP 2 version `c`** : infrastructure Terraform (TP 1c) + dashboard Streamlit, avec bypass `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1`.

> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, basculez sur [`solutions/tp2/`](../tp2/) (avec token).
>
> Corrigé associé : [`../../02c-Chapitre2-Pratique-02-terraform-localstack-ajout-ui-hobby-no-token.md`](../../02c-Chapitre2-Pratique-02-terraform-localstack-ajout-ui-hobby-no-token.md)

## Différence avec `solutions/tp2/`

Identique sauf :
- `.env.example` : `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1` au lieu de `LOCALSTACK_AUTH_TOKEN=...`
- `docker-compose.yml` : transmet le bypass au lieu du token

Le reste (Terraform, `app.py`, `lib/`, `pages/`) est **identique**.

## Démarrage rapide

```bash
cp .env.example .env

docker compose up -d

cd terraform
terraform init
terraform apply -auto-approve
cd ..

python -m venv .venv
# Activer venv selon votre OS
pip install -r requirements.txt

streamlit run app.py
```

## Nettoyage

```bash
cd terraform
terraform destroy -auto-approve
cd ..
docker compose down -v
```
