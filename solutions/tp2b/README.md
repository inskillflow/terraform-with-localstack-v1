# Solution — TP 2 (Terraform + Streamlit dashboard)

État de référence du projet à la fin du **TP 2** : infrastructure Terraform (TP 1) + dashboard Streamlit de validation.

> Corrigé associé : [../../02-Chapitre2-Pratique-02-terraform-localstack-ajout-ui.md](../../02-Chapitre2-Pratique-02-terraform-localstack-ajout-ui.md)

## Contenu

```text
tp2b/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app.py                          page d'accueil (Dashboard)
├── lib/
│   ├── __init__.py
│   └── aws_clients.py              clients boto3 + lecture .env + terraform output
├── pages/                          pages Streamlit
│   ├── 1_Terraform_outputs.py
│   ├── 2_S3.py
│   ├── 3_DynamoDB.py
│   └── 4_A_propos.py
└── terraform/
    ├── provider.tf
    ├── variables.tf
    ├── main.tf
    └── outputs.tf
```

## Prérequis

- Tous les prérequis du TP 1
- Python ≥ 3.10
- Auth Token LocalStack dans `.env`

## Démarrage rapide

```bash
# 1. Configurer .env
cp .env.example .env
# Editer .env : mettre le vrai LOCALSTACK_AUTH_TOKEN

# 2. Demarrer LocalStack
docker compose up -d

# 3. Appliquer Terraform
cd terraform
terraform init
terraform apply -auto-approve
cd ..

# 4. Creer l'environnement Python
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# macOS / Linux / Git Bash : source .venv/bin/activate

# 5. Installer les dependances
pip install -r requirements.txt

# 6. Lancer Streamlit
streamlit run app.py
# Ouvrir http://localhost:8501
```

## Pages

| Page | Rôle |
|---|---|
| Dashboard (`app.py`) | Santé LocalStack + noms de ressources attendus |
| Terraform outputs | Compare `.env` aux `terraform output -json` |
| S3 | Vérifie le bucket, upload / list / delete |
| DynamoDB | Vérifie la table, ajoute / scan / delete d'items |
| À propos | Explication pédagogique |

## Nettoyage

```bash
cd terraform
terraform destroy -auto-approve
cd ..
docker compose down -v
```
