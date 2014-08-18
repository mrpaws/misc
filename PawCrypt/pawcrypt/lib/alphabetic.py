""" 
    alphabetic.py - library for alphabetic and polyalphabetic substitition modules
"""

__author__ = 'paws@delimitize.com'

import string

def shift(char,shift):
    """Attempt alphabetic shift operation (26)"""
    try:
        return string.lowercase[(string.lowercase.index(char)+shift) % 26]
    except ValueError:
        return char

def unshift(char,shift):
    """Attempt alphabetic deshift operation (26)"""
    try:
        return string.lowercase[(string.lowercase.index(char)-shift) % 26]
    except ValueError:
        return char
   
class VigenereSquare(dict):

    """tabula recta object implemented as a dict of lists"""

    def __init__(self):
        i=0 
        for char in string.lowercase:
            self[char]=[shift(c,i) for c in string.lowercase]
            i=i+1

