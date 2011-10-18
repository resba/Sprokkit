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
import socket, sys, string, time

# Step 2: Enter your information for the bot. Incl Port of IRC Server, Nick that
# the Bot will take, host (IRC server), RealName, Channel that you want the bot
# to function in, and IDENT value.
port = 6667
nick = "Sprokkit"
host = 'irc.eu.esper.net'
name =  "SprokkitBot"
channel = '#sprokkit'
ident = 'Loveitwhenweletloose'
#Nickpasscheck: 1 - The nick requires a pass. 0 - The nick does NOT require a pass.
nickpasscheck = 1
#Nickpass: Password for Nick (If required.)
nickpass = 'changeme'

#botadmin: your nick is inputted for access to debug commands such as graceful shutdown and debug messages
botadmin = 'resba'

#DebugSwitch: For use when debug is needed.
debug = 0

# Now we just initialize socket.socket and connect to the server, giving out
# the bot's info to the server.
woot = socket.socket()
woot.connect ( (host, port) )
woot.send ( 'NICK ' + nick + '\r\n' )
woot.send ( 'USER ' + ident + ' 0 * :BukkitBot\r\n' )
global nameslist
global sentmessage
global messageable
messageable = ''
lastUsed = time.time()
# Beginning the Loop here.
while 1:
    data = woot.recv ( 1204 )
    print(data)
    globalnullvalue = ""

    def filterResponse():
        sentmessage = data
        if (debug == 1):
            woot.send ( 'PRIVMSG '+channel+' :Loaded filterResponse Function with '+sentmessage+' as the trigger. \r\n' )
        #The command has been called. First check to see what type of command was called.
        if data.find ( ':!' ) != -1:
            global messageable 
            messageable = channel
            if (debug == 1):
                woot.send ( 'PRIVMSG '+channel+' :The command was an announement ! \r\n' )
            #The command was an announcement. now we check for privilages.
            mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            if (debug == 1):
                woot.send ( 'PRIVMSG '+channel+' :Last Message: %s\r\n'%mySubString )
            atsymbol = "@"
            voicesymbol = "+"
            #If the nameslist variable contains the user with some sort of privilage. The check ends and returns to the command.
            if nameslist.find(atsymbol+mySubString) != -1:           
                if (debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are an op \r\n' )
                #because this is a global filter, the messageable is named the channel because its an announcement.
                return 0
            elif nameslist.find(voicesymbol+mySubString) != -1:
                if (debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are voiced \r\n' )
                return 0
            else:
                #If the user is NOT privilidged, then they need to jump through a few more hoops.
                if(debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are not a privilidged user \r\n' )
                if(time.time() - lastUsed) > 10:
                    global lastUsed
                    lastUsed = time.time()
                    if (debug == 1):
                        woot.send ('PRIVMSG '+channel+' :lastUsed Check Passed, now returning to command \r\n' )
                    return 0
                else:
                    if (debug == 1):
                        woot.send ( 'PRIVMSG '+channel+' :Command Cooldown Active. Ignoring Command \r\n' )
                    return 1
        elif data.find ( ':^' ) != -1:
            #The Command was a Privmsg, so we send the privmsg.
            global readUserName
            readUserName = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            global messageable 
            messageable = readUserName
            return 0
# Feelin' up the channel.
    if data.find ( '376' ) != -1:
        woot.send( 'JOIN '+channel+'\r\n' )
    if data.find ( '353' ) != -1:
        nameslist = data
        if (debug == 1):
            woot.send( 'PRIVMSG '+channel+' :Found new NAMES Listing: %s\r\n' %nameslist )
    if data.find ( 'PING' ) != -1:
        woot.send( 'PONG ' + data.split() [1] + '\r\n');
    if (nickpasscheck == 1):
        if data.find ( 'NickServ!' ) != -1:
            woot.send ( 'PRIVMSG NickServ :IDENTIFY '+nick+' '+nickpass+'\r\n' )
            nickpasscheck = 0

    if data.find ( 'test' ) != -1:
        if (filterResponse() == 0):
            woot.send( 'PRIVMSG '+messageable+' :Test command \r\n' ) 
    def debugGrace():
        global messageable
        if (messageable == ''):
            messageable = channel
        if (debug == 1):
            woot.send('PRIVMSG '+messageable+' :debugGrace() has been loaded \r\n' )
        sentmessage = data
        mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
        if (mySubString == botadmin or mySubString == botadmin2):
            if(debug == 1):
                woot.send('PRIVMSG '+messageable+' :You are one of the predefined users who can use this command. debugGrace() returns 1 \r\n' )
            return 1
        else:
            if(debug == 1):
                woot.send('PRIVMSG '+messageable+' :You are one of the predefined users who can use this command. debugGrace() returns 0 \r\n' )
            return 0
# Command to gracefully close Wikkit and disconnect it from the
# Server.
    if data.find ( '!debug.timetogo') != -1:
        thenull = ""
        if (debugGrace() == 1):
            woot.send ("QUIT :I have been Deadeded. %s\r\n" % thenull )
            woot.close()
            sys.exit()
#Toggles Debug
    if data.find ( '!debug.debug') != -1:
        if (debugGrace()==1):
            if (debug == 0):
                debug = 1
                woot.send ('PRIVMSG '+messageable+' :Debug is ON \r\n')
            elif (debug == 1):
                debug = 0
                woot.send ('PRIVMSG '+messageable+' :Debug is OFF \r\n')
#Fun debug commands
    if data.find ( '!debug.reloader' ) != -1:
        if (debugGrace()==1):
            woot.send ( 'NAMES '+messageable+' \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Boom! \r\n')
    if data.find ( '!debug.lastUsed') != -1:
        if (debugGrace()==1):
            woot.send ('PRIVMSG '+messageable+' :%s\r\n' % lastUsed )
    if data.find ( '!debug.time.time' ) != -1:
        if (debugGrace()==1):
            woot.send ('PRIVMSG '+messageable+' :%s\r\n' % time.time() )


"""