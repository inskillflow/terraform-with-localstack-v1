<a id="top"></a>

# TP 2 (version `c`) — Dashboard Streamlit pour valider les ressources créées avec Terraform (sans token)

> **Version `c` — sans compte ni token.** Cette version suppose que vous avez fait le **TP 1 version `c`** (bypass `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1`). Si vous avez fait le TP 1 version `b` (avec token), basculez sur [`02b-...md`](02b-Chapitre2-Pratique-02-terraform-localstack-ajout-ui.md).
>
> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, basculez sur la version `b` (token requis).
>
> **Cours visé :** Terraform, Infrastructure as Code, LocalStack, validation d'infrastructure, Streamlit  
>
> **Niveau :** Débutant complet  
>
> **Prérequis :** le TP 1 (version `c`) doit déjà être réalisé. LocalStack doit être démarré (avec bypass) et Terraform doit avoir créé un bucket S3 et une table DynamoDB.  
>
> **Objectif principal :** apprendre à vérifier visuellement, avec une interface Streamlit, que les ressources déclarées dans Terraform existent réellement dans LocalStack.  
>
> **Important :** ce TP reste un TP orienté Terraform. Streamlit est utilisé comme tableau de bord de validation. Streamlit ne remplace pas Terraform et ne doit pas créer l’infrastructure.  
>
> **Ressources validées :** bucket S3, table DynamoDB, outputs Terraform  
>
> **Outils utilisés :** Terraform, LocalStack, Docker Compose, Python, Streamlit, boto3, AWS CLI  
>
> **Durée recommandée :** 3 à 5 heures  
>
> **Livrables :** application Streamlit fonctionnelle, captures d’écran, réponses aux questions, mini-rapport.

---

## À lire avant de commencer

Dans le TP 1, vous avez appris à créer une infrastructure AWS simulée localement avec Terraform et LocalStack.

Dans ce TP 2, vous allez créer un **dashboard Streamlit** qui permet de voir les ressources créées.

Le but n’est pas d’apprendre Streamlit pour lui-même.

Le but est de répondre à cette question :

```text
Est-ce que les ressources créées par Terraform existent vraiment dans LocalStack ?
```

Ce TP sert donc à faire le lien entre :

```text
Code Terraform
     |
     v
Ressources créées dans LocalStack
     |
     v
Validation visuelle dans Streamlit
```

Phrase importante :

```text
Terraform est la source de vérité de l’infrastructure.
Streamlit est un outil de visualisation et de validation.
```

---

## Ce que vous allez construire

Vous allez créer une interface web avec cinq pages :

```text
1. Dashboard
2. Terraform outputs
3. S3 — Ressource Terraform
4. DynamoDB — Ressource Terraform
5. À propos
```

L’application permettra de :

```text
tester si LocalStack répond ;
lire les outputs Terraform ;
comparer les outputs Terraform avec les valeurs du fichier .env ;
tester si le bucket S3 existe ;
envoyer un fichier dans le bucket créé par Terraform ;
lister les fichiers du bucket ;
supprimer un fichier ;
tester si la table DynamoDB existe ;
ajouter un étudiant dans la table créée par Terraform ;
lister les étudiants ;
supprimer un étudiant.
```

---

## Architecture pédagogique

```text
Terraform
   |
   v
Crée les ressources dans LocalStack
   |
   v
S3 + DynamoDB
   |
   v
Streamlit les affiche et les manipule
```

Architecture technique :

```text
Utilisateur
   |
   v
Streamlit
   |
   v
boto3
   |
   v
LocalStack : http://localhost:4566
   |
   +--> S3 créé par Terraform
   |
   +--> DynamoDB créé par Terraform
```

---

## Structure finale attendue

```text
terraform-localstack-debutant/
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── app.py
│
└── terraform/
    ├── provider.tf
    ├── variables.tf
    ├── main.tf
    └── outputs.tf
```

---

## Instructions générales

> **À lire attentivement**
>
> - Ne lancez pas Streamlit avant d’avoir démarré LocalStack.
> - Ne lancez pas Streamlit avant d’avoir exécuté `terraform apply`.
> - Streamlit ne doit pas créer l’infrastructure.
> - Les ressources doivent venir de Terraform.
> - Le dashboard doit servir à vérifier les ressources créées.
> - Les valeurs du fichier `.env` doivent correspondre aux `terraform output`.
> - À la fin, vous devez expliquer le lien entre Terraform, LocalStack, boto3 et Streamlit.

