import wx
from py190sms import *

ID_USERNAME = wx.NewId()
ID_PASSWORD = wx.NewId()
ID_CAPTCHA = wx.NewId()
ID_CAPTCHA_OK = wx.NewId()
ID_CAPTCHA_AGGIORNA = wx.NewId()
ID_NAME = wx.NewId()
ID_NUMBER = wx.NewId()

#####      
#
#   Account   
#   
#
class AccountManagement(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "Gestione", size=(186,220))

        app = wx.GetApp()

        # StaticBox
        wx.StaticBox(self, -1, "Account Vodafone", pos=(10, 5), size=(160, 173))
        
        # Immagine Account
        img = wx.Image("img/account.png", wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(img), pos=(65, 35))

        # Combobox (lista accounts)
        cb = wx.ComboBox(self, -1, app.user, (30, 103), (119, -1), account.keys(), wx.CB_READONLY)
        
        # Pulsante "Aggiungi account"
        ID_ADD_BUTTON = wx.NewId()
        add_image = wx.Bitmap("img/add.png", wx.BITMAP_TYPE_PNG)
        add_button = wx.BitmapButton(self, ID_ADD_BUTTON, add_image, pos=(30, 135))
        add_button.SetToolTipString("Aggiungi account")

        # Pulsante "Rimuovi account"
        ID_DEL_BUTTON = wx.NewId()
        del_image = wx.Bitmap("img/del.png", wx.BITMAP_TYPE_PNG)
        del_button = wx.BitmapButton(self, ID_DEL_BUTTON, del_image, pos=(75, 135))
        del_button.SetToolTipString("Rimuovi account")

        # Pulsante "Applica account"
        ID_APPLY_BUTTON = wx.NewId()
        apply_image = wx.Bitmap("img/apply.png", wx.BITMAP_TYPE_PNG)
        apply_button = wx.BitmapButton(self, ID_APPLY_BUTTON, apply_image, pos=(120, 135))
        apply_button.SetToolTipString("Applica account selezionato")

        # Bind
        self.Bind(wx.EVT_BUTTON, self.Add, id=ID_ADD_BUTTON)
        self.Bind(wx.EVT_BUTTON, self.Del, id=ID_DEL_BUTTON)
        self.Bind(wx.EVT_BUTTON, self.Apply, id=ID_APPLY_BUTTON)
        self.Bind(wx.EVT_TEXT, self.OnSelection, cb)
        self.Bind(wx.EVT_CLOSE, self.Close)

    def OnSelection(self, evt):
        self.selection = evt.GetString()

    def Add(self, evt):
        self.Destroy()
        if account == {}:
            self.CreateAccountDefault()
            return 0
        dlg = AddAccount()
        dlg.ShowModal()

    def Del(self, evt):
        if self.CheckError():
            return 1
        try:
            del account[self.selection]
            if account == {}:
                app.default_user = ""               
        except:
            pass
        self.Destroy()
        dlg = AccountManagement()
        dlg.ShowModal()

    def CreateAccountDefault(self):
            app = wx.GetApp()
            app.user = ""
            dlg = AddAccount()
            dlg.ShowModal()

    def Apply(self, evt):
        app = wx.GetApp()
        if self.CheckError():
            return 1
        app.user = self.selection
        app.pswd = account[app.user]
        app.default_user = self.selection
        app.win.user_txt.SetLabel(self.selection)   # Modifico il valore (account) del frame principale
        app.win.SetTitle("py190sms: "+self.selection)    # Modifico il titolo del frame principale
        self.Destroy()
        
    def CheckError(self):
        try:
            self.selected = self.selection
            return 0
        except:
            wx.MessageBox("Non hai selezionato nessun account.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return 1

    def Close(self, event):
        app = wx.GetApp()
        if account == {}:
            n = self.MsgClose()
            if n == 2:
                app.win.user_txt.SetLabel("")
                app.win.SetTitle("py190sms: ")
                self.Destroy()
        if account.has_key(app.user) is not True:
                app.win.user_txt.SetLabel("")
                app.win.SetTitle("py190sms: ") 
        self.Destroy()
        
    def MsgClose(self):
        ret =  wx.MessageBox('Sicuro di non voler creare un account predefinito?', "Avviso", wx.YES_NO | wx.CENTRE |wx.NO_DEFAULT)
        return ret
        
class AddAccount(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "py190sms", size=(200,265))

        app = wx.GetApp()

        self.username = ""
        self.password = ""

        # StatixBox
        wx.StaticBox(self, -1, "Dati account Vodafone", pos=(10, 5), size=(174, 218))

        # Immagine Login
        img = wx.Image("img/login.png", wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(img), pos=(71, 35))

        # Username
        wx.StaticText(self, -1, "Username", pos=(35, 100))
        self.user = wx.TextCtrl(self, ID_USERNAME, "", pos=(35, 115), size=(124, 20))

        # Password
        wx.StaticText(self, -1, "Password", pos=(35, 145))
        self.pasw = wx.TextCtrl(self, ID_PASSWORD, "", pos=(35, 160), size=(124, 20), style=wx.TE_PASSWORD)

        # Pulsante "OK"
        ID_OK_BUTTON = wx.NewId()
        ok_image = wx.Bitmap("img/apply_pic.png", wx.BITMAP_TYPE_PNG)
        ok_button = wx.BitmapButton(self, ID_OK_BUTTON, ok_image, pos=(35, 189), size=(50,25))
        ok_button.SetToolTipString("Aggiungi questo account")

        # Pulsante "RESET"
        ID_RESET_BUTTON = wx.NewId()
        reset_image = wx.Bitmap("img/cancel.png", wx.BITMAP_TYPE_PNG)
        reset_button = wx.BitmapButton(self, ID_RESET_BUTTON, reset_image, pos=(109, 189), size=(50,25))
        reset_button.SetToolTipString("Cancella i dati inseriti")
        
        # Bind
        self.Bind(wx.EVT_TEXT, self.OnUsername, id=ID_USERNAME)
        self.Bind(wx.EVT_TEXT, self.OnPassword, id=ID_PASSWORD)
        self.Bind(wx.EVT_BUTTON, self.Ok, id=ID_OK_BUTTON)
        self.Bind(wx.EVT_BUTTON, self.Reset, id=ID_RESET_BUTTON)
        self.Bind(wx.EVT_CLOSE, self.Close)
        
    def OnUsername(self, evt):
        self.username = evt.GetString()
    
    def OnPassword(self, evt):
        self.password = evt.GetString()

    def Ok(self, evt):
        app = wx.GetApp()
        if app.CheckErrorConnection(self):
            return 0 
        if self.username == "":
            wx.MessageBox("Per proseguire devi inserire il tuo Username.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return 0
        if self.password == "":
            wx.MessageBox("Per proseguire devi inserire la tua Password.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return 0
        if self.CheckAccount(self.username, self.password):
            wx.MessageBox("Username o password non corretti.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return 0
        if app.user == "" or account == {}:
            app.user = self.username
            app.pswd = self.password
            app.default_user = app.user
            try:
                app.win.user_txt.SetLabel(app.user)
            except: pass
            account[self.username] = self.password
            wx.MessageBox("L'account "+self.username+" e' stato impostato come predefinito.", "py190sms", wx.OK | wx.ICON_INFORMATION)
            self.Destroy()
        else:
            account[self.username] = self.password
            wx.MessageBox("E' stato aggiunto il nuovo Account.", "py190sms", wx.OK | wx.ICON_INFORMATION)
            self.Destroy()
            dlg = AccountManagement()
            dlg.ShowModal()

    def Reset(self, evt):
        self.user.SetValue("")
        self.pasw.SetValue("")

    def Close(self, event):
        app = wx.GetApp()
        if account == {}:
            n = self.MsgClose()
            if n == 2:
                self.Destroy()
        else:
            self.Destroy()
        
    def MsgClose(self):
        ret =  wx.MessageBox('Sicuro di non voler creare un account predefinito?', "Avviso", wx.YES_NO | wx.CENTRE |wx.NO_DEFAULT)
        return ret

    def CheckAccount(self, user, pasw):
        b = Browser()
        b.open("http://www.190.it/190/trilogy/jsp/home.do")
        b.select_form("loginForm")
        b["username"] = user
        b["password"] = pasw
        risp = b.submit()
        if "loginFailed.do" in b.geturl():
            b.close()
            return 1
        b.close()
        return 0


#####      
#
#   Captcha   
#   
#
class Captcha(wx.Dialog):
    def __init__(self):   
        wx.Dialog.__init__(self, None, -1, "Captcha", size=(205,187))

        app = wx.GetApp()

        # StaticBox
        wx.StaticBox(self, -1, "Inserisci codice", pos=(10, 5), size=(180, 140))

        # Immagine Codice Captcha
        self.CaptchaImage()

        # Captcha
        wx.TextCtrl(self, ID_CAPTCHA, "", pos=(51, 74), size=(100, 20))
        
        # Pulsante "Ok"
        wx.Button(self, ID_CAPTCHA_OK, "Ok", pos=(103, 110))

        # Pulsante "Aggiorna"
        wx.Button(self, ID_CAPTCHA_AGGIORNA, "Aggiorna", pos=(23, 110))

        # Bind
        self.Bind(wx.EVT_BUTTON, self.Ok, id=ID_CAPTCHA_OK)
        self.Bind(wx.EVT_TEXT, self.OnCaptcha, id=ID_CAPTCHA)        
        self.Bind(wx.EVT_BUTTON, self.UpdateCaptcha, id=ID_CAPTCHA_AGGIORNA)
        self.Bind(wx.EVT_CLOSE, self.Close)

    def OnCaptcha(self, evt):
        app = wx.GetApp()
        app.captcha = evt.GetString()

    def CaptchaImage(self):
        captcha_image = wx.Image("rnCode.jpg", wx.BITMAP_TYPE_JPEG)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(captcha_image), pos=(24, 30))
                  
    def UpdateCaptcha(self, evt):
        self.Close(self)
        app = wx.GetApp()
        app.UpgradeCaptcha()
        
    def Ok(self, evt):
        app = wx.GetApp()
        brw = app.state_br
        if app.captcha == "":
            wx.MessageBox("Per proseguire devi inserire il codice segreto.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return 0
        brw.select_form("fsmsMessageForm")
        brw["verifyCode"] = app.captcha
        risp = brw.submit()
        if "send.do" in brw.geturl():
            wx.MessageBox("Messaggio inviato.", "py190sms", wx.OK | wx.ICON_INFORMATION)
            self.Destroy()
            os.remove("rnCode.jpg")
            app.SaveSMS(app.user, app.receiverNumber, app.message)
            brw.close()
            return 0
        if "prepare.do" in brw.geturl():
            wx.MessageBox("Codice segreto errato. Riprova.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            self.UpdateCaptcha(self)
            return 0
        
    def Close(self, evt):
        self.Destroy()

        
#####      
#
#   Rubrica   
#   
#
class AddressBookManagement(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "Gestione", size=(186,220))

        app = wx.GetApp()

        # StaticBox
        wx.StaticBox(self, -1, "Rubrica", pos=(10, 5), size=(160, 173))
        
        # Immagine Rubrica
        img = wx.Image("img/rubrica.png", wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(img), pos=(65, 35))

        # Combobox (lista persone)
        cb = wx.ComboBox(self, -1, "", (30, 103), (119, -1), addressBook.keys(), wx.CB_READONLY)
        
        # Pulsante "Aggiungi Numero"
        ID_ADD_BUTTON = wx.NewId()
        add_image = wx.Bitmap("img/add.png", wx.BITMAP_TYPE_PNG)
        add_button = wx.BitmapButton(self, ID_ADD_BUTTON, add_image, pos=(30, 135))
        add_button.SetToolTipString("Aggiungi numero")

        # Pulsante "Rimuovi account"
        ID_DEL_BUTTON = wx.NewId()
        del_image = wx.Bitmap("img/del.png", wx.BITMAP_TYPE_PNG)
        del_button = wx.BitmapButton(self, ID_DEL_BUTTON, del_image, pos=(75, 135))
        del_button.SetToolTipString("Rimuovi numero")

        # Pulsante "Applica account"
        ID_APPLY_BUTTON = wx.NewId()
        apply_image = wx.Bitmap("img/apply.png", wx.BITMAP_TYPE_PNG)
        apply_button = wx.BitmapButton(self, ID_APPLY_BUTTON, apply_image, pos=(120, 135))
        apply_button.SetToolTipString("Scegli numero selezionato")

        # Bind
        self.Bind(wx.EVT_BUTTON, self.Add, id=ID_ADD_BUTTON)
        self.Bind(wx.EVT_BUTTON, self.Del, id=ID_DEL_BUTTON)
        self.Bind(wx.EVT_BUTTON, self.Apply, id=ID_APPLY_BUTTON)
        self.Bind(wx.EVT_TEXT, self.OnSelection, cb)
        self.Bind(wx.EVT_CLOSE, self.Close)

    def OnSelection(self, evt):
        self.selection = evt.GetString()

    def Add(self, evt):
        self.Destroy()
        dlg = AddNumber()
        dlg.ShowModal()

    def Del(self, evt):
        if self.CheckError():
            return 1
        try:
            del addressBook[self.selection]
        except:
            pass
        self.Destroy()
        dlg = AddressBookManagement()
        dlg.ShowModal()

    def Apply(self, evt):
        app = wx.GetApp()
        if self.CheckError():
            return 1
        app.receiverNumber = addressBook[self.selected]
        app.win.DEST.SetValue(app.receiverNumber)
        self.Destroy()
        
    def CheckError(self):
        try:
            self.selected = self.selection
            return 0
        except:
            wx.MessageBox("Non hai selezionato nessun numero.", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return 1

    def Close(self, event):
        self.Destroy()

class AddNumber(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "Rubrica", size=(200,265))

        self.name = ""
        self.number = ""

        # StatixBox
        wx.StaticBox(self, -1, "Inserisci numero Vodafone", pos=(10, 5), size=(174, 218))

        # Immagine Rubrica
        img = wx.Image("img/rubrica.png", wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(img), pos=(71, 35))

        # Nome
        wx.StaticText(self, -1, "Nome", pos=(35, 100))
        self.name_textctrl = wx.TextCtrl(self, ID_NAME, "", pos=(35, 115), size=(124, 20))

        # Numero
        wx.StaticText(self, -1, "Numero", pos=(35, 145))
        self.number_textctrl = wx.TextCtrl(self, ID_NUMBER, "", pos=(35, 160), size=(124, 20))

        # Pulsante "OK"
        ID_OK_BUTTON = wx.NewId()
        ok_image = wx.Bitmap("img/apply_pic.png", wx.BITMAP_TYPE_PNG)
        ok_button = wx.BitmapButton(self, ID_OK_BUTTON, ok_image, pos=(35, 189), size=(50,25))
        ok_button.SetToolTipString("Aggiungi questo numero")

        # Pulsante "RESET"
        ID_RESET_BUTTON = wx.NewId()
        reset_image = wx.Bitmap("img/cancel.png", wx.BITMAP_TYPE_PNG)
        reset_button = wx.BitmapButton(self, ID_RESET_BUTTON, reset_image, pos=(109, 189), size=(50,25))
        reset_button.SetToolTipString("Cancella i dati inseriti")
        
        # Bind
        self.Bind(wx.EVT_TEXT, self.OnName, id=ID_NAME)
        self.Bind(wx.EVT_TEXT, self.OnNumber, id=ID_NUMBER)
        self.Bind(wx.EVT_BUTTON, self.Ok, id=ID_OK_BUTTON)
        self.Bind(wx.EVT_BUTTON, self.Reset, id=ID_RESET_BUTTON)
        self.Bind(wx.EVT_CLOSE, self.Close)
        
    def OnName(self, evt):
        self.name = evt.GetString()
    
    def OnNumber(self, evt):
        self.number = evt.GetString()

    def Ok(self, evt):
        app = wx.GetApp()
        if self.name == "":
            wx.MessageBox("Per proseguire devi inserire il Nome", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return True
        if self.number == "":
            wx.MessageBox("Per proseguire devi inserire il Numero", "Attenzione", wx.OK | wx.ICON_EXCLAMATION)
            return True
        if app.CheckErrorNumber(self.number):
            return True
        addressBook[self.name] = self.number
        wx.MessageBox("E' stato aggiunto il nuovo numero.", "py190sms", wx.OK | wx.ICON_INFORMATION)
        self.Destroy()
        dlg = AddressBookManagement()
        dlg.ShowModal()

    def Reset(self, evt):
        self.name_textctrl.SetValue("")
        self.number_textctrl.SetValue("")

    def Close(self, event):
        self.Destroy()

        
