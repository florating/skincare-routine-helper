import os
import sys

# Get name of the directory where this file is present.
current = os.path.dirname(os.path.realpath(__file__))
print(f'NOTE: current os.path.dirname(os.path.realpath(__file__)) = {current} for __file__ = {__file__}\n')

# Get name of the parent directory, relative to the current directory.
parent = os.path.dirname(current)
print(f'NOTE: parent = {parent}\n')

# Adding the parent directory to the sys.path.
sys.path.append(parent)