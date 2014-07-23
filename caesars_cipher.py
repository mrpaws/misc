""" 
    caesars_cipher.py - implementation of Caesar's Cipher

        Self-inflicted practice exercise while working on Khan Academy's
        Cryptography learning material

        https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/a/shift-cipher
"""
__author__ = 'mrpaws'

import string

class CaesarsCipher():
    """ Implementation of Caesar Cipher"""

    def __init__(self,key,msg):
        if msg:
            self.msg = msg
        if key:
            self.key = key
        if key and msg:
            self.cipher()
            print self.result

    def cipher(self):
        """Perform Caesar Cipher shift operation on string"""
        for i in self.msg.lower():
            try: 
                """if python didn't load the mapping into memory for us already 
                   via string, we could enumerate the alphabet and parse the list
                   to find pos
                """
                pos = string.lowercase.index(i)
            except ValueError as e: 
                result = "{c}{n}".format(c=result,n=i)
                continue
            shift_pos = pos + self.key
            if shift_pos > 25:
                shift_pos = shift_pos-25 
            return self.result = "{c}{n}".format(
                c=result,
                n=string.lowercase[shift_pos % 26])

