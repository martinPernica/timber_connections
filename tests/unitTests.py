import unittest
import os
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))
parrent_dir = os.path.dirname(current_dir)
scripts_dir = os.path.join(parrent_dir, "scripts")
print(scripts_dir)
sys.path.append(scripts_dir)

import groupOfBolts
import connectors
import timberShearJoints

print(dir())

