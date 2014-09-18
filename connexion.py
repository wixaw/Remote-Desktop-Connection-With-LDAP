#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################
#############################

## Par William Vincent - william66750 - @ - g m a i l (.) com
## Description : selection de serveur TSE par le biais de l'annuaire LDAP 
## Dependances: python-ldap, MySQLdb

#############################
#############################






#############################
####### Libraries
#############################

# Traitement de cmd bash
import os
import subprocess

# traitement de chaine de carractere
import re

# Gestion des fenetres
import pygtk
import gtk , gobject

# Base de donnees
import MySQLdb

#Recuper info machine
import socket, fcntl, struct 


#Recuperer le temps
from time import gmtime, strftime

#############################






#############################
####### Classe
#############################

class GTK_Main():

 
    #Definir ip machine
    def get_ip_address(ifname):
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    return socket.inet_ntoa(fcntl.ioctl( s.fileno(), 0x8915, struct.pack('256s', ifname[:15]) )[20:24])
	    
    ### Variables
    #Declarer variables globales
    global monip, monposte
    
    
    #Declarer infos
    monposte = socket.gethostname()
    monip = get_ip_address('eth0')
    print "IP %s " % ( monip )
    
    
    ### GENERAL
    def __init__(self):
		
		##################
		### Fonctions
		##################
		
		##################
		# Fontion > Log de connexion
		def connexion(userLog):
			
			try:
				infoid = 0
				db = MySQLdb.connect("host","user","passwd","base")
			
				#mise en forme de la date
				dateinfo = strftime("%Y-%m-%d %H:%M:%S", gmtime())
				
				cursor = db.cursor()
				sql = "INSERT INTO logs VALUES (NULL, '%s', '%s', NULL, '%s', '%s')" % ( userLog, dateinfo , monposte , monip )
				cursor.execute(sql)
				db.commit()
				
				# recuperer id
				infoid = cursor.lastrowid 
				db.close()
				print "log co OK"
				
			except:
				print "log co ERREUR"
				pass
				
				   
			
			return infoid
		
		
		
		
		
		
		
		
		
		##################
		# Fontion > Log de deconnexion
		def deconnexion(infoidLog):
		
			try:
				db = MySQLdb.connect("host","user","passwd","base")
			
				dateinfoquit = strftime("%Y-%m-%d %H:%M:%S", gmtime())
				cursor = db.cursor()
				sql = "UPDATE logs  SET date_logout='%s' WHERE id=%s" % ( dateinfoquit, infoidLog )
				cursor.execute(sql)
				db.commit()
				db.close()
				print "log deco OK"
				
			except:
				print "log deco ERREUR"
				pass
				
			
		
		
		
		
		
		
		
		##################
		# Fontion > SESSION RDP
		def connexionRDP(userCO , passwdCO , serveurCO, domaine):
			
			#Executer    
			subprocess.call(['/usr/bin/rdesktop', '-u', userCO, '-p', passwdCO, '-d', 'mecaprotec', '-r', 'sound:local', '-r' , 'disk:CLEUSB=/media/OLYMPUS/', '-NfzP' , '-x' , 'm' ,serveurCO ])










		##################
		# Fontion > Clic de connexion - Requete LDAP 
		def loginClicked(loginButton):
			
			#Declarer variables globales
			global user, passwd
			
			#Recuperer valeur variables 
			user = loginUserT.get_text()
			passwd = loginPassT.get_text()


			#Requete ldap
			cmd="ldapsearch -LLL -x -D 'uid=%s,ou=Users,o=mondomaine,dc=mondomaine,dc=fr' -h ldap -w '%s' -b dc=mondomaine,dc=fr memberUid=%s memberOf" % (user,passwd,user)
			#Exectuer
			proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			proc.wait()
			proc.returncode

			#Test : MOT DE PASSE
			if proc.returncode != 0:
				message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE)
				message.set_markup("Probleme de mot de passe.")
				message.run()
				message.destroy()
				gtk.main()
			
			# Stockage des groupes LDAP
			search = proc.stdout
			search = [line.strip('\n') for line in search]
			result = dict()
		
			#Variable de tests ( Liste de serveurs ou non )
			count = 0
			
			### Mise en forme de la chaine de carractere
			for line in search:
				
				# Ne garder que les serveur TSE
				if "TSE_" in line:

					try:
						# Supprimer les champs inutiles
						line = re.sub(r'dn: cn=TSE_','',line)
						line = re.sub(r',ou=groups,o=mondomaine,dc=mondomaine,dc=fr','',line)

						# Afficher les champs
						buttonSelect1 = gtk.ToggleButton(line)
						buttonSelect1.connect("toggled", boutonClicked, line, ".mondomaine.fr")
						selectvbox.pack_start(buttonSelect1, True, True, 0)
						
						# Test
						count += 1
						serveurUnique = line
						dom = ".mondomaine.fr"

					except:
						
						pass
					      
				# MultiDomaine	      
				if "TSEGROUPE2_" in line:

					try:
						# Supprimer les champs inutiles
						line = re.sub(r'dn: cn=TSEGROUPE2_','',line)
						line = re.sub(r',ou=groups,o=mondomaine,dc=mondomaine,dc=fr','',line)

						# Afficher les champs
						buttonSelect1 = gtk.ToggleButton(line)
						buttonSelect1.connect("toggled", boutonClicked, line, ".mondomaine2.be")
						selectvbox.pack_start(buttonSelect1, True, True, 0)
						
						# Test
						count += 1
						serveurUnique = line
						dom = ".mondomaine.be"

					except:
						pass
						
						
			### Access serveur = 1  -> Connexion
			if count == 1: 
				print "Connexion direct : "
				print "log : "
				# Log de connexion".mondomaine.fr"
				infoid = connexion(user)
				
				print "Session RDP : "
				### ConnexionRDP
				connexionRDP( user , passwd , serveurUnique , dom)	

				print "log : "
				# Log de deconnexion
				deconnexion(infoid)
				
				# Effacer les fenetres
				serveur.destroy()
				login.destroy()
			

			### Access > 2 Serveurs :  Effacer fenetre login + Afficher fenetre liste serveurs
			else:
				print "Connexion multi serveur : "
				# Effacer fenetre login
				login.hide()
				
				# Afficher liste de serveurs
				serveur.show_all()








		##################
		# Fontion >  Clic sur serveur : Lancer Connexion RDP	

		def boutonClicked(selectButton, serveurTse, domaine):

			print "log : "
			# Log de connexion
			infoid = connexion(user)

			print "Session RDP : "
			### ConnexionRDP
			connexionRDP( user , passwd , serveurTse , domaine )	

			print "log : "
			# Log de deconnexion
			deconnexion(infoid)

			# Effacer les fenetres
			serveur.destroy()
			login.destroy()
	



		##################
		# // ###### // FIN DES FONCTIONS
		##################












		##################
		# Mise en forme
		##################

		##################
		# MEF > FORMULAIRE DE CONNEXION


		# Options de fenetres
		login = gtk.Window()
		login.set_size_request(800, 200)
		login.set_border_width(10)



		# Champs
		login.connect("destroy", gtk.main_quit)
		login.set_title("Connexion RDP MonDomaine - Login")


		loginVbox = gtk.VBox(homogeneous=False)
		loginLabel = gtk.Label("Veuillez entrer vos identifiants MonDomaine")
		loginHbox1 = gtk.HBox(homogeneous=True, spacing=3)
		loginHbox2 = gtk.HBox(homogeneous=True, spacing=3)
		loginUserL = gtk.Label("Nom d'utilisateur :")
		loginPassL = gtk.Label("Mot de passe :")
		loginUserT = gtk.Entry()
		loginPassT = gtk.Entry()
		loginPassT.set_visibility(False)
	


		# Permet de press enter key afin de connecter directement sans cliquer
		loginPassT.connect("activate", loginClicked)

		# Logo mondomaine
		imageHBox = gtk.Image()
		imageHBox.set_from_file("/usr/share/connexion/logo.png")

		#Bouton de connection
		loginButton = gtk.Button(label="Connexion")
		loginButton.connect("clicked", loginClicked)


	
		login.add(loginVbox)
		loginVbox.pack_start(imageHBox, expand=True)
		loginVbox.pack_start(loginLabel, expand=False)
		loginVbox.pack_start(loginHbox1, expand=False)
		loginVbox.pack_start(loginHbox2, expand=False)
		loginVbox.pack_start(loginButton, False, False, 0)	
		loginHbox1.pack_start(loginUserL, expand=False)
		loginHbox1.pack_start(loginUserT, expand=True)
		loginHbox2.pack_start(loginPassL, expand=False)
		loginHbox2.pack_start(loginPassT, expand=True)



		##################
		# MEF > LISTE DES SERVEURS
		serveur = gtk.Window()
		serveur.connect("destroy", gtk.main_quit)

		serveur.set_size_request(800, 400)
		serveur.set_border_width(10)
		serveur.set_title("Connexion RDP MonDomaine - Connexion")


		selectvbox = gtk.VBox(homogeneous=False)


		infoLabel = gtk.Label("Veuillez cliquer sur le serveur a connecter :")
		infoHbox4 = gtk.HBox(homogeneous=True, spacing=3)
		selectvbox.pack_start(infoLabel, expand=False)
		selectvbox.pack_start(infoHbox4, expand=False)


		serveur.add(selectvbox)
        
        
		##################
		# MEF > Afficher la page de login
		login.show_all()


		##################
		# // ###### // FIN DE MISE EN FORME
		##################







#############################
# Generer la page
#############################

# Afficher TOUJOURS
while 1:
	
	#Afficher
	GTK_Main()
	gtk.main()


