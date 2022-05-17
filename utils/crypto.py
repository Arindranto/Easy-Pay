# -*- coding: Utf-8 -*-

# This file contain the crypting methods for datas
def crypt(txt):
    "Crypt the text using Cesar's cryptography variation"
    crypted= ''
    for letter in txt:
        # Crypt only ASCII characters
        order= ord(letter)
        # Uppercase letters with key 13
        if (order >= ord('A') and order <= ord('Z')):
            crypted+= chr((order - ord('A') + 13) % 26 + ord('A'))
        # Lowercase letters with key 9
        elif (order >= ord('a') and order <= ord('z')):
            crypted+= chr((order - ord('a') + 9) % 26 + ord('a'))
        # Numbers with key 5
        elif (order >= ord('0') and order <= ord('9')):
            crypted+= chr((order - ord('0') + 5) % 10 + ord('0'))
        # Spaces replaced by *
        elif letter == ' ':
            crypted+= '*'
        # * replaced by a space
        elif letter == '*':
            crypted+= ' '
        # Other character
        else:
            crypted+= letter
    return crypted

###############################################################################################################################################################
def decrypt(txt):
    "Decrypt the text using Cesar's cryptography variation"
    decrypted= ''
    for letter in txt:
        # Crypt only ASCII characters
        order= ord(letter)
        # Uppercase letters with key 13
        if (order >= ord('A') and order <= ord('Z')):
            decrypted+= chr((order - ord('A') - 13) % 26 + ord('A'))
        # Lowercase letters with key 9
        elif (order >= ord('a') and order <= ord('z')):
            decrypted+= chr((order - ord('a') - 9) % 26 + ord('a'))
        # Numbers with key 5
        elif (order >= ord('0') and order <= ord('9')):
            decrypted+= chr((order - ord('0') - 5) % 10 + ord('0'))
        # Spaces replaced by *
        elif letter == ' ':
            decrypted+= '*'
        # * replaced by a space
        elif letter == '*':
            decrypted+= ' '
        # Other character
        else:
            decrypted+= letter
    return decrypted

###############################################################################################################################################################
def normalize(txt):
    "Make every word beginning in capital letter"
    return txt.title()  # Actually an existing python function
    '''word_list= txt.split()
    txt= ''
    for word in word_list:
        txt+= word.capitalize() + ' '    # A space between the letters
    txt= txt[0:len(txt) - 1]
    return txt'''

###############################################################################################################################################################
if __name__ == '__main__':
    word= input('Enter the text to encrypt: ')
    crypted= crypt(word)
    print('Crypted: ', crypted)
    print('Decrypted: ', decrypt(crypted))
    print('Normalized: ', normalize(word))