#!/usr/bin/env python
# coding: utf-8
#
# esPyBackup - Simple backup for elasticsearch
# Author: Carlos Augusto Malucelli
# www.carlosmalucelli.com
# https://github.com/malucelli/esPyBackup
#

# esPyBackup Moduels
from esLib import EsBackup

# Main
esBkp = EsBackup()
esBkp.backupByIndice("twitter")
