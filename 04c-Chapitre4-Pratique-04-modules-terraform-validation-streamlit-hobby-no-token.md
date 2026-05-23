<a id="top"></a>

# TP 4 (version `c`) — Organiser Terraform avec des modules et valider avec Streamlit (sans token)

> **Version `c` — sans compte ni token.** Cette version suppose que vous avez fait les TPs 1c, 2c et 3c (bypass `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1`). Sinon, basculez sur [`04b-...md`](04b-Chapitre4-Pratique-04-modules-terraform-validation-streamlit.md).
>
> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, basculez sur la version `b`.
>
> **Cours visé :** Terraform, Infrastructure as Code, modules Terraform, LocalStack, Streamlit  
>
> **Niveau :** Débutant avancé  
>
> **Prérequis :** les TPs 1, 2 et 3 (version `c`) doivent être réalisés. Le projet contient déjà S3, DynamoDB, SQS, des variables, des outputs et un dashboard Streamlit.  
>
> **Objectif principal :** apprendre à organiser un projet Terraform avec des modules réutilisables, puis vérifier dans Streamlit que les ressources créées par les modules existent toujours dans LocalStack.  
>
> **Important :** Streamlit reste obligatoire comme outil de validation visuelle, mais le sujet principal est Terraform. Dans ce TP, Streamlit sert à confirmer que la réorganisation en modules n’a pas cassé l’infrastructure.  
>
> **Ressources concernées :** S3, DynamoDB, SQS  
>
> **Outils utilisés :** Terraform, LocalStack, Docker Compose, AWS CLI, Streamlit  
>
> **Durée recommandée :** 4 à 6 heures  
>
> **Livrables :** structure Terraform modulaire, outputs fonctionnels, dashboard Streamlit validé, captures d’écran, mini-rapport.

---

## À lire avant de commencer

Jusqu’ici, vous avez créé les ressources dans un fichier `main.tf`.

Cette approche fonctionne pour un petit TP.

Mais dans un projet plus grand, un seul fichier `main.tf` peut devenir trop long.

Exemple de problème :

```text
main.tf contient S3 ;
main.tf contient DynamoDB ;
main.tf contient SQS ;
main.tf contiendra peut-être Lambda ;
main.tf contiendra peut-être IAM ;
main.tf devient difficile à lire.
```

La solution est d’utiliser des **modules Terraform**.

Un module permet de regrouper le code d’une ressource ou d’un composant.

Dans ce TP, vous allez créer trois modules :

```text
module s3
module dynamodb
module sqs
```

Puis le fichier principal appellera ces modules.

Le dashboard Streamlit devra ensuite vérifier que les ressources créées par les modules existent toujours.

---

## Idée centrale du TP

Avant les modules :

```text
terraform/main.tf
   |
   +--> aws_s3_bucket
   +--> aws_dynamodb_table
   +--> aws_sqs_queue
```

Après les modules :

```text
terraform/main.tf
   |
   +--> module "documents_bucket"
   +--> module "students_table"
   +--> module "notifications_queue"
```

Chaque module contient sa propre logique.

---

## Pourquoi garder Streamlit ?

Parce qu’un étudiant peut croire qu’une réorganisation du code ne change rien.

Mais dans Terraform, une mauvaise réorganisation peut créer des effets importants :

```text
ressources renommées ;
ressources détruites ;
ressources recréées ;
outputs cassés ;
application Streamlit incapable de trouver les ressources.
```

Streamlit sert donc à vérifier concrètement :

```text
S3 existe encore ;
DynamoDB existe encore ;
SQS existe encore ;
les outputs correspondent encore à .env ;
l’application peut encore utiliser les ressources.
```

---

## Architecture pédagogique

```text
Modules Terraform
   |
   v
Ressources LocalStack
   |
   v
terraform output
   |
   v
.env
   |
   v
Streamlit valide visuellement
```

---

## Barème proposé

| Partie | Travail demandé | Points |
|---|---|---:|
| **I** | Comprendre le rôle des modules Terraform | 15 |
| **II** | Préparer la structure `modules/` | 20 |
| **III** | Créer le module S3 | 25 |
| **IV** | Créer le module DynamoDB | 25 |
| **V** | Créer le module SQS | 25 |
| **VI** | Réécrire le `main.tf` racine avec des appels de modules | 30 |
| **VII** | Adapter les outputs racine | 25 |
| **VIII** | Exécuter `terraform init`, `fmt`, `validate`, `plan` | 30 |
| **IX** | Interpréter les changements proposés par Terraform | 30 |
| **X** | Appliquer proprement | 15 |
| **XI** | Valider dans Streamlit | 30 |
| **XII** | Questions et mini-rapport | 30 |
| | **TOTAL** | **280 pts** |

