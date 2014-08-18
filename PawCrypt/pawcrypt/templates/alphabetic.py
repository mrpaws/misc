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

    @property
    def msg(self):
        """the message for operation"""
        return self._msg

    @msg.setter
    def msg(self, msg):
        ciphered = False
        self.result = ''
        self._msg = msg    

    @property
    def shift(self):
        """the shift or key """
        return self._shift

    @shift.setter
    def shift(self, shift):
        ciphered = False
        self.result = ''
        if type(shift) is str:
            shift = shift.lower()
        self._shift = shift  

    def __init__(self,**kwargs):
        """Takes optional keyword parameters (msg, shift, op)"""
        self.msg = kwargs.get('msg','')
        self.shift = kwargs.get('shift','')
        op = kwargs.get('op', False)
        if op:
            try:
                op = getattr(self,op)
            except AttributeError as e: 
                raise CipherError("valid operations: (encode|decode).")
            op()
            print "cipher={c}|key={s}|{r}".format(c=self.__module__.split('.')[2],
                                                  s=self.shift,
                                                  r=self.result)

    def encode(self):
        """ wrapper function for encryption"""
        if self.ciphered:
            raise CipherError("already encoded.")
        try:
            self.result = self.doEncode(self.msg,self.shift)
        except Exception as e:
            raise CipherError("encoding failure: {}.".format(e))
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
            raise CipherError("decoding failure {}.".format(e))
        self.ciphered = False
        return self.result

    def doEncode(self):
        """override with function that encodes"""
        raise CipherError("override this func and return the encoded msg")
    
    def doDecode(self):
        """override with function that decodes"""
        raise CipherError("override this funct and return the decoded msg")
       
