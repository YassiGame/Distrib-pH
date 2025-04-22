# 📊 Distrib‑pH

Un outil interactif en Python qui **calcule et trace la répartition en pourcentage** d’un **acide faible (HA)** et de sa **base conjuguée (A⁻)** en fonction du **pH** (de 0 à 14), à partir de son **pKa**.

Ce projet permet de **visualiser l'équilibre acide/base** à l’aide d’un **diagramme de distribution**, utile aussi bien en chimie analytique qu’en enseignement.

## ✨ Aperçu

📈 Pourcentage de présence de HA et A⁻

🧪 Calcul basé sur la formule : %HA = 1 / (1 + 10^(pH - pKa)) × 100

📉 Plage de pH analysée : 0 à 14

🎨 Visualisation claire avec Matplotlib

## 🧠 Exemple de calcul

- pKa entré : `4.75`
- Le programme calcule pour chaque pH :
  - `%HA = 1 / (1 + 10^(pH - pKa)) × 100`
  - `%A⁻ = 100 - %HA`

Et affiche un **graphe dynamique** de la répartition des deux espèces.

## 📦 Installation

1. Clone ce dépôt :
```bash
git clone https://github.com/ton-utilisateur/distrib-ph.git
cd distrib-ph
```

2. Installe les dépendances :
```bash
pip install -r requirements.txt
```

## 🚀 Lancer le programme
```bash
python main.py
```

> Tu seras invité à entrer une valeur de pKa, puis le programme calculera automatiquement la répartition et affichera le diagramme de distribution.

## 🖼️ Exemple de résultat
![image](https://github.com/user-attachments/assets/d1c55e8a-2e4a-4e90-95b1-c3b6a561bf9d)
![image](https://github.com/user-attachments/assets/c7a89f36-e48b-4f76-ba32-5b9a03d9b4e4)
![image](https://github.com/user-attachments/assets/d250b3b9-01c0-4143-a5e5-c70d7dabc656)



## 📘 À propos

Développé comme outil pédagogique pour faciliter la compréhension des équilibres acido-basiques.

> Idéal pour les étudiants en chimie, les enseignants, ou toute personne souhaitant visualiser la zone de prédominance d’un acide ou de sa base conjuguée.

## 📝 Licence

Distribué sous licence GNU.
Libre à toi de modifier, partager, et utiliser ce code.