---

## Table des matières

| # | Section |
|---|---|
| 1 | [Partie I — Comprendre les modules Terraform](#partie-1) |
| 2 | [Partie II — Observer la structure actuelle](#partie-2) |
| 3 | [Partie III — Créer la structure `modules/`](#partie-3) |
| 4 | [Partie IV — Créer le module S3](#partie-4) |
| 5 | [Partie V — Créer le module DynamoDB](#partie-5) |
| 6 | [Partie VI — Créer le module SQS](#partie-6) |
| 7 | [Partie VII — Réécrire le `main.tf` racine](#partie-7) |
| 8 | [Partie VIII — Réécrire les outputs racine](#partie-8) |
| 9 | [Partie IX — Réinitialiser Terraform avec les modules](#partie-9) |
| 10 | [Partie X — Lire attentivement `terraform plan`](#partie-10) |
| 11 | [Partie XI — Appliquer les changements](#partie-11) |
| 12 | [Partie XII — Vérifier les outputs](#partie-12) |
| 13 | [Partie XIII — Valider dans Streamlit](#partie-13) |
| 14 | [Partie XIV — Exercices guidés](#partie-14) |
| 15 | [Partie XV — Erreurs fréquentes](#partie-15) |
| 16 | [Partie XVI — Questions de compréhension](#partie-16) |
| 17 | [Partie XVII — Mini-rapport à remettre](#partie-17) |
| 18 | [Corrigé / Indications](#corrige) |

---

<a id="partie-1"></a>

## Partie I — Comprendre les modules Terraform

<details>
<summary><strong>1.1 C’est quoi un module Terraform ?</strong></summary>

Un module Terraform est un dossier qui contient du code Terraform réutilisable.

Un module peut contenir :

```text
main.tf
variables.tf
outputs.tf
```

Exemple :

```text
modules/s3/
├── main.tf
├── variables.tf
└── outputs.tf
```

Ce module peut être appelé depuis le fichier principal.

</details>

<details>
<summary><strong>1.2 Pourquoi utiliser des modules ?</strong></summary>

Les modules permettent de :

```text
mieux organiser le code ;
éviter un main.tf trop long ;
réutiliser du code ;
séparer les responsabilités ;
rendre le projet plus professionnel.
```

Sans modules, tout est mélangé.

Avec modules, chaque ressource ou groupe de ressources a son propre espace.

</details>

<details>
<summary><strong>1.3 Exemple simple</strong></summary>

Au lieu d’écrire directement :

```hcl
resource "aws_s3_bucket" "documents" {
  bucket = "${var.project_name}-${var.environment}-documents"
}
```

dans le `main.tf` racine, on appelle un module :

```hcl
module "documents_bucket" {
  source = "./modules/s3"

  project_name  = var.project_name
  environment   = var.environment
  owner_name    = var.owner_name
  bucket_suffix = "documents"
}
```

Le module contient la ressource réelle.

</details>

<details>
<summary><strong>1.4 Ce que Streamlit doit prouver</strong></summary>

Après la migration en modules, Streamlit doit prouver que :

```text
le bucket S3 existe ;
la table DynamoDB existe ;
la file SQS existe ;
les outputs Terraform fonctionnent encore ;
.env correspond toujours aux outputs ;
les opérations applicatives fonctionnent encore.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-2"></a>

## Partie II — Observer la structure actuelle

<details>
<summary><strong>2.1 Structure actuelle probable</strong></summary>

Votre dossier Terraform ressemble probablement à ceci :

```text
terraform/
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── main.tf
└── outputs.tf
```

Le fichier `main.tf` contient directement :

```text
aws_s3_bucket
aws_dynamodb_table
aws_sqs_queue
```

</details>

<details>
<summary><strong>2.2 Lire l’état actuel</strong></summary>

```bash
cd terraform
terraform state list
```

Résultat attendu :

```text
aws_dynamodb_table.students
aws_s3_bucket.documents
aws_sqs_queue.notifications
```

</details>

<details>
<summary><strong>2.3 Lire les outputs actuels</strong></summary>

```bash
terraform output
```

Notez :

```text
s3_bucket_name
dynamodb_table_name
sqs_queue_name
sqs_queue_url
```

Ces valeurs seront utiles pour vérifier si la migration en modules conserve les mêmes noms.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-3"></a>

## Partie III — Créer la structure `modules/`

<details>
<summary><strong>3.1 Créer les dossiers</strong></summary>

Dans le dossier `terraform/`, créez :

```bash
mkdir -p modules/s3
mkdir -p modules/dynamodb
mkdir -p modules/sqs
```

Sous PowerShell :

```powershell
New-Item -ItemType Directory -Force modules\s3
New-Item -ItemType Directory -Force modules\dynamodb
New-Item -ItemType Directory -Force modules\sqs
```

</details>

<details>
<summary><strong>3.2 Créer les fichiers de chaque module</strong></summary>

Dans chaque module, créez :

```text
main.tf
variables.tf
outputs.tf
```

Structure attendue :

```text
terraform/
└── modules/
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

</details>

<details>
<summary><strong>3.3 Pourquoi trois modules ?</strong></summary>

On sépare les responsabilités :

```text
module s3       -> stockage de fichiers
module dynamodb -> données des étudiants
module sqs      -> messages
```

Chaque module devient plus facile à lire.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-4"></a>

## Partie IV — Créer le module S3

<details>
<summary><strong>4.1 `modules/s3/main.tf`</strong></summary>

```hcl
resource "aws_s3_bucket" "this" {
  bucket = "${var.project_name}-${var.environment}-${var.bucket_suffix}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
    Module      = "s3"
  }
}
```

</details>

<details>
<summary><strong>4.2 `modules/s3/variables.tf`</strong></summary>

```hcl
variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
}

variable "owner_name" {
  description = "Responsable ou groupe"
  type        = string
}

variable "bucket_suffix" {
  description = "Suffixe du bucket S3"
  type        = string
  default     = "documents"
}
```

</details>

<details>
<summary><strong>4.3 `modules/s3/outputs.tf`</strong></summary>

```hcl
output "bucket_name" {
  description = "Nom du bucket S3 créé par le module"
  value       = aws_s3_bucket.this.bucket
}
```

</details>

<details>
<summary><strong>4.4 Pourquoi le nom local est `this` ?</strong></summary>

Dans un module, on utilise souvent un nom générique comme :

```text
this
```

Parce que le module lui-même donne déjà le contexte.

Dans `modules/s3`, `aws_s3_bucket.this` signifie :

```text
le bucket principal de ce module S3
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-5"></a>

## Partie V — Créer le module DynamoDB

<details>
<summary><strong>5.1 `modules/dynamodb/main.tf`</strong></summary>

```hcl
resource "aws_dynamodb_table" "this" {
  name         = "${var.project_name}-${var.environment}-${var.table_suffix}"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "student_id"

  attribute {
    name = "student_id"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
    Module      = "dynamodb"
  }
}
```

</details>

<details>
<summary><strong>5.2 `modules/dynamodb/variables.tf`</strong></summary>

```hcl
variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
}

variable "owner_name" {
  description = "Responsable ou groupe"
  type        = string
}

variable "table_suffix" {
  description = "Suffixe de la table DynamoDB"
  type        = string
  default     = "students"
}
```

</details>

<details>
<summary><strong>5.3 `modules/dynamodb/outputs.tf`</strong></summary>

```hcl
output "table_name" {
  description = "Nom de la table DynamoDB créée par le module"
  value       = aws_dynamodb_table.this.name
}
```

</details>

<details>
<summary><strong>5.4 Ce que le module reçoit</strong></summary>

Le module reçoit :

```text
project_name
environment
owner_name
table_suffix
```

Il construit ensuite le nom de la table.

Exemple :

```text
tp-validation-dev-students
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-6"></a>

## Partie VI — Créer le module SQS

<details>
<summary><strong>6.1 `modules/sqs/main.tf`</strong></summary>

```hcl
resource "aws_sqs_queue" "this" {
  name = "${var.project_name}-${var.environment}-${var.queue_suffix}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
    Module      = "sqs"
  }
}
```

</details>

<details>
<summary><strong>6.2 `modules/sqs/variables.tf`</strong></summary>

```hcl
variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
}

variable "owner_name" {
  description = "Responsable ou groupe"
  type        = string
}

variable "queue_suffix" {
  description = "Suffixe de la file SQS"
  type        = string
  default     = "notifications"
}
```

</details>

<details>
<summary><strong>6.3 `modules/sqs/outputs.tf`</strong></summary>

```hcl
output "queue_name" {
  description = "Nom de la file SQS créée par le module"
  value       = aws_sqs_queue.this.name
}

output "queue_url" {
  description = "URL de la file SQS créée par le module"
  value       = aws_sqs_queue.this.url
}
```

</details>

<details>
<summary><strong>6.4 Pourquoi deux outputs pour SQS ?</strong></summary>

Pour SQS, on a souvent besoin :

```text
du nom de la file ;
de l’URL de la file.
```

L’URL est particulièrement utile pour :

```text
envoyer un message ;
lire un message ;
supprimer un message.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-7"></a>

## Partie VII — Réécrire le `main.tf` racine

<details>
<summary><strong>7.1 Sauvegarder l’ancien main.tf</strong></summary>

Avant de modifier, faites une copie :

```bash
cp main.tf main-old.tf
```

PowerShell :

```powershell
Copy-Item main.tf main-old.tf
```

</details>

<details>
<summary><strong>7.2 Nouveau `terraform/main.tf`</strong></summary>

Remplacez le contenu par :

```hcl
module "documents_bucket" {
  source = "./modules/s3"

  project_name  = var.project_name
  environment   = var.environment
  owner_name    = var.owner_name
  bucket_suffix = "documents"
}

module "students_table" {
  source = "./modules/dynamodb"

  project_name = var.project_name
  environment  = var.environment
  owner_name   = var.owner_name
  table_suffix = "students"
}

module "notifications_queue" {
  source = "./modules/sqs"

  project_name = var.project_name
  environment  = var.environment
  owner_name   = var.owner_name
  queue_suffix = "notifications"
}
```

</details>

<details>
<summary><strong>7.3 Ce que fait ce fichier</strong></summary>

Le fichier racine ne crée plus directement les ressources.

Il appelle les modules :

```text
documents_bucket utilise modules/s3
students_table utilise modules/dynamodb
notifications_queue utilise modules/sqs
```

Terraform va ensuite créer les ressources à partir des modules.

</details>

<details>
<summary><strong>7.4 Attention importante</strong></summary>

Même si les noms des ressources AWS restent identiques, les adresses Terraform changent.

Avant :

```text
aws_s3_bucket.documents
```

Après :

```text
module.documents_bucket.aws_s3_bucket.this
```

Cela peut provoquer des changements dans `terraform plan`.

Il faut lire le plan attentivement.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-8"></a>

## Partie VIII — Réécrire les outputs racine

<details>
<summary><strong>8.1 Pourquoi modifier les outputs ?</strong></summary>

Avant, les outputs pointaient vers des ressources directes.

Exemple :

```hcl
aws_s3_bucket.documents.bucket
```

Maintenant, les ressources sont dans les modules.

Il faut donc pointer vers les outputs des modules.

</details>

<details>
<summary><strong>8.2 Nouveau `terraform/outputs.tf`</strong></summary>

```hcl
output "s3_bucket_name" {
  description = "Nom du bucket S3 créé par le module s3"
  value       = module.documents_bucket.bucket_name
}

output "dynamodb_table_name" {
  description = "Nom de la table DynamoDB créée par le module dynamodb"
  value       = module.students_table.table_name
}

output "sqs_queue_name" {
  description = "Nom de la file SQS créée par le module sqs"
  value       = module.notifications_queue.queue_name
}

output "sqs_queue_url" {
  description = "URL de la file SQS créée par le module sqs"
  value       = module.notifications_queue.queue_url
}

output "localstack_endpoint" {
  description = "Endpoint LocalStack utilisé"
  value       = "http://localhost:4566"
}

output "project_name" {
  description = "Nom du projet"
  value       = var.project_name
}

output "environment_name" {
  description = "Nom de l'environnement"
  value       = var.environment
}

output "owner_name" {
  description = "Responsable ou groupe"
  value       = var.owner_name
}
```

</details>

<details>
<summary><strong>8.3 Pourquoi garder les mêmes noms d’outputs ?</strong></summary>

On garde :

```text
s3_bucket_name
dynamodb_table_name
sqs_queue_name
sqs_queue_url
```

pour ne pas casser Streamlit.

Ainsi, même si le code Terraform est réorganisé, l’application de validation peut continuer à lire les mêmes outputs.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-9"></a>

## Partie IX — Réinitialiser Terraform avec les modules

<details>
<summary><strong>9.1 Pourquoi relancer init ?</strong></summary>

Quand on ajoute des modules, il faut relancer :

```bash
terraform init
```

Terraform doit détecter et préparer les modules locaux.

</details>

<details>
<summary><strong>9.2 Commandes</strong></summary>

Dans le dossier `terraform/` :

```bash
terraform init
terraform fmt -recursive
terraform validate
```

</details>

<details>
<summary><strong>9.3 Pourquoi `fmt -recursive` ?</strong></summary>

`terraform fmt` formate le dossier courant.

Mais les modules sont dans des sous-dossiers.

Donc on utilise :

```bash
terraform fmt -recursive
```

pour formater aussi :

```text
modules/s3
modules/dynamodb
modules/sqs
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-10"></a>

## Partie X — Lire attentivement `terraform plan`

<details>
<summary><strong>10.1 Exécuter le plan</strong></summary>

```bash
terraform plan
```

</details>

<details>
<summary><strong>10.2 Point très important</strong></summary>

Terraform peut proposer de détruire et recréer des ressources parce que leur adresse interne a changé.

Avant :

```text
aws_s3_bucket.documents
```

Après :

```text
module.documents_bucket.aws_s3_bucket.this
```

Même si le nom du bucket est identique, Terraform peut croire que c’est une nouvelle ressource.

</details>

<details>
<summary><strong>10.3 Deux approches pédagogiques possibles</strong></summary>

Approche simple pour débutants :

```text
Accepter le remplacement dans LocalStack, car c’est un environnement local.
```

Approche plus avancée :

```text
Utiliser terraform state mv pour déplacer l’état Terraform sans recréer les ressources.
```

Dans ce TP débutant, on peut accepter le remplacement si le professeur l’autorise.

Mais il faut comprendre ce qui se passe.

</details>

<details>
<summary><strong>10.4 Question importante</strong></summary>

Dans le rapport, vous devez répondre :

```text
Terraform a-t-il proposé de remplacer les ressources ?
Pourquoi ?
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-11"></a>

## Partie XI — Appliquer les changements

<details>
<summary><strong>11.1 Appliquer</strong></summary>

Si le plan est compris et accepté :

```bash
terraform apply
```

Répondez :

```text
yes
```

</details>

<details>
<summary><strong>11.2 Lire le nouvel état</strong></summary>

```bash
terraform state list
```

Résultat attendu :

```text
module.documents_bucket.aws_s3_bucket.this
module.notifications_queue.aws_sqs_queue.this
module.students_table.aws_dynamodb_table.this
```

</details>

<details>
<summary><strong>11.3 Ce que cela prouve</strong></summary>

Cela prouve que les ressources sont maintenant gérées par des modules Terraform.

Les adresses Terraform ont changé.

Mais les ressources restent organisées autour de :

```text
S3
DynamoDB
SQS
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-12"></a>

## Partie XII — Vérifier les outputs

<details>
<summary><strong>12.1 Exécuter terraform output</strong></summary>

```bash
terraform output
```

Vous devez voir :

```text
s3_bucket_name
dynamodb_table_name
sqs_queue_name
sqs_queue_url
localstack_endpoint
project_name
environment_name
owner_name
```

</details>

<details>
<summary><strong>12.2 Vérifier les noms</strong></summary>

Les noms doivent correspondre au fichier `.env`.

Si les noms ont changé, mettez à jour `.env`.

</details>

<details>
<summary><strong>12.3 Revenir à la racine</strong></summary>

```bash
cd ..
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-13"></a>

## Partie XIII — Valider dans Streamlit

<details>
<summary><strong>13.1 Lancer Streamlit</strong></summary>

À la racine du projet :

```bash
streamlit run app.py
```

</details>

<details>
<summary><strong>13.2 Vérifier la page Terraform outputs</strong></summary>

Ouvrez :

```text
Terraform outputs
```

Vous devez voir que les valeurs `.env` correspondent aux outputs Terraform.

Objectif :

```text
S3 = OK
DynamoDB = OK
SQS = OK
```

</details>

<details>
<summary><strong>13.3 Vérifier S3</strong></summary>

Dans :

```text
S3 — Ressource Terraform
```

testez :

```text
vérifier le bucket ;
envoyer un fichier ;
lister le fichier.
```

</details>

<details>
<summary><strong>13.4 Vérifier DynamoDB</strong></summary>

Dans :

```text
DynamoDB — Ressource Terraform
```

testez :

```text
ajouter un étudiant ;
lister les étudiants.
```

</details>

<details>
<summary><strong>13.5 Vérifier SQS</strong></summary>

Dans :

```text
SQS — Ressource Terraform
```

testez :

```text
envoyer un message ;
lire le message ;
supprimer le message.
```

</details>

<details>
<summary><strong>13.6 Conclusion pédagogique</strong></summary>

Si tout fonctionne dans Streamlit, cela signifie :

```text
les modules Terraform ont créé les ressources ;
les outputs fonctionnent ;
.env est cohérent ;
l’application peut utiliser l’infrastructure.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-14"></a>

## Partie XIV — Exercices guidés

<details>
<summary><strong>Exercice 1 — Ajouter un suffixe paramétrable</strong></summary>

Dans le module S3, changez :

```hcl
bucket_suffix = "documents"
```

par une variable différente dans l’appel du module :

```hcl
bucket_suffix = "files"
```

Lancez :

```bash
terraform plan
```

Question :

```text
Terraform veut-il remplacer le bucket ?
Pourquoi ?
```

</details>

<details>
<summary><strong>Exercice 2 — Ajouter un output dans un module</strong></summary>

Dans `modules/s3/outputs.tf`, ajoutez :

```hcl
output "module_name" {
  value = "s3"
}
```

Puis exposez cette valeur dans le `outputs.tf` racine.

Question :

```text
Pourquoi faut-il parfois remonter un output du module vers la racine ?
```

</details>

<details>
<summary><strong>Exercice 3 — Casser volontairement un chemin de module</strong></summary>

Changez temporairement :

```hcl
source = "./modules/s3"
```

par :

```hcl
source = "./modules/s3-faux"
```

Lancez :

```bash
terraform init
```

Question :

```text
Quelle erreur apparaît ?
```

Remettez ensuite le bon chemin.

</details>

<details>
<summary><strong>Exercice 4 — Vérifier Streamlit après chaque changement</strong></summary>

Après chaque modification Terraform :

```text
terraform plan
terraform apply
terraform output
mise à jour éventuelle de .env
test Streamlit
```

Question :

```text
Pourquoi faut-il conserver cette discipline ?
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-15"></a>

## Partie XV — Erreurs fréquentes

<details>
<summary><strong>Erreur 1 — Module not found</strong></summary>

Cause possible :

```text
Le chemin source est incorrect.
```

Vérifiez :

```hcl
source = "./modules/s3"
```

</details>

<details>
<summary><strong>Erreur 2 — Variable manquante dans un module</strong></summary>

Message possible :

```text
Missing required argument
```

Cause :

```text
Le module attend une variable, mais l’appel du module ne la fournit pas.
```

Solution :

```text
vérifier variables.tf du module ;
vérifier l’appel du module dans main.tf.
```

</details>

<details>
<summary><strong>Erreur 3 — Output introuvable</strong></summary>

Message possible :

```text
Unsupported attribute
```

Cause :

```text
Vous appelez module.documents_bucket.bucket_name, mais le module n’a pas d’output bucket_name.
```

Solution :

```text
ajouter output "bucket_name" dans modules/s3/outputs.tf.
```

</details>

<details>
<summary><strong>Erreur 4 — Streamlit ne trouve plus la ressource</strong></summary>

Cause possible :

```text
les noms ont changé ;
.env n’a pas été mis à jour ;
terraform output ne correspond plus.
```

Solution :

```bash
terraform output
```

Puis corriger `.env`.

</details>

<details>
<summary><strong>Erreur 5 — Terraform veut tout détruire</strong></summary>

Cause possible :

```text
vous avez changé les adresses Terraform en passant aux modules.
```

Dans LocalStack, cela peut être acceptable pour apprendre.

Dans AWS réel, il faudrait être beaucoup plus prudent.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-16"></a>

## Partie XVI — Questions de compréhension

1. Quel est l’objectif principal de ce TP ?
2. Pourquoi utilise-t-on des modules Terraform ?
3. Quelle est la différence entre une ressource directe et une ressource dans un module ?
4. Pourquoi le `main.tf` racine devient-il plus court avec des modules ?
5. Quel est le rôle de `source = "./modules/s3"` ?
6. Pourquoi chaque module possède-t-il son propre `variables.tf` ?
7. Pourquoi chaque module possède-t-il son propre `outputs.tf` ?
8. Pourquoi le module SQS expose-t-il `queue_url` ?
9. Pourquoi les outputs racine doivent-ils appeler les outputs des modules ?
10. Pourquoi faut-il relancer `terraform init` après avoir ajouté des modules ?
11. Pourquoi utilise-t-on `terraform fmt -recursive` ?
12. Pourquoi Terraform peut-il proposer de remplacer les ressources ?
13. Quelle est la différence entre le nom AWS d’une ressource et son adresse Terraform ?
14. Pourquoi ce remplacement est-il moins grave dans LocalStack que dans AWS réel ?
15. Pourquoi faut-il vérifier Streamlit après la migration en modules ?
16. Que prouve la page Terraform outputs dans Streamlit ?
17. Que faut-il faire si `.env` ne correspond plus aux outputs Terraform ?
18. Pourquoi Streamlit ne doit-il pas créer les ressources ?
19. Comment les modules rendent-ils le projet plus professionnel ?
20. Comment ce TP prépare-t-il à une vraie infrastructure cloud ?

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-17"></a>

## Partie XVII — Mini-rapport à remettre

## Informations générales

```text
Nom :
Date :
Groupe :
project_name :
environment :
owner_name :
```

## Captures demandées

```text
1. Structure terraform/modules/.
2. Module s3 complet.
3. Module dynamodb complet.
4. Module sqs complet.
5. main.tf racine avec appels de modules.
6. outputs.tf racine.
7. terraform init.
8. terraform fmt -recursive.
9. terraform validate.
10. terraform plan.
11. terraform apply.
12. terraform state list avec module....
13. terraform output.
14. Streamlit page Terraform outputs avec OK.
15. Streamlit validation S3.
16. Streamlit validation DynamoDB.
17. Streamlit validation SQS.
```

## Questions à intégrer

```text
1. Expliquez ce que vous avez changé dans l’organisation Terraform.
2. Expliquez pourquoi les modules sont utiles.
3. Expliquez ce que Terraform a proposé dans le plan.
4. Expliquez comment vous avez vérifié les outputs.
5. Expliquez comment Streamlit prouve que la migration en modules fonctionne.
```

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="corrige"></a>

## Corrigé / Indications

<details>
<summary><strong>Indication 1 — Module</strong></summary>

Un module est un dossier Terraform réutilisable. Il contient ses propres ressources, variables et outputs.

</details>

<details>
<summary><strong>Indication 2 — Outputs racine</strong></summary>

Les outputs racine doivent exposer les valeurs importantes des modules pour que les autres outils, comme Streamlit, puissent les utiliser.

</details>

<details>
<summary><strong>Indication 3 — Adresse Terraform</strong></summary>

Une ressource directe peut avoir une adresse comme `aws_s3_bucket.documents`. Une ressource dans un module peut avoir une adresse comme `module.documents_bucket.aws_s3_bucket.this`.

</details>

<details>
<summary><strong>Indication 4 — Streamlit</strong></summary>

Streamlit valide que les ressources créées par les modules sont accessibles. Il ne remplace pas Terraform.

</details>

---

## Score final

| Partie | Note obtenue | Note maximale |
|---|---:|---:|
| Compréhension modules | | 15 |
| Structure modules | | 20 |
| Module S3 | | 25 |
| Module DynamoDB | | 25 |
| Module SQS | | 25 |
| main.tf racine | | 30 |
| outputs racine | | 25 |
| init/fmt/validate/plan | | 30 |
| Interprétation plan | | 30 |
| apply | | 15 |
| Streamlit | | 30 |
| Rapport | | 30 |
| **TOTAL** | | **280** |

---

*Fin du TP 4 — Organiser Terraform avec des modules et valider avec Streamlit.*
