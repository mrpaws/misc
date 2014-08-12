""" 
    vigenere_cipher.py - implementation of Viginere Cipher

        Self-inflicted practice exercise while working on Khan Academy's
        Cryptography learning material
         
       https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/e/vigenere_cipher_encryption    
       http://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
       
      

"""
__author__ = 'mrpaws'

import string
from pawcrypt.templates.alphabetic import Cipher,CipherError
from pawcrypt.lib.alphabetic import shift,unshift

class Vigenere(Cipher):

    """ Implementation of Vigenere Cipher"""

    _tabula_recta = dict.fromkeys(string.lowercase,list(string.lowercase))

    def __init__(self,**kwargs):
        """Build the vigenere square for decryiption"""
        super(Vigenere,self).__init__(**kwargs)
        i=0
        for char in list(string.lowercase):
            self._tabula_recta[char]=[shift(c,i) for c in self._tabula_recta[char]]
            i=i+1

    def cipher(self):
        """Perform Caesar Cipher cipher"""
        self.ciphered = True
        return self.result

    def decipher(self):
        """Perform Caesar Cipher shift decipher"""
        self.ciphered = False
        return self.result

