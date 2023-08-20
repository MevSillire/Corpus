# Traitement de Données de Corpus et Population de Base de Données
Ce répertoire contient des scripts Python pour traiter les données de corpus, générer des indices et peupler une base de données MySQL avec les données traitées. Les scripts sont conçus pour gérer des données en langue française et comprennent des fonctionnalités de tokenisation, de segmentation en phrases et de génération d'indices divers pour le stockage et la récupération efficaces des données du corpus.

### Prérequis
Avant d'exécuter les scripts, assurez-vous de disposer de ce qui suit :
- Python 3.x installé.
- Bibliothèques Python requises : mysql-connector, pandas, re, spacy, nltk.
- Un serveur de base de données MySQL avec des informations d'identification appropriées.


### Utilisation
1) Préparation des Données : Placez vos données de corpus dans un fichier séparé par des tabulations (TSV). Les colonnes du fichier TSV doivent correspondre aux colonnes attendues : ['corpus', 'text', 'end_utterance', 'name_speaker', 'start_utterance', 'text_synchronisé', 'sub_corpus', 'langue_enregistrement', 'duration_sub_corpus', 'date_sub_corpus', 'description_sub_corpus', 'place_sub_corpus', 'gender_speaker', 'age_speaker', 'education_speaker', 'french_status_speaker', 'notes_speaker', 'birth_place_speaker', 'profession_speaker', 'link_sub_corpus', 'path_wav', 'text_utterance', 'publisher_corpus', 'type_corpus', 'description_corpus', 'author_sub_corpus', 'type_sub_corpus','right_sub_corpus', 'acoustic_quality_sub_corpus']

2) Configuration de la Base de Données : Ouvrez le script et inscrivez vos informations d'identification pour la base de données MySQL dans les fonctions 'pop.*'

3) Exécution du Script : Dans votre terminal, naviguez vers le répertoire où se trouve le script et exécutez-le avec la commande suivante : python nom_du_script.py fichier_entree.tsv nom_corpus.
Remplacez nom_du_script.py par le nom réel du fichier de script Python, fichier_entree.tsv par le chemin vers votre fichier de données de corpus en entrée et nom_corpus par le nom souhaité pour votre corpus.

4) Aperçu des Tables : Le script affichera un aperçu des tables qui seront insérées dans la base de données. Vous pouvez les passer en revue et confirmer ou annuler l'opération.

5) Insertion des Données : Si vous êtes satisfait des tables affichées, saisissez 'T' et appuyez sur Entrée pour confirmer et insérer les données dans la base de données. Si vous souhaitez annuler, saisissez un autre caractère.

### Contact
Pour toute question ou assistance, n'hésitez pas à contacter maeva.sillaire9@etu.univ-lorraine.fr.
