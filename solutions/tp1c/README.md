# Solution — TP 1c (Terraform + LocalStack sans token, S3 + DynamoDB)

État de référence du projet à la fin du **TP 1 version `c`** (bypass legacy `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1`).

> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, basculez sur [`solutions/tp1/`](../tp1/) (avec token).
>
> Corrigé associé : [`../../01c-Chapitre1-Pratique-01-terraform-localstack-hobby-no-token.md`](../../01c-Chapitre1-Pratique-01-terraform-localstack-hobby-no-token.md)

## Contenu

```text
tp1c/
├── .env.example          modele a copier vers .env (juste le bypass)
├── .gitignore
├── docker-compose.yml    LocalStack via Docker Compose (bypass)
├── README.md             ce fichier
└── terraform/
    ├── provider.tf       provider AWS redirige vers LocalStack (identique a tp1/)
    ├── variables.tf
    ├── main.tf           ressources S3 + DynamoDB (identique a tp1/)
    └── outputs.tf
```

## Différence avec `solutions/tp1/`

| Fichier | `tp1/` | `tp1c/` |
|---|---|---|
| `.env.example` | `LOCALSTACK_AUTH_TOKEN=...` | `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1` |
| `docker-compose.yml` | passe le token au conteneur | passe le bypass au conteneur |
| `terraform/` | identique | **identique** |
| Compte LocalStack | requis | **non requis** |

## Prérequis

- Docker Desktop démarré
- Terraform ≥ 1.6
- AWS CLI v2 (pour vérification)
- **Aucun compte LocalStack requis** (jusqu'au 6 nov. 2026)

## Démarrage rapide

```bash
cp .env.example .env

docker compose up -d

curl http://localhost:4566/_localstack/info
# Attendu : "edition": "community"

cd terraform
terraform init
terraform plan
terraform apply -auto-approve

aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

## Ressources créées

- Bucket S3 : `tp-localstack-dev-documents`
- Table DynamoDB : `tp-localstack-dev-students`

## Nettoyage

```bash
cd terraform
terraform destroy -auto-approve
cd ..
docker compose down -v
```
