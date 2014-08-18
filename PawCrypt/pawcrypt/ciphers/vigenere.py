""" 
    vigenere_cipher.py - implementation of Viginere Cipher

       - Uses a 26 letter alphabet via strings module
 
       TODO: Operate on any given character set.

       https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/e/vigenere_cipher_encryption    
       http://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
"""
__author__ = 'paws@delimitize.com'

from string import lowercase as lc
from pawcrypt.templates.alphabetic import Cipher
from pawcrypt.lib.alphabetic import shift,unshift

class Vigenere(Cipher):

    """ Implementation of Vigenere Cipher"""

    def __init__(self,**kwargs):
        """Initialize parameters"""
        super(Vigenere,self).__init__(**kwargs)

    def doEncode(self,msg,key):
        """Encode Vigenere cipher"""
        result = ''
        key_len=len(key)
        key_pos = 0
        for i in msg.lower():
            try:
                _ = lc.index(i)
            except(ValueError):
                result = "{}{}".format(result,i)
                continue
            if key_pos == key_len:
                key_pos=0
            newchr = shift(i,lc.index(key[key_pos]))
            key_pos=key_pos+1 
            result = "{}{}".format(result,newchr)
        return result

    def doDecode(self,msg,key):
        """Decode Vigenere cipher"""
        result = ''
        key_len=len(key)
        key_pos = 0
        for i in msg.lower():
            try:
                _ = lc.index(i)
            # blindly add unknown chars
            except(ValueError):
                result = "{}{}".format(result,i)
                continue
            if key_pos == key_len:
                key_pos=0
            newchr = unshift(i,lc.index(key[key_pos]))
            key_pos=key_pos+1
            result = "{}{}".format(result,newchr)
        return result

