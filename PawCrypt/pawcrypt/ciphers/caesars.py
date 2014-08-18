""" 
    caesars_cipher.py - implementation of Caesar's Cipher

        TODO: adjust to work for any given character sets

        Practice from content learned at :
        https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/a/shift-cipher
"""
__author__ = 'paws@delimitize.com'

from pawcrypt.templates.alphabetic import Cipher,CipherError
from pawcrypt.lib.alphabetic import shift,unshift

class Caesars(Cipher):

    """ Py strings Implementation of Caesar's Cipher"""

    def encode(self,msg,shift):
        """Perform Caesar Cipher cipher"""
        result=''
        for i in msg.lower():
            result="{}{}".format(result,shift(i,shift))
        return self.result

    def decode(self,msg,shift):
        """Perform Caesar Cipher shift decipher"""
        for i in msg.lower():
            self.result="{}{}".format(result,unshift(i,shift))
        return self.result
