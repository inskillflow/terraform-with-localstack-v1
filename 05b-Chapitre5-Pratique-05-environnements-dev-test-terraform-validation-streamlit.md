<a id="top"></a>

# TP 5 — Gérer plusieurs environnements Terraform et les valider avec Streamlit

> **Cours visé :** Terraform, Infrastructure as Code, environnements, LocalStack, Streamlit  
>
> **Niveau :** Débutant avancé  
>
> **Prérequis :** les TP 1 à 4 doivent être réalisés. Le projet utilise déjà des modules Terraform pour S3, DynamoDB et SQS.  
>
> **Objectif principal :** apprendre à séparer une infrastructure Terraform en plusieurs environnements, par exemple `dev` et `test`, puis utiliser Streamlit pour choisir l’environnement à valider.  
>
> **Important :** Terraform reste le sujet principal. Streamlit est obligatoire dans la progression, mais il sert à visualiser et valider les environnements créés par Terraform.  
>
> **Environnements créés :** `dev` et `test`  
>
> **Ressources par environnement :** S3, DynamoDB, SQS  
>
> **Outils utilisés :** Terraform, LocalStack, Docker Compose, Streamlit, boto3, AWS CLI  
>
> **Durée recommandée :** 4 à 6 heures  
>
> **Livrables :** structure multi-environnements, captures Terraform, dashboard Streamlit avec sélection d’environnement, mini-rapport.

---

## À lire avant de commencer

Jusqu’ici, votre projet Terraform créait une seule infrastructure.

Mais dans un vrai projet, on travaille souvent avec plusieurs environnements.

Exemples :

```text
dev  -> environnement de développement
test -> environnement de test
prod -> environnement de production
```

Dans ce TP, nous allons utiliser seulement :

```text
dev
test
```

Chaque environnement aura ses propres ressources :

```text
dev  -> bucket S3 dev, table DynamoDB dev, file SQS dev
test -> bucket S3 test, table DynamoDB test, file SQS test
```

L’objectif est d’apprendre à organiser Terraform comme ceci :

```text
terraform/
├── modules/
│   ├── s3/
│   ├── dynamodb/
│   └── sqs/
└── environments/
    ├── dev/
    └── test/
```

Puis Streamlit permettra de choisir :

```text
Environnement à valider : dev ou test
```

---

## Idée centrale

Terraform crée les environnements.

Streamlit ne crée pas les environnements.

Streamlit lit les outputs Terraform de l’environnement choisi, puis valide les ressources.

```text
terraform/environments/dev
        |
        v
terraform output -json
        |
        v
Streamlit affiche et teste dev
```

```text
terraform/environments/test
        |
        v
terraform output -json
        |
        v
Streamlit affiche et teste test
```

---

## Structure finale attendue

```text
terraform-localstack-debutant/
│
├── app.py
├── .env
├── .env.example
├── docker-compose.yml
│
└── terraform/
    ├── modules/
    │   ├── s3/
    │   ├── dynamodb/
    │   └── sqs/
    │
    └── environments/
        ├── dev/
        │   ├── provider.tf
        │   ├── variables.tf
        │   ├── terraform.tfvars
        │   ├── main.tf
        │   └── outputs.tf
        │
        └── test/
            ├── provider.tf
            ├── variables.tf
            ├── terraform.tfvars
            ├── main.tf
            └── outputs.tf
```

---

## Barème proposé

| Partie | Travail demandé | Points |
|---|---|---:|
| **I** | Comprendre la notion d’environnement | 15 |
| **II** | Créer la structure `environments/dev` et `environments/test` | 20 |
| **III** | Créer l’environnement `dev` | 30 |
| **IV** | Créer l’environnement `test` | 30 |
| **V** | Initialiser et appliquer `dev` | 25 |
| **VI** | Initialiser et appliquer `test` | 25 |
| **VII** | Comparer les outputs des deux environnements | 25 |
| **VIII** | Mettre à jour Streamlit pour sélectionner l’environnement | 35 |
| **IX** | Valider `dev` dans Streamlit | 25 |
| **X** | Valider `test` dans Streamlit | 25 |
| **XI** | Questions et mini-rapport | 30 |
| | **TOTAL** | **285 pts** |

