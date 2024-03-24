import requests
import re
import os
import time
import shutil
from bs4 import BeautifulSoup

class GetInfo():
    def __init__(self,configFile):

        self.config = configFile
        self.lien=self.config['CHAPITRE_INFO']['lien']
        self.chapitreprecedent= self.config['CHAPITRE_INFO']['chapitreprecedent']
        self.path = str(self.config['BOT_INFO']['path'])
        self.folderNameBrut = str(self.config['BOT_INFO']['brutFolder'])
        self.pathfolderBrut = self.path+self.folderNameBrut
        self.userAgent= str(self.config['BOT_INFO']['userAgent'])
        self.page = ""
        self.title=""
        self.nextLien=''
        self.lienImage=set()
        self.headers={
            'User-Agent': self.userAgent,
        }

    def supFolder(self):
        try:
            shutil.rmtree(self.pathfolderBrut)
            return True
        except:
            #print('dosier déjà supprimer')
            return False


    def VerifNewChapitre (self):
        response = requests.get(self.lien, headers=self.headers)
        if response.status_code == 200:

            self.page = BeautifulSoup(response .text, 'html.parser')
            items = self.page.find('h1',{"id":"chapter-heading"})
            if (items != None ):
                
                if(str(items.text) != str(self.chapitreprecedent) ):
                    #print('NEW CHAPITRE')
                    return True
                else:
                    #print('pas de nouveau chapitre')  
                    return False
            else:
                #print('pas de nouveau chapitre')
                return False
        else:
            print('Erreu acquisition page'+str(response .status_code))



    def GetTitle(self):

        self.title = self.page.find('h1',{"id":"chapter-heading"}).text
        return( self.title)


    def UpdateLien(self):

        numero_chapitre_actuel = int(self.lien.split('-')[-2])
        nouveau_numero_chapitre = numero_chapitre_actuel + 1
        self.nextLien = self.lien.replace(f'-{numero_chapitre_actuel}-', f'-{nouveau_numero_chapitre}-')
        return(self.nextLien)
    


    def Extract_urls(self,input_string):
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = re.findall(url_pattern, input_string)
        return urls[0]

    def DwonImage(self):
        for item in self.lienImage:
            tentatives = 0
            while tentatives < 5:
                try:
                    response = requests.get(str(item), headers=self.headers)
                    if response.status_code == 200:
                        tmp = item.split('/')
                        name = tmp[-1]
                        if not os.path.exists(self.pathfolderBrut):
                            os.makedirs(self.pathfolderBrut)

                        with open(self.pathfolderBrut + str(name), "wb") as f:
                            f.write(response.content)
                            #print(f"L'image {name} a été téléchargée avec succès.")
                            break  
                    else:
                        print(f"Échec du téléchargement de l'image {item}.")
                except Exception as e:
                    print(f"Une erreur s'est produite lors du téléchargement de l'image {item}: {str(e)}")
                
                tentatives += 1
                if tentatives < 5:
                    print("Nouvelle tentative dans 1 seconde...")
                    time.sleep(1)
            else:

                print(f"Échec du téléchargement de l'image {item} après plusieurs tentatives.")

                raise Exception(f"Échec du téléchargement de l'image {item} après plusieurs tentatives.")


    def GetScan(self):
        items = self.page.find_all('img', attrs={"class": "wp-manga-chapter-img"})
        for item in items:
            self.lienImage.add(self.Extract_urls(str(item)))
        
        self.DwonImage()



    


