# -*- coding: utf-8 -*-

import subprocess, urllib, getopt, sys, shutil, ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

esServer = config.get('conf','server')
esPort = config.get('conf','port')
esIndicePath = config.get('conf','indicePath')

class EsRestore:

    def main(self):
        backupDir = ""
        mappingFile = ""
        indice = ""
        optlist , args = getopt.getopt(sys.argv[1:],'i:m:d:')
        for (option,value) in optlist:
            if option == '-i':
                indice = value
            elif option == '-m':
                mappingFile = value
            elif option == '-d':
                backupDir = value
        if (indice == "" or mappingFile == "" or backupDir == ""):
            print "Usage:\n esPyRestore.py -i indiceName -m mappingFile -d bakcupDir\n"
        else:
            self.restoreByIndice(indice,mappingFile,backupDir)

    def restoreByIndice(self, indiceName, mappingFile, backupDir):

        # Move indice data and preserve owner and group
        # Copytree not preserve mods :/
        try:
            shutil.move(backupDir,esIndicePath)
        except:
            print "Move indice error"

        # Import indice mapping
        fhMapping = open(mappingFile,"r")
        params = fhMapping.read()
        fhMapping.close()
        result = urllib.urlopen("http://"+esServer+":"+str(esPort)+"/"+indiceName+"/", params)
        print "Restore success!"