---

## Table des matières

| # | Section |
|---|---|
| 1 | [Partie I — Comprendre les environnements](#partie-1) |
| 2 | [Partie II — Préparer la structure](#partie-2) |
| 3 | [Partie III — Créer l’environnement dev](#partie-3) |
| 4 | [Partie IV — Créer l’environnement test](#partie-4) |
| 5 | [Partie V — Initialiser et appliquer dev](#partie-5) |
| 6 | [Partie VI — Initialiser et appliquer test](#partie-6) |
| 7 | [Partie VII — Comparer les outputs](#partie-7) |
| 8 | [Partie VIII — Mettre à jour Streamlit](#partie-8) |
| 9 | [Partie IX — Valider dev dans Streamlit](#partie-9) |
| 10 | [Partie X — Valider test dans Streamlit](#partie-10) |
| 11 | [Partie XI — Exercices guidés](#partie-11) |
| 12 | [Partie XII — Erreurs fréquentes](#partie-12) |
| 13 | [Partie XIII — Questions de compréhension](#partie-13) |
| 14 | [Partie XIV — Mini-rapport à remettre](#partie-14) |
| 15 | [Corrigé / Indications](#corrige) |

---

<a id="partie-1"></a>

## Partie I — Comprendre les environnements

<details>
<summary><strong>1.1 C’est quoi un environnement ?</strong></summary>

Un environnement est une version séparée de l’infrastructure.

Exemple :

```text
dev  -> pour développer et tester rapidement
test -> pour valider avant une version plus sérieuse
prod -> pour les vrais utilisateurs
```

Dans ce TP, nous n’utilisons pas `prod`.

Nous utilisons seulement :

```text
dev
test
```

</details>

<details>
<summary><strong>1.2 Pourquoi séparer dev et test ?</strong></summary>

Si tout est mélangé, une erreur peut avoir un impact sur tout le projet.

Avec plusieurs environnements :

```text
on peut expérimenter dans dev ;
on peut vérifier dans test ;
on évite de casser tout le projet ;
on garde une séparation claire.
```

</details>

<details>
<summary><strong>1.3 Ce que Terraform va faire</strong></summary>

Terraform va créer des ressources avec des noms différents.

Exemple :

```text
tp-platform-dev-documents
tp-platform-dev-students
tp-platform-dev-notifications
```

et :

```text
tp-platform-test-documents
tp-platform-test-students
tp-platform-test-notifications
```

Ainsi, les ressources `dev` et `test` ne se mélangent pas.

</details>

<details>
<summary><strong>1.4 Ce que Streamlit va faire</strong></summary>

Streamlit va afficher un menu :

```text
Choisir l'environnement à valider
```

L’étudiant pourra choisir :

```text
dev
test
```

Puis Streamlit lira les outputs Terraform correspondants.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-2"></a>

## Partie II — Préparer la structure

<details>
<summary><strong>2.1 Créer le dossier environments</strong></summary>

Dans le dossier `terraform/` :

```bash
mkdir -p environments/dev
mkdir -p environments/test
```

PowerShell :

```powershell
New-Item -ItemType Directory -Force environments\dev
New-Item -ItemType Directory -Force environments\test
```

</details>

<details>
<summary><strong>2.2 Structure attendue</strong></summary>

```text
terraform/
├── modules/
│   ├── s3/
│   ├── dynamodb/
│   └── sqs/
└── environments/
    ├── dev/
    └── test/
```

</details>

<details>
<summary><strong>2.3 Pourquoi garder modules séparé ?</strong></summary>

Les modules sont réutilisés par chaque environnement.

Donc :

```text
dev utilise les modules
test utilise les mêmes modules
```

Cela évite de recopier le code des ressources.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-3"></a>

## Partie III — Créer l’environnement dev

<details>
<summary><strong>3.1 Fichiers à créer</strong></summary>

Dans :

```text
terraform/environments/dev/
```

créez :

```text
provider.tf
variables.tf
terraform.tfvars
main.tf
outputs.tf
```

</details>

<details>
<summary><strong>3.2 `provider.tf`</strong></summary>

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = var.aws_region
  access_key = "test"
  secret_key = "test"

  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3       = var.localstack_endpoint
    dynamodb = var.localstack_endpoint
    sqs      = var.localstack_endpoint
    iam      = var.localstack_endpoint
    sts      = var.localstack_endpoint
  }
}
```

</details>

<details>
<summary><strong>3.3 `variables.tf`</strong></summary>

```hcl
variable "project_name" {
  description = "Nom du projet utilisé pour nommer les ressources locales"
  type        = string
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
}

variable "owner_name" {
  description = "Nom du groupe, de l'équipe ou de l'étudiant responsable"
  type        = string
}

variable "aws_region" {
  description = "Région AWS simulée par LocalStack"
  type        = string
  default     = "us-east-1"
}

variable "localstack_endpoint" {
  description = "Endpoint LocalStack"
  type        = string
  default     = "http://localhost:4566"
}
```

</details>

<details>
<summary><strong>3.4 `terraform.tfvars` pour dev</strong></summary>

```hcl
project_name = "tp-platform"
environment  = "dev"
owner_name   = "groupe-01"

aws_region          = "us-east-1"
localstack_endpoint = "http://localhost:4566"
```

</details>

<details>
<summary><strong>3.5 `main.tf`</strong></summary>

```hcl
module "documents_bucket" {
  source = "../../modules/s3"

  project_name  = var.project_name
  environment   = var.environment
  owner_name    = var.owner_name
  bucket_suffix = "documents"
}

module "students_table" {
  source = "../../modules/dynamodb"

  project_name = var.project_name
  environment  = var.environment
  owner_name   = var.owner_name
  table_suffix = "students"
}

module "notifications_queue" {
  source = "../../modules/sqs"

  project_name = var.project_name
  environment  = var.environment
  owner_name   = var.owner_name
  queue_suffix = "notifications"
}
```

</details>

<details>
<summary><strong>3.6 `outputs.tf`</strong></summary>

```hcl
output "s3_bucket_name" {
  value = module.documents_bucket.bucket_name
}

output "dynamodb_table_name" {
  value = module.students_table.table_name
}

output "sqs_queue_name" {
  value = module.notifications_queue.queue_name
}

output "sqs_queue_url" {
  value = module.notifications_queue.queue_url
}

output "localstack_endpoint" {
  value = var.localstack_endpoint
}

output "aws_region" {
  value = var.aws_region
}

output "project_name" {
  value = var.project_name
}

output "environment_name" {
  value = var.environment
}

output "owner_name" {
  value = var.owner_name
}
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-4"></a>

## Partie IV — Créer l’environnement test

<details>
<summary><strong>4.1 Copier la structure de dev</strong></summary>

Vous pouvez copier les fichiers de `dev` vers `test`.

Bash :

```bash
cp environments/dev/*.tf environments/test/
cp environments/dev/terraform.tfvars environments/test/
```

PowerShell :

```powershell
Copy-Item environments\dev\*.tf environments\test\
Copy-Item environments\dev\terraform.tfvars environments\test\
```

</details>

<details>
<summary><strong>4.2 Modifier `terraform.tfvars` pour test</strong></summary>

Dans :

```text
terraform/environments/test/terraform.tfvars
```

mettez :

```hcl
project_name = "tp-platform"
environment  = "test"
owner_name   = "groupe-01"

aws_region          = "us-east-1"
localstack_endpoint = "http://localhost:4566"
```

</details>

<details>
<summary><strong>4.3 Pourquoi seule la variable environment change ?</strong></summary>

On garde le même projet :

```text
tp-platform
```

Mais on change l’environnement :

```text
dev
test
```

Terraform créera donc des ressources différentes.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-5"></a>

## Partie V — Initialiser et appliquer dev

<details>
<summary><strong>5.1 Aller dans dev</strong></summary>

```bash
cd terraform/environments/dev
```

</details>

<details>
<summary><strong>5.2 Exécuter les commandes Terraform</strong></summary>

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Répondez :

```text
yes
```

</details>

<details>
<summary><strong>5.3 Lire les outputs dev</strong></summary>

```bash
terraform output
```

Résultat attendu :

```text
tp-platform-dev-documents
tp-platform-dev-students
tp-platform-dev-notifications
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-6"></a>

## Partie VI — Initialiser et appliquer test

<details>
<summary><strong>6.1 Aller dans test</strong></summary>

Depuis le dossier `dev` :

```bash
cd ../test
```

</details>

<details>
<summary><strong>6.2 Exécuter Terraform</strong></summary>

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Répondez :

```text
yes
```

</details>

<details>
<summary><strong>6.3 Lire les outputs test</strong></summary>

```bash
terraform output
```

Résultat attendu :

```text
tp-platform-test-documents
tp-platform-test-students
tp-platform-test-notifications
```

</details>

<details>
<summary><strong>6.4 Revenir à la racine du projet</strong></summary>

Depuis `terraform/environments/test` :

```bash
cd ../../..
```

Vous devez revenir dans :

```text
terraform-localstack-debutant/
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-7"></a>

## Partie VII — Comparer les outputs

<details>
<summary><strong>7.1 Output dev</strong></summary>

```bash
terraform -chdir=terraform/environments/dev output
```

</details>

<details>
<summary><strong>7.2 Output test</strong></summary>

```bash
terraform -chdir=terraform/environments/test output
```

</details>

<details>
<summary><strong>7.3 Ce que vous devez remarquer</strong></summary>

Les noms doivent être différents.

Exemple :

```text
tp-platform-dev-documents
tp-platform-test-documents
```

Même service.

Deux environnements.

Deux ressources différentes.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-8"></a>

## Partie VIII — Mettre à jour Streamlit

<details>
<summary><strong>8.1 Remplacer `app.py`</strong></summary>

Utilisez le fichier `app.py` fourni dans ce TP.

Il permet de :

```text
détecter les environnements dans terraform/environments/ ;
sélectionner dev ou test ;
lire les outputs Terraform de l’environnement choisi ;
valider S3, DynamoDB et SQS pour cet environnement.
```

</details>

<details>
<summary><strong>8.2 Modifier `.env`</strong></summary>

Ajoutez :

```env
DEFAULT_TERRAFORM_ENV=dev
```

Ce paramètre indique quel environnement est sélectionné par défaut.

</details>

<details>
<summary><strong>8.3 Installer les dépendances si nécessaire</strong></summary>

```bash
pip install -r requirements.txt
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-9"></a>

## Partie IX — Valider dev dans Streamlit

<details>
<summary><strong>9.1 Lancer Streamlit</strong></summary>

À la racine :

```bash
streamlit run app.py
```

</details>

<details>
<summary><strong>9.2 Sélectionner dev</strong></summary>

Dans la barre latérale, choisissez :

```text
dev
```

</details>

<details>
<summary><strong>9.3 Tester les ressources dev</strong></summary>

Dans le Dashboard :

```text
Tester LocalStack
Tester S3
Tester DynamoDB
Tester SQS
```

Tout doit fonctionner.

</details>

<details>
<summary><strong>9.4 Ajouter des données dev</strong></summary>

Dans DynamoDB, ajoutez :

```text
DEV-S001
```

Dans SQS, envoyez :

```text
Message envoyé dans dev
```

Dans S3, envoyez un fichier :

```text
dev-file.txt
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-10"></a>

## Partie X — Valider test dans Streamlit

<details>
<summary><strong>10.1 Sélectionner test</strong></summary>

Dans la barre latérale, choisissez :

```text
test
```

</details>

<details>
<summary><strong>10.2 Tester les ressources test</strong></summary>

Dans le Dashboard :

```text
Tester LocalStack
Tester S3
Tester DynamoDB
Tester SQS
```

Tout doit fonctionner.

</details>

<details>
<summary><strong>10.3 Ajouter des données test</strong></summary>

Dans DynamoDB, ajoutez :

```text
TEST-S001
```

Dans SQS, envoyez :

```text
Message envoyé dans test
```

Dans S3, envoyez un fichier :

```text
test-file.txt
```

</details>

<details>
<summary><strong>10.4 Comparer dev et test</strong></summary>

Revenez à `dev`, puis à `test`.

Vous devez observer que les ressources sont séparées.

Les données ajoutées dans `dev` ne doivent pas apparaître dans `test`, car les ressources ont des noms différents.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-11"></a>

## Partie XI — Exercices guidés

<details>
<summary><strong>Exercice 1 — Ajouter un environnement stage</strong></summary>

Créez :

```text
terraform/environments/stage
```

Copiez les fichiers de `dev`.

Modifiez :

```hcl
environment = "stage"
```

Appliquez Terraform.

Relancez Streamlit.

Question :

```text
L’environnement stage apparaît-il automatiquement dans Streamlit ?
```

</details>

<details>
<summary><strong>Exercice 2 — Modifier owner_name seulement dans test</strong></summary>

Dans `test/terraform.tfvars`, modifiez :

```hcl
owner_name = "groupe-test"
```

Puis :

```bash
terraform plan
terraform apply
```

Question :

```text
Terraform remplace-t-il les ressources ou modifie-t-il seulement les tags ?
```

</details>

<details>
<summary><strong>Exercice 3 — Supprimer temporairement un environnement</strong></summary>

Renommez temporairement :

```text
terraform/environments/test
```

en :

```text
terraform/environments/test-disabled
```

Relancez Streamlit.

Question :

```text
Comment Streamlit réagit-il ?
```

Remettez le nom original ensuite.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-12"></a>

## Partie XII — Erreurs fréquentes

<details>
<summary><strong>Erreur 1 — Aucun environnement trouvé</strong></summary>

Cause :

```text
Le dossier terraform/environments/ n’existe pas.
```

Solution :

```text
Créer terraform/environments/dev et terraform/environments/test.
```

</details>

<details>
<summary><strong>Erreur 2 — Outputs Terraform indisponibles</strong></summary>

Cause :

```text
terraform apply n’a pas été exécuté dans cet environnement.
```

Solution :

```bash
terraform -chdir=terraform/environments/dev apply
terraform -chdir=terraform/environments/test apply
```

</details>

<details>
<summary><strong>Erreur 3 — Module introuvable</strong></summary>

Cause :

```text
source = "../../modules/s3" incorrect ou dossier modules absent.
```

Solution :

```text
Vérifier la structure terraform/modules/.
```

</details>

<details>
<summary><strong>Erreur 4 — Ressources dev et test mélangées</strong></summary>

Cause :

```text
environment est identique dans dev et test.
```

Solution :

```text
dev/terraform.tfvars doit contenir environment = "dev"
test/terraform.tfvars doit contenir environment = "test"
```

</details>

<details>
<summary><strong>Erreur 5 — Même state Terraform utilisé par erreur</strong></summary>

Chaque environnement doit avoir son propre dossier et son propre fichier state local.

Ne lancez pas tout depuis le mauvais dossier.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-13"></a>

## Partie XIII — Questions de compréhension

1. Quel est l’objectif principal de ce TP ?
2. Pourquoi sépare-t-on `dev` et `test` ?
3. Pourquoi les deux environnements doivent-ils avoir des noms de ressources différents ?
4. Quel est le rôle du dossier `terraform/environments/` ?
5. Quel est le rôle du dossier `terraform/modules/` ?
6. Pourquoi `dev` et `test` peuvent-ils utiliser les mêmes modules ?
7. Pourquoi chaque environnement possède-t-il son propre `terraform.tfvars` ?
8. Pourquoi chaque environnement possède-t-il ses propres outputs ?
9. Que lit Streamlit pour savoir quelles ressources afficher ?
10. Pourquoi Streamlit ne doit-il pas créer les environnements ?
11. Que se passe-t-il si `terraform apply` n’a pas été fait dans `test` ?
12. Pourquoi `terraform -chdir=... output -json` est-il pratique ?
13. Comment Streamlit détecte-t-il les environnements disponibles ?
14. Pourquoi les données de `dev` ne doivent-elles pas apparaître dans `test` ?
15. Quelle est la différence entre un module et un environnement ?
16. Pourquoi `environment = "test"` change-t-il les noms de ressources ?
17. Comment ajouter un nouvel environnement `stage` ?
18. Pourquoi cette structure est-elle plus professionnelle ?
19. Quelles erreurs peuvent arriver avec plusieurs environnements ?
20. Comment ce TP renforce-t-il l’apprentissage de Terraform ?

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-14"></a>

## Partie XIV — Mini-rapport à remettre

## Informations générales

```text
Nom :
Date :
Groupe :
Environnements créés :
project_name :
owner_name :
```

## Captures demandées

```text
1. Structure terraform/environments/.
2. Structure terraform/modules/.
3. dev/terraform.tfvars.
4. test/terraform.tfvars.
5. terraform apply dans dev.
6. terraform apply dans test.
7. terraform output dev.
8. terraform output test.
9. Streamlit sélection dev.
10. Streamlit Dashboard dev validé.
11. Streamlit S3 dev.
12. Streamlit DynamoDB dev.
13. Streamlit SQS dev.
14. Streamlit sélection test.
15. Streamlit Dashboard test validé.
16. Comparaison visuelle dev/test.
```

## Questions à intégrer

```text
1. Expliquez pourquoi on sépare dev et test.
2. Expliquez comment les modules sont réutilisés.
3. Expliquez comment Streamlit lit les outputs d’un environnement.
4. Expliquez une erreur rencontrée.
5. Expliquez pourquoi cette organisation est plus professionnelle.
```

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="corrige"></a>

## Corrigé / Indications

<details>
<summary><strong>Indication 1 — Environnement</strong></summary>

Un environnement est une instance séparée de l’infrastructure. `dev` et `test` doivent avoir des ressources séparées.

</details>

<details>
<summary><strong>Indication 2 — Module</strong></summary>

Un module contient du code réutilisable. Les environnements appellent les mêmes modules avec des variables différentes.

</details>

<details>
<summary><strong>Indication 3 — Streamlit</strong></summary>

Streamlit lit les outputs Terraform de l’environnement sélectionné. Il valide les ressources, mais ne les crée pas.

</details>

<details>
<summary><strong>Indication 4 — Outputs</strong></summary>

Les outputs permettent à Streamlit de connaître les noms exacts des ressources à tester.

</details>

---

## Score final

| Partie | Note obtenue | Note maximale |
|---|---:|---:|
| Compréhension environnements | | 15 |
| Structure | | 20 |
| Environnement dev | | 30 |
| Environnement test | | 30 |
| Apply dev | | 25 |
| Apply test | | 25 |
| Outputs | | 25 |
| Streamlit multi-env | | 35 |
| Validation dev | | 25 |
| Validation test | | 25 |
| Rapport | | 30 |
| **TOTAL** | | **285** |

---

*Fin du TP 5 — Gérer plusieurs environnements Terraform et les valider avec Streamlit.*
