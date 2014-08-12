""" 
    caesars_cipher.py - implementation of Caesar's Cipher

        Self-inflicted practice exercise while working on Khan Academy's
        Cryptography learning material

        https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/a/shift-cipher
"""
__author__ = 'paws@delimitize.com'

from pawcrypt.templates.alphabetic import Cipher,CipherError
from pawcrypt.lib.alphabetic import shift,unshift

class Caesars(Cipher):

    """ Implementation of Caesar Cipher"""

    def __init__(self,**kwargs):
        super(Caesars,self).__init__(**kwargs)

    def cipher(self):
        """Perform Caesar Cipher cipher"""
        super(Caesars,self).cipher()
        for i in self.msg.lower():
            self.result="{}{}".format(self.result,shift(i,self.shift))
        self.ciphered = True
        return self.result

    def decipher(self):
        """Perform Caesar Cipher shift decipher"""
        super(Caesars,self).decipher()
        for i in self.msg.lower():
            self.result="{}{}".format(self.result,unshift(i,self.shift))
        self.ciphered = False
        return self.result
