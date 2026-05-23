<a id="top"></a>

# Chapitre 5 — Théorie : multi-environnements dev / test

> **Pré-requis :** TPs 1 à 4 terminés.
>
> Document théorique. Aucune commande à exécuter ici.

---

## 1. Ce que vous allez construire

Vous allez **instancier les modules du TP 4 dans deux environnements isolés** :

- un environnement `dev`,
- un environnement `test`.

Chaque environnement a son **propre `terraform.tfstate`**, ses **propres ressources** dans LocalStack, et son **propre cycle de vie**.

```text
terraform/
├── modules/                       (inchanges, viennent du TP 4)
│   ├── s3/
│   ├── dynamodb/
│   └── sqs/
└── environments/
    ├── dev/
    │   ├── provider.tf
    │   ├── variables.tf
    │   ├── terraform.tfvars       environment = "dev"
    │   ├── main.tf                appelle les modules
    │   └── outputs.tf
    └── test/
        ├── provider.tf
        ├── variables.tf
        ├── terraform.tfvars       environment = "test"
        ├── main.tf
        └── outputs.tf
```

Streamlit recevra un **sélecteur d'environnement** dans la sidebar : choisir `dev` ou `test` change la cible.

## 2. Pourquoi multi-environnements ?

C'est une pratique standard de l'industrie :

```text
dev  : on bricole, on casse, on recommence.
test : on valide automatiquement.
prod : on touche le moins possible.
```

Les bénéfices :

- **Donnees isolees** : un drop de table dans `test` ne touche pas `dev`.
- **Cycle de vie distinct** : on peut détruire `test` sans impact sur `dev`.
- **Nommage clair** : `tp-localstack-dev-documents` vs `tp-localstack-test-documents`.
- **Coût et risque maîtrisés** : `dev` peut être petit, `test` peut être plus riche, `prod` peut être verrouillé.

## 3. Idée centrale du TP 5

```text
LE MEME CODE TERRAFORM est instancie DEUX FOIS,
avec des VARIABLES DIFFERENTES.

Grace aux modules du TP 4, on ne copie-colle rien.
On ne fait que dupliquer un petit wrapper par environnement.
```

## 4. Compétences visées

- Comprendre la **séparation environnement / modules**.
- Utiliser `terraform -chdir=<dir>` pour viser un environnement.
- Lire deux `terraform.tfstate` séparés.
- Gérer plusieurs environnements en Streamlit (sélecteur dynamique).
- Comparer les outputs entre environnements (`dev` vs `test`).

## 5. Quel parcours suivre ?

| Vous avez fait le TP 4 en… | Faites le TP 5 en… |
|---|---|
| `04b` | [`05b-...md`](05b-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit.md) |
| `04c` | [`05c-...-hobby-no-token.md`](05c-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit-hobby-no-token.md) |

## 6. Temps estimé

| Phase | Durée |
|---|---|
| Lecture intro + analyse | ~30 min |
| Créer `environments/dev/` | ~30 min |
| Appliquer dev | ~15 min |
| Créer `environments/test/` (copie + ajustement) | ~20 min |
| Appliquer test | ~15 min |
| Adapter Streamlit avec sélecteur d'env | ~45 min |
| Valider dev puis test dans l'UI | ~30 min |
| Mini-rapport | ~30 min |
| **Total** | **~3 h 15** |

## 7. Pièges à éviter

| Erreur | Solution |
|---|---|
| Oublier d'exécuter `terraform init` dans le nouveau dossier | Chaque env est indépendant : un `init` par dossier. |
| `terraform apply` lancé à la racine au lieu du sous-dossier | Toujours `cd terraform/environments/<env>` ou `terraform -chdir=...`. |
| Modifier les modules au lieu des wrappers | Les modules sont **partagés** : on les modifie consciemment. |
| `.tfstate` mélangés | Chaque dossier env a son propre `.tfstate`. |

## 8. Ce que vous n'allez PAS faire ici

- ❌ Déployer sur le vrai AWS.
- ❌ Backends distants (Terraform Cloud, S3 backend, Consul).
- ❌ CI/CD (GitHub Actions, GitLab CI).
- ❌ Plus de 2 environnements (vous pourrez ajouter `stage` en exercice).

---

> **Prêt ?** Ouvrez :
> - [`05b-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit.md`](05b-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit.md) — version avec token.
> - [`05c-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit-hobby-no-token.md`](05c-Chapitre5-Pratique-05-environnements-dev-test-terraform-validation-streamlit-hobby-no-token.md) — version sans token.

<p align="right"><a href="#top">↑ Retour en haut</a></p>
