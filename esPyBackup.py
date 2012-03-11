#!/usr/bin/python
#
# esPyBackup - Simple backup of elasticsearch
# Author: Carlos Augusto Malucelli
# www.carlosmalucelli.com
# https://github.com/malucelli/esPyBackup
#

# Python Modules
import os
import sys

# esPyBackup Moduels
sys.path.append(os.path.dirname(sys.argv[0]) + "/class/")
from EsBackup import *

# Main
EsBackup().backupByIndice("twitter")

