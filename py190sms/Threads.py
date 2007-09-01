from py190sms import *
from threading import Thread
    
class CheckConnection(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = wx.GetApp()
        while 1:
            ping = self.ping()
            sleep(2)
            ping1 = self.ping()
            if ping != ping1:
                app.state_cn = ping1
                if ping1:
                    try:
                        app.win.MsgConn("Connesso", app.win.verde)
                    except: pass
                else:
                    try:
                        app.win.MsgConn("Non connesso", app.win.rosso)
                    except: pass
                    
    def ping(self):
        app = wx.GetApp()
        ping = os.popen("ping -n 1 www.google.it", "r")
        if "Impossibile" in str(ping.readlines()):
            app.state_cn = 0
            return False
        else:
            app.state_cn = 1
            return True
