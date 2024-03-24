try:

    import configparser
    from Class.SendMail import SendMail
    from Class.GetInfo import GetInfo
    from Class.ScanManager import ScanManager
    import datetime


    lastHour = 0
    lastDay = 0
    while True:
        Time = datetime.datetime.now()
        configFile =configparser.ConfigParser()
        configFile.read('CONFIG.ini')
        mailSizeMax = int(configFile['BOT_INFO']['mailSizeMax'])

        EnvoyerMail = SendMail(configFile)
        RecupInfo = GetInfo(configFile)
        GestionScan = ScanManager(configFile)

        #DEFINIR UNE CADENCE DE RECHERCHE DE NOUVEAU CHAPITRE

        # VERIFIER SI LE DENIER CHAPITRE A DEJA ETE ENVOYER
        if( RecupInfo.VerifNewChapitre() == True and lastHour != Time.hour):
            lastHour = Time.hour
            print("###################################")
            #NOUVEAU CHAPITRE RECUPE NOM NUM ET LIEN
            RecupInfo.GetTitle()

            print("RECUPERATION DU NOUVEAU CHAPITRE")

            # RECUPE IMAGE ET STOCKER DANS DOSSIER
            print("TELECHARGEMENT")
            RecupInfo.supFolder()
            RecupInfo.GetScan()

            #PREPARATION DES SCAN
            print("COMPRESION DES SCAN")
            range=0
            while True:
                GestionScan.supFolder()
                GestionScan.reduire_taille_image(range)
                range+=10
                if(float(GestionScan.sizeFolder())<mailSizeMax):
                    break

            # FAIRE MAIL
            Objet= '🆕'+str(RecupInfo.title)+'🆕'
            Message = "BONNE LECTURE 😊😊😊\n"
            # ENVOYER MAIL
            print("ENVOI DU NOUVEAU CHAPITRE")
            EnvoyerMail.SendMail(Objet,Message,False)

            # SAUVEGARER EN TEN QUE DERNIER CHAP#
            configFile['CHAPITRE_INFO']['chapitreprecedent']= str(RecupInfo.title)
            configFile['CHAPITRE_INFO']['lien']= str(RecupInfo.UpdateLien())
            with open('config.ini', 'w') as configfile:
                configFile.write(configfile)
                
            print("###################################")
        elif(lastDay != Time.day ):
            lastDay = Time.day
            Objet= '✅✅✅'+"TOUJOUS VIVANT"+'✅✅✅'
            Message = "NOUVEAU JOUR SANS PROBLEME \n"
            # ENVOYER MAIL
            EnvoyerMail.SendMail(Objet,Message,True)


except Exception as e:
    #print(e);sys.exit()
    Objet= '⛔⛔⛔'+"ERREUR BOT MAIL"+'⛔⛔⛔'
    Message = "ERREUR BOT MAIL \n"+str(e)
    # ENVOYER MAIL
    EnvoyerMail.SendMail(Objet,Message,True)
