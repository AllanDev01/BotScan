
import smtplib  
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
from email.utils import formataddr
from email.mime.image import MIMEImage
from os import listdir
from os.path import isfile, join



class SendMail():
    def __init__(self,configFile):
        
        self.config = configFile

        self.expediteur = self.config['BOT_INFO']['MailExpediteur']
        self.mot_de_passe = self.config['BOT_INFO']['MotDePasse']
        self.serveur_smtp = self.config['BOT_INFO']['ServeurSmtp']
        self.path = str(self.config['BOT_INFO']['path'])
        self.folderNameLite = str(configFile['BOT_INFO']['liteFolder'])
        self.pathfolderLite = self.path+self.folderNameLite
        self.port = self.config['BOT_INFO']['Port']
        self.destinataire = self.config['DESTINATEUR_INFO']['Mail']
        self.destinataireError = self.config['DESTINATEUR_INFO']['MailError']

    def SendMail(self,Objet,Message,NotScan):

        message = MIMEMultipart()  

        message['From'] = formataddr(('🍖 ONE PIECE 🍖', self.expediteur))
        message['To'] = self.destinataire
        message['Subject'] = Objet

        message.attach(MIMEText(Message, 'plain')) 
        if(NotScan==False):
            only_files = [f for f in listdir(self.pathfolderLite) if isfile(join(self.pathfolderLite, f))]
            image_files = [f for f in only_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

            for image_file in image_files:
                with open(join(self.pathfolderLite, image_file), 'rb') as img_file:
                    img = MIMEImage(img_file.read())
                    img.add_header('Content-Disposition', 'attachment', filename=image_file)
                    message.attach(img)
        
 
        session = smtplib.SMTP(self.serveur_smtp, self.port)
        session.starttls()  
        session.login(self.expediteur, self.mot_de_passe)  

        texte = message.as_string()  
        session.sendmail(self.expediteur, self.destinataire, texte)  
        session.quit()  