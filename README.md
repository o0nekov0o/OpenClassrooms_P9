# Développez une application Web en utilisant Django - Projet n°9/13 Développeur Python
Ce dont il est question dans ce projet, c'est de le mener via le scénario suivant : Après un entretien réussi, on décroche le poste de lead développeur Python pour la jeune startup LITReview. Son objectif est de commercialiser un produit permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande. 

## Comment utiliser l'application Web développée ?

#### Première étape : téléchargement
Télécharger le répertoire Github à partir le lien ci-dessous :
https://github.com/o0nekov0o/OpenClassrooms_P9/archive/refs/heads/master.zip

#### Deuxième étape : installation
A l'aide de votre invite de commandes, placez-vous à la racine du répertoire téléchargé.
Lancez-y ensuite la commande suivante afin de créer votre environnement virtuel :
```bash
  python -m venv env
```
Depuis Windows, exécutez la commande suivante pour activer votre environnement virtuel :
```bash
  call env/Scripts/activate.bat
```
Si jamais cela ne fonctionne pas, exécutez Powershell en tant qu'administrateur. Une fois que la nouvelle invite de commandes est alors ouverte, exécutez-y le code suivant :
```bash
  Set-ExecutionPolicy RemoteSigned
```
Une fois que cela est fait, revenez à votre première invite de commandes puis entrez-y : 
```bash
  env/Scripts/activate
```
Depuis un autre OS, vous n'aurez qu'à rentrer ceci à l'intérieur de votre invite de commandes afin de pouvoir activer votre environnement virtuel (Mac/Linux/Autres systèmes) :
```bash
  source env/bin/activate
```
Enfin, pour installer les paquets requis, rentrez ensuite le code ci-dessous :
```bash
  pip install -r requirements.txt
```

#### Troisième étape : utilisation
Toujours depuis l'invite de commandes, rentrez enfin les deux commandes suivantes :
```bash
  cd LITReview
  python manage.py runserver
```
Une fois le serveur démarré, il ne vous restera plus qu'à cliquer sur le rien renvoyé par le terminal afin d'accéder au site et utiliser l'application Web qui a été développée.
