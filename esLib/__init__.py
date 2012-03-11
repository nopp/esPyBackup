# -*- coding: utf-8 -*-

import subprocess, urllib

class EsBackup:

        # Config
        esServer = "localhost"
        esPort = 9200
        esIndicePath = "/var/lib/elasticsearch/elasticsearch/nodes/0/indices"
        mappingFile = "/tmp/mapping"
        backupDir = "/home/carlos/backup/"

	def backupByIndice(self, indiceName):

		# Generate mapping from indice
		fhMapping = open(self.mappingFile,"w")
		mapping = urllib.urlopen("http://"+self.esServer+":"+str(self.esPort)+"/"+indiceName+"/_mapping?pretty=true")
		fhMapping.writelines("{\"settings\":{\"number_of_shards\":5,\"number_of_replicas\":1},\"mappings\":{\n")
		fhMapping.writelines(mapping)
		fhMapping.close()
		subprocess.call("sed -i '2,3d' "+self.mappingFile,shell=True)

		# Generate .tar.gz with metadata and data
		result = subprocess.call("cd "+self.esIndicePath+" && tar czfP "+self.backupDir+"/backup_"+indiceName+".tar.gz "+indiceName+"/ "+self.mappingFile ,shell=True)
		subprocess.call("rm "+self.mappingFile,shell=True)
		if(result == 0):
			print "Backup success!"

	def restoreByIndice(self, indiceName):

		fhMapping = open(self.mappingFile,"r")
		params = fhMapping.read()
		fhMapping.close()
		result = urllib.urlopen("http://"+self.esServer+":"+str(self.esPort)+"/"+indiceName+"/", params)
		if(result == 0):
			# Move indice dir to es indice path	
			subprocess.call("cp -r "+indiceName+" "+self.esIndicePath,shell=True)
			print "Restore success!"
