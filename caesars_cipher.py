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

    result = ''
    msg = ''
    key = ''
    ciphered = False

    def __init__(self,key,msg):
        if msg:
            self.msg = msg
        if key:
            self.key = key

    def cipher(self):
        """Perform Caesar Cipher shiftcipher"""
        self.result = ''
        for i in self.msg.lower():
            try: 
                pos = string.lowercase.index(i)
            except ValueError as e: 
                self.result = "{c}{n}".format(c=self.result,n=i)
                continue
            shift_pos = pos + self.key
            if shift_pos > 25:
                shift_pos = shift_pos-25 
            self.result = "{c}{n}".format(
                c=self.result,
                n=string.lowercase[shift_pos % 26])
        self.ciphered = True
        return self.result

    def decipher(self):
        """Perform Caesar Cipher shift decipher"""
        if self.ciphered is True: 
            self.msg=self.result
            self.result=''
        for i in self.msg.lower():
            try:
                pos = string.lowercase.index(i)
            except ValueError as e:
                self.result = "{c}{n}".format(c=self.result,n=i)
                continue
            shift_pos = pos - self.key
            if shift_pos < 0:
                shift_pos = shift_pos+25
            self.result = "{c}{n}".format(
                c=self.result,
                n=string.lowercase[shift_pos % 26])
        return self.result

