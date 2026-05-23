# Solution — TP 5 (Multi-environnements dev / test)

État de référence du projet à la fin du **TP 5** : on instancie les modules Terraform du TP 4 dans **deux environnements isolés** (`dev` et `test`), et Streamlit permet de basculer entre les deux.

> Corrigé associé : [../../05-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit.md](../../05-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit.md)

## Structure

```text
tp5b/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app.py                          dashboard avec selecteur d'env
├── lib/
│   ├── __init__.py
│   └── aws_clients.py              lit `terraform output` de l'env choisi
├── pages/
│   ├── 1_Terraform_outputs.py
│   ├── 2_S3.py
│   ├── 3_DynamoDB.py
│   ├── 4_SQS.py
│   └── 5_A_propos.py
└── terraform/
    ├── modules/                    (identique au TP 4)
    │   ├── s3/
    │   ├── dynamodb/
    │   └── sqs/
    └── environments/
        ├── dev/
        │   ├── provider.tf
        │   ├── variables.tf
        │   ├── terraform.tfvars    environment = "dev"
        │   ├── main.tf
        │   └── outputs.tf
        └── test/
            ├── provider.tf
            ├── variables.tf
            ├── terraform.tfvars    environment = "test"
            ├── main.tf
            └── outputs.tf
```

## Ressources créées par environnement

| Service | dev | test |
|---|---|---|
| Bucket S3 | `tp-localstack-dev-documents` | `tp-localstack-test-documents` |
| Table DynamoDB | `tp-localstack-dev-students` | `tp-localstack-test-students` |
| File SQS | `tp-localstack-dev-notifications` | `tp-localstack-test-notifications` |

## Démarrage rapide

```bash
cp .env.example .env
# Editer .env : token + DEFAULT_TERRAFORM_ENV=dev (ou test)

docker compose up -d

# 1) Deployer dev
cd terraform/environments/dev
terraform init
terraform apply -auto-approve
cd ../..

# 2) Deployer test
cd terraform/environments/test
terraform init
terraform apply -auto-approve
cd ../../..

# 3) Lancer Streamlit
python -m venv .venv
# Activer venv selon votre OS
pip install -r requirements.txt
streamlit run app.py
```

## Vérification rapide

```bash
terraform -chdir=terraform/environments/dev output
terraform -chdir=terraform/environments/test output
```

Les noms de ressources doivent être différents entre dev et test.

## Nettoyage

```bash
cd terraform/environments/dev && terraform destroy -auto-approve && cd ../../..
cd terraform/environments/test && terraform destroy -auto-approve && cd ../../..
docker compose down -v
```

## Aller plus loin

- Ajouter un environnement `stage` (copier `test/`, ajuster `terraform.tfvars`).
- Utiliser un **backend distant** par environnement (Terraform Cloud, S3, ...).
- Faire varier la **configuration** d'un environnement à l'autre via les `tfvars` (taille DynamoDB, retention SQS, ...).
