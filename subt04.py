#!/usr/bin/python
# This Python file uses the following encoding: utf-8
# subt03.py

import wx
import sys
import os
import wx.html2

from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

# default_path_series = "\\\\BUFALITO\\share02\\SERIES"
# default_path_serien = "\\\\BUFALITO\\share02\\SERIES NUEVAS"
default_path_series = "e:\\auxiliar"
default_path_serien = "e:\\descargas"


class MyBrowser(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((800, 600))

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        # dlg = wx.MessageDialog(self,
        #    "Do you really want to close this application?",
        #    "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            #  The result is either wx.ID_OK or wx.ID_CANCEL
        # result = dlg.ShowModal()
        # dlg.Destroy()
        # if result == wx.ID_OK:
        self.Destroy()
        # The Destroy function is used to terminate the application
        # No usar CLose, es loop

class IndiceSubs(object):
    def __init__(self, serie, numpag):
        """Constructor"""
        self.id = id(self)
        self.serie = serie
        self.numpag = numpag

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

class Repo_sub(wx.Frame):

    def __init__(self, parent, id, title):

        wx.Frame.__init__(self, parent, id, title, size=(500, 600))
        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)

        self.list = CheckListCtrl(rightPanel)

        self.list.InsertColumn(0, 'Serie')
        self.list.InsertColumn(1, 'Numero')
        self.list.SetColumnWidth(0, 250)
        self.list.SetColumnWidth(1, 50)

        proceso_carpeta(default_path_series, prelistado)
        proceso_carpeta(default_path_serien, prelistado)
        prelista2 = sorted(prelistado[:])

        color_linea = 0

        for i in range(len(prelista2)):
            # prelista2[i][0] la carpeta
            # prelista2[i][1] el archivo
            # prelista2[i][2] el numero

            file_name, file_extension = os.path.splitext(prelista2[i][1])
            file_path = prelista2[i][0]
            file_num = prelista2[i][2]

            manija = self.list.InsertStringItem(sys.maxint, file_name)
            self.list.SetStringItem(manija, 1, file_num)

            color_linea += 1
            if color_linea % 2 == 0:
                self.list.SetItemBackgroundColour(manija, "white")
            else:
                self.list.SetItemBackgroundColour(manija, "yellow")

            # guardo en el listado
            renglon = IndiceSubs(serie = file_name, numpag = file_num)
            listado.append(renglon)

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        bot_sel = wx.Button(leftPanel, -1, 'Selec.todo', size=(100, -1))
        bot_des = wx.Button(leftPanel, -1, 'Deselec.todo', size=(100, -1))

        bot_subtitulo = wx.Button(leftPanel, -1, 'Pagina sub', size=(100, -1))
        bot_final = wx.Button(leftPanel, -1, 'Fin', size=(100, -1))

        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=bot_sel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=bot_des.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSubtitulo, id=bot_subtitulo.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnFin, id=bot_final.GetId())

        vbox2.Add(bot_sel, 0, wx.TOP, 5)
        vbox2.Add(bot_des)
        vbox2.Add((-1, 10))
        vbox2.Add(bot_subtitulo)
        vbox2.Add((-1, 10))
        vbox2.Add(bot_final)

        leftPanel.SetSizer(vbox2)

        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add((-1, 10))
        vbox.Add((-1, 10))

        rightPanel.SetSizer(vbox)

        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

    def OnSelectAll(self, event):
        num = self.list.GetItemCount()
        for ix in range(num):
            self.list.CheckItem(ix)

    def OnDeselectAll(self, event):
        num = self.list.GetItemCount()
        for ix in range(num):
            self.list.CheckItem(ix, False)

    def OnSubtitulo(self, event):
        num = self.list.GetItemCount()
        for yy in range(num):
            linea = listado[yy]
            if self.list.IsChecked(yy):

                dlg = wx.TextEntryDialog(None,'Ingrese pagina de '+linea.serie,'Nro ', linea.numpag)
                if dlg.ShowModal() == wx.ID_OK:
                    nro = dlg.GetValue()
                dlg.Destroy()

                # guardo en estructura
                self.list.SetStringItem(yy, 1, nro)
                self.list.CheckItem(yy, False)
                linea.numpag = nro
                # agrego en diccionario
                diccionario[linea.serie] = nro

                # visualizo pagina web
                dialog = MyBrowser(None, -1)
                el_link = "http://www.tusubtitulo.com/show/"+nro
                dialog.browser.LoadURL(el_link)
                dialog.Show()

    def OnFin(self, event):

        sigue_el_loop[0] = ["Final"]
        self.Close(True)
        self.Destroy()

def proceso_carpeta(carp, lista):
    # saco recursividad, tomo un nivel
    # pongo cartel...
    msg = "Procesando archivos ..."
    busyDlg = wx.BusyInfo(msg)

    contenido = os.listdir(carp)
    for ii in range(len(contenido)):

            item = contenido[ii]
            s = os.path.join(carp, item)
            if not (os.path.isfile(s)):
                num = diccionario.get(item," ")
                lista.append([carp,item,num])
                # print "carp=",carp," item=",item," num= ",num
    busyDlg = None

def cargo_diccionario():
    handle = open("seriesynumeros.txt")
    for line in handle:
        line = line.rstrip()
        if len(line) > 0:
            posicion = line.find("|")
            clave = line[:posicion]
            numero = line[posicion+1:]
            diccionario[clave] = numero
    handle.close()

def guardo_diccionario():
    handle = open("seriesynumeros.txt","w")
    for key in diccionario:
        clave = key
        numero = diccionario[key]
        if len(numero.rstrip())  > 0:
            linea = clave+"|"+numero+"\n"
            handle.write(linea)
    handle.close()


app = wx.App(redirect=True)

sigue_el_loop = list()
sigue_el_loop.append(["Sigue"])
# sigue_el_loop[0]: "Sigue" = loop principal

listado = list()
prelistado = list()
prelista2 = list()
diccionario = dict()

cargo_diccionario()

while sigue_el_loop[0]==["Sigue"]:

    if len(listado) > 0:
        del listado[:]
        del prelistado[:]
        del prelista2[:]

    Repo_sub(None, -1, "series y subtitulos")
    app.MainLoop()

guardo_diccionario()
