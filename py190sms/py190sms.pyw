# -*- coding: cp1252 -*-
#
# py190sms
#
# Copyright (C) 2007 by Cesco
# ceskino87@hotmail.it
#
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


# Descrizione del file
__module_name__ = "py190sms"
__module_version__ = __revision__ = versione = "0.4"
__module_description__ = "Permette di spedire SMS dal sito 190.it"

# Importazione dei moduli necessari
import wx, os, dumbdbm, shelve
import  wx.lib.dialogs
from time import sleep, localtime, ctime
from mechanoid import Browser
from Threads import *

# Assegnazione id univoco
MENU_FILE_ACCOUNT_MANAGEMENT = wx.NewId()
MENU_FILE_ADD_ACCOUNT = wx.NewId()
MENU_FILE_QUIT = wx.NewId()
MENU_RUBRICA_ADDRESSBOOK_MANAGEMENT = wx.NewId()
MENU_RUBRICA_ADD_NUMBER = wx.NewId()
MENU_ABOUT_INFO = wx.NewId()
ID_SMS_BUTTON = wx.NewId()
ID_SEND_BUTTON = wx.NewId()
ID_QUIT_BUTTON = wx.NewId()
ID_RECEIVERNUMBER = wx.NewId()
ID_MESSAGE = wx.NewId()
ID_CHAR_AVAILABLE = wx.NewId()

try:
    os.mkdir(os.getcwd()+"/db")
except: pass

try:
    os.mkdir(os.getcwd()+"/logs")
except: pass

# Database (Account e Rubrica)
db = shelve.open(os.getcwd()+"/db/py190sms_db")

# Se ci sono, carico le informazioni dal database
if db == {}:
    account = {}
    addressBook = {}
else:
    account = db["Account"]
    addressBook = db["Rubrica"]

from Dialogs import *    

