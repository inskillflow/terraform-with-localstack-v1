<a id="top"></a>

# TP guidé (version `c`) — Terraform avec LocalStack, Docker Compose et fichier `.env` (sans token)

> **Version `c` — sans compte ni token.** Cette version utilise le bypass officiel `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1` pour démarrer LocalStack **sans Auth Token**.
>
> **⚠️ Date butoir : 6 novembre 2026.** Après cette date, le bypass ne fonctionnera plus. Si vous lisez ce TP après le 6 nov. 2026, ouvrez plutôt [`01b-Chapitre1-Pratique-01-terraform-localstack.md`](01b-Chapitre1-Pratique-01-terraform-localstack.md) (version avec token Hobby/Student).

> **Cours visé :** Infrastructure as Code, Terraform, Docker, Docker Compose, LocalStack, simulation AWS locale  
>
> **Niveau :** Débutant complet  
>
> **Objectif :** apprendre à créer une infrastructure AWS simulée localement avec Terraform, sans utiliser un vrai compte AWS pour créer les ressources.  
>
> **Services AWS simulés dans ce TP :** Amazon S3 et Amazon DynamoDB  
>
> **Plan LocalStack utilisé :** image standard `localstack/localstack` en mode **bypass legacy** (variable `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1`). Aucun compte ni token requis, mais le bypass cesse de fonctionner après le **6 novembre 2026**.  
>
> **Outils utilisés :** Docker Desktop, Docker Compose, LocalStack, Terraform, AWS CLI, VS Code  
>
> **Durée recommandée :** 3 à 5 heures  
>
> **Mode de travail :** individuel ou en binôme  
>
> **Livrables :** dossier de projet complet, captures d’écran, réponses aux questions de compréhension, mini-rapport final.

---

## À lire avant de commencer

Ce TP est écrit pour des étudiants débutants. Il ne faut pas seulement copier-coller les commandes. Il faut comprendre ce que chaque commande fait, où elle doit être exécutée et quel résultat est attendu.

Dans ce TP, vous allez utiliser **Terraform** pour créer des ressources AWS, mais ces ressources ne seront pas créées dans AWS réel. Elles seront créées dans **LocalStack**, un environnement local qui simule AWS dans Docker.

Le principe général est le suivant :

```text
Votre ordinateur
   |
   v
Docker Desktop
   |
   v
Conteneur LocalStack
   |
   v
Services AWS simulés : S3, DynamoDB
```

Terraform va penser qu’il parle à AWS, mais en réalité il va parler à LocalStack sur cette adresse :

```text
http://localhost:4566
```

Le port `4566` est donc très important : c’est la porte d’entrée principale de LocalStack.

---

## Ce que vous allez construire

À la fin du TP, vous aurez un projet avec cette structure :

```text
terraform-localstack-debutant/
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
│
└── terraform/
    ├── provider.tf
    ├── variables.tf
    ├── main.tf
    └── outputs.tf
```

Et vous aurez créé localement :

```text
1 bucket S3
1 table DynamoDB
```

Ces ressources seront simulées par LocalStack. Elles ne seront pas créées dans AWS réel.

---

## Instructions générales

> **À lire attentivement**
>
> - Travaillez étape par étape.
> - Ne sautez pas les vérifications.
> - Cette version utilise le **bypass legacy** : aucun compte LocalStack n'est requis.
> - Le bypass est activé via la variable `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1` dans `.env`.
> - **Date butoir 6 novembre 2026** : après cette date, basculez sur la version `b` (avec token).
> - Les clés AWS utilisées dans ce TP sont fictives : `test` / `test`.
> - `.env` ne contient pas de secret dans cette version, mais on l'ignore quand même dans Git (bonne pratique pour la suite).
> - Vous devez toujours vérifier que LocalStack fonctionne avant de lancer Terraform.
> - Vous devez toujours faire `terraform plan` avant `terraform apply`.
> - À la fin, vous devez faire `terraform destroy`.

---

## Barème proposé

| Partie | Travail demandé | Points |
|---|---|---:|
| **I** | Comprendre les outils (Terraform, Docker, Docker Compose, LocalStack) | 10 |
| **II** | Vérifier les prérequis (Docker, Compose, Terraform, AWS CLI) | 10 |
| **III** | Comprendre le bypass legacy et ses limites | 5 |
| **IV** | Vérifier que l'image LocalStack se télécharge | 5 |
| **V** | Créer le dossier du projet | 5 |
| **VI** | Créer le fichier `.env` | 10 |
| **VII** | Créer `.env.example` | 5 |
| **VIII** | Créer `.gitignore` | 5 |
| **IX** | Créer `docker-compose.yml` | 15 |
| **X** | Vérifier la configuration Docker Compose (`docker compose config`) | 5 |
| **XI** | Démarrer LocalStack avec Docker Compose | 10 |
| **XII** | Vérifier que LocalStack fonctionne (HTTP `/info`) | 10 |
| **XIII** | Variante avec `docker pull` et `docker run` | 5 |
| **XIV** | Créer les fichiers Terraform (`provider`, `variables`, `main`, `outputs`) | 5 |
| **XV** | Comprendre `provider.tf` et le bloc `endpoints` | 10 |
| **XVI** | Créer les ressources S3 et DynamoDB en HCL | 15 |
| **XVII** | Exécuter Terraform (`init`, `fmt`, `validate`, `plan`, `apply`) | 15 |
| **XVIII** | Vérifier les ressources avec AWS CLI | 10 |
| **XIX** | Détruire l'infrastructure (`terraform destroy`, `docker compose down`) | 5 |
| **XX** | Identifier et résoudre les erreurs fréquentes | 5 |
| **XXI** | Répondre aux 20 questions de compréhension | 15 |
| **XXII** | Remettre le mini-rapport avec captures et synthèse | 20 |
| | **TOTAL** | **200 pts** |

---

## Table des matières

