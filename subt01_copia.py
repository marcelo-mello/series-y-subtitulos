#!/usr/bin/python
# This Python file uses the following encoding: utf-8
#subt01_copia.py

import wx
import sys
import os, shutil, stat, re
import datetime

from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

miLista = list()
sigue_el_loop = list()
reps = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'n','Ñ':'N','.':' ' }


default_path_origen = "D:\descargas"
default_path_pelis = "\\\\BUFALITO\\share02\\PELICULAS"
default_path_series = "\\\\BUFALITO\\share02\\SERIES"
default_path_serien = "\\\\BUFALITO\\share02\\SERIES NUEVAS"

# default_path_origen = "E:\descargas"
# default_path_pelis = "E:"+"\\"+"nueva\peli"
# default_path_series = "E:"+"\\"+"nueva\serie"
# default_path_serien = "E:"+"\\"+"nueva"+"\\"+"nueva"

class Archivo(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, nombre, extension, tamanio, tipo, destino, capitulo):
        """Constructor"""
        self.id = id(self)
        self.nombre = nombre
        self.extension = extension
        self.tamanio = tamanio
        self.tipo = tipo
        self.destino = destino
        self.capitulo = capitulo


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)


class Repository(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(850, 600))

        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)

        self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
        self.list = CheckListCtrl(rightPanel)

        # self.cargo_contenido()

        self.list.InsertColumn(0, 'Nombre')
        self.list.InsertColumn(1, 'Ext')
        self.list.InsertColumn(2, 'Tamanio', wx.LIST_FORMAT_RIGHT)
        self.list.InsertColumn(3, 'Tipo')

        self.list.SetColumnWidth(0, 350)
        self.list.SetColumnWidth(1, 50)
        self.list.SetColumnWidth(2, 100)
        self.list.SetColumnWidth(3, 100)

        if len(miLista) > 0:
            del miLista[:]

        files = os.listdir(default_path_origen)
        # carga doble
        color_linea = 0
        for i in files:
            (name, ext) = os.path.splitext(i)
            ex = ext[1:]
            size = os.path.getsize(default_path_origen+"\\"+i)

            manija = self.list.InsertStringItem(sys.maxint, name)
            self.list.SetStringItem(manija, 1, ex)
            self.list.SetStringItem(manija, 2, str(size/1024) + ' KB')
            self.list.SetStringItem(manija, 3, "  ")

            color_linea += 1
            if color_linea % 2 == 0:
                self.list.SetItemBackgroundColour(manija, "white")
            else:
                self.list.SetItemBackgroundColour(manija, "light blue")

            remo = Archivo(nombre = name, extension = ex, tamanio = size / 1024, tipo = " ", destino=" ", capitulo=" ")
            miLista.append(remo)



        vbox2 = wx.BoxSizer(wx.VERTICAL)

        sel = wx.Button(leftPanel, -1, 'Selec.todo', size=(100, -1))
        des = wx.Button(leftPanel, -1, 'Deselec.todo', size=(100, -1))

        bot_serie = wx.Button(leftPanel, -1, 'Serie', size=(100, -1))
        bot_snuev = wx.Button(leftPanel, -1, 'Serie nueva', size=(100, -1))
        bot_peli = wx.Button(leftPanel, -1, 'Pelicula', size=(100, -1))
        bot_borrar = wx.Button(leftPanel, -1, 'Borrar', size=(100, -1))

        apply = wx.Button(leftPanel, -1, 'Procesar', size=(100, -1))
        final = wx.Button(leftPanel, -1, 'Fin', size=(100, -1))

        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=sel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=des.GetId())

        self.Bind(wx.EVT_BUTTON, self.OnSerie, id=bot_serie.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSerieN, id=bot_snuev.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnPeli, id=bot_peli.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBorrar, id=bot_borrar.GetId())

        self.Bind(wx.EVT_BUTTON, self.OnApply, id=apply.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnFin, id=final.GetId())

        vbox2.Add(sel, 0, wx.TOP, 5)
        vbox2.Add(des)
        vbox2.Add((-1, 10))
        vbox2.Add(bot_serie)
        vbox2.Add(bot_snuev)
        vbox2.Add(bot_peli)
        vbox2.Add(bot_borrar)
        vbox2.Add((-1, 10))
        vbox2.Add(apply)
        vbox2.Add((-1, 10))
        vbox2.Add(final)

        leftPanel.SetSizer(vbox2)

        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add((-1, 10))
        vbox.Add(self.log, 0.5, wx.EXPAND)
        vbox.Add((-1, 10))

        rightPanel.SetSizer(vbox)

        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        panel.SetSizer(hbox)

