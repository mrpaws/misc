""" 
    base.py - base class for alphabetic cipher implementations
"""
__author__ = 'paws@delimitize.com'

class CipherError(Exception):
    pass

class Cipher(object):

    """ Cipher Base Class"""

    result = ''
    ciphered = False

    def get_msg(self):
        return self._msg
    def set_msg(self, msg):
        ciphered = False
        self.results = ''
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
                raise CipherError("Valid operations: (cipher|decipher).")
            op()
            print "(Shift: {s}): {r}".format(s=self.shift,r=self.result)

    def cipher(self):
        """operates cipher operations on class objects"""
        msg = self.get_msg()
        self.result = ''
        self.ciphered = True
        return False

    def decipher(self):
        """performs decipher operatoins on class objects"""
        if self.ciphered is True:
            self.set_msg(self.result)
            self.result = ''
        else: 
            msg = self.msg
        self.ciphered = False
        return False
       

