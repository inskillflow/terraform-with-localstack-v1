<a id="top"></a>

# Chapitre 4 — Théorie : refactor en modules Terraform

> **Pré-requis :** TPs 1, 2 et 3 terminés.
>
> Document théorique. Aucune commande à exécuter ici.

---

## 1. Ce que vous allez construire

Vous allez **réorganiser le code Terraform du TP 3 en modules réutilisables**, sans changer les ressources produites.

Avant (TP 3) :

```text
terraform/
├── provider.tf
├── variables.tf
├── main.tf        <-- aws_s3_bucket + aws_dynamodb_table + aws_sqs_queue dedans
└── outputs.tf
```

Après (TP 4) :

```text
terraform/
├── provider.tf
├── variables.tf
├── main.tf        <-- juste 3 appels de modules
├── outputs.tf     <-- re-expose les outputs des modules
└── modules/
    ├── s3/
    │   ├── main.tf       aws_s3_bucket.this
    │   ├── variables.tf
    │   └── outputs.tf
    ├── dynamodb/
    │   ├── main.tf       aws_dynamodb_table.this
    │   ├── variables.tf
    │   └── outputs.tf
    └── sqs/
        ├── main.tf       aws_sqs_queue.this
        ├── variables.tf
        └── outputs.tf
```

## 2. Pourquoi des modules ?

Les modules apportent **quatre bénéfices** majeurs :

```text
1. Reutilisabilite : creer 5 buckets devient trivial.
2. Lisibilite      : main.tf racine devient court et lisible.
3. Encapsulation   : un module = une responsabilite.
4. Test            : on peut tester un module isolement.
```

Et un piège à connaître :

```text
Les noms des ressources AWS restent identiques.
MAIS les adresses Terraform changent :

    Avant : aws_s3_bucket.documents
    Apres : module.documents_bucket.aws_s3_bucket.this

terraform plan le voit comme un changement, alors qu'en pratique
le bucket AWS ne bougera pas. Il faut savoir lire le plan attentivement.
```

## 3. Test de réussite du TP 4

**Si le refactor est bien fait, Streamlit (du TP 3) doit fonctionner sans aucune modification.**

```text
Meme noms de bucket.
Meme noms de table.
Meme noms de file SQS.
Meme outputs Terraform.
```

C'est la **garantie d'un refactor propre** : on change le code, pas le comportement.

## 4. Compétences visées

- Créer un **module local** dans `modules/<service>/`.
- Déclarer ses **variables**, **resources** et **outputs**.
- Appeler le module depuis `main.tf` racine avec `source = "./modules/..."`.
- Re-exposer les outputs au niveau racine.
- Comprendre l'**adressage** des ressources dans un projet modulaire.
- Utiliser `terraform fmt -recursive`.

## 5. Quel parcours suivre ?

| Vous avez fait le TP 3 en… | Faites le TP 4 en… |
|---|---|
| `03b` | [`04b-...md`](04b-Chapitre4-Pratique-04-modules-terraform-validation-streamlit.md) |
| `03c` | [`04c-...-hobby-no-token.md`](04c-Chapitre4-Pratique-04-modules-terraform-validation-streamlit-hobby-no-token.md) |

## 6. Temps estimé

| Phase | Durée |
|---|---|
| Lecture intro + analyse de l'existant | ~30 min |
| Créer `modules/s3/` | ~30 min |
| Créer `modules/dynamodb/` | ~20 min |
| Créer `modules/sqs/` | ~20 min |
| Réécrire le `main.tf` racine et les outputs | ~30 min |
| `terraform init` + lecture du plan | ~20 min |
| `terraform apply` + validation Streamlit | ~30 min |
| Mini-rapport | ~30 min |
| **Total** | **~3 h** |

## 7. Concept central : `aws_s3_bucket.this`

Dans un module, on utilise souvent un nom générique :

```text
this = "le bucket principal de ce module"
```

Parce que le **module lui-même donne déjà le contexte**. Inutile d'écrire `aws_s3_bucket.s3_module_main_bucket_for_documents` ; le nom `this` suffit.

## 8. Ce que vous n'allez PAS faire ici

- ❌ Publier les modules sur Terraform Registry (hors scope).
- ❌ Versionner les modules (`version = "1.0.0"`).
- ❌ Multi-environnements (c'est le TP 5).
- ❌ Backends Terraform distants.

---

> **Prêt ?** Ouvrez :
> - [`04b-Chapitre4-Pratique-04-modules-terraform-validation-streamlit.md`](04b-Chapitre4-Pratique-04-modules-terraform-validation-streamlit.md) — version avec token.
> - [`04c-Chapitre4-Pratique-04-modules-terraform-validation-streamlit-hobby-no-token.md`](04c-Chapitre4-Pratique-04-modules-terraform-validation-streamlit-hobby-no-token.md) — version sans token.

<p align="right"><a href="#top">↑ Retour en haut</a></p>