class py190smsFrame(wx.Frame):
    def __init__(self):
        app = wx.GetApp()
        
        # Frame
        wx.Frame.__init__(self, None, -1, "py190sms: "+app.default_user, wx.DefaultPosition, wx.Size(260, 400), wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.CenterOnScreen()

        # Icona
        self.SetIcon(wx.Icon("img/icona.ico", wx.BITMAP_TYPE_ICO ))
        
        # Pannello
        self.panel = wx.Panel(self, -1)

        # Voce "File"
        menu_file = wx.Menu()
        submenu = wx.Menu()
        submenu.Append(MENU_FILE_ACCOUNT_MANAGEMENT, "&Gestione accounts\tCtrl+S", "Gestisci i tuoi accounts Vodafone")
        submenu.Append(MENU_FILE_ADD_ACCOUNT, "&Aggiungi un account\tCtrl+A", "Aggiungi un account Vodafone (190.it)")
        menu_file.AppendMenu(-1, "Impostazioni", submenu)
        menu_file.AppendSeparator()
        menu_file.Append(MENU_FILE_QUIT, "&Esci\tCtrl+Q", "Esci dal programma")

        # Voce "Rubrica"
        menu_addressBook = wx.Menu()
        menu_addressBook.Append(MENU_RUBRICA_ADDRESSBOOK_MANAGEMENT, "&Gestione rubrica\tCtrl+R", "Gestisci la tua rubrica personale")
        menu_addressBook.Append(MENU_RUBRICA_ADD_NUMBER, "&Aggiungi un numero\tCtrl+N", "Aggiungi un numero alla rubrica")

        # Voce "?"
        menu_about = wx.Menu()
        menu_about.Append(MENU_ABOUT_INFO, "Informazioni...", "Informazioni su py190sms")
        
        # Creazione Barra Menu' (File, Rubrica, ?)
        menuBar = wx.MenuBar()
        menuBar.Append(menu_file, "&File")
        menuBar.Append(menu_addressBook, "&Rubrica")
        menuBar.Append(menu_about, "&?")
        self.SetMenuBar(menuBar)

        # StaticBox (Account)
        wx.StaticBox(self.panel, -1, "Account", pos=(10, 5), size=(118, 55))

        # Account 
        jpg_u = wx.Image("img/user.png", wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(jpg_u), pos=(20, 27))
        self.user_txt = wx.StaticText(self.panel, -1, app.user, pos=(47, 32))
        if account == {}:   # Se non ci sono accounts modifico il frame
            self.user_txt.SetLabel("")
        else:
            self.user_txt.SetLabel(app.default_user)

        # StaticBox (Rete)
        wx.StaticBox(self.panel, -1, "Rete", pos=(133, 5), size=(112, 55))

        # Rete
        jpg_s = wx.Image("img/stato.png", wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(jpg_s), pos=(141, 27))
        self.verde = wx.Colour(0,150,0)
        self.rosso = wx.Colour(200,0,0)
        self.state_txt = wx.StaticText(self.panel, -1, "", pos=(169, 32))
        ping = os.popen("ping -n 1 www.google.it", "r")
        if "Impossibile" in str(ping.readlines()):
            self.MsgConn("Non connesso", self.rosso)
        else:
            self.MsgConn("Connesso", self.verde)

        # StaticBox (Desinatario)
        wx.StaticBox(self.panel, -1, "Destinatario", pos=(10, 70), size=(235, 55))

        # Destinatario
        self.DEST = wx.TextCtrl(self.panel, ID_RECEIVERNUMBER, "", pos=(20, 92), size=(95,20))
        wx.StaticText(self.panel, -1, "Inserisci num. Vodafone", pos=(121, 95))

        # StaticBox (Messaggio)
        wx.StaticBox(self.panel, -1, "Messaggio", pos=(10, 135), size=(235, 150))

        # Messaggio
        self.MEX = wx.TextCtrl(self.panel, ID_MESSAGE, "", pos=(20, 155), size=(215, 90), style=wx.TE_MULTILINE)
        wx.StaticText(self.panel, -1, "Caratteri disponibili:", pos=(100, 258))
        c = wx.TextCtrl(self.panel, ID_CHAR_AVAILABLE, str(app.num_c), pos=(205, 255), size=(30,20), style=wx.TE_READONLY)
        
        # Pulsanti (Sms, Invia, Esci)
        sms_image = wx.Bitmap("img/cerca.png", wx.BITMAP_TYPE_PNG)
        wx.BitmapButton(self.panel, ID_SMS_BUTTON, sms_image, pos=(10, 295))
        self.start = wx.Button(self.panel, ID_SEND_BUTTON, "Invia", pos=(85, 295), style=wx.ID_OK)
        wx.Button(self.panel, ID_QUIT_BUTTON, "Esci", pos=(170, 295))

        # Bind
        self.Bind(wx.EVT_MENU, self.Close, id=MENU_FILE_QUIT)
        self.Bind(wx.EVT_MENU, self.CallAccountManagement, id=MENU_FILE_ACCOUNT_MANAGEMENT)
        self.Bind(wx.EVT_MENU, self.CallAddAccount, id=MENU_FILE_ADD_ACCOUNT)
        self.Bind(wx.EVT_MENU, self.CallAddressBookManagement, id=MENU_RUBRICA_ADDRESSBOOK_MANAGEMENT)
        self.Bind(wx.EVT_MENU, self.CallAddNumber, id=MENU_RUBRICA_ADD_NUMBER)
        self.Bind(wx.EVT_MENU, self.AboutDialog, id=MENU_ABOUT_INFO)
        self.Bind(wx.EVT_TEXT, self.OnReceiverNumber, id=ID_RECEIVERNUMBER)
        self.Bind(wx.EVT_TEXT, lambda x: self.OnMessage(c, self.MEX), id=ID_MESSAGE)
        self.Bind(wx.EVT_BUTTON, self.ShowLogs, id=ID_SMS_BUTTON)
        self.Bind(wx.EVT_BUTTON, app.CallSendSMS, id=ID_SEND_BUTTON)
        self.Bind(wx.EVT_BUTTON, self.Close, id=ID_QUIT_BUTTON)
        self.Bind(wx.EVT_CLOSE, self.Close)

        # Creazione barra di stato
        self.CreateStatusBar(1, wx.ST_SIZEGRIP)
        self.SetStatusText("Inserisci i dati e invia il tuo SMS!")

    def MsgConn(self, msg, color):
        self.state_txt.SetLabel(msg)
        self.state_txt.SetForegroundColour(color)

    def ShowLogs(self, evt):
        app = wx.GetApp()
        year = str(localtime()[0])
        month = ctime().split(" ")[1]
        file_name = month+" "+year+".txt"
        try:
            f = open(os.getcwd()+"/logs/"+app.user+"/"+file_name, "r")
        except:
            wx.MessageBox("Ancora non hai mandato nessun SMS.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return 1
        msg = f.read()
        f.close()
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, msg, "Gli SMS inviati da "+app.user) 
        dlg.ShowModal()

    def CallAccountManagement(self, evt):
        dlg = AccountManagement()
        dlg.ShowModal()

    def CallAddNumber(self, evt):
        dlg = AddNumber()
        dlg.ShowModal()
        
    def CallAddAccount(self, evt):
        dlg = AddAccount()
        dlg.ShowModal()

    def CallAddressBookManagement(self, evt):
        dlg = AddressBookManagement()
        dlg.ShowModal()
        
    def OnReceiverNumber(self, evt):
        app = wx.GetApp()
        app.receiverNumber = evt.GetString()

    def OnMessage(self, evt, mesg):
        app = wx.GetApp()
        app.message = mesg.GetValue()
        len_stringa = len(app.message)
        caratteri = app.num_c - len_stringa
        if caratteri <= 0:
            wx.MessageBox("Il messaggio puo' contenere al massimo " + str(app.num_c) + " caratteri.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            app.message = app.message[:359]
            mesg.SetValue(app.message)
        evt.SetValue(str(caratteri))

    def AboutDialog(self, evt):
        DescriptionFile = open(os.getcwd()+"/DESCRIPTION", "r")
        DescriptionText = DescriptionFile.read()
        DescriptionFile.close()
        LicenseFile = open(os.getcwd()+"/LICENSE", "r")
        LicenseText = LicenseFile.read()
        LicenseFile.close()
        info = wx.AboutDialogInfo()
        info.Name = "py190sms"
        info.Version = versione
        info.Copyright = "Copyright (C) 2007  Francesco Pasqua"
        info.Description =  DescriptionText    
        info.WebSite = ("http://py190sms.sourceforge.net", "py190sms sul Web")
        info.Developers = ["\n\tFrancesco Pasqua (alias Cesco)", "ceskino87@hotmail.it"]
        info.License = LicenseText
        wx.AboutBox(info)
        
    def Close(self, event):
        app = wx.GetApp()
        n = self.fctClose()
        if n == 2:
            db["default_user"] = app.user
            db["Account"] = account
            db["Rubrica"] = addressBook
            db.close()
            self.Destroy()
            try:
                os.remove("rnCode.jpg")
            except: pass
        
    def fctClose(self):
        ret =  wx.MessageBox('Vuoi proprio uscire?', "Avviso", wx.YES_NO | wx.CENTRE |wx.NO_DEFAULT)
        return ret
            

class py190sms(wx.App):
    def CheckErrorConnection(self, evt):
        if self.state_cn == 0:
            wx.MessageBox("Per proseguire devi essere connesso ad Internet.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION);
            return True
        
    def CheckErrorUser(self, evt):
        self.user = self.default_user
        if self.user == "":
            wx.MessageBox("Per proseguire devi aggiungere e selezionare un account.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION);
            return True
        return False
        
    def CheckErrorNumber(self, number):
        if number == "":
            wx.MessageBox("Per proseguire devi inserire un numero di telefono cellulare.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION);
            return True
        if number.isdigit() == 0:
            wx.MessageBox("Nel numero telefonico hai inserito caratteri non numerici.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return True            
        if number[0] == "0":
            wx.MessageBox("Il numero di cellulare non puo' iniziare con 0.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return True
        if number[0:3] not in self.mobilePrefix:
            wx.MessageBox("Il numero inserito non e' un cellulare.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return True
        if len(number) < 9 or len(number) > 10:
            wx.MessageBox("Il numero di cellulare deve essere di nove o dieci cifre.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return True
        return False
    
    def CheckErrorMessage(self, evt):
        if self.message == "":
            wx.MessageBox("Per proseguire devi scrivere il tuo messaggio.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION);
            return True
        if self.message.isspace():
            wx.MessageBox("Il messaggio deve contenere almeno un carattere.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION);
            return True
        return False
        
    def CallSendSMS(self, evt):
        if self.CheckErrorConnection(self) or self.CheckErrorUser(self) or self.CheckErrorNumber(self.receiverNumber) or self.CheckErrorMessage(self):
            return True
        else:
            if self.SendSMS(self.user, self.pswd, self.receiverNumber, self.message) is not True:
                dlg = Captcha()
                dlg.ShowModal()
            
    def SendSMS(self, user, pasw, number, msg):
        step = 8
        
        dlg = wx.ProgressDialog("py190sms", "", step)

        keepGoing = True
        count = 0

        while keepGoing and count < step:
            count += 1
            wx.MilliSleep(250)

            if count == 1:
                (keepGoing, skip) = dlg.Update(count, "Connessione al sito 190.it")
                b = Browser()
                b.open("http://www.190.it/190/trilogy/jsp/home.do")
            if count == 2:
                (keepGoing, skip) = dlg.Update(count, "Invio dati personali...")
                b.select_form("loginForm")
                b["username"] = user
                b["password"] = pasw
                risp = b.submit()
            if count == 3:
                (keepGoing, skip) = dlg.Update(count, "Invio dati personali...")
                b.open("http://190.it/190/trilogy/jsp/dispatcher.do?ty_key=fdt_invia_sms&tk=9616,2")
            if count == 4:
                (keepGoing, skip) = dlg.Update(count, "Invio dati personali...")
                try:
                    query = b.follow_link(text="Continua[IMG]")
                except:
                    wx.MessageBox("Non e' possibile inviare sms. Verifica al sito 190.it!", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
                    b.close()
                    dlg.Destroy()
                    return True
                if "box_sup_limitesms.gif" in str(query.readlines()):
                    wx.MessageBox("Hai superato il limite giornaliero di SMS.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
                    b.close()
                    dlg.Destroy()
                    return True
            if count == 5:
                (keepGoing, skip) = dlg.Update(count, "Invio SMS in corso...")
                b.select_form("fsmsMessageForm")
                b["receiverNumber"] = number
                b["message"] = msg
            if count == 6:
                (keepGoing, skip) = dlg.Update(count, "Invio SMS in corso...")
                risp = b.submit()
                if "Ti ricordiamo che puoi inviare SMS via Web solo a numeri di cellulare Vodafone" in str(risp.readlines()) or "Il numero di telefono del destinatario del messaggio non e' valido" in str(risp.readlines()):
                    wx.MessageBox("Questo sito permette di inviare SMS solo ai cellulari Vodafone.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
                    b.close()
                    dlg.Destroy()
                    return True
                b.select_form("fsmsMessageForm")
            if count == 7:
                (keepGoing, skip) = dlg.Update(count, "Invio SMS in corso...")
                risp = b.submit()
            if count == 8:
                break
        dlg.Destroy()
        self.GetCapchaImage(b)
        self.state_br = b
        return False


        
    def GetCapchaImage(self, br):
        rnCode = br.open("http://www.areaprivati.190.it/190/fsms/generateimg.do")
        f = file("rnCode.jpg", "wb")
        while 1:
            data = rnCode.read(1024)
            if not data: break
            f.write(data)
        f.close()
        br.back()

    def UpgradeCaptcha(self):
        br = self.state_br
        br.reload()
        self.GetCapchaImage(br)
        self.state_br = br
        dlg = Captcha()
        dlg.ShowModal()

    def SaveSMS(self, user, number, sms):
        try:
            os.mkdir("logs/"+user)
        except: pass
        time = localtime()
        month = ctime().split(" ")[1]
        dd = str(time[2])
        mm = str(time[1])
        aa = str(time[0])
        data = dd+"/"+mm+"/"+aa
        clock = str(time[3])+":"+str(time[4])    
        file_name = month+" "+aa+".txt"
        f = open(os.getcwd()+"/logs/"+user+"/"+file_name, "a")
        f.write("A: "+number)
        f.write("\nOra: "+clock)
        f.write("\nData: "+data)
        f.write("\nMessaggio: "+sms)
        f.write("\n\n\n")
        f.close()

    def OnInit(self):        
        self.num_c = 360
        self.receiverNumber = ""
        self.message = ""
        self.mobilePrefix = [ "380", "383", "388", "389", "391", "392", "393", "373",
                          "340", "343", "346", "347", "348", "349", "377", "331",
                          "333", "334", "335", "338", "339", "363", "366", "330",
                          "336", "337", "360", "368", "320", "323", "327", "328",
                          "329" ]
        self.captcha = ""
        self.state_br = ""

        self.state_cn = ""      # True: Connesso - False: Non connesso (Il thread gli dara' il valore)
        
        # Rilevo lo stato della connessione 
        conn = CheckConnection()
        conn.start()

        try:
            if account.has_key(db["default_user"]) is not True:
                self.user = account.keys()[0]
                self.pswd = db["Account"][self.user]
                self.default_user = account.keys()[0]
            else:
                self.user = db["default_user"]
                self.pswd = db["Account"][self.user]
                self.default_user = db["default_user"]
        except:
            self.user = ""
            self.pswd = ""
            self.default_user = ""
            dlg = AddAccount()
            dlg.ShowModal()
        
        frame = py190smsFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        self.win = frame
        return True

if __name__ == '__main__':
    a = py190sms()
    a.MainLoop()
