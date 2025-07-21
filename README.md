# ristorante
ristorante

Prerequisites

-	Visual Studio Code
-	Python Extension for VS Code
-	Git
-	Python 3.9
-	Flask
-	Mailtrap

1.	Installation et Déploiement

Lancez VSCode et installez l’extension “Python” publiée par Microsoft. Après avoir créé le dossier, ouvrez un terminal intégré dans VS Code pour cloner le dépôt et exécuter les commandes suivantes :

	« git clone https://github.com/VitorPinto1/ristorante.git »
	« cd ristorante »

2. 	Configuration de l’environnement

Activez l’environnement virtuel Python dans le terminal :

	« source env/bin/activate »  # Unix ou MacOS
	« env\Scripts\activate »    # Windows

Installer les paquets requis à partir de requirements.txt :

  « pip install -r requirements.txt » 

3. 	Lancer l’application

Exécutez l’application avec Flask dans le terminal :

	« python app.py »
	« flask run »

4. 	Accéder à l’application

Ouvrez votre navigateur et allez à :
	
 	http://127.0.0.1:5000/

Pour consulter les e-mails, ouvrez votre navigateur et allez à :

	-https://www.mailjet.com/fr/
  
Vous aurez besoin de vos identifiants utilisateur Mailjet.

Conclusion

En suivant ces étapes, vous devriez pouvoir déployer l’application web localement et tester ses fonctionnalités.