---

## Barème proposé

| Partie | Travail demandé | Points |
|---|---|---:|
| **I** | Comprendre le rôle de Streamlit comme validation Terraform | 10 |
| **II** | Vérifier LocalStack | 10 |
| **III** | Vérifier `terraform output` | 15 |
| **IV** | Mettre à jour `.env` selon les outputs Terraform | 15 |
| **V** | Créer l’environnement Python | 15 |
| **VI** | Installer les dépendances | 10 |
| **VII** | Lancer l’application Streamlit | 10 |
| **VIII** | Lire et comparer les outputs Terraform dans Streamlit | 25 |
| **IX** | Valider S3 dans Streamlit | 25 |
| **X** | Valider DynamoDB dans Streamlit | 25 |
| **XI** | Expliquer le rôle de Terraform comme source de vérité | 20 |
| **XII** | Mini-rapport et captures | 20 |
| | **TOTAL** | **200 pts** |

---

## Table des matières

| # | Section |
|---|---|
| 1 | [Partie I — Comprendre le rôle du dashboard](#partie-1) |
| 2 | [Partie II — Vérifier que le TP 1 est terminé](#partie-2) |
| 3 | [Partie III — Lire les outputs Terraform](#partie-3) |
| 4 | [Partie IV — Compléter le fichier `.env`](#partie-4) |
| 5 | [Partie V — Créer `requirements.txt`](#partie-5) |
| 6 | [Partie VI — Créer l’environnement Python](#partie-6) |
| 7 | [Partie VII — Installer les dépendances](#partie-7) |
| 8 | [Partie VIII — Ajouter le fichier `app.py`](#partie-8) |
| 9 | [Partie IX — Lancer Streamlit](#partie-9) |
| 10 | [Partie X — Tester le Dashboard](#partie-10) |
| 11 | [Partie XI — Vérifier les outputs Terraform dans Streamlit](#partie-11) |
| 12 | [Partie XII — Tester S3](#partie-12) |
| 13 | [Partie XIII — Tester DynamoDB](#partie-13) |
| 14 | [Partie XIV — Exercices Terraform + Streamlit](#partie-14) |
| 15 | [Partie XV — Erreurs fréquentes](#partie-15) |
| 16 | [Partie XVI — Questions de compréhension](#partie-16) |
| 17 | [Partie XVII — Mini-rapport à remettre](#partie-17) |
| 18 | [Corrigé / Indications](#corrige) |

---

<a id="partie-1"></a>

## Partie I — Comprendre le rôle du dashboard

<details>
<summary><strong>1.1 Ce TP reste orienté Terraform</strong></summary>

Dans ce TP, Streamlit est un outil secondaire.

Le sujet principal reste :

```text
la validation d’une infrastructure créée avec Terraform
```

Streamlit sert à voir les ressources.

Terraform reste responsable de leur création.

Mauvaise compréhension :

```text
Streamlit crée l’infrastructure.
```

Bonne compréhension :

```text
Terraform crée l’infrastructure.
Streamlit la valide visuellement.
```

</details>

<details>
<summary><strong>1.2 Pourquoi ajouter une interface Streamlit ?</strong></summary>

Avec AWS CLI, on peut vérifier les ressources dans le terminal.

Mais une interface visuelle aide les débutants à comprendre concrètement ce qui a été créé.

Exemple :

```text
Terraform crée un bucket S3.
Streamlit montre ce bucket.
L’étudiant envoie un fichier dans ce bucket.
Il comprend que le bucket existe vraiment.
```

</details>

<details>
<summary><strong>1.3 Règle importante</strong></summary>

Si une ressource n’est pas déclarée dans Terraform, elle ne fait pas partie de l’infrastructure attendue.

Streamlit ne doit pas corriger une infrastructure incomplète.

Il doit seulement révéler si elle est correcte ou non.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-2"></a>

## Partie II — Vérifier que le TP 1 est terminé

<details>
<summary><strong>2.1 Démarrer LocalStack</strong></summary>

À la racine du projet :

```bash
docker compose up -d
```

Vérifiez :

```bash
docker ps
```

Vous devez voir :

```text
localstack-main
```

</details>

<details>
<summary><strong>2.2 Vérifier LocalStack</strong></summary>

Bash ou Git Bash :

```bash
curl http://localhost:4566/_localstack/info
```

PowerShell :

```powershell
Invoke-WebRequest -Uri http://localhost:4566/_localstack/info
```

</details>

<details>
<summary><strong>2.3 Vérifier que Terraform a déjà créé les ressources</strong></summary>

```bash
cd terraform
terraform state list
cd ..
```

Vous devez voir au minimum :

```text
aws_s3_bucket.documents
aws_dynamodb_table.students
```

Si vous ne voyez rien, cela signifie que `terraform apply` n’a pas été exécuté ou que l’état Terraform est absent.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-3"></a>

## Partie III — Lire les outputs Terraform

<details>
<summary><strong>3.1 Exécuter terraform output</strong></summary>

```bash
cd terraform
terraform output
cd ..
```

Résultat attendu :

```text
dynamodb_table_name = "tp-localstack-dev-students"
localstack_endpoint = "http://localhost:4566"
s3_bucket_name = "tp-localstack-dev-documents"
```

</details>

<details>
<summary><strong>3.2 Pourquoi les outputs sont importants ?</strong></summary>

Les outputs sont le pont entre Terraform et le reste du projet.

Ils permettent de récupérer :

```text
le nom du bucket ;
le nom de la table ;
l’endpoint utilisé.
```

L’application Streamlit doit utiliser les mêmes valeurs.

</details>

<details>
<summary><strong>3.3 Sortie JSON utilisée par Streamlit</strong></summary>

Le dashboard Streamlit peut lire les outputs avec :

```bash
terraform -chdir=terraform output -json
```

Cette commande donne une sortie structurée en JSON.

Elle permet à l’application de comparer :

```text
valeurs déclarées par Terraform
VS
valeurs configurées dans .env
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-4"></a>

## Partie IV — Compléter le fichier `.env`

<details>
<summary><strong>4.1 Contenu recommandé</strong></summary>

À la racine du projet, ouvrez `.env`.

Ajoutez ou vérifiez :

```env
LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1
DEBUG=1
PERSISTENCE=1
LOCALSTACK_DOCKER_NAME=localstack-main
LOCALSTACK_VOLUME_DIR=./volume

LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test

S3_BUCKET_NAME=tp-localstack-dev-documents
DYNAMODB_TABLE_NAME=tp-localstack-dev-students
```

> Pas de `LOCALSTACK_AUTH_TOKEN` : on est en mode bypass legacy hérité du TP 1c.

</details>

<details>
<summary><strong>4.2 Vérifier que `.env` correspond à Terraform</strong></summary>

Comparez avec :

```bash
cd terraform
terraform output
cd ..
```

Les valeurs doivent correspondre.

Exemple :

```text
terraform output s3_bucket_name
```

doit correspondre à :

```env
S3_BUCKET_NAME=...
```

</details>

<details>
<summary><strong>4.3 Mettre à jour `.env.example`</strong></summary>

Dans `.env.example`, mettez les mêmes variables (aucun secret n'est requis dans cette version `c`) :

```env
LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1
DEBUG=1
PERSISTENCE=1
LOCALSTACK_DOCKER_NAME=localstack-main
LOCALSTACK_VOLUME_DIR=./volume

LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test

S3_BUCKET_NAME=tp-localstack-dev-documents
DYNAMODB_TABLE_NAME=tp-localstack-dev-students
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-5"></a>

## Partie V — Créer `requirements.txt`

<details>
<summary><strong>5.1 Créer le fichier</strong></summary>

À la racine du projet :

```text
requirements.txt
```

</details>

<details>
<summary><strong>5.2 Contenu</strong></summary>

```text
streamlit
boto3
python-dotenv
pandas
requests
```

</details>

<details>
<summary><strong>5.3 Rôle des bibliothèques</strong></summary>

| Bibliothèque | Rôle |
|---|---|
| `streamlit` | Interface de validation |
| `boto3` | Communication avec LocalStack |
| `python-dotenv` | Lecture du fichier `.env` |
| `pandas` | Tableaux |
| `requests` | Test HTTP de LocalStack |

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-6"></a>

## Partie VI — Créer l’environnement Python

<details>
<summary><strong>6.1 Créer l’environnement</strong></summary>

```bash
python -m venv .venv
```

Sous Windows avec Python 3.12 :

```powershell
py -3.12 -m venv .venv
```

</details>

<details>
<summary><strong>6.2 Activer sous PowerShell</strong></summary>

```powershell
.venv\Scripts\Activate.ps1
```

Si PowerShell bloque :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis relancez l’activation.

</details>

<details>
<summary><strong>6.3 Activer sous Git Bash</strong></summary>

```bash
source .venv/Scripts/activate
```

</details>

<details>
<summary><strong>6.4 Activer sous Linux/macOS</strong></summary>

```bash
source .venv/bin/activate
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-7"></a>

## Partie VII — Installer les dépendances

<details>
<summary><strong>7.1 Mettre pip à jour</strong></summary>

```bash
python -m pip install --upgrade pip
```

</details>

<details>
<summary><strong>7.2 Installer</strong></summary>

```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><strong>7.3 Vérifier</strong></summary>

```bash
pip list
```

Vous devez voir :

```text
streamlit
boto3
python-dotenv
pandas
requests
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-8"></a>

## Partie VIII — Ajouter le fichier `app.py`

<details>
<summary><strong>8.1 Placer le fichier</strong></summary>

Placez le fichier fourni :

```text
app.py
```

à la racine du projet :

```text
terraform-localstack-debutant/app.py
```

</details>

<details>
<summary><strong>8.2 Ce que contient l’application</strong></summary>

L’application contient :

```text
Dashboard
Terraform outputs
S3 — Ressource Terraform
DynamoDB — Ressource Terraform
À propos
```

Le point important est la page :

```text
Terraform outputs
```

Elle lit les outputs Terraform et compare avec `.env`.

</details>

<details>
<summary><strong>8.3 Pourquoi cette page est importante ?</strong></summary>

Elle montre clairement que Streamlit n’invente pas les noms des ressources.

L’application doit utiliser les ressources déclarées par Terraform.

Si `.env` ne correspond pas aux outputs Terraform, l’application le signale.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-9"></a>

## Partie IX — Lancer Streamlit

<details>
<summary><strong>9.1 Lancer</strong></summary>

À la racine du projet :

```bash
streamlit run app.py
```

</details>

<details>
<summary><strong>9.2 Ouvrir</strong></summary>

Ouvrez :

```text
http://localhost:8501
```

</details>

<details>
<summary><strong>9.3 Vérifier le menu</strong></summary>

Vous devez voir :

```text
Dashboard
Terraform outputs
S3 — Ressource Terraform
DynamoDB — Ressource Terraform
À propos
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-10"></a>

## Partie X — Tester le Dashboard

<details>
<summary><strong>10.1 Tester LocalStack</strong></summary>

Cliquez sur :

```text
Tester LocalStack
```

Résultat attendu :

```text
LocalStack répond correctement.
```

</details>

<details>
<summary><strong>10.2 Tester S3</strong></summary>

Cliquez sur :

```text
Tester le bucket S3
```

Résultat attendu :

```text
Le bucket S3 existe et répond correctement.
```

</details>

<details>
<summary><strong>10.3 Tester DynamoDB</strong></summary>

Cliquez sur :

```text
Tester la table DynamoDB
```

Résultat attendu :

```text
La table DynamoDB existe et répond correctement.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-11"></a>

## Partie XI — Vérifier les outputs Terraform dans Streamlit

<details>
<summary><strong>11.1 Ouvrir la page Terraform outputs</strong></summary>

Dans le menu, cliquez sur :

```text
Terraform outputs
```

</details>

<details>
<summary><strong>11.2 Résultat attendu</strong></summary>

L’application exécute :

```bash
terraform -chdir=terraform output -json
```

Elle doit afficher les outputs Terraform.

Elle affiche ensuite une comparaison :

```text
Terraform output
VS
.env
```

</details>

<details>
<summary><strong>11.3 Interprétation</strong></summary>

Si tout est correct, vous devez voir :

```text
OK
```

pour le bucket et la table.

Si vous voyez :

```text
Différent
```

cela veut dire que `.env` ne correspond pas à l’infrastructure Terraform.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-12"></a>

## Partie XII — Tester S3

<details>
<summary><strong>12.1 Ouvrir la page S3</strong></summary>

Cliquez sur :

```text
S3 — Ressource Terraform
```

</details>

<details>
<summary><strong>12.2 Vérifier le bucket</strong></summary>

Cliquez sur :

```text
Vérifier que le bucket existe
```

</details>

<details>
<summary><strong>12.3 Envoyer un fichier</strong></summary>

Créez un fichier :

```text
test-terraform-dashboard.txt
```

Contenu :

```text
Ce fichier a été envoyé dans un bucket créé par Terraform.
```

Envoyez-le avec le bouton Streamlit.

</details>

<details>
<summary><strong>12.4 Vérifier avec AWS CLI</strong></summary>

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://tp-localstack-dev-documents/
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-13"></a>

## Partie XIII — Tester DynamoDB

<details>
<summary><strong>13.1 Ouvrir la page DynamoDB</strong></summary>

Cliquez sur :

```text
DynamoDB — Ressource Terraform
```

</details>

<details>
<summary><strong>13.2 Ajouter un étudiant</strong></summary>

Exemple :

```text
student_id : S001
first_name : Sara
last_name : Benali
program : Cloud Computing
```

</details>

<details>
<summary><strong>13.3 Vérifier dans le tableau</strong></summary>

Cliquez sur :

```text
Actualiser la liste des étudiants
```

L’étudiant doit apparaître.

</details>

<details>
<summary><strong>13.4 Vérifier avec AWS CLI</strong></summary>

```bash
aws --endpoint-url=http://localhost:4566 dynamodb scan \
  --table-name tp-localstack-dev-students
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-14"></a>

## Partie XIV — Exercices Terraform + Streamlit

> **Objectif :** montrer que Streamlit reflète les changements Terraform.

<details>
<summary><strong>Exercice 1 — Modifier le nom du projet</strong></summary>

Dans `terraform/variables.tf`, modifiez :

```hcl
default = "tp-localstack"
```

par :

```hcl
default = "tp-validation"
```

Puis exécutez :

```bash
cd terraform
terraform plan
terraform apply
terraform output
cd ..
```

Mettez à jour `.env` avec les nouveaux noms.

Relancez Streamlit.

Observez la page :

```text
Terraform outputs
```

</details>

<details>
<summary><strong>Exercice 2 — Ajouter un output Terraform</strong></summary>

Dans `outputs.tf`, ajoutez un output supplémentaire :

```hcl
output "environment_name" {
  value = var.environment
}
```

Puis :

```bash
terraform apply
terraform output
```

Objectif :

```text
comprendre comment Terraform expose des informations utiles aux autres outils.
```

</details>

<details>
<summary><strong>Exercice 3 — Casser volontairement .env</strong></summary>

Modifiez temporairement :

```env
S3_BUCKET_NAME=nom-faux
```

Relancez Streamlit.

Observez :

```text
la page Terraform outputs signale une différence ;
le test S3 échoue.
```

Remettez ensuite la bonne valeur.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-15"></a>

## Partie XV — Erreurs fréquentes

<details>
<summary><strong>Erreur 1 — Terraform outputs indisponibles</strong></summary>

Cause possible :

```text
terraform apply n’a pas été exécuté.
Terraform n’est pas installé.
Le dossier terraform n’existe pas.
```

Solution :

```bash
cd terraform
terraform init
terraform apply
terraform output
cd ..
```

</details>

<details>
<summary><strong>Erreur 2 — Bucket introuvable</strong></summary>

Cause possible :

```text
S3_BUCKET_NAME ne correspond pas à terraform output.
```

Solution :

```bash
cd terraform
terraform output
cd ..
```

Puis corrigez `.env`.

</details>

<details>
<summary><strong>Erreur 3 — Table DynamoDB introuvable</strong></summary>

Cause possible :

```text
DYNAMODB_TABLE_NAME ne correspond pas à terraform output.
```

Solution :

```bash
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

Puis corrigez `.env`.

</details>

<details>
<summary><strong>Erreur 4 — LocalStack arrêté</strong></summary>

Solution :

```bash
docker compose up -d
docker ps
```

</details>

<details>
<summary><strong>Erreur 5 — Module Python manquant</strong></summary>

Solution :

```bash
pip install -r requirements.txt
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-16"></a>

## Partie XVI — Questions de compréhension

1. Pourquoi ce TP reste-t-il un TP Terraform même si on utilise Streamlit ?
2. Quel est le rôle exact de Streamlit dans ce TP ?
3. Pourquoi Terraform est-il appelé la source de vérité de l’infrastructure ?
4. Pourquoi faut-il comparer `.env` avec `terraform output` ?
5. Que signifie `terraform output -json` ?
6. Pourquoi boto3 utilise-t-il `endpoint_url=http://localhost:4566` ?
7. Que se passe-t-il si `.env` contient un mauvais nom de bucket ?
8. Que se passe-t-il si Terraform n’a jamais créé la table DynamoDB ?
9. Quelle est la différence entre créer une ressource et valider une ressource ?
10. Pourquoi Streamlit ne doit-il pas créer le bucket dans ce TP ?
11. Que montre la page `Terraform outputs` ?
12. Que montre la page `S3 — Ressource Terraform` ?
13. Que montre la page `DynamoDB — Ressource Terraform` ?
14. Pourquoi est-il utile de vérifier aussi avec AWS CLI ?
15. Que signifie `terraform state list` ?
16. Pourquoi doit-on faire `terraform plan` avant `terraform apply` dans les exercices ?
17. Que faut-il faire après avoir changé le nom d’une ressource Terraform ?
18. Pourquoi un dashboard visuel aide-t-il les débutants ?
19. Quelle amélioration pourrait être ajoutée au dashboard ?
20. Comment ce TP prépare-t-il à une vraie architecture cloud ?

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-17"></a>

## Partie XVII — Mini-rapport à remettre

## Informations générales

```text
Nom :
Date :
Système d’exploitation :
Version Terraform :
Version Python :
Version Streamlit :
Endpoint LocalStack :
Nom du bucket S3 :
Nom de la table DynamoDB :
```

## Captures demandées

```text
1. docker ps montrant localstack-main.
2. terraform state list.
3. terraform output.
4. fichier .env.example.
5. streamlit run app.py.
6. page Dashboard avec tests réussis.
7. page Terraform outputs avec comparaison OK.
8. page S3 avec fichier envoyé.
9. vérification AWS CLI du fichier S3.
10. page DynamoDB avec étudiant ajouté.
11. vérification AWS CLI de DynamoDB.
12. exercice avec modification d’une variable Terraform.
```

## Questions à intégrer au rapport

```text
1. Expliquez pourquoi Terraform reste la source de vérité.
2. Expliquez le rôle de Streamlit dans ce TP.
3. Expliquez comment les outputs Terraform sont utilisés.
4. Expliquez une erreur rencontrée et sa correction.
5. Expliquez comment ce TP vous aide à mieux comprendre Terraform.
```

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="corrige"></a>

## Corrigé / Indications

<details>
<summary><strong>Indication 1 — Pourquoi ce TP reste orienté Terraform ?</strong></summary>

Parce que les ressources affichées dans Streamlit doivent être créées par Terraform. Streamlit ne remplace pas Terraform, il valide visuellement ce que Terraform a créé.

</details>

<details>
<summary><strong>Indication 2 — Pourquoi comparer `.env` et `terraform output` ?</strong></summary>

Parce que `.env` configure l’application. Si `.env` contient des noms différents de ceux créés par Terraform, l’application risque de chercher des ressources inexistantes.

</details>

<details>
<summary><strong>Indication 3 — Pourquoi `terraform output -json` ?</strong></summary>

La sortie JSON permet à un programme comme Streamlit de lire les outputs Terraform automatiquement.

</details>

<details>
<summary><strong>Indication 4 — Pourquoi boto3 ?</strong></summary>

boto3 permet à Python d’appeler S3 et DynamoDB. Ici, grâce à `endpoint_url`, il appelle LocalStack au lieu d’AWS réel.

</details>

---

## Score final

| Partie | Note obtenue | Note maximale |
|---|---:|---:|
| Rôle du dashboard | | 10 |
| LocalStack | | 10 |
| Outputs Terraform | | 15 |
| `.env` | | 15 |
| Environnement Python | | 15 |
| Dépendances | | 10 |
| Application Streamlit | | 10 |
| Comparaison outputs/.env | | 25 |
| Validation S3 | | 25 |
| Validation DynamoDB | | 25 |
| Explication Terraform | | 20 |
| Rapport | | 20 |
| **TOTAL** | | **200** |

---

*Fin du TP 2 — Dashboard Streamlit pour valider les ressources créées avec Terraform.*
