<a id="top"></a>

# TP 3 (version `c`) — Ajouter une file SQS avec Terraform et la valider dans Streamlit (sans token)

> **Version `c` — sans compte ni token.** Cette version suppose que vous avez fait les TPs 1c et 2c (bypass `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1`). Sinon, basculez sur [`03b-...md`](03b-Chapitre3-Pratique-03-ajouter-sqs-terraform-validation-streamlit.md).
>
> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, basculez sur la version `b`.
>
> **Cours visé :** Terraform, Infrastructure as Code, LocalStack, SQS, Streamlit, validation d'infrastructure  
>
> **Niveau :** Débutant avancé  
>
> **Prérequis :** les TPs 1 et 2 (version `c`) doivent être réalisés. Le projet contient déjà S3, DynamoDB, des variables Terraform, des outputs et un dashboard Streamlit.  
>
> **Objectif principal :** apprendre à ajouter une nouvelle ressource AWS simulée avec Terraform, ici une file SQS, puis la valider visuellement dans Streamlit.  
>
> **Important :** Streamlit reste obligatoire dans la progression, mais il reste un outil de validation. Le cœur du TP est Terraform : ajouter une ressource, lire le plan, appliquer, exposer les outputs, puis vérifier dans le dashboard.  
>
> **Ressource ajoutée :** Amazon SQS simulé dans LocalStack  
>
> **Ressources déjà présentes :** S3, DynamoDB  
>
> **Outils utilisés :** Terraform, LocalStack, Docker Compose, AWS CLI, Python, Streamlit, boto3  
>
> **Durée recommandée :** 3 à 5 heures  
>
> **Livrables :** fichiers Terraform modifiés, dashboard Streamlit mis à jour, captures d’écran, mini-rapport.

---

## À lire avant de commencer

Dans les TP précédents, vous avez créé une infrastructure locale avec Terraform et LocalStack.

Vous avez déjà :

```text
un bucket S3 ;
une table DynamoDB ;
des variables Terraform ;
des outputs Terraform ;
un dashboard Streamlit de validation.
```

Dans ce TP, vous allez ajouter une nouvelle ressource :

```text
une file SQS
```

Puis vous allez modifier Streamlit pour voir et manipuler cette file.

Le principe reste le même :

```text
Terraform crée la ressource.
terraform output expose la ressource.
.env configure l’application.
Streamlit valide la ressource.
```

Phrase à retenir :

```text
Chaque nouvelle ressource Terraform doit être visible dans le dashboard Streamlit.
```

---

## Pourquoi ajouter SQS ?

SQS est un service de file de messages.

Une file de messages permet de découpler des composants.

Exemple simple :

```text
Une application envoie un message.
Le message attend dans la file.
Une autre application peut le lire plus tard.
```

Dans ce TP, l’objectif n’est pas d’étudier SQS en profondeur.

L’objectif est de comprendre comment ajouter une nouvelle ressource Terraform et la valider.

---

## Architecture avant le TP

```text
Terraform
   |
   +--> S3
   |
   +--> DynamoDB
```

Streamlit valide :

```text
S3
DynamoDB
```

---

## Architecture après le TP

```text
Terraform
   |
   +--> S3
   |
   +--> DynamoDB
   |
   +--> SQS
```

Streamlit valide :

```text
S3
DynamoDB
SQS
```

---

## Ce que l’application Streamlit devra permettre

La nouvelle page SQS devra permettre de :

```text
vérifier que la file SQS existe ;
envoyer un message dans la file ;
lire les messages disponibles ;
supprimer un message lu ;
voir les outputs Terraform liés à SQS.
```

---

## Barème proposé

| Partie | Travail demandé | Points |
|---|---|---:|
| **I** | Comprendre le rôle de SQS | 10 |
| **II** | Ajouter l’endpoint SQS dans le provider | 15 |
| **III** | Ajouter la ressource SQS dans `main.tf` | 25 |
| **IV** | Ajouter les outputs SQS | 20 |
| **V** | Exécuter `terraform fmt`, `validate`, `plan` | 25 |
| **VI** | Interpréter le plan Terraform | 20 |
| **VII** | Appliquer avec `terraform apply` | 15 |
| **VIII** | Vérifier SQS avec AWS CLI | 20 |
| **IX** | Mettre à jour `.env` | 15 |
| **X** | Mettre à jour Streamlit | 35 |
| **XI** | Tester SQS dans Streamlit | 30 |
| **XII** | Questions et mini-rapport | 25 |
| | **TOTAL** | **255 pts** |

