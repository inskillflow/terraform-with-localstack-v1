# Solution — TP 3 (TP 2 + SQS)

État de référence du projet à la fin du **TP 3** : on ajoute une file **SQS** à l'infrastructure et au dashboard du TP 2.

> Corrigé associé : [../../03-Chapitre3-Pratique-03-ajouter-sqs-terraform-validation-streamlit.md](../../03-Chapitre3-Pratique-03-ajouter-sqs-terraform-validation-streamlit.md)

## Ce qui change par rapport au TP 2

| Fichier | Changement |
|---|---|
| `terraform/main.tf` | + `resource "aws_sqs_queue" "notifications"` |
| `terraform/outputs.tf` | + `sqs_queue_name` et `sqs_queue_url` |
| `terraform/variables.tf` | + variable `owner_name` |
| `terraform/provider.tf` | + endpoint `sqs` |
| `.env.example` | + `SQS_QUEUE_NAME` et `SQS_QUEUE_URL` |
| `lib/aws_clients.py` | + `sqs_client()`, `queue_name()`, `queue_url()` |
| `pages/` | + `4_SQS.py` (envoyer / recevoir / supprimer des messages) |

## Démarrage rapide

```bash
cp .env.example .env
# Editer .env : token + recuperer SQS_QUEUE_URL apres terraform apply

docker compose up -d

cd terraform
terraform init
terraform apply -auto-approve
terraform output sqs_queue_url   # copier dans .env
cd ..

python -m venv .venv
# Activer venv selon votre OS
pip install -r requirements.txt

streamlit run app.py
```

## Ressources créées

- Bucket S3 : `tp-localstack-dev-documents`
- Table DynamoDB : `tp-localstack-dev-students`
- File SQS : `tp-localstack-dev-notifications`

## Nettoyage

```bash
cd terraform
terraform destroy -auto-approve
cd ..
docker compose down -v
```
