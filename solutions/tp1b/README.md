# Solution — TP 1 (Terraform + LocalStack, S3 + DynamoDB)

État de référence du projet à la fin du **TP 1**.

> Corrigé associé : [../../01-Chapitre1-Pratique-01-terraform-localstack.md](../../01-Chapitre1-Pratique-01-terraform-localstack.md)

## Contenu

```text
tp1b/
├── .env.example          modele a copier vers .env
├── .gitignore
├── docker-compose.yml    LocalStack via Docker Compose
├── README.md             ce fichier
└── terraform/
    ├── provider.tf       provider AWS redirige vers LocalStack
    ├── variables.tf      variables project_name et environment
    ├── main.tf           ressources S3 + DynamoDB
    └── outputs.tf        outputs Terraform
```

## Prérequis

- Docker Desktop démarré
- Terraform ≥ 1.6
- AWS CLI v2 (pour vérification)
- Compte LocalStack (plan Hobby ou Student) avec un Auth Token

## Démarrage rapide

```bash
# 1. Copier le modele .env et y mettre votre Auth Token
cp .env.example .env
# Editer .env et remplacer 'your-localstack-auth-token-here' par votre vrai token

# 2. Demarrer LocalStack
docker compose up -d

# 3. Verifier que LocalStack repond
curl http://localhost:4566/_localstack/info

# 4. Appliquer Terraform
cd terraform
terraform init
terraform plan
terraform apply -auto-approve

# 5. Verifier avec AWS CLI
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

## Ressources créées

- Bucket S3 : `tp-localstack-dev-documents`
- Table DynamoDB : `tp-localstack-dev-students` (clé `student_id`, type `S`)

## Nettoyage

```bash
cd terraform
terraform destroy -auto-approve
cd ..
docker compose down -v
```
