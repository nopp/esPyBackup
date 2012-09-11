# -*- coding: utf-8 -*-

import subprocess, urllib, getopt, sys, shutil, ConfigParser, datetime, os

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

esServer = config.get('conf','server')
esPort = config.get('conf','port')
esIndicePath = config.get('conf','indicePath')
esBackupDir = config.get('conf','backupDir')

#
# Backup Class
#

class EsBackup:

    def main(self):
        dirBackup = ""
        indice = ""
        optlist , args = getopt.getopt(sys.argv[1:],'i:')
        for (option,value) in optlist:
            if option == '-i':
                indice = value
        if (indice == ""):
            print "Usage:\n esPyBackup.py -i indiceName\n"
        else:
            self.backupByIndice(indice)

    def backupByIndice(self, indiceName):

        # Date
        date = datetime.datetime.now()
        backupDate = str(date.day)+""+str(date.month)+""+str(date.year)

        # Create backup dir
        os.makedirs(esBackupDir+"/"+backupDate)
        dirBackup = esBackupDir+"/"+backupDate

        # Generate mapping from indice
        mappingFile = indiceName+"_mapping"
        fhMapping = open(dirBackup+"/"+mappingFile,"w")
        mapping = urllib.urlopen("http://"+esServer+":"+str(esPort)+"/"+indiceName+"/_mapping?pretty=true")
        fhMapping.writelines("{\"settings\":{\"number_of_shards\":5,\"number_of_replicas\":1},\"mappings\":{\n")
        fhMapping.writelines(mapping)
        fhMapping.close()
        result = subprocess.call("sed -i '2,3d' "+dirBackup+"/"+mappingFile,shell=True)
        if(result == 0):
            # Generate .tar.gz with metadata and data
            result = subprocess.call("cd "+esIndicePath+" && tar czfP "+dirBackup+"/backup_"+indiceName+".tar.gz "+indiceName+"/ "+dirBackup+"/"+mappingFile ,shell=True)
            if(result == 0):
               subprocess.call("rm "+dirBackup+"/"+mappingFile,shell=True)
               print "Backup success!"
            else:
               print "Backup failed!"
        else:
            print "Backup failed!"
