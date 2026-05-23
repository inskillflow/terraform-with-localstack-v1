# Solution — TP 4 (Modules Terraform)

État de référence du projet à la fin du **TP 4** : on refactore le Terraform du TP 3 en **modules réutilisables** sans changer les ressources produites.

> Corrigé associé : [../../04-Chapitre4-Pratique-04-modules-terraform-validation-streamlit.md](../../04-Chapitre4-Pratique-04-modules-terraform-validation-streamlit.md)

## Ce qui change par rapport au TP 3

```text
tp4/
├── ...
└── terraform/
    ├── main.tf            <-- appelle 3 modules
    ├── outputs.tf         <-- re-expose les outputs des modules
    ├── variables.tf       <-- project_name, environment, owner_name
    ├── provider.tf
    └── modules/           <-- NOUVEAU
        ├── s3/
        │   ├── main.tf
        │   ├── variables.tf
        │   └── outputs.tf
        ├── dynamodb/
        │   ├── main.tf
        │   ├── variables.tf
        │   └── outputs.tf
        └── sqs/
            ├── main.tf
            ├── variables.tf
            └── outputs.tf
```

Les ressources produites gardent les **mêmes noms** :
`tp-localstack-dev-{documents,students,notifications}`. Le dashboard Streamlit (identique à celui du TP 3) doit donc continuer à fonctionner.

## Démarrage rapide

```bash
cp .env.example .env
# Editer .env : token + SQS_QUEUE_URL apres terraform apply

docker compose up -d

cd terraform
terraform init                  # detecte les 3 modules locaux
terraform fmt -recursive        # formate aussi les modules
terraform validate
terraform plan
terraform apply -auto-approve
terraform output sqs_queue_url
cd ..

python -m venv .venv
# Activer venv selon votre OS
pip install -r requirements.txt

streamlit run app.py
```

> **Astuce diagnostic** : `terraform state list` doit afficher des adresses
> du style `module.documents_bucket.aws_s3_bucket.this` (au lieu de
> `aws_s3_bucket.documents` dans les TPs 1-3).

## Nettoyage

```bash
cd terraform
terraform destroy -auto-approve
cd ..
docker compose down -v
```
