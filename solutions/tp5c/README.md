# Solution — TP 5c (Multi-environnements dev / test, sans token)

État de référence du projet à la fin du **TP 5 version `c`** : multi-environnements (dev + test) sur la base modulaire du TP 4c.

> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, basculez sur [`solutions/tp5b/`](../tp5b/) (avec token).
>
> Corrigé associé : [`../../05c-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit-hobby-no-token.md`](../../05c-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit-hobby-no-token.md)

## Différence avec `solutions/tp5b/`

Identique sauf `.env.example` et `docker-compose.yml` (bypass au lieu de token).

## Démarrage rapide

```bash
cp .env.example .env

docker compose up -d

cd terraform/environments/dev
terraform init
terraform apply -auto-approve
cd ../..

cd terraform/environments/test
terraform init
terraform apply -auto-approve
cd ../../..

python -m venv .venv
pip install -r requirements.txt

streamlit run app.py
```

## Ressources créées par environnement

| Service | dev | test |
|---|---|---|
| Bucket S3 | `tp-localstack-dev-documents` | `tp-localstack-test-documents` |
| Table DynamoDB | `tp-localstack-dev-students` | `tp-localstack-test-students` |
| File SQS | `tp-localstack-dev-notifications` | `tp-localstack-test-notifications` |

## Nettoyage

```bash
cd terraform/environments/dev && terraform destroy -auto-approve && cd ../../..
cd terraform/environments/test && terraform destroy -auto-approve && cd ../../..
docker compose down -v
```
