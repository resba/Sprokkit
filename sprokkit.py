#!/usr/bin/python
# Sprokkit IRC Bot. Built to test socket.socket() permissions.
# Script by Resba
# Version: 0.1
# 
# License: Do not remove this original copyright for fair use. 
# Give credit where credit is due!
# 
#
# NOTE: All commented lines of CODE are debug messages for when something goes wrong.

# Step 1: Import all the necessary libraries.
import socket, sys, string, time, feedparser

# Step 2: Enter your information for the bot. Incl Port of IRC Server, Nick that
# the Bot will take, host (IRC server), RealName, Channel that you want the bot
# to function in, and IDENT value.
port = 6667
nick = 'Sprokkit'
host = 'canis.esper.net'
name =  "Nothing Short of a Miracle"
channel = '#bukkitwikibots'
ident = 'ilikeoctogons'

# Now we just initialize socket.socket and connect to the server, giving out
# the bot's info to the server.
woot = socket.socket()
woot.connect ( (host, port) )
woot.send ( 'NICK ' + nick + '\r\n' )
woot.send ( 'USER ' + ident + ' ' +  ident + ' ' + ident + ' :Sprokkit\r\n' )
global nameslist
global sentmessage
global messageable
lastUsed = time.time()
# Beginning the Loop here.
while 1:
    data = woot.recv ( 1204 )
    print(data)
    globalnullvalue = ""

    def filterResponse():
        sentmessage = data
        woot.send ( 'PRIVMSG '+channel+' :Loaded filterResponse Function with '+sentmessage+' as the trigger. \r\n' )
        #The command has been called. First check to see what type of command was called.
        if data.find ( '!' ) != -1:
            woot.send ( 'PRIVMSG '+channel+' :The command was an announement ! \r\n' )
            #The command was an announcement. now we check for privilages.
            mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            woot.send ( 'PRIVMSG '+channel+' :Last Message: %s\r\n'%mySubString )
            atsymbol = "@"
            voicesymbol = "+"
            #Following Declarations of Privilidged Symbols, we run a names check.
            woot.send ( 'NAMES ' + channel + ' \r\n' )
            nameslist = data
            #If the nameslist variable contains the user with some sort of privilage. The check ends and returns to the command.
            if nameslist.find(atsymbol+mySubString) != -1:           
                woot.send ( 'PRIVMSG '+channel+' :You are an op \r\n' )
                #because this is a global filter, the messageable is named the channel because its an announcement.
                messageable = channel
                return 0
            elif nameslist.find(voicesymbol+mySubString) != -1:
            	woot.send ( 'PRIVMSG '+channel+' :You are voiced \r\n' )
            	messageable = channel
                return 0
            else:
                #If the user is NOT privilidged, then they need to jump through a few more hoops.
                woot.send ( 'PRIVMSG '+channel+' :You are not a privilidged user \r\n' )
                if(time.time() - lastUsed) > 10:
                    global lastUsed
                    lastUsed = time.time()
                    woot.send ('PRIVMSG '+channel+' :lastUsed Check Passed, now returning to command \r\n' )
                    messageable = channel
                    return 0
                else:
                    woot.send ( 'PRIVMSG '+channel+' :Command Cooldown Active. Ignoring Command \r\n' )
                    return 1
        elif data.find ( '^' ) != -1:
            #The Command was a Privmsg, so we send the privmsg.
            global readUserName
            readUserName = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            messageable = readUserName
            return 0
# Feelin' up the channel.
    if data.find ( '376' ) != -1:
        woot.send( 'JOIN '+channel+'\r\n' )
    if data.find ( '353' ) != -1:
        nameslist = data
        woot.send( 'PRIVMSG '+channel+' :Found new NAMES Listing: %s\r\n' %nameslist )
    if data.find ( 'PING' ) != -1:
        woot.send( 'PONG ' + data.split() [1] + '\r\n')        	
    if data.find ( 'MODE' ) != -1:
        woot.send ( 'PRIVMSG '+channel+' :MODE Command Was Sent. \r\n' )
        woot.send ( 'NAMES ' + channel + ' \r\n' )

    if data.find ( 'test' ) != -1:
        if (filterResponse() == 0):
            woot.send( 'PRIVMSG '+messageable+' :Test command ' ) 

# Debug commands to help with Sprokkit Development.
    if data.find ( '!debug:say' ) != -1:
        lastMessage = data
        parsedMessage = lastMessage[lastMessage.find("!debug:say")+1:lastMessage.find("~.")]
        woot.send ( 'PRIVMSG '+channel+' :%s\r\n' % parsedMessage )
    if data.find ( '!debug:reloader' ) != -1:
        woot.send ( 'NAMES '+channel+' \r\n' )
    if data.find ( 'MODE' ) != -1:
        woot.send ( 'PRIVMSG '+channel+' :MODE Command Was Sent. \r\n' )
        woot.send ( 'NAMES '+channel+' \r\n' )
    if data.find ( '!debug:lastUsed') != -1:
        woot.send ("PRIVMSG "+channel+" :%s\r\n" % lastUsed )
    if data.find ( '!debug:time.time' ) != -1:
        woot.send ("PRIVMSG "+channel+" :%s\r\n" % time.time() )

"""
# Command Cooldown function. Basically checks to see if its been about 5 seconds
# before someone is allowed to use another one of Wikkity's commands.
    def commandCooldown():
#        woot.send ( 'PRIVMSG '+channel+' :Loaded commandCooldown Function \r\n' )
        if(time.time() - lastUsed) > 10:
            global lastUsed
            lastUsed = time.time()
#            woot.send ("PRIVMSG "+channel+" :lastUsed Check Passed, now returning to command %s\r\n" % globalnullvalue)
            return 0
        else:
#            woot.send ( 'PRIVMSG '+channel+' :Command Cooldown Active. Ignoring Command \r\n' )
            return 1
#        woot.send ( 'PRIVMSG '+channel+' :lastUsed Check Completed \r\n' )
    def readUser():
    	if data.find ( '^' ) != -1:
    	    lastmessage = data
            global readUserName
            readUserName = lastmessage[lastmessage.find(":")+1:lastmessage.find("!")]
            messageable = readUserName
            return 0
        elif data.find( '!' ) != -1:
            return 0
"""