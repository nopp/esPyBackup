# -*- coding: utf-8 -*-

import subprocess, urllib, getopt, sys

class config:

	esServer = "localhost"
	esPort = 9200
	esIndicePath = "/var/lib/elasticsearch/elasticsearch/nodes/0/indices"

#
# Backup Class
#

class EsBackup(config):

	def main(self):
		dirBackup = ""
		indice = ""
		optlist , args = getopt.getopt(sys.argv[1:],'d:i:')
		for (option,value) in optlist:
			if option == '-d':
				dirBackup = value
   			elif option == '-i':
				indice = value
		if (dirBackup == "" or indice == ""):
			print "Usage:\n esPyBackup.py -d dirBackupPath -i indiceName\n"
		else:
			self.backupByIndice(indice,dirBackup)

	def backupByIndice(self, indiceName, dirBackup):

		# Generate mapping from indice
		mappingFile = indiceName+"_mapping"
		fhMapping = open(dirBackup+"/"+mappingFile,"w")
		mapping = urllib.urlopen("http://"+self.esServer+":"+str(self.esPort)+"/"+indiceName+"/_mapping?pretty=true")
		fhMapping.writelines("{\"settings\":{\"number_of_shards\":5,\"number_of_replicas\":1},\"mappings\":{\n")
		fhMapping.writelines(mapping)
		fhMapping.close()
		subprocess.call("sed -i '2,3d' "+dirBackup+"/"+mappingFile,shell=True)

		# Generate .tar.gz with metadata and data
		result = subprocess.call("cd "+self.esIndicePath+" && tar czfP "+dirBackup+"/backup_"+indiceName+".tar.gz "+indiceName+"/ "+dirBackup+"/"+mappingFile ,shell=True)
		subprocess.call("rm "+dirBackup+"/"+mappingFile,shell=True)
		if(result == 0):
			print "Backup success!"

#
# Restore Class
#

class EsRestore(config):

	def main(self):
		backupDir = ""
		mappingFile = ""
		indice = ""
		optlist , args = getopt.getopt(sys.argv[1:],'d:i:')
		for (option,value) in optlist:
			if option == '-i':
				indice = value
   			elif option == '-m':
				mappingFile = value
		if (indice == "" or mappingFile == "" or backupDir == ""):
			print "Usage:\n esPyRestore.py -i indiceName -m mappingFile -d bakcupDir\n"
		else:
			self.restoreByIndice(indice,mappingFile,backupDir)

	def restoreByIndice(self, indiceName, mappingFile, backupDir):

		fhMapping = open(self.mappingFile,"r")
		params = fhMapping.read()
		fhMapping.close()
		result = urllib.urlopen("http://"+self.esServer+":"+str(self.esPort)+"/"+indiceName+"/", params)
		if(result == 0):
			# Move indice dir to es indice path	
			subprocess.call("cp -r "+backupDir+"/"+indiceName+" "+self.esIndicePath,shell=True)
			print "Restore success!"
