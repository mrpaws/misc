""" 
    caesars_cipher.py - implementation of Caesar's Cipher

        Self-inflicted practice exercise while working on Khan Academy's
        Cryptography learning material

        https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/a/shift-cipher
"""
__author__ = 'mrpaws'

import string

class CCException(Exception):
    """Caesar's Cipher exceptions"""
    pass

class CaesarsCipher(object):
    """ Implementation of Caesar Cipher"""

    result = ''
    ciphered = False

    def get_msg(self):
        return self._msg
    def set_msg(self, msg):
        ciphered = False
        self._msg = msg    

    msg = property(get_msg, set_msg)

    def __init__(self,**kwargs):
        """Takes optional keyword parameters (msg, shift, op)"""
        self.set_msg(kwargs.get('msg',''))
        self.shift = kwargs.get('shift','')
        op = kwargs.get('op', False)
        if op is not False:
            try:
                op = getattr(self,op)
            except AttributeError as e: 
                raise CCException("Valid operations: (cipher|decipher).")
            op()
            print "(Shift: {s}): {r}".format(s=self.shift,r=self.result)

    def cipher(self):
        """Perform Caesar Cipher cipher"""
        msg = self.get_msg()
        self.result = ''
        for i in msg.lower():
            if i is ' ':
                self.result="{} ".format(self.result)
                continue
            pos = string.lowercase.index(i)
            self.result = "{}{}".format(self.result,
                string.lowercase[(pos+self.shift) % 26]) # 
        self.ciphered = True
        return self.result

    def decipher(self):
        """Perform Caesar Cipher shift decipher"""
        if self.ciphered is True:
            msg = self.result
            self.result = ''
        else: 
            msg = self.msg
        for i in msg.lower():
            if i is ' ': 
                self.result="{} ".format(self.result)
                continue
            pos = string.lowercase.index(i)
            self.result = "{c}{n}".format(
                c=self.result,
                n=string.lowercase[(pos-self.shift) % 26])
        self.ciphered = False
        return self.result

