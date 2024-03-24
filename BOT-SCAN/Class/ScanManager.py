from PIL import Image

import os
import shutil
from os import listdir
from os.path import isfile, join


class ScanManager():
    def __init__(self,configFile):
        self.config = configFile
        self.path = str(self.config['BOT_INFO']['path'])
        self.folderNameLite = str(configFile['BOT_INFO']['liteFolder'])
        self.folderNameBrut = str(configFile['BOT_INFO']['brutFolder'])
        self.scanSizeMax = int(configFile['BOT_INFO']['scanSizeMax'])
        self.pathfolderLite = self.path+self.folderNameLite
        self.pathfolderBrut = self.path+self.folderNameBrut
        self.namePDF= str(self.config['BOT_INFO']['namePDF'])


        self.sizeScan = 0
     

    def  sizeFolder(self):
        sizeTmp=0
        for chemin_dossier_actuel, dossiers, fichiers in os.walk(self.pathfolderLite):
            for fichier in fichiers:
                chemin_fichier = os.path.join(chemin_dossier_actuel, fichier)
                sizeTmp += os.path.getsize(chemin_fichier)
        self.sizeScan=((sizeTmp)/(1024*1024) )
        return self.sizeScan       



    def supFolder(self):
        try:
            shutil.rmtree(self.pathfolderLite)
            return True
        except:
            print('dosier déjà supprimer')
            return False

    
    def reduire_taille_image(self,index=0):
        only_files = [f for f in listdir(self.pathfolderBrut) if isfile(join(self.pathfolderBrut, f))]
        image_files = [f for f in only_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        self.scanSizeMax-=index
        if not os.path.exists(self.pathfolderLite):
            os.makedirs(self.pathfolderLite)

        for image_file in image_files:

            image_pathScanBrut = join(self.pathfolderBrut, image_file)
            image = Image.open(image_pathScanBrut)
            image.thumbnail((self.scanSizeMax,self.scanSizeMax))
            image.save(join(self.pathfolderLite, image_file))