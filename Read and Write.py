#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        # secteur utilisé
        sectorBlock = 2

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A,  sectorBlock, key, uid)
        print ("\n")

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            # Variable for the data to write
            #data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
            data = [] #[0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            
            # Fill the data with 0xFF
            #for x in range(0,15):
            #    data.append(0xFF)
            #print ("Sector initialized with :", data)
            
            # Read block 
            MIFAREReader.MFRC522_Read( sectorBlock, data)
            print ("Sector read :", data)
            
            # ajouter 1 au premier octet du secteur
            #arr = bytearray(data)
            data[0] = data[0] + 1
            print ("Sector modified :", data)
            
            # Write the data
            MIFAREReader.MFRC522_Write( sectorBlock, data)
            print ("sector written")

            # Check to see if it was written
            data = []
            MIFAREReader.MFRC522_Read(sectorBlock,data)
            print ("Sector check :", data)

           # data = []
            # Fill the data with 0x00
            #for x in range(0,16):
             #   data.append(0x00)

            #print "Now we fill it with 0x00:"
            #MIFAREReader.MFRC522_Write(sectorBlock, data)
            #print "\n"

            #print ("It is now empty:")
            # Check to see if it was written
            #MIFAREReader.MFRC522_Read(sectorBlock)
            #print ("\n")

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
             # continue_reading = False
        else:
            print ("Authentication error")