""" 
    base.py - base class for alphabetic encode implementations
"""
__author__ = 'paws@delimitize.com'

class CipherError(Exception):

    """General purpose Exception object for inheriting at will, for exceptions"""
    pass

class Cipher(object):

    """ Cipher Base Class - abstract general object mgmt/usage qol"""

    ciphered = False
    result = ''

    # used as aids for direct access via property 
    def get_msg(self):
        return self._msg
    def set_msg(self, msg):
        ciphered = False
        self.result = ''
        self._msg = msg    

    def get_shift(self):
        return self._shift
    def set_shift(self, shift):
        ciphered = False
        self.result = ''
        self._shift = shift  

    msg = property(get_msg, set_msg)
    shift = property(get_shift, set_shift)

    def __init__(self,**kwargs):
        """Takes optional keyword parameters (msg, shift, op)"""
        self.set_msg(kwargs.get('msg',''))
        self.set_shift(kwargs.get('shift',''))
        op = kwargs.get('op', False)
        if op:
            try:
                op = getattr(self,op)
            except AttributeError as e: 
                raise CipherError("Valid operations: (encode|decode).")
            op()
            print "|cipher={c}|key={s})|{r}".format(c=self.__module__.split('.')[2],
                                                 s=self.shift,
                                                 r=self.result)

    def encode(self):
        """ wrapper function for encryption"""
        if self.ciphered:
            raise CipherError("Already encoded.")
        try:
            self.result = self.doEncode(self.msg,self.shift)
        except Exception as e:
            raise CipherError("Encoding failure: {}.".format(e))
        self.ciphered = True
        return self.result

    def decode(self):
        """wrapper function for decryption"""
        if self.ciphered:
            msg = self.result 
            self.result = ''
        else:
            msg = self.msg
        try:
            self.result = self.doDecode(msg,self.shift)
        except Exception as e:
            raise CipherError("Decoding failure {}.".format(e))
        self.ciphered = False
        return self.result

    def doEncode(self):
        """override with function that encodes"""
        return None
    
    def doDecode(self):
        """override with function that decodes"""
        return None
       