#       self.log.Clear()
        format = "%Y%m%d"
        today = datetime.datetime.today()
        s = "c:\python27\log_"+today.strftime(format)+".txt"
        if os.path.isfile(s):
            self.log.LoadFile(s)


        self.Centre()
        self.Show(True)


    def OnSelectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i)

    def OnDeselectAll(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i, False)

    def OnApply(self, event):
        linea = Archivo

        cuenta_serie = 0
        tot_serie = 0
        cuenta_serien = 0
        tot_serien = 0
        cuenta_pelicula = 0
        tot_pelicula = 0

        num = self.list.GetItemCount()

        for i in range(num):
            linea = miLista[i]
            if linea.tipo == "Serie":
                cuenta_serie = cuenta_serie + 1
            elif linea.tipo == "Serie nueva":
                cuenta_serien = cuenta_serien + 1
            elif linea.tipo == "Pelicula":
                cuenta_pelicula = cuenta_pelicula + 1

        self.log.AppendText("--------------------------------------"+'\n')
        self.log.AppendText("Procesando "+str(cuenta_serie)+" series, "+
        str(cuenta_serien)+" series nuevas y "+str(cuenta_pelicula)+" peliculas" + '\n')

        # primera pasada

        for i in range(num):
            linea = miLista[i]

            if linea.tipo == "Serie":

                sigo_dialogo = True

                dir_dest = default_path_series
                # pido la carpeta
                dialog = wx.DirDialog(None, "Elija carpeta de la SERIE "+linea.nombre,
                defaultPath = dir_dest, style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
                if dialog.ShowModal() == wx.ID_OK:
                    dir_dest = dialog.GetPath()
                else:
                    # corto el dialogo, no rollback
                    sigo_dialogo = False
                dialog.Destroy()

                # pido el numero de capitulo
                if sigo_dialogo:
                    tira = re.findall(r'\d+',linea.nombre)
                    capitulo = ""
                    for x in range(len(tira)):
                        capitulo += tira[x]
                    if len(capitulo) == 0:
                        capitulo = '101'

                    dlg = wx.TextEntryDialog(None,'Ingrese el nro. de capitulo de '+linea.nombre, 'Capitulo', capitulo)
                    if dlg.ShowModal() == wx.ID_OK:
                        capitulo = dlg.GetValue()
                    else:
                        # corto el dialogo, no rollback
                        sigo_dialogo = False
                    dlg.Destroy()
                if sigo_dialogo:
                    # guardo los datos ingresados
                    nuevo_destino = dir_dest
                    nuevo_capitulo = capitulo
                    nuevo_tipo = linea.tipo
                else:
                    nuevo_destino = linea.destino
                    nuevo_capitulo = linea.capitulo
                    nuevo_tipo = " "

                    self.list.SetStringItem(i, 3, " ")
                    # saco la marca de serie

                # sust en miLista
                nuevo_valor = Archivo(
                nombre = linea.nombre,
                extension = linea.extension,
                tamanio = linea.tamanio,
                tipo = nuevo_tipo,
                destino = nuevo_destino,
                capitulo = nuevo_capitulo )

                miLista[i] = nuevo_valor

            elif linea.tipo == "Serie nueva":

                sigo_dialogo = True

                dir_dest = default_path_serien
                # pido la carpeta
                dialog = wx.DirDialog(None, "Elija carpeta de la SERIE NUEVA "+linea.nombre,
                defaultPath = dir_dest, style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
                if dialog.ShowModal() == wx.ID_OK:
                    dir_dest = dialog.GetPath()
                else:
                    # corto el dialogo, no rollback
                    sigo_dialogo = False
                dialog.Destroy()

                if sigo_dialogo:
                    # pido el numero de capitulo
                    tira = re.findall(r'\d+',linea.nombre)
                    capitulo = ""
                    for x in range(len(tira)):
                        capitulo += tira[x]
                    if len(capitulo) == 0:
                        capitulo = '101'

                    dlg = wx.TextEntryDialog(None,'Ingrese el nro. de capitulo de '+linea.nombre, 'Capitulo', capitulo)
                    if dlg.ShowModal() == wx.ID_OK:
                        capitulo = dlg.GetValue()
                    else:
                        # corto el dialogo, no rollback
                        sigo_dialogo = False
                    dlg.Destroy()

                if sigo_dialogo:
                    # guardo los datos ingresados
                    nuevo_destino = dir_dest
                    nuevo_capitulo = capitulo
                    nuevo_tipo = linea.tipo
                else:
                    nuevo_destino = linea.destino
                    nuevo_capitulo = linea.capitulo
                    nuevo_tipo = " "

                    self.list.SetStringItem(i, 3, " ")

                # sust en miLista
                nuevo_valor = Archivo(
                nombre = linea.nombre,
                extension = linea.extension,
                tamanio = linea.tamanio,
                tipo = nuevo_tipo,
                destino = nuevo_destino,
                capitulo = nuevo_capitulo )

                miLista[i] = nuevo_valor

            elif linea.tipo == "Pelicula":

                sigo_dialogo = True

                dir_dest = default_path_pelis
                carpeta = replace_all(linea.nombre, reps)

                dlg = wx.TextEntryDialog(None,'Ingrese la carpeta para la PELICULA '+
                linea.nombre,'Nombre de carpeta de pelicula', carpeta)
                if dlg.ShowModal() == wx.ID_OK:
                    dir_dest = dir_dest + '\\' + dlg.GetValue()
                else:
                    # corto el dialogo, no rollback
                    sigo_dialogo = False
                dlg.Destroy()

                if sigo_dialogo:
                    # guardo los datos ingresados
                    nuevo_destino = dir_dest
                    nuevo_capitulo = "0"
                    nuevo_tipo = linea.tipo
                else:
                    nuevo_destino = linea.destino
                    nuevo_capitulo = linea.capitulo
                    nuevo_tipo = " "

                    self.list.SetStringItem(i, 3, " ")

                # sust en miLista
                nuevo_valor = Archivo(
                nombre = linea.nombre,
                extension = linea.extension,
                tamanio = linea.tamanio,
                tipo = nuevo_tipo,
                destino = nuevo_destino,
                capitulo = nuevo_capitulo )

                miLista[i] = nuevo_valor

        # segunda pasada

        for i in range(num):
            linea = miLista[i]
            today = datetime.datetime.today()
            s = today.strftime("%H:%M ")

            if linea.tipo == "Serie":
                tot_serie = tot_serie + 1
                self.log.AppendText(s+"Procesando serie "+str(tot_serie) +
                " de "+str(cuenta_serie)+" : "+ linea.nombre + "\n")

                if not Proceso_Archivo("S", linea.nombre, linea.extension, linea.destino, linea.capitulo):
                    self.log.AppendText("Error copia serie "+ linea.nombre + "\n")

            elif linea.tipo == "Serie nueva":
                tot_serien = tot_serien + 1
                self.log.AppendText(s+"Procesando serie nueva "+str(tot_serien) +
                " de "+str(cuenta_serien)+" : "+ linea.nombre + "\n")

                if not Proceso_Archivo("N", linea.nombre, linea.extension, linea.destino, linea.capitulo):
                    self.log.AppendText("Error copia serie nueva"+ linea.nombre + "\n")

            elif linea.tipo == "Pelicula":
                tot_pelicula = tot_pelicula + 1
                self.log.AppendText(s+"Procesando pelicula "+str(tot_pelicula) +
                " de "+str(cuenta_pelicula)+" : "+ linea.nombre + "\n")

                if not Proceso_Archivo("P", linea.nombre, linea.extension, linea.destino, linea.capitulo):
                    self.log.AppendText("Error copia pelicula"+ linea.nombre + "\n")

            elif linea.tipo == "Borrar":
                self.log.AppendText(s+"Borrando archivo "+ linea.nombre + "\n")
                if not Proceso_Archivo("B", linea.nombre, linea.extension, linea.destino, linea.capitulo):
                    self.log.AppendText("Error al borrar archivo "+ linea.nombre + "\n")

            self.list.SetStringItem(i, 3, " ")
            linea.tipo = " "
            miLista[i] = linea

        format = "%Y%m%d"
        today = datetime.datetime.today()
        s = today.strftime(format)
        self.log.SaveFile("c:\python27\log_"+s+".txt")

        self.Close(True)
        self.Destroy()

    def OnSerie(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            if self.list.IsChecked(i):
                self.list.SetStringItem(i, 3, "Serie")
                self.list.CheckItem(i, False)

                remo_antes = miLista[i]
                remo_antes.tipo = "Serie"
                miLista[i] = remo_antes

    def OnSerieN(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            if self.list.IsChecked(i):
                self.list.SetStringItem(i, 3, "Serie nueva")
                self.list.CheckItem(i, False)

                remo_antes = miLista[i]
                remo_antes.tipo = "Serie nueva"
                miLista[i] = remo_antes


    def OnPeli(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            if self.list.IsChecked(i):
                self.list.SetStringItem(i, 3, "Pelicula")
                self.list.CheckItem(i, False)

                remo_antes = miLista[i]
                remo_antes.tipo = "Pelicula"
                miLista[i] = remo_antes

    def OnBorrar(self, event):
        num = self.list.GetItemCount()
        for i in range(num):
            if self.list.IsChecked(i):
                self.list.SetStringItem(i, 3, "Borrar")
                self.list.CheckItem(i, False)

                remo_antes = miLista[i]
                remo_antes.tipo = "Borrar"
                miLista[i] = remo_antes

    def OnFin(self, event):

        format = "%Y%m%d"
        today = datetime.datetime.today()
        s = today.strftime(format)
        self.log.SaveFile("c:\python27\log_"+s+".txt")
        sigue_el_loop[0] = ["Final"]
        self.Close(True)
        self.Destroy()

def Proceso_Archivo(tip, nom, exx, dest, capt):

    if (tip == "S") or (tip == "N"):

        num_capitulo = int(capt)
        num_temporada = int(num_capitulo / 100)
        if num_temporada < 10:
            str_temporada = "S0"+str(num_temporada)
        else:
            str_temporada = "S"+str(num_temporada)

        carpeta_temporada = os.path.join(dest,str_temporada)

        if not os.path.exists(carpeta_temporada):
                os.makedirs(carpeta_temporada)

        # copio el archivo

        copia_origen = os.path.join(default_path_origen,nom+"."+exx)
        copia_destino =os.path.join(carpeta_temporada,capt+" "+nom+"."+exx)

    elif tip == "P":
        # copio el archivo

        if not os.path.exists(dest):
                os.makedirs(dest)

        copia_origen = os.path.join(default_path_origen,nom+"."+exx)
        copia_destino =os.path.join(dest,nom+"."+exx)
    else:
        copia_origen = os.path.join(default_path_origen,nom+"."+exx)

    sigue = True
    if tip == "B":
        # borra archivo
        os.chmod(copia_origen,stat.S_IWRITE)
        os.remove(copia_origen)

    else:
        if not os.path.isfile(copia_destino):
            try:
                shutil.copy2(copia_origen, copia_destino)
            except shutil.Error as e:
                # print "Error de copia: " + e
                sigue = False
            except IOError as e:
                # print "Error IO de copia: " + e
                sigue = False
        if sigue:
            os.chmod(copia_origen,stat.S_IWRITE)
            os.remove(copia_origen)
    return sigue

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

app = wx.App()
sigue_el_loop.append(["Sigue"])
while sigue_el_loop[0]==["Sigue"]:
    Repository(None, -1, 'Procesador de descargas')
    app.MainLoop()
