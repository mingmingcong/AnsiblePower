#coding=utf-8
import base64
from string import join
from Crypto.Cipher import AES




class Encrypt(object):

    AES_KEY = '452741f662c2d5e1'

    @staticmethod
    def encrypt(text):
        """
        AES加密，文本必须要16的倍数，不是则补足。
        :return:
        """
        key = Encrypt.AES_KEY
        cryptor = AES.new(key,AES.MODE_ECB)

        length = 16
        count = len(text)
        add = length - (count % length)
        text += ('\0' * add)
        ciphertext = base64.encodestring(cryptor.encrypt(text))
        return join(ciphertext.split('\n'),'')



    @staticmethod
    def decrypt(text):
        """
        解码时去掉末尾空格
        """
        key = Encrypt.AES_KEY
        cryptor = AES.new(key,AES.MODE_ECB)
        plain_text = cryptor.decrypt(base64.decodestring(text))
        return plain_text.rstrip('\0')


print  Encrypt.encrypt("ewewewew")