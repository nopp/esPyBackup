import subprocess
import urllib
import sys
import os

sys.path.append(os.path.dirname(sys.argv[0]) + "/class/")
from EsConfig import *

class EsBackup:

	def backupByIndice(self, indiceName):

		# Generate mapping from indice
		fhMapping = open(mappingFile,"w")
		mapping = urllib.urlopen("http://"+esServer+":"+str(esPort)+"/"+indiceName+"/_mapping?pretty=true")
		fhMapping.writelines("{\"settings\":{\"number_of_shards\":5,\"number_of_replicas\":1},\"mappings\":{\n")
		fhMapping.writelines(mapping)
		fhMapping.close()
		subprocess.call("sed -i '2,3d' "+mappingFile,shell=True)

		# Generate .tar.gz with metadata and data
		result = subprocess.call("cd "+esIndicePath+" && tar czfP "+backupDir+"/backup_"+indiceName+".tar.gz "+indiceName+"/ "+mappingFile ,shell=True)
		subprocess.call("rm "+mappingFile,shell=True)
		if(result == 0):
			print "Backup success!"

	
