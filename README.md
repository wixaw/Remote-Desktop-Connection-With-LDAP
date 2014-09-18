RDCL - Remote Desktop Connection with LDAP                                                                                                    
=====

Description :
---------
	Ce programme permet la sélection et la connexion RDP à des serveurs Windows TSE par le biais de l'annuaire LDAP

Langage : 
---------
	Programme écrit en Python 

Dépendances : 
---------
	- Binaire RDP : rdesktop ( peut-être remplacer par freeRDP mais des problèmes d'affichages ont était constaté )
	- Librairies : gtk, python-mysqldb, ldap-utils

Fonctions : 
---------
	- Gestion des multi groupe LDAP ( un utilisateur peut avoir droit à se connecter à plusieurs serveurs TSE )
	- Log Connexions/Déconnexion
	- Interface graphique
	- Multi Domaine

Utilisation :
---------
	Le script peut être adapté à vos besoins. Vous pouvez me contacter pour des problèmes d'integration à votre envirronement 

	Si l'utilisateur a droit à un seul serveur TSE : Connexion RDP direct, sinon propose la liste des serveurs disponibles ( memberOf ldap ) 

Table SQL : 
---------

	--
	-- Structure de la table `logs`
	--

	CREATE TABLE IF NOT EXISTS `logs` (
	  `id` int(11) NOT NULL,
	  `user` varchar(200) DEFAULT NULL,
	  `date_login` datetime NOT NULL,
	  `date_logout` datetime DEFAULT NULL,
	  `poste` varchar(200) DEFAULT NULL,
	  `ip` varchar(200) DEFAULT NULL
	) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
	

Copies d'écran :
---------
	- A venir