| # | Section |
|---|---|
| 1 | [Partie I — Comprendre les outils](#partie-1) |
| 2 | [Partie II — Vérifier les prérequis](#partie-2) |
| 3 | [Partie III — Comprendre le bypass legacy](#partie-3) |
| 4 | [Partie IV — Télécharger l'image LocalStack](#partie-4) |
| 5 | [Partie V — Créer le dossier du projet](#partie-5) |
| 6 | [Partie VI — Créer le fichier `.env`](#partie-6) |
| 7 | [Partie VII — Créer `.env.example`](#partie-7) |
| 8 | [Partie VIII — Créer `.gitignore`](#partie-8) |
| 9 | [Partie IX — Créer `docker-compose.yml`](#partie-9) |
| 10 | [Partie X — Vérifier la configuration Docker Compose](#partie-10) |
| 11 | [Partie XI — Démarrer LocalStack avec Docker Compose](#partie-11) |
| 12 | [Partie XII — Vérifier que LocalStack fonctionne](#partie-12) |
| 13 | [Partie XIII — Variante avec `docker pull` et `docker run`](#partie-13) |
| 14 | [Partie XIV — Créer les fichiers Terraform](#partie-14) |
| 15 | [Partie XV — Comprendre `provider.tf`](#partie-15) |
| 16 | [Partie XVI — Créer les ressources S3 et DynamoDB](#partie-16) |
| 17 | [Partie XVII — Exécuter Terraform](#partie-17) |
| 18 | [Partie XVIII — Vérifier avec AWS CLI](#partie-18) |
| 19 | [Partie XIX — Détruire l’infrastructure](#partie-19) |
| 20 | [Partie XX — Erreurs fréquentes](#partie-20) |
| 21 | [Partie XXI — Questions de compréhension](#partie-21) |
| 22 | [Partie XXII — Mini-rapport à remettre](#partie-22) |
| 23 | [Corrigé / Indications](#corrige) |

---

<a id="partie-1"></a>

## Partie I — Comprendre les outils

> **Objectif :** comprendre le rôle de Terraform, Docker, Docker Compose, LocalStack et AWS CLI avant d’exécuter les commandes.

<details>
<summary><strong>1.1 C’est quoi Terraform ?</strong></summary>

Terraform est un outil d’**Infrastructure as Code**.

Cela veut dire que vous décrivez l’infrastructure dans des fichiers texte au lieu de cliquer manuellement dans une interface web.

Exemple :

```hcl
resource "aws_s3_bucket" "documents" {
  bucket = "tp-localstack-documents"
}
```

Ce code veut dire :

```text
Je veux créer un bucket S3 nommé tp-localstack-documents.
```

Terraform lit les fichiers `.tf`, comprend ce que vous voulez créer, puis prépare un plan.

Les commandes principales sont :

| Commande | Rôle |
|---|---|
| `terraform init` | Prépare le projet Terraform |
| `terraform fmt` | Formate les fichiers Terraform |
| `terraform validate` | Vérifie la syntaxe |
| `terraform plan` | Montre ce qui va être créé |
| `terraform apply` | Crée les ressources |
| `terraform destroy` | Supprime les ressources |

</details>

<details>
<summary><strong>1.2 C’est quoi AWS dans ce TP ?</strong></summary>

AWS est une plateforme cloud.

Dans AWS réel, on peut créer :

```text
S3        -> stockage de fichiers
DynamoDB  -> base de données NoSQL
EC2       -> machines virtuelles
Lambda    -> fonctions serverless
SQS       -> files de messages
IAM       -> gestion des droits
```

Mais dans ce TP, on ne veut pas créer de vraies ressources dans AWS.

Pourquoi ?

```text
Parce que cela peut coûter de l’argent.
Parce que cela nécessite un vrai compte AWS.
Parce que les débutants peuvent se tromper.
Parce que la correction devient plus difficile.
```

On va donc utiliser LocalStack pour simuler AWS localement.

</details>

<details>
<summary><strong>1.3 C’est quoi LocalStack ?</strong></summary>

LocalStack est un outil qui simule des services AWS sur votre ordinateur.

Au lieu d’envoyer les commandes vers AWS réel, on les envoie vers :

```text
http://localhost:4566
```

Schéma :

```text
Terraform
   |
   | au lieu d’appeler AWS réel
   v
LocalStack
   |
   v
S3 local + DynamoDB local
```

Avantages :

```text
Pas de coût AWS.
Pas de vraie ressource cloud.
Plus facile à tester.
Plus facile à recommencer.
Plus sécuritaire pour apprendre.
```

</details>

<details>
<summary><strong>1.4 C’est quoi Docker ?</strong></summary>

Docker permet d’exécuter des applications dans des conteneurs.

Un conteneur est comme une petite boîte isolée qui contient une application et ce dont elle a besoin pour fonctionner.

Dans ce TP :

```text
Docker exécute LocalStack.
LocalStack simule AWS.
Terraform parle à LocalStack.
```

Donc Docker est indispensable pour démarrer LocalStack simplement.

</details>

<details>
<summary><strong>1.5 C’est quoi Docker Compose ?</strong></summary>

Docker Compose permet de décrire un conteneur dans un fichier `docker-compose.yml`.

Sans Docker Compose, il faudrait écrire une très longue commande `docker run`.

Avec Docker Compose, on écrit une configuration claire :

```yaml
services:
  localstack:
    image: localstack/localstack:latest
    ports:
      - "127.0.0.1:4566:4566"
```

Puis on démarre avec :

```bash
docker compose up -d
```

Docker Compose est plus pratique pour les étudiants parce que :

```text
Le fichier est lisible.
La configuration est réutilisable.
On évite les longues commandes difficiles.
On peut versionner le fichier dans Git.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-2"></a>

## Partie II — Vérifier les prérequis

> **Objectif :** vérifier que votre ordinateur est prêt avant de commencer.

<details>
<summary><strong>2.1 Ouvrir le terminal</strong></summary>

Selon votre système, ouvrez :

| Système | Terminal recommandé |
|---|---|
| Windows | PowerShell ou Windows Terminal |
| macOS | Terminal |
| Linux | Terminal |
| Windows avec Git | Git Bash possible |

Dans ce TP, les commandes seront principalement données en version :

```text
bash
```

et parfois en version :

```text
powershell
```

</details>

<details>
<summary><strong>2.2 Vérifier Docker</strong></summary>

Exécutez :

```bash
docker --version
```

Résultat attendu :

```text
Docker version XX.XX.X
```

Si vous obtenez :

```text
docker: command not found
```

ou :

```text
'docker' n’est pas reconnu
```

cela signifie que Docker n’est pas installé ou que Docker Desktop n’est pas démarré.

À faire :

```text
1. Installer Docker Desktop.
2. Ouvrir Docker Desktop.
3. Attendre que Docker soit démarré.
4. Relancer la commande.
```

</details>

<details>
<summary><strong>2.3 Vérifier Docker Compose</strong></summary>

Exécutez :

```bash
docker compose version
```

Résultat attendu :

```text
Docker Compose version vX.XX.X
```

Attention : la commande moderne est :

```bash
docker compose version
```

et non obligatoirement :

```bash
docker-compose version
```

Les deux peuvent fonctionner selon les installations, mais dans ce TP on utilise :

```bash
docker compose
```

</details>

<details>
<summary><strong>2.4 Vérifier Terraform</strong></summary>

Exécutez :

```bash
terraform version
```

Résultat attendu :

```text
Terraform v1.x.x
```

Si la commande ne fonctionne pas, installez Terraform avant de continuer.

</details>

<details>
<summary><strong>2.5 Vérifier AWS CLI</strong></summary>

Exécutez :

```bash
aws --version
```

Résultat attendu :

```text
aws-cli/2.x.x
```

AWS CLI est utilisé pour vérifier les ressources créées dans LocalStack.

Si AWS CLI n’est pas installé, vous pouvez quand même faire une partie du TP, mais la vérification S3 et DynamoDB sera plus difficile.

</details>

<details>
<summary><strong>2.6 Capture demandée</strong></summary>

Prenez une capture d’écran montrant les commandes suivantes et leurs résultats :

```bash
docker --version
docker compose version
terraform version
aws --version
```

Cette capture prouve que votre environnement est prêt.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-3"></a>

## Partie III — Comprendre le bypass legacy

> **Objectif :** comprendre ce qu'est le bypass legacy, pourquoi on l'utilise dans cette version, et pourquoi il est limité dans le temps.

<details>
<summary><strong>3.1 Le contexte 2026</strong></summary>

**Changement important du 23 mars 2026 :**

LocalStack a unifié sa distribution. L'ancienne édition « Community » sans token a été dépréciée. Désormais, **une seule image Docker** est distribuée, et elle exige normalement un **Auth Token** au démarrage.

**Mais** LocalStack a prévu une période de transition jusqu'au **6 novembre 2026** : il est possible de démarrer LocalStack sans compte ni token, en activant un **bypass** explicite.

</details>

<details>
<summary><strong>3.2 Qu'est-ce que le bypass exactement ?</strong></summary>

Le bypass est une **variable d'environnement** transmise au conteneur LocalStack :

```env
LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1
```

Quand LocalStack la voit, il démarre en mode « compatibilité Community » :

```text
+ Aucun compte LocalStack n'est requis.
+ Aucun Auth Token n'est requis.
+ Niveau de fonctionnalites equivalent au plan Hobby.
+ S3, DynamoDB, SQS, Lambda de base, etc.
```

Et il affiche un message d'avertissement dans les logs vous rappelant la date butoir.

</details>

<details>
<summary><strong>3.3 Date butoir : 6 novembre 2026</strong></summary>

```text
+--------------------------------------------------+
|                                                  |
|  Apres le 6 novembre 2026, le bypass cessera     |
|  de fonctionner. LocalStack refusera alors de    |
|  demarrer sans Auth Token.                       |
|                                                  |
+--------------------------------------------------+
```

Si vous lisez ce TP **après** cette date, basculez immédiatement sur la version `b` du TP : [`01b-Chapitre1-Pratique-01-terraform-localstack.md`](01b-Chapitre1-Pratique-01-terraform-localstack.md).

Le code Terraform y est identique. Seule la configuration LocalStack change (création de compte + token).

</details>

<details>
<summary><strong>3.4 Quels services AWS sont disponibles ?</strong></summary>

En mode bypass, vous avez accès aux mêmes services qu'avec le plan Hobby :

```text
S3        -> stockage de fichiers
DynamoDB  -> base de donnees NoSQL
SQS       -> files de messages
Lambda    -> fonctions serverless (de base)
IAM       -> gestion des droits (de base)
SNS, Kinesis, CloudWatch, etc.
```

C'est **largement suffisant** pour apprendre Terraform avec S3 et DynamoDB dans ce TP, et pour tout le parcours `c` (TPs 1c à 5c).

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-4"></a>

## Partie IV — Télécharger l'image LocalStack

> **Objectif :** vérifier que Docker peut télécharger l'image LocalStack avant de la configurer dans Docker Compose.

<details>
<summary><strong>4.1 Pourquoi télécharger l'image maintenant ?</strong></summary>

Quand on lancera `docker compose up -d`, Docker téléchargera automatiquement l'image. Mais il est plus pédagogique de séparer les deux étapes :

```text
1. Telecharger l'image manuellement -> on voit ce qui se passe.
2. Plus tard, demarrer avec docker compose -> tout est rapide.
```

Cela permet aussi de vérifier que Docker Desktop fonctionne et que la connexion à Docker Hub est correcte.

</details>

<details>
<summary><strong>4.2 Commande à exécuter</strong></summary>

Dans le terminal :

```bash
docker pull localstack/localstack:latest
```

Cette commande télécharge l'image unifiée LocalStack 2026 (même image que la version `b`, c'est le bypass qui change le comportement au démarrage).

Résultat attendu (extrait) :

```text
latest: Pulling from localstack/localstack
...
Status: Downloaded newer image for localstack/localstack:latest
docker.io/localstack/localstack:latest
```

</details>

<details>
<summary><strong>4.3 Vérifier que l'image est présente</strong></summary>

```bash
docker images localstack/localstack
```

Résultat attendu :

```text
REPOSITORY              TAG       IMAGE ID       CREATED       SIZE
localstack/localstack   latest    xxxxxxxxxxxx   x days ago    xxx MB
```

Si vous voyez cette ligne, l'image est bien sur votre ordinateur.

</details>

<details>
<summary><strong>4.4 Pourquoi pas d'auth token ?</strong></summary>

Dans la version `b`, on récupérerait ici un Auth Token sur `app.localstack.cloud`. Dans la version `c`, on saute cette étape : à la place, on activera le bypass `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1` dans `.env` à la Partie VI.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-5"></a>

## Partie V — Créer le dossier du projet

> **Objectif :** préparer une structure propre avant d’écrire les fichiers.

<details>
<summary><strong>5.1 Choisir l’emplacement du projet</strong></summary>

Choisissez un endroit simple, par exemple :

```text
Documents
Bureau
C:\Users\votre_nom\Documents
```

Évitez les dossiers avec des noms très longs ou des caractères spéciaux.

</details>

<details>
<summary><strong>5.2 Créer le dossier principal</strong></summary>

Dans le terminal, exécutez :

```bash
mkdir terraform-localstack-debutant
cd terraform-localstack-debutant
```

Explication :

```text
mkdir terraform-localstack-debutant
```

crée un dossier.

```text
cd terraform-localstack-debutant
```

entre dans ce dossier.

Vérifiez que vous êtes au bon endroit :

```bash
pwd
```

Sous PowerShell, vous pouvez aussi faire :

```powershell
Get-Location
```

</details>

<details>
<summary><strong>5.3 Créer le dossier terraform</strong></summary>

Exécutez :

```bash
mkdir terraform
```

Vérifiez :

```bash
ls
```

Sous PowerShell :

```powershell
dir
```

Vous devez voir :

```text
terraform
```

</details>

<details>
<summary><strong>5.4 Structure attendue à ce moment</strong></summary>

À ce stade, vous devez avoir :

```text
terraform-localstack-debutant/
└── terraform/
```

Si ce n’est pas le cas, ne continuez pas. Corrigez d’abord la structure.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-6"></a>

## Partie VI — Créer le fichier `.env`

> **Objectif :** créer le fichier qui contient les variables locales, dont la variable du bypass legacy.

<details>
<summary><strong>6.1 Créer le fichier dans VS Code</strong></summary>

Ouvrez le dossier dans VS Code :

```bash
code .
```

Si la commande `code .` ne fonctionne pas, ouvrez VS Code manuellement, puis faites :

```text
File
Open Folder
terraform-localstack-debutant
```

Dans VS Code :

```text
1. Clic droit dans la zone des fichiers.
2. New File.
3. Nommer le fichier : .env
```

Attention : le nom doit être exactement :

```text
.env
```

Il ne faut pas créer :

```text
env
.env.txt
env.txt
```

</details>

<details>
<summary><strong>6.2 Contenu du fichier .env</strong></summary>

Copiez ceci dans `.env` :

```env
LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1
DEBUG=1
PERSISTENCE=1
LOCALSTACK_DOCKER_NAME=localstack-main
LOCALSTACK_VOLUME_DIR=./volume
```

Aucun token n'est requis. La variable `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1` indique à LocalStack que vous savez qu'un compte sera requis après le 6 nov. 2026, et que vous acceptez de démarrer en mode bypass jusque-là.

> **Bonne pratique :** même si `.env` ne contient pas de secret dans ce TP, on l'ignore quand même dans Git (Partie VIII). Dans la suite du cours et dans tout projet réel, `.env` finira par contenir des secrets, donc autant prendre l'habitude.

</details>

<details>
<summary><strong>6.3 Explication ligne par ligne</strong></summary>

```env
LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1
```

Active le bypass legacy. **Sans cette ligne, LocalStack refuse de démarrer** car la nouvelle image exige normalement un Auth Token.

---

```env
DEBUG=1
```

Active des messages de diagnostic plus détaillés.

C'est utile pour apprendre et comprendre les erreurs.

---

```env
PERSISTENCE=1
```

Demande à LocalStack de garder certaines données localement.

---

```env
LOCALSTACK_DOCKER_NAME=localstack-main
```

Donne un nom clair au conteneur Docker.

---

```env
LOCALSTACK_VOLUME_DIR=./volume
```

Indique le dossier local utilisé pour stocker les données de LocalStack.

</details>

<details>
<summary><strong>6.4 Vérifier le fichier .env</strong></summary>

Dans le terminal, depuis la racine du projet :

```bash
ls -la
```

Sous PowerShell :

```powershell
dir -Force
```

Vous devez voir :

```text
.env
terraform
```

Si `.env` n’apparaît pas, il est peut-être mal nommé.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-7"></a>

## Partie VII — Créer `.env.example`

> **Objectif :** créer un modèle partageable sans secret.

<details>
<summary><strong>7.1 Pourquoi créer .env.example ?</strong></summary>

Le fichier `.env` est local et **ignoré par Git**. Mais les autres personnes qui clonent le projet doivent savoir **quelles variables sont nécessaires**.

On crée donc un modèle public :

```text
.env.example
```

Ce fichier liste les variables, avec des valeurs d'exemple ou par défaut. Quand une autre personne clone le projet, elle copie `.env.example` vers `.env`.

Dans cette version `c`, `.env` et `.env.example` peuvent même être identiques (aucun secret). C'est dans les TPs suivants ou un vrai projet que `.env` finira par diverger (clés API, mots de passe…).

</details>

<details>
<summary><strong>7.2 Créer le fichier</strong></summary>

Dans VS Code :

```text
1. New File
2. Nommer le fichier : .env.example
```

Copiez ceci :

```env
LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1
DEBUG=1
PERSISTENCE=1
LOCALSTACK_DOCKER_NAME=localstack-main
LOCALSTACK_VOLUME_DIR=./volume
```

</details>

<details>
<summary><strong>7.3 Différence entre .env et .env.example</strong></summary>

| Fichier | Peut contenir un secret ? | Peut être envoyé sur Git ? |
|---|---|---|
| `.env` | Oui (en général) | Non |
| `.env.example` | Non | Oui |

Règle à retenir :

```text
.env = fichier personnel local
.env.example = modele pour les autres
```

Dans cette version `c` du TP, ni `.env` ni `.env.example` ne contiennent de secret. On garde quand même les deux pour prendre la bonne habitude.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-8"></a>

## Partie VIII — Créer `.gitignore`

> **Objectif :** empêcher Git d’envoyer les secrets et fichiers temporaires.

<details>
<summary><strong>8.1 Créer le fichier .gitignore</strong></summary>

Dans VS Code :

```text
1. New File
2. Nommer le fichier : .gitignore
```

Copiez ceci :

```gitignore
.env
volume/

.terraform/
terraform/.terraform/
terraform/.terraform.lock.hcl

terraform/terraform.tfstate
terraform/terraform.tfstate.backup

*.log
```

</details>

<details>
<summary><strong>8.2 Pourquoi ignorer .env ?</strong></summary>

La ligne :

```gitignore
.env
```

empêche Git d'envoyer le fichier `.env`.

Dans cette version `c`, `.env` ne contient pas de secret. **Mais on prend dès maintenant la bonne habitude** : dans un vrai projet, et dans les TPs suivants, `.env` contient presque toujours :

```text
mot de passe de base de donnees
cle d'API externe
jeton d'authentification (LOCALSTACK_AUTH_TOKEN par exemple)
```

C'est pour cela que **tout** `.env` doit être ignoré par défaut.

</details>

<details>
<summary><strong>8.3 Pourquoi ignorer terraform.tfstate ?</strong></summary>

Terraform crée un fichier :

```text
terraform.tfstate
```

Ce fichier contient l’état de l’infrastructure.

Dans un vrai projet, ce fichier peut contenir des informations sensibles.

Dans ce TP, on l’ignore pour éviter de partager l’état local.

</details>

<details>
<summary><strong>8.4 Vérifier la structure après cette étape</strong></summary>

Vous devez avoir :

```text
terraform-localstack-debutant/
│
├── .env
├── .env.example
├── .gitignore
│
└── terraform/
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-9"></a>

## Partie IX — Créer `docker-compose.yml`

> **Objectif :** écrire la configuration qui démarre LocalStack dans Docker.

<details>
<summary><strong>9.1 Créer le fichier</strong></summary>

À la racine du projet, créez :

```text
docker-compose.yml
```

Attention : il doit être au même niveau que `.env`.

Structure correcte :

```text
terraform-localstack-debutant/
├── .env
├── docker-compose.yml
└── terraform/
```

Structure incorrecte :

```text
terraform-localstack-debutant/
├── .env
└── terraform/
    └── docker-compose.yml
```

</details>

<details>
<summary><strong>9.2 Contenu complet de docker-compose.yml</strong></summary>

Copiez ceci :

```yaml
services:
  localstack:
    container_name: ${LOCALSTACK_DOCKER_NAME:-localstack-main}
    image: localstack/localstack:latest

    ports:
      - "127.0.0.1:4566:4566"
      - "127.0.0.1:4510-4559:4510-4559"

    environment:
      - LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=${LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT:?Bypass legacy requis dans .env}
      - DEBUG=${DEBUG:-0}
      - PERSISTENCE=${PERSISTENCE:-1}

    volumes:
      - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
```

</details>

<details>
<summary><strong>9.3 Explication très simple du fichier</strong></summary>

```yaml
services:
```

On déclare les services à démarrer.

Ici, il y a un seul service :

```yaml
localstack:
```

Ce service correspond au conteneur LocalStack.

---

```yaml
container_name: ${LOCALSTACK_DOCKER_NAME:-localstack-main}
```

On donne un nom au conteneur.

Si `.env` contient :

```env
LOCALSTACK_DOCKER_NAME=localstack-main
```

alors le conteneur s’appellera :

```text
localstack-main
```

---

```yaml
image: localstack/localstack:latest
```

Docker va utiliser l'image unifiée LocalStack 2026. Au démarrage, elle exigerait normalement un Auth Token, mais le bypass legacy contourne cette exigence (jusqu'au 6 nov. 2026).

---

```yaml
ports:
  - "127.0.0.1:4566:4566"
```

Cette ligne expose le port `4566`.

Cela permet à Terraform et AWS CLI d'appeler :

```text
http://localhost:4566
```

---

```yaml
environment:
  - LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=${LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT:?Bypass legacy requis dans .env}
```

Cette ligne transmet le drapeau de bypass au conteneur. La syntaxe `${VAR:?message}` veut dire : « si `VAR` est absent, **refuse de démarrer** et affiche le message ». Cela évite qu'on lance LocalStack sans le bypass, ce qui produirait une erreur cryptique.

---

```yaml
  - DEBUG=${DEBUG:-0}
  - PERSISTENCE=${PERSISTENCE:-1}
```

Ces lignes transmettent les variables `DEBUG` et `PERSISTENCE` au conteneur. Si elles sont absentes du `.env`, des valeurs par défaut (`0` et `1`) sont utilisées.

---

```yaml
volumes:
  - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
```

Cette ligne connecte un dossier local à LocalStack pour stocker des données.

---

```yaml
- "/var/run/docker.sock:/var/run/docker.sock"
```

Cette ligne permet à LocalStack d’interagir avec Docker pour certains services.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-10"></a>

## Partie X — Vérifier la configuration Docker Compose

> **Objectif :** vérifier que Docker Compose lit correctement `.env`.

<details>
<summary><strong>10.1 Se placer au bon endroit</strong></summary>

Dans le terminal, vous devez être à la racine du projet :

```text
terraform-localstack-debutant/
```

Vérifiez avec :

```bash
pwd
```

ou sous PowerShell :

```powershell
Get-Location
```

Vous devez être dans le dossier qui contient :

```text
.env
docker-compose.yml
terraform/
```

</details>

<details>
<summary><strong>10.2 Lancer la vérification</strong></summary>

Exécutez :

```bash
docker compose config
```

Cette commande ne démarre pas encore LocalStack.

Elle vérifie seulement que le fichier `docker-compose.yml` est correct et que les variables sont remplacées.

</details>

<details>
<summary><strong>10.3 Résultat attendu</strong></summary>

Vous devez voir une configuration complète.

Vous devez voir par exemple :

```yaml
container_name: localstack-main
image: localstack/localstack:latest
```

Si vous voyez :

```text
Bypass legacy requis dans .env
```

cela signifie que Docker Compose ne trouve pas la variable de bypass. Vérifiez que :

```text
1. Le fichier .env existe.
2. Le fichier .env est au meme niveau que docker-compose.yml.
3. La ligne LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1 est presente dans .env.
4. La valeur est 1 (pas vide).
```

</details>

<details>
<summary><strong>10.4 Erreur fréquente : .env au mauvais endroit</strong></summary>

Correct :

```text
terraform-localstack-debutant/
├── .env
├── docker-compose.yml
└── terraform/
```

Incorrect :

```text
terraform-localstack-debutant/
├── docker-compose.yml
└── terraform/
    └── .env
```

Le fichier `.env` doit être à côté de `docker-compose.yml`.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-11"></a>

## Partie XI — Démarrer LocalStack avec Docker Compose

> **Objectif :** lancer LocalStack dans un conteneur Docker.

<details>
<summary><strong>11.1 Démarrer LocalStack</strong></summary>

Depuis la racine du projet, exécutez :

```bash
docker compose up -d
```

Explication :

```text
docker compose
```

utilise le fichier `docker-compose.yml`.

```text
up
```

démarre les services.

```text
-d
```

signifie "detached", donc en arrière-plan.

</details>

<details>
<summary><strong>11.2 Vérifier le conteneur</strong></summary>

Exécutez :

```bash
docker ps
```

Vous devez voir un conteneur avec le nom :

```text
localstack-main
```

Et une image :

```text
localstack/localstack:latest
```

</details>

<details>
<summary><strong>11.3 Lire les logs</strong></summary>

Exécutez :

```bash
docker logs -f localstack-main
```

Pour arrêter l’affichage des logs :

```text
CTRL + C
```

Cela n’arrête pas forcément le conteneur. Cela arrête seulement l’affichage des logs.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-12"></a>

## Partie XII — Vérifier que LocalStack fonctionne

> **Objectif :** confirmer que LocalStack répond correctement.

<details>
<summary><strong>12.1 Vérifier avec curl</strong></summary>

Exécutez :

```bash
curl http://localhost:4566/_localstack/info
```

Résultat attendu approximatif :

```json
{
  "edition": "community",
  "is_license_activated": false,
  "version": "x.y.z"
}
```

Le mot clé `community` confirme que vous êtes bien en mode bypass (équivalent fonctionnel du plan Hobby), sans token.

Si vous voyez `is_license_activated: true`, vous êtes en réalité sur la version `b` (avec token). Vérifiez votre `.env`.

</details>

<details>
<summary><strong>12.2 Vérifier avec PowerShell</strong></summary>

Si vous êtes sous PowerShell :

```powershell
Invoke-WebRequest -Uri http://localhost:4566/_localstack/info
```

Si PowerShell affiche beaucoup de texte, ce n’est pas forcément une erreur. L’important est que la requête réponde.

</details>

<details>
<summary><strong>12.3 Ce que cette vérification prouve</strong></summary>

Elle prouve que :

```text
Le conteneur LocalStack est demarre.
Le port 4566 fonctionne.
LocalStack repond aux requetes HTTP.
Le bypass legacy a ete accepte par LocalStack.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-13"></a>

## Partie XIII — Variante avec `docker pull` et `docker run`

> **Objectif :** comprendre la méthode manuelle sans Docker Compose.

<details>
<summary><strong>13.1 Vérifier que l'image est présente</strong></summary>

Vous avez déjà téléchargé l'image en Partie IV. Si vous avez sauté cette étape, exécutez-la maintenant :

```bash
docker pull localstack/localstack:latest
```

</details>

<details>
<summary><strong>13.2 Démarrer avec docker run</strong></summary>

Linux, macOS ou Git Bash :

```bash
docker run --rm -it \
  --name localstack-main \
  -p 127.0.0.1:4566:4566 \
  -p 127.0.0.1:4510-4559:4510-4559 \
  -e LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1 \
  -e DEBUG=1 \
  -e PERSISTENCE=1 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  localstack/localstack:latest
```

PowerShell :

```powershell
docker run --rm -it `
  --name localstack-main `
  -p 127.0.0.1:4566:4566 `
  -p 127.0.0.1:4510-4559:4510-4559 `
  -e LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1 `
  -e DEBUG=1 `
  -e PERSISTENCE=1 `
  -v /var/run/docker.sock:/var/run/docker.sock `
  localstack/localstack:latest
```

Aucun token n'est passé : le bypass est activé en clair.

</details>

<details>
<summary><strong>13.3 Pourquoi Docker Compose reste préférable ?</strong></summary>

Avec `docker run`, la commande est longue.

Avec Docker Compose, la configuration est dans un fichier.

Pour un TP débutant, Docker Compose est préférable parce que :

```text
Les etudiants voient la configuration.
Le professeur peut corriger plus facilement.
Les erreurs sont plus faciles a reperer.
Le projet est plus professionnel.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-14"></a>

## Partie XIV — Créer les fichiers Terraform

> **Objectif :** préparer les fichiers `.tf` qui décrivent l’infrastructure.

<details>
<summary><strong>14.1 Aller dans le dossier terraform</strong></summary>

Depuis la racine :

```bash
cd terraform
```

Vérifiez :

```bash
pwd
```

Vous devez être dans :

```text
terraform-localstack-debutant/terraform
```

</details>

<details>
<summary><strong>14.2 Créer les fichiers</strong></summary>

Créez ces fichiers :

```text
provider.tf
variables.tf
main.tf
outputs.tf
```

Dans VS Code, vous pouvez faire :

```text
Clic droit sur le dossier terraform
New File
provider.tf
```

Puis répéter pour les autres fichiers.

</details>

<details>
<summary><strong>14.3 Rôle de chaque fichier</strong></summary>

| Fichier | Rôle |
|---|---|
| `provider.tf` | Configure Terraform et AWS |
| `variables.tf` | Déclare les variables |
| `main.tf` | Déclare les ressources à créer |
| `outputs.tf` | Affiche les résultats utiles |

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-15"></a>

## Partie XV — Comprendre `provider.tf`

> **Objectif :** configurer Terraform pour parler à LocalStack au lieu d’AWS réel.

<details>
<summary><strong>15.1 Contenu complet de provider.tf</strong></summary>

Copiez ceci dans `terraform/provider.tf` :

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
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3       = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
    iam      = "http://localhost:4566"
    sts      = "http://localhost:4566"
  }
}
```

</details>

<details>
<summary><strong>15.2 Pourquoi access_key et secret_key valent test ?</strong></summary>

Dans AWS réel, il faudrait de vraies clés.

Mais ici, nous utilisons LocalStack.

Donc on utilise des valeurs fictives :

```hcl
access_key = "test"
secret_key = "test"
```

Ces valeurs ne donnent pas accès à AWS réel.

</details>

<details>
<summary><strong>15.3 Pourquoi le bloc endpoints est obligatoire ?</strong></summary>

Le bloc :

```hcl
endpoints {
  s3       = "http://localhost:4566"
  dynamodb = "http://localhost:4566"
}
```

dit à Terraform :

```text
Pour S3, ne va pas vers AWS réel.
Va vers LocalStack.

Pour DynamoDB, ne va pas vers AWS réel.
Va vers LocalStack.
```

Sans ce bloc, Terraform pourrait essayer d’appeler AWS réel.

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-16"></a>

## Partie XVI — Créer les ressources S3 et DynamoDB

> **Objectif :** écrire le code Terraform qui crée un bucket S3 et une table DynamoDB.

<details>
<summary><strong>16.1 Créer variables.tf</strong></summary>

Dans `terraform/variables.tf`, copiez :

```hcl
variable "project_name" {
  description = "Nom du projet utilisé pour nommer les ressources locales"
  type        = string
  default     = "tp-localstack"
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
  default     = "dev"
}
```

</details>

<details>
<summary><strong>16.2 Créer main.tf</strong></summary>

Dans `terraform/main.tf`, copiez :

```hcl
resource "aws_s3_bucket" "documents" {
  bucket = "${var.project_name}-${var.environment}-documents"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_dynamodb_table" "students" {
  name         = "${var.project_name}-${var.environment}-students"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "student_id"

  attribute {
    name = "student_id"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

</details>

<details>
<summary><strong>16.3 Créer outputs.tf</strong></summary>

Dans `terraform/outputs.tf`, copiez :

```hcl
output "s3_bucket_name" {
  description = "Nom du bucket S3 créé dans LocalStack"
  value       = aws_s3_bucket.documents.bucket
}

output "dynamodb_table_name" {
  description = "Nom de la table DynamoDB créée dans LocalStack"
  value       = aws_dynamodb_table.students.name
}

output "localstack_endpoint" {
  description = "Endpoint LocalStack utilisé par Terraform"
  value       = "http://localhost:4566"
}
```

</details>

<details>
<summary><strong>16.4 Noms des ressources attendues</strong></summary>

Avec les valeurs par défaut :

```hcl
project_name = "tp-localstack"
environment  = "dev"
```

Terraform créera :

```text
tp-localstack-dev-documents
tp-localstack-dev-students
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-17"></a>

## Partie XVII — Exécuter Terraform

> **Objectif :** initialiser, vérifier, planifier et appliquer l’infrastructure.

<details>
<summary><strong>17.1 Vérifier que LocalStack tourne</strong></summary>

Avant Terraform, vérifiez :

```bash
docker ps
```

Vous devez voir :

```text
localstack-main
```

Si LocalStack ne tourne pas :

```bash
cd ..
docker compose up -d
cd terraform
```

</details>

<details>
<summary><strong>17.2 Initialiser Terraform</strong></summary>

Dans le dossier `terraform/` :

```bash
terraform init
```

Résultat attendu :

```text
Terraform has been successfully initialized!
```

Cette commande télécharge le provider AWS.

</details>

<details>
<summary><strong>17.3 Formater les fichiers</strong></summary>

```bash
terraform fmt
```

Cette commande rend les fichiers `.tf` plus propres.

</details>

<details>
<summary><strong>17.4 Valider la syntaxe</strong></summary>

```bash
terraform validate
```

Résultat attendu :

```text
Success! The configuration is valid.
```

</details>

<details>
<summary><strong>17.5 Voir le plan</strong></summary>

```bash
terraform plan
```

Résultat attendu :

```text
Plan: 2 to add, 0 to change, 0 to destroy.
```

Cela signifie :

```text
Terraform va créer 2 ressources.
Il ne va rien modifier.
Il ne va rien supprimer.
```

</details>

<details>
<summary><strong>17.6 Appliquer</strong></summary>

```bash
terraform apply
```

Terraform demande :

```text
Do you want to perform these actions?
```

Répondez :

```text
yes
```

Résultat attendu :

```text
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-18"></a>

## Partie XVIII — Vérifier avec AWS CLI

> **Objectif :** confirmer que les ressources existent dans LocalStack.

<details>
<summary><strong>18.1 Configurer AWS CLI avec des valeurs fictives</strong></summary>

Exécutez :

```bash
aws configure
```

Répondez :

```text
AWS Access Key ID: test
AWS Secret Access Key: test
Default region name: us-east-1
Default output format: json
```

</details>

<details>
<summary><strong>18.2 Lister les buckets S3</strong></summary>

```bash
aws --endpoint-url=http://localhost:4566 s3 ls
```

Résultat attendu :

```text
tp-localstack-dev-documents
```

</details>

<details>
<summary><strong>18.3 Créer un fichier test</strong></summary>

Linux, macOS ou Git Bash :

```bash
echo "Bonjour LocalStack" > test.txt
```

PowerShell :

```powershell
"Bonjour LocalStack" | Out-File -FilePath test.txt -Encoding utf8
```

</details>

<details>
<summary><strong>18.4 Envoyer le fichier dans S3</strong></summary>

```bash
aws --endpoint-url=http://localhost:4566 s3 cp test.txt s3://tp-localstack-dev-documents/
```

Lister le contenu :

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://tp-localstack-dev-documents/
```

Résultat attendu :

```text
test.txt
```

</details>

<details>
<summary><strong>18.5 Lister les tables DynamoDB</strong></summary>

```bash
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

Résultat attendu :

```json
{
  "TableNames": [
    "tp-localstack-dev-students"
  ]
}
```

</details>

<details>
<summary><strong>18.6 Ajouter un étudiant dans DynamoDB</strong></summary>

Linux, macOS ou Git Bash :

```bash
aws --endpoint-url=http://localhost:4566 dynamodb put-item \
  --table-name tp-localstack-dev-students \
  --item '{"student_id":{"S":"S001"}}'
```

PowerShell :

```powershell
aws --endpoint-url=http://localhost:4566 dynamodb put-item `
  --table-name tp-localstack-dev-students `
  --item '{\"student_id\":{\"S\":\"S001\"}}'
```

Lire la table :

```bash
aws --endpoint-url=http://localhost:4566 dynamodb scan \
  --table-name tp-localstack-dev-students
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-19"></a>

## Partie XIX — Détruire l’infrastructure

> **Objectif :** supprimer proprement les ressources créées par Terraform.

<details>
<summary><strong>19.1 Détruire avec Terraform</strong></summary>

Dans le dossier `terraform/` :

```bash
terraform destroy
```

Répondez :

```text
yes
```

Résultat attendu :

```text
Destroy complete! Resources: 2 destroyed.
```

</details>

<details>
<summary><strong>19.2 Arrêter LocalStack</strong></summary>

Revenir à la racine :

```bash
cd ..
```

Arrêter LocalStack :

```bash
docker compose down
```

</details>

<details>
<summary><strong>19.3 Supprimer aussi les volumes</strong></summary>

Pour supprimer les données locales :

```bash
docker compose down -v
```

Attention :

```text
Cette commande supprime les données locales associées au conteneur.
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-20"></a>

## Partie XX — Erreurs fréquentes

<details>
<summary><strong>Erreur 1 — LocalStack refuse de démarrer sans token</strong></summary>

Message possible dans les logs :

```text
This image requires an authentication token...
```

ou Docker Compose qui affiche :

```text
Bypass legacy requis dans .env
```

Cause probable :

```text
La variable LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT n'est pas dans .env.
Le fichier .env n'est pas au meme niveau que docker-compose.yml.
La valeur du flag est vide (= au lieu de =1).
```

Vérifiez :

```bash
ls -la
```

ou PowerShell :

```powershell
dir -Force
```

Si l'erreur persiste, vérifiez le contenu de `.env` :

```bash
cat .env
```

Vous devez voir la ligne :

```env
LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1
```

</details>

<details>
<summary><strong>Erreur 1bis — Date butoir dépassée (après 6 nov. 2026)</strong></summary>

Si vous lisez ce TP après le **6 novembre 2026** et que LocalStack refuse de démarrer même avec le bypass, c'est que le bypass a expiré.

Solution : basculez sur la version `b` :
- Suivez [`01b-Chapitre1-Pratique-01-terraform-localstack.md`](01b-Chapitre1-Pratique-01-terraform-localstack.md).
- Créez un compte gratuit sur `app.localstack.cloud`.
- Récupérez un Auth Token.
- Mettez-le dans `.env` à la place de `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1`.

Le code Terraform reste identique.

</details>

<details>
<summary><strong>Erreur 1ter — Docker Desktop non démarré</strong></summary>

Message possible :

```text
error during connect: open //./pipe/docker_engine: ...
```

ou :

```text
Cannot connect to the Docker daemon
```

À faire :

```text
1. Ouvrir Docker Desktop manuellement.
2. Attendre que l'icone soit "running" (verte).
3. Relancer la commande.
```

Vérifiez ensuite :

```bash
docker info
```

</details>

<details>
<summary><strong>Erreur 2 — Port 4566 déjà utilisé</strong></summary>

Message possible :

```text
port is already allocated
```

Vérifiez :

```bash
docker ps
```

Arrêtez l’ancien conteneur :

```bash
docker stop localstack-main
```

Puis relancez :

```bash
docker compose up -d
```

</details>

<details>
<summary><strong>Erreur 3 — Terraform appelle AWS réel</strong></summary>

Cause probable :

```text
Le bloc endpoints est absent ou incorrect.
```

Vérifiez `provider.tf` :

```hcl
endpoints {
  s3       = "http://localhost:4566"
  dynamodb = "http://localhost:4566"
}
```

</details>

<details>
<summary><strong>Erreur 4 — AWS CLI demande des identifiants</strong></summary>

Exécutez :

```bash
aws configure
```

Répondez :

```text
test
test
us-east-1
json
```

</details>

<details>
<summary><strong>Erreur 5 — Bucket déjà existant</strong></summary>

Changez le nom dans `variables.tf` :

```hcl
default = "tp-localstack-votre-nom"
```

Puis relancez :

```bash
terraform plan
terraform apply
```

</details>

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-21"></a>

## Partie XXI — Questions de compréhension

> **Consigne :** répondez en 2 à 4 phrases par question.

1. Quel est le rôle de Terraform dans ce TP ?
2. Quel est le rôle de Docker ?
3. Quel est le rôle de Docker Compose ?
4. Quel est le rôle de LocalStack ?
5. Pourquoi ne crée-t-on pas directement les ressources dans AWS réel ?
6. Quel est le rôle du port `4566` ?
7. Qu'est-ce que le bypass legacy `LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1` et jusqu'à quand est-il valable ?
8. Pourquoi `.env` ne doit-il pas être envoyé sur GitHub, même quand il ne contient aucun secret dans cette version du TP ?
9. Quelle est la différence entre `.env` et `.env.example` ?
10. Pourquoi utilise-t-on `access_key = "test"` et `secret_key = "test"` ?
11. Pourquoi le bloc `endpoints` est-il indispensable ?
12. Que fait `terraform init` ?
13. Que fait `terraform plan` ?
14. Que fait `terraform apply` ?
15. Que fait `terraform destroy` ?
16. Quelle est la différence entre un bucket S3 et une table DynamoDB ?
17. Pourquoi AWS CLI doit-il utiliser `--endpoint-url=http://localhost:4566` ?
18. Pourquoi Docker Compose est-il plus pratique que `docker run` ?
19. Quelles erreurs peuvent arriver si `.env` est au mauvais endroit ?
20. Pourquoi faut-il nettoyer l’environnement à la fin ?

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="partie-22"></a>

## Partie XXII — Mini-rapport à remettre

> **Objectif :** documenter votre travail.

### Informations générales

```text
Nom :
Date :
Système d’exploitation :
Version Docker :
Version Docker Compose :
Version Terraform :
Version AWS CLI :
```

### Captures demandées

```text
1. Capture des versions : Docker, Docker Compose, Terraform, AWS CLI.
2. Capture du fichier .env.example.
3. Capture du fichier docker-compose.yml.
4. Capture de docker compose config.
5. Capture de docker ps montrant localstack-main.
6. Capture de la réponse de http://localhost:4566/_localstack/info.
7. Capture de terraform init.
8. Capture de terraform validate.
9. Capture de terraform plan.
10. Capture de terraform apply.
11. Capture de aws s3 ls.
12. Capture de aws dynamodb list-tables.
13. Capture de terraform destroy.
```

### Questions à intégrer dans le rapport

```text
1. Expliquez en vos mots ce que fait LocalStack.
2. Expliquez pourquoi Terraform doit être redirigé vers LocalStack.
3. Expliquez pourquoi le fichier .env est sensible.
4. Expliquez ce que vous avez créé avec Terraform.
5. Expliquez une erreur rencontrée et comment vous l’avez corrigée.
```

<p align="right"><a href="#top">↑ Retour en haut</a></p>

---

<a id="corrige"></a>

## Corrigé / Indications

> Une indication par question de la Partie XXI. Ce sont des **pistes de réponse**, pas des réponses complètes : vous devez reformuler avec vos propres mots dans le rapport.

<details>
<summary><strong>Q1 — Rôle de Terraform</strong></summary>

Terraform est un outil d'**Infrastructure as Code** : on décrit l'infrastructure dans des fichiers `.tf`, puis Terraform crée, modifie ou détruit les ressources de façon reproductible. Dans ce TP, Terraform décrit un bucket S3 et une table DynamoDB et les crée dans LocalStack.

</details>

<details>
<summary><strong>Q2 — Rôle de Docker</strong></summary>

Docker permet d'exécuter une application dans un **conteneur** isolé. Ici, Docker exécute LocalStack sans avoir à installer LocalStack directement sur le système. Le même conteneur fonctionne sur Windows, macOS et Linux.

</details>

<details>
<summary><strong>Q3 — Rôle de Docker Compose</strong></summary>

Docker Compose permet de décrire un ou plusieurs conteneurs dans un fichier `docker-compose.yml` lisible et versionnable. On évite la commande `docker run` longue et difficile à relire.

</details>

<details>
<summary><strong>Q4 — Rôle de LocalStack</strong></summary>

LocalStack **simule AWS localement**. Il imite les API de S3, DynamoDB et d'autres services, mais tout reste sur la machine de l'étudiant. Aucune ressource réelle n'est créée dans le cloud d'Amazon.

</details>

<details>
<summary><strong>Q5 — Pourquoi pas AWS réel ?</strong></summary>

Créer des ressources dans AWS réel coûte de l'argent, demande un compte payant et expose à des erreurs (clé exposée, ressource oubliée qui facture). LocalStack permet d'apprendre sans risque et sans coût.

</details>

<details>
<summary><strong>Q6 — Rôle du port 4566</strong></summary>

`4566` est la **porte d'entrée HTTP unique de LocalStack**. Terraform et AWS CLI envoient toutes leurs requêtes à `http://localhost:4566`, et LocalStack route en interne vers le service simulé (S3, DynamoDB, etc.).

</details>

<details>
<summary><strong>Q7 — Bypass legacy</strong></summary>

`LOCALSTACK_ACKNOWLEDGE_ACCOUNT_REQUIREMENT=1` est un drapeau officiel de LocalStack qui permet de démarrer le conteneur **sans Auth Token**. Il sert de période de transition entre l'ancien modèle (Community sans token) et le nouveau (image unifiée avec token obligatoire).

Le bypass est **valable jusqu'au 6 novembre 2026**. Après cette date, LocalStack refusera de démarrer sans token, et il faudra basculer sur le plan Hobby ou Student (version `b` du cours).

</details>

<details>
<summary><strong>Q8 — Pourquoi ignorer .env dans Git ?</strong></summary>

Dans cette version `c`, `.env` ne contient pas de secret. **Mais** on prend l'habitude tout de suite : dans un projet réel (et dans la version `b` de ce TP), `.env` contient toujours des mots de passe, des clés d'API ou des jetons (`LOCALSTACK_AUTH_TOKEN` par exemple). Un `.gitignore` qui inclut `.env` évite qu'un secret se retrouve par accident sur GitHub.

</details>

<details>
<summary><strong>Q9 — Différence `.env` vs `.env.example`</strong></summary>

`.env` est **personnel et local**, jamais commité. `.env.example` est un **modèle public** qui liste les variables attendues, avec des valeurs d'exemple non sensibles. Une autre personne qui clone le projet copie `.env.example` vers `.env` et complète.

</details>

<details>
<summary><strong>Q10 — Pourquoi `access_key = "test"` ?</strong></summary>

LocalStack accepte n'importe quelle valeur pour `access_key` et `secret_key` (par défaut `test` / `test`). Ces valeurs ne donnent aucun accès à AWS réel : elles servent juste à satisfaire le provider Terraform qui exige des champs renseignés.

</details>

<details>
<summary><strong>Q11 — Pourquoi le bloc `endpoints` ?</strong></summary>

Sans `endpoints`, le provider AWS de Terraform appelle les URLs officielles d'Amazon (`s3.amazonaws.com`, etc.) — donc le **vrai cloud**, avec un risque de coût ou d'erreur d'authentification. Le bloc `endpoints` force Terraform à envoyer toutes les requêtes à `http://localhost:4566`, c'est-à-dire à LocalStack.

</details>

<details>
<summary><strong>Q12 — Que fait `terraform init` ?</strong></summary>

`terraform init` **prépare le dossier** : il télécharge les providers déclarés (ici `hashicorp/aws`), crée le dossier `.terraform/` et le fichier `.terraform.lock.hcl`. À exécuter au moins une fois après avoir cloné un projet ou modifié les versions des providers.

</details>

<details>
<summary><strong>Q13 — Que fait `terraform plan` ?</strong></summary>

`terraform plan` **calcule la différence** entre l'état actuel de l'infrastructure (`terraform.tfstate`) et ce que décrivent les fichiers `.tf`. Il affiche les ressources à créer, modifier ou détruire, **sans rien appliquer**. C'est l'étape de revue.

</details>

<details>
<summary><strong>Q14 — Que fait `terraform apply` ?</strong></summary>

`terraform apply` **applique le plan** : il crée, modifie ou détruit réellement les ressources auprès du provider (ici LocalStack). Il demande une confirmation `yes` avant d'agir, sauf si on passe `-auto-approve`.

</details>

<details>
<summary><strong>Q15 — Que fait `terraform destroy` ?</strong></summary>

`terraform destroy` **supprime toutes les ressources gérées** par le projet Terraform courant. Il demande une confirmation `yes`. C'est l'inverse de `apply` et c'est essentiel pour ne pas laisser traîner des ressources (et donc des coûts, en AWS réel).

</details>

<details>
<summary><strong>Q16 — S3 vs DynamoDB</strong></summary>

- **S3** est un service de **stockage d'objets** (fichiers entiers : images, PDF, CSV…). On y dépose des objets dans des « buckets ».
- **DynamoDB** est une **base de données NoSQL** orientée clé-valeur et document. On y stocke des items avec une clé primaire et des attributs.

S3 = fichiers. DynamoDB = enregistrements structurés.

</details>

<details>
<summary><strong>Q17 — Pourquoi `--endpoint-url=http://localhost:4566` en AWS CLI ?</strong></summary>

Par défaut, AWS CLI parle au vrai AWS. L'option `--endpoint-url` force la CLI à parler à LocalStack à la place. Sans elle, `aws s3 ls` essaierait de lister les buckets du compte AWS réel (qui n'existe pas ou refusera les fausses clés `test`).

</details>

<details>
<summary><strong>Q18 — Docker Compose vs `docker run`</strong></summary>

`docker run` exige une longue commande à retaper à chaque démarrage et n'est pas versionnable. Docker Compose enregistre la même chose dans un fichier `docker-compose.yml` lisible, commité dans Git, partagé en équipe, et lancé par un simple `docker compose up -d`.

</details>

<details>
<summary><strong>Q19 — Conséquences d'un `.env` mal placé</strong></summary>

Si `.env` n'est pas au même niveau que `docker-compose.yml`, Docker Compose ne le trouve pas. Les variables (`LOCALSTACK_DOCKER_NAME`, `DEBUG`, `PERSISTENCE`…) sont alors absentes ou tombent sur leurs valeurs par défaut, ce qui peut donner un conteneur mal configuré ou un message d'erreur du type « variable is not set ».

</details>

<details>
<summary><strong>Q20 — Pourquoi nettoyer à la fin ?</strong></summary>

`terraform destroy` libère les ressources LocalStack, `docker compose down` arrête le conteneur, et `docker compose down -v` supprime aussi le volume local. Cela évite : un conteneur qui mange de la RAM, un port 4566 occupé pour la prochaine session, et un état Terraform incohérent au démarrage suivant.

</details>

---

## Score final

| Partie | Note obtenue | Note maximale |
|---|---:|---:|
| I — Comprendre les outils | | 10 |
| II — Vérifier les prérequis | | 10 |
| III — Comprendre le bypass legacy | | 5 |
| IV — Vérifier l'image LocalStack | | 5 |
| V — Créer le dossier du projet | | 5 |
| VI — Créer `.env` | | 10 |
| VII — Créer `.env.example` | | 5 |
| VIII — Créer `.gitignore` | | 5 |
| IX — Créer `docker-compose.yml` | | 15 |
| X — Vérifier `docker compose config` | | 5 |
| XI — Démarrer LocalStack | | 10 |
| XII — Vérifier LocalStack (HTTP `/info`) | | 10 |
| XIII — Variante `docker run` | | 5 |
| XIV — Créer les fichiers Terraform | | 5 |
| XV — Comprendre `provider.tf` | | 10 |
| XVI — Créer S3 et DynamoDB | | 15 |
| XVII — Exécuter Terraform | | 15 |
| XVIII — Vérifier avec AWS CLI | | 10 |
| XIX — Détruire l'infrastructure | | 5 |
| XX — Erreurs fréquentes | | 5 |
| XXI — Questions de compréhension | | 15 |
| XXII — Mini-rapport | | 20 |
| **TOTAL** | | **200** |

---

## Références utiles

- LocalStack — Changements de tarification 2026 : https://blog.localstack.cloud/2026-upcoming-pricing-changes/
- LocalStack — Annonce 2026.03.0 (date butoir bypass) : https://blog.localstack.cloud/localstack-for-aws-release-2026-03-0/
- LocalStack — Getting Started : https://docs.localstack.cloud/getting-started/
- LocalStack — Installation Docker : https://docs.localstack.cloud/getting-started/installation/
- LocalStack — Intégration Terraform : https://docs.localstack.cloud/user-guide/integrations/terraform/
- LocalStack — Plans & tarification (pour plus tard) : https://www.localstack.cloud/pricing
- Terraform — Provider AWS : https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- Docker Compose — Variables `.env` : https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/
- Théorie du cours : [00-theorie-terraform-localstack.md](00-theorie-terraform-localstack.md)
- Version `b` (avec token, pérenne) : [01b-Chapitre1-Pratique-01-terraform-localstack.md](01b-Chapitre1-Pratique-01-terraform-localstack.md)
- README du cours : [README.md](README.md)

---

*Fin du TP guidé — Terraform avec LocalStack.*
