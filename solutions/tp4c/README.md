# Solution — TP 4c (Modules Terraform, sans token)

État de référence du projet à la fin du **TP 4 version `c`** : refactor en modules du TP 3c.

> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, basculez sur [`solutions/tp4b/`](../tp4b/) (avec token).
>
> Corrigé associé : [`../../04c-Chapitre4-Pratique-04-modules-terraform-validation-streamlit-hobby-no-token.md`](../../04c-Chapitre4-Pratique-04-modules-terraform-validation-streamlit-hobby-no-token.md)

## Différence avec `solutions/tp4b/`

Identique sauf `.env.example` et `docker-compose.yml` (bypass au lieu de token).

## Démarrage rapide

```bash
cp .env.example .env

docker compose up -d

cd terraform
terraform init
terraform fmt -recursive
terraform validate
terraform apply -auto-approve
cd ..

python -m venv .venv
pip install -r requirements.txt

streamlit run app.py
```