---

## Table des matières

| # | Section |
|---|---|
| 1 | [Partie I — Comprendre SQS](#partie-1) |
| 2 | [Partie II — Vérifier l’état initial](#partie-2) |
| 3 | [Partie III — Ajouter l’endpoint SQS au provider Terraform](#partie-3) |
| 4 | [Partie IV — Ajouter la ressource SQS dans `main.tf`](#partie-4) |
| 5 | [Partie V — Ajouter les outputs SQS](#partie-5) |
| 6 | [Partie VI — Exécuter `terraform fmt` et `validate`](#partie-6) |
| 7 | [Partie VII — Lire `terraform plan`](#partie-7) |
| 8 | [Partie VIII — Appliquer avec `terraform apply`](#partie-8) |
| 9 | [Partie IX — Vérifier SQS avec AWS CLI](#partie-9) |
| 10 | [Partie X — Mettre à jour `.env`](#partie-10) |
| 11 | [Partie XI — Mettre à jour Streamlit](#partie-11) |
| 12 | [Partie XII — Tester SQS dans Streamlit](#partie-12) |
| 13 | [Partie XIII — Exercices Terraform + Streamlit](#partie-13) |
| 14 | [Partie XIV — Erreurs fréquentes](#partie-14) |
| 15 | [Partie XV — Questions de compréhension](#partie-15) |
| 16 | [Partie XVI — Mini-rapport à remettre](#partie-16) |
| 17 | [Corrigé / Indications](#corrige) |

---

<a id="partie-1"></a>

## Partie I — Comprendre SQS

<details>
<summary><strong>1.1 C’est quoi SQS ?</strong></summary>

SQS signifie :

```text
Simple Queue Service
```

C’est un service AWS qui permet de stocker temporairement des messages dans une file.

Une file fonctionne comme une file d’attente.

Exemple :

```text
Message 1
Message 2
Message 3
```

Les messages attendent dans la file jusqu’à ce qu’une application les lise.

</details>

<details>
<summary><strong>1.2 Pourquoi utiliser une file de messages ?</strong></summary>

Une file de messages permet de séparer deux parties d’un système.

Exemple :

```text
Application A envoie un message.
Application B lit le message plus tard.
```

Cela permet :

```text
de découpler les composants ;
d’absorber des pics de charge ;
de ne pas perdre immédiatement les demandes ;
de traiter les messages progressivement.
```

</details>

<details>
<summary><strong>1.3 Ce que nous allons faire dans ce TP</strong></summary>

Nous allons créer une file SQS avec Terraform.

Ensuite, Streamlit permettra de :

```text
tester la file ;
envoyer un message ;
lire les messages ;
supprimer un message.
```

Mais la création de la file reste la responsabilité de Terraform.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-2"></a>

## Partie II — Vérifier l’état initial

<details>
<summary><strong>2.1 Démarrer LocalStack</strong></summary>

À la racine du projet :

```bash
docker compose up -d
docker ps
```

Vous devez voir :

```text
localstack-main
```

</details>

<details>
<summary><strong>2.2 Vérifier les ressources actuelles</strong></summary>

```bash
cd terraform
terraform state list
cd ..
```

Vous devez déjà voir :

```text
aws_s3_bucket.documents
aws_dynamodb_table.students
```

Après ce TP, vous devrez aussi voir :

```text
aws_sqs_queue.notifications
```

</details>

<details>
<summary><strong>2.3 Lire les outputs actuels</strong></summary>

```bash
cd terraform
terraform output
cd ..
```

Notez les outputs actuels avant modification.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-3"></a>

## Partie III — Ajouter l’endpoint SQS au provider Terraform

<details>
<summary><strong>3.1 Ouvrir `provider.tf`</strong></summary>

Ouvrez :

```text
terraform/provider.tf
```

Dans le bloc `endpoints`, vous avez déjà probablement :

```hcl
endpoints {
  s3       = "http://localhost:4566"
  dynamodb = "http://localhost:4566"
  iam      = "http://localhost:4566"
  sts      = "http://localhost:4566"
}
```

</details>

<details>
<summary><strong>3.2 Ajouter sqs</strong></summary>

Ajoutez :

```hcl
sqs = "http://localhost:4566"
```

Le bloc devient :

```hcl
endpoints {
  s3       = "http://localhost:4566"
  dynamodb = "http://localhost:4566"
  sqs      = "http://localhost:4566"
  iam      = "http://localhost:4566"
  sts      = "http://localhost:4566"
}
```

</details>

<details>
<summary><strong>3.3 Pourquoi ajouter cet endpoint ?</strong></summary>

Terraform utilise le provider AWS.

Sans endpoint SQS, Terraform pourrait ne pas envoyer les appels SQS vers LocalStack.

L’objectif est toujours :

```text
ne pas appeler AWS réel ;
appeler LocalStack.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-4"></a>

## Partie IV — Ajouter la ressource SQS dans `main.tf`

<details>
<summary><strong>4.1 Ouvrir `main.tf`</strong></summary>

Ouvrez :

```text
terraform/main.tf
```

Vous avez déjà le bucket S3 et la table DynamoDB.

</details>

<details>
<summary><strong>4.2 Ajouter la file SQS</strong></summary>

Ajoutez à la fin du fichier :

```hcl
resource "aws_sqs_queue" "notifications" {
  name = "${var.project_name}-${var.environment}-notifications"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
  }
}
```

</details>

<details>
<summary><strong>4.3 Explication du bloc</strong></summary>

```hcl
resource "aws_sqs_queue" "notifications"
```

signifie :

```text
Créer une file SQS.
Dans Terraform, son nom local est notifications.
```

La ligne :

```hcl
name = "${var.project_name}-${var.environment}-notifications"
```

construit un nom automatiquement.

Exemple :

```text
tp-validation-dev-notifications
```

</details>

<details>
<summary><strong>4.4 Pourquoi utiliser les mêmes variables ?</strong></summary>

On utilise :

```text
project_name
environment
owner_name
```

pour garder une convention cohérente.

Ainsi, toutes les ressources suivent la même logique :

```text
tp-validation-dev-documents
tp-validation-dev-students
tp-validation-dev-notifications
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-5"></a>

## Partie V — Ajouter les outputs SQS

<details>
<summary><strong>5.1 Ouvrir `outputs.tf`</strong></summary>

Ouvrez :

```text
terraform/outputs.tf
```

</details>

<details>
<summary><strong>5.2 Ajouter le nom de la file</strong></summary>

Ajoutez :

```hcl
output "sqs_queue_name" {
  description = "Nom de la file SQS créée dans LocalStack"
  value       = aws_sqs_queue.notifications.name
}
```

</details>

<details>
<summary><strong>5.3 Ajouter l’URL de la file</strong></summary>

Ajoutez aussi :

```hcl
output "sqs_queue_url" {
  description = "URL de la file SQS créée dans LocalStack"
  value       = aws_sqs_queue.notifications.url
}
```

</details>

<details>
<summary><strong>5.4 Pourquoi l’URL est importante ?</strong></summary>

Pour SQS, le nom de la file n’est pas toujours suffisant.

Pour envoyer ou recevoir des messages, AWS CLI et boto3 utilisent souvent l’URL de la file.

C’est pour cela qu’on expose :

```text
sqs_queue_url
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-6"></a>

## Partie VI — Exécuter `terraform fmt` et `validate`

<details>
<summary><strong>6.1 Formater</strong></summary>

```bash
cd terraform
terraform fmt
```

</details>

<details>
<summary><strong>6.2 Valider</strong></summary>

```bash
terraform validate
```

Résultat attendu :

```text
Success! The configuration is valid.
```

</details>

<details>
<summary><strong>6.3 Ne continuez pas si validate échoue</strong></summary>

Si `terraform validate` échoue, ne faites pas `apply`.

Corrigez d’abord :

```text
les accolades ;
les guillemets ;
les noms de variables ;
les blocs mal fermés.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-7"></a>

## Partie VII — Lire `terraform plan`

<details>
<summary><strong>7.1 Exécuter le plan</strong></summary>

```bash
terraform plan
```

</details>

<details>
<summary><strong>7.2 Résultat attendu</strong></summary>

Terraform doit proposer d’ajouter une ressource :

```text
Plan: 1 to add, 0 to change, 0 to destroy.
```

La ressource ajoutée doit être :

```text
aws_sqs_queue.notifications
```

</details>

<details>
<summary><strong>7.3 Interpréter</strong></summary>

Si Terraform propose aussi de détruire S3 ou DynamoDB, arrêtez-vous.

Cela signifie que d’autres changements ont été faits.

Question à poser :

```text
Ai-je changé project_name ?
Ai-je changé environment ?
Ai-je modifié les noms de ressources existantes ?
```

</details>

<details>
<summary><strong>7.4 Capture demandée</strong></summary>

Prenez une capture du plan montrant :

```text
aws_sqs_queue.notifications
Plan: 1 to add
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-8"></a>

## Partie VIII — Appliquer avec `terraform apply`

<details>
<summary><strong>8.1 Appliquer</strong></summary>

```bash
terraform apply
```

Répondez :

```text
yes
```

</details>

<details>
<summary><strong>8.2 Résultat attendu</strong></summary>

Vous devez voir :

```text
Apply complete!
```

Puis :

```bash
terraform state list
```

doit afficher :

```text
aws_sqs_queue.notifications
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-9"></a>

## Partie IX — Vérifier SQS avec AWS CLI

<details>
<summary><strong>9.1 Lister les files SQS</strong></summary>

```bash
aws --endpoint-url=http://localhost:4566 sqs list-queues
```

Vous devez voir l’URL de la file.

</details>

<details>
<summary><strong>9.2 Lire les outputs Terraform</strong></summary>

```bash
terraform output
```

Vous devez voir :

```text
sqs_queue_name
sqs_queue_url
```

</details>

<details>
<summary><strong>9.3 Envoyer un message avec AWS CLI</strong></summary>

Remplacez l’URL par celle de votre output :

```bash
aws --endpoint-url=http://localhost:4566 sqs send-message \
  --queue-url "COLLER_ICI_SQS_QUEUE_URL" \
  --message-body "Message envoyé depuis AWS CLI dans une file créée par Terraform"
```

PowerShell :

```powershell
aws --endpoint-url=http://localhost:4566 sqs send-message `
  --queue-url "COLLER_ICI_SQS_QUEUE_URL" `
  --message-body "Message envoyé depuis AWS CLI dans une file créée par Terraform"
```

</details>

<details>
<summary><strong>9.4 Lire un message avec AWS CLI</strong></summary>

```bash
aws --endpoint-url=http://localhost:4566 sqs receive-message \
  --queue-url "COLLER_ICI_SQS_QUEUE_URL"
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-10"></a>

## Partie X — Mettre à jour `.env`

<details>
<summary><strong>10.1 Ajouter les variables SQS</strong></summary>

À la racine, ouvrez `.env`.

Ajoutez :

```env
SQS_QUEUE_NAME=tp-validation-dev-notifications
SQS_QUEUE_URL=COLLER_ICI_L_OUTPUT_sqs_queue_url
```

La valeur exacte de `SQS_QUEUE_URL` vient de :

```bash
cd terraform
terraform output
```

</details>

<details>
<summary><strong>10.2 Mettre à jour `.env.example`</strong></summary>

Ajoutez aussi dans `.env.example` :

```env
SQS_QUEUE_NAME=tp-validation-dev-notifications
SQS_QUEUE_URL=http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/tp-validation-dev-notifications
```

</details>

<details>
<summary><strong>10.3 Pourquoi mettre l’URL dans `.env` ?</strong></summary>

boto3 peut retrouver une file par son nom.

Mais l’URL est directement utilisée pour :

```text
envoyer un message ;
recevoir un message ;
supprimer un message.
```

Il est donc utile de l’exposer.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-11"></a>

## Partie XI — Mettre à jour Streamlit

<details>
<summary><strong>11.1 Ajouter SQS dans le dashboard</strong></summary>

Le fichier `app.py` fourni avec ce TP contient déjà :

```text
une page SQS — Ressource Terraform ;
un test de la file SQS ;
l’envoi de messages ;
la lecture de messages ;
la suppression de messages.
```

Remplacez l’ancien `app.py` par celui fourni.

</details>

<details>
<summary><strong>11.2 Nouvelle page ajoutée</strong></summary>

Dans le menu Streamlit, vous devez voir :

```text
SQS — Ressource Terraform
```

</details>

<details>
<summary><strong>11.3 Nouvelle comparaison dans Terraform outputs</strong></summary>

La page :

```text
Terraform outputs
```

compare maintenant aussi :

```text
sqs_queue_name
sqs_queue_url
```

avec :

```text
SQS_QUEUE_NAME
SQS_QUEUE_URL
```

dans `.env`.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-12"></a>

## Partie XII — Tester SQS dans Streamlit

<details>
<summary><strong>12.1 Lancer Streamlit</strong></summary>

À la racine :

```bash
streamlit run app.py
```

</details>

<details>
<summary><strong>12.2 Vérifier la page Terraform outputs</strong></summary>

Ouvrez :

```text
Terraform outputs
```

Vous devez voir :

```text
File SQS = OK
URL SQS = OK
```

Si ce n’est pas le cas, corrigez `.env`.

</details>

<details>
<summary><strong>12.3 Ouvrir la page SQS</strong></summary>

Ouvrez :

```text
SQS — Ressource Terraform
```

Cliquez sur :

```text
Vérifier que la file SQS existe
```

Résultat attendu :

```text
La file SQS existe.
```

</details>

<details>
<summary><strong>12.4 Envoyer un message</strong></summary>

Dans la zone de texte, écrivez :

```text
Message envoyé depuis Streamlit dans une file créée par Terraform.
```

Cliquez sur :

```text
Envoyer le message dans SQS
```

</details>

<details>
<summary><strong>12.5 Lire le message</strong></summary>

Cliquez sur :

```text
Lire les messages SQS
```

Le message doit apparaître dans un tableau.

</details>

<details>
<summary><strong>12.6 Supprimer le message</strong></summary>

Sélectionnez le message lu.

Cliquez sur :

```text
Supprimer ce message
```

Relisez les messages pour vérifier qu’il n’apparaît plus.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-13"></a>

## Partie XIII — Exercices Terraform + Streamlit

<details>
<summary><strong>Exercice 1 — Changer le nom de la file SQS</strong></summary>

Modifiez le nom dans `main.tf` :

```hcl
name = "${var.project_name}-${var.environment}-events"
```

Exécutez :

```bash
terraform plan
```

Question :

```text
Terraform veut-il remplacer la file ?
Pourquoi ?
```

N’appliquez pas sans comprendre.

</details>

<details>
<summary><strong>Exercice 2 — Ajouter un output pédagogique</strong></summary>

Ajoutez :

```hcl
output "sqs_validation_message" {
  value = "La file SQS ${aws_sqs_queue.notifications.name} est gérée par Terraform"
}
```

Puis :

```bash
terraform apply
terraform output
```

Question :

```text
Pourquoi un output peut-il aider une application de validation ?
```

</details>

<details>
<summary><strong>Exercice 3 — Casser volontairement `.env`</strong></summary>

Mettez temporairement :

```env
SQS_QUEUE_NAME=nom-faux
```

Relancez Streamlit.

Observez :

```text
Terraform outputs
SQS — Ressource Terraform
```

Question :

```text
Comment l’erreur est-elle visible ?
```

Remettez ensuite la bonne valeur.

</details>

<details>
<summary><strong>Exercice 4 — Envoyer plusieurs messages</strong></summary>

Envoyez trois messages différents dans SQS.

Lisez-les dans Streamlit.

Question :

```text
Pourquoi une file de messages est-elle utile dans une architecture cloud ?
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-14"></a>

## Partie XIV — Erreurs fréquentes

<details>
<summary><strong>Erreur 1 — SQS non reconnu dans Terraform</strong></summary>

Vérifiez que le provider AWS est correctement installé :

```bash
terraform init
terraform validate
```

</details>

<details>
<summary><strong>Erreur 2 — SQS appelle AWS réel</strong></summary>

Vérifiez que le provider contient :

```hcl
sqs = "http://localhost:4566"
```

dans le bloc `endpoints`.

</details>

<details>
<summary><strong>Erreur 3 — QueueDoesNotExist</strong></summary>

Cause possible :

```text
La file n’a pas été créée.
Le nom de la file dans .env est incorrect.
L’URL de la file est incorrecte.
```

Solutions :

```bash
terraform output
aws --endpoint-url=http://localhost:4566 sqs list-queues
```

</details>

<details>
<summary><strong>Erreur 4 — Message lu mais pas supprimé</strong></summary>

Dans SQS, lire un message ne le supprime pas automatiquement.

Pour le supprimer, il faut utiliser le `ReceiptHandle`.

Streamlit le fait avec :

```text
delete_message
```

</details>

<details>
<summary><strong>Erreur 5 — `.env` pas à jour</strong></summary>

Après `terraform apply`, relisez :

```bash
terraform output
```

Puis mettez à jour :

```env
SQS_QUEUE_NAME
SQS_QUEUE_URL
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-15"></a>

## Partie XV — Questions de compréhension

1. Quel est l’objectif principal de ce TP ?
2. Pourquoi ce TP reste-t-il centré sur Terraform ?
3. Quel est le rôle de Streamlit dans ce TP ?
4. Quel service AWS simulé ajoute-t-on ?
5. À quoi sert SQS ?
6. Pourquoi faut-il ajouter `sqs` dans le bloc `endpoints` ?
7. Que fait `aws_sqs_queue.notifications` ?
8. Pourquoi utilise-t-on `var.project_name` et `var.environment` pour nommer la file ?
9. Pourquoi faut-il ajouter `sqs_queue_name` en output ?
10. Pourquoi faut-il ajouter `sqs_queue_url` en output ?
11. Pourquoi faut-il exécuter `terraform plan` avant `apply` ?
12. Que signifie `Plan: 1 to add` ?
13. Que faut-il faire si Terraform veut détruire S3 ou DynamoDB ?
14. Pourquoi faut-il mettre à jour `.env` après `terraform apply` ?
15. Pourquoi Streamlit compare-t-il `.env` avec `terraform output` ?
16. Quelle est la différence entre envoyer un message et lire un message ?
17. Pourquoi lire un message ne le supprime-t-il pas automatiquement ?
18. Pourquoi faut-il un `ReceiptHandle` pour supprimer un message ?
19. Pourquoi SQS est-il utile dans une architecture cloud ?
20. Comment ce TP renforce-t-il l’apprentissage de Terraform ?

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-16"></a>

## Partie XVI — Mini-rapport à remettre

## Informations générales

```text
Nom :
Date :
Groupe :
project_name :
environment :
Nom de la file SQS :
URL de la file SQS :
```

## Captures demandées

```text
1. provider.tf avec l’endpoint sqs.
2. main.tf avec aws_sqs_queue.notifications.
3. outputs.tf avec sqs_queue_name et sqs_queue_url.
4. terraform fmt.
5. terraform validate.
6. terraform plan montrant 1 ressource à ajouter.
7. terraform apply.
8. terraform state list montrant aws_sqs_queue.notifications.
9. terraform output montrant sqs_queue_name et sqs_queue_url.
10. aws sqs list-queues.
11. .env mis à jour.
12. Streamlit page Terraform outputs avec SQS OK.
13. Streamlit page SQS avec message envoyé.
14. Streamlit page SQS avec message lu.
15. Streamlit page SQS avec message supprimé.
```

## Questions à intégrer

```text
1. Expliquez ce que vous avez ajouté dans Terraform.
2. Expliquez pourquoi SQS est une ressource Terraform.
3. Expliquez comment Terraform expose l’URL SQS.
4. Expliquez comment Streamlit utilise cette URL.
5. Expliquez pourquoi Streamlit reste un outil de validation et non de création d’infrastructure.
```

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="corrige"></a>

## Corrigé / Indications

<details>
<summary><strong>Indication 1 — Ressource SQS</strong></summary>

La file SQS doit être déclarée avec `aws_sqs_queue`. Elle doit être créée par Terraform et visible ensuite dans LocalStack.

</details>

<details>
<summary><strong>Indication 2 — Endpoint SQS</strong></summary>

L’endpoint SQS permet au provider AWS de rediriger les appels SQS vers LocalStack au lieu d’AWS réel.

</details>

<details>
<summary><strong>Indication 3 — Outputs SQS</strong></summary>

`sqs_queue_name` permet de connaître le nom de la file. `sqs_queue_url` permet à AWS CLI, boto3 et Streamlit d’envoyer et lire des messages.

</details>

<details>
<summary><strong>Indication 4 — Streamlit</strong></summary>

Streamlit valide la file SQS créée avec Terraform. Il ne doit pas créer la file.

</details>

---

## Score final

| Partie | Note obtenue | Note maximale |
|---|---:|---:|
| Compréhension SQS | | 10 |
| Endpoint SQS | | 15 |
| Ressource SQS | | 25 |
| Outputs SQS | | 20 |
| fmt / validate / plan | | 25 |
| Interprétation plan | | 20 |
| apply | | 15 |
| AWS CLI | | 20 |
| `.env` | | 15 |
| Streamlit | | 35 |
| Tests SQS | | 30 |
| Rapport | | 25 |
| **TOTAL** | | **255** |

---

*Fin du TP 4 — Ajouter une file SQS avec Terraform et la valider dans Streamlit.*
