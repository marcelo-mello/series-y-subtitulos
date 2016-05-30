#!/usr/bin/python
# This Python file uses the following encoding: utf-8
# subt02_pega.py

import wx
import sys
import os, shutil, stat, re, copy
import datetime, time
import wx.html2

from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

reps = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'n','Ñ':'N','.':' ' }

default_path_origen = "D:\\descargas"
default_path_pelis = "\\\\BUFALITO\\share02\\PELICULAS"
default_path_series = "\\\\BUFALITO\\share02\\SERIES"
default_path_serien = "\\\\BUFALITO\\share02\\SERIES NUEVAS"

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
        self.Destroy()

#----------------------------------------------------------------------
class Archivo(object):
    def __init__(self, serie, capitulo, extension, accion, archsub, tipo):
        """Constructor"""
        self.id = id(self)
        self.serie = serie
        self.capitulo = capitulo
        self.extension = extension
        self.accion = accion
        self.archsub = archsub
        self.tipo = tipo

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

class Repository(wx.Frame):

    def __init__(self, parent, id, title):

        def guardo_en_control(self,el_path,la_serie,la_ext,el_status,el_tipo,el_color):

            # si es parcial y marcado no lo agrego
            if not ((el_status[:3] == "***") and (sigue_el_loop[1] == ["PARCIAL"])):

                manija = self.list.InsertStringItem(sys.maxint, el_path[19:])
                self.list.SetStringItem(manija, 1, la_serie)
                self.list.SetStringItem(manija, 2, la_ext)
                self.list.SetStringItem(manija, 3, el_status)

                if el_status[:3] == "***":
                    self.list.SetItemBackgroundColour(manija, "green")
                elif color_linea % 2 == 0:
                    self.list.SetItemBackgroundColour(manija, "white")
                else:
                    self.list.SetItemBackgroundColour(manija, "yellow")

                # guardo en el listado
                renglon = Archivo(
                serie = el_path,
                capitulo = la_serie,
                extension = la_ext,
                accion = el_status,
                archsub = " ",
                tipo = el_tipo)
                listado.append(renglon)

        wx.Frame.__init__(self, parent, id, title, size=(850, 600))

        renglon = Archivo
        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)

        self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
        self.list = CheckListCtrl(rightPanel)

        self.list.InsertColumn(0, 'Ubicacion')
        self.list.InsertColumn(1, 'Archivo')
        self.list.InsertColumn(2, 'Ext')
        self.list.InsertColumn(3, 'Accion')
        self.list.SetColumnWidth(0, 250)
        self.list.SetColumnWidth(1, 300)
        self.list.SetColumnWidth(2, 50)
        self.list.SetColumnWidth(3, 150)

        proceso_carpeta(carpeta_inicial[0], prelistado)
        prelista2 = sorted(prelistado[:])

        file_path = " "
        file_name = " "
        file_extension = " "
        file_status = " "
        file_what = " "
        nombre_arch = " "

        color_linea = 0

        for i in range(len(prelista2)):
            # prelista2[i][0] la carpeta
            # prelista2[i][1] el archivo
            # prelista2[i][2] el premarcado
            # prelista2[i][3] que es

            path_anterior = file_path
            serie_anterior = file_name
            ext_anterior = file_extension
            status_anterior = file_status
            what_anterior = file_what
            nombre_arch_ant = nombre_arch

            file_name, file_extension = os.path.splitext(prelista2[i][1])
            file_path = prelista2[i][0]
            file_status = prelista2[i][2]
            file_what = prelista2[i][3]

            if file_name.endswith(".es") and (file_what == "Subt"):
                largo_file_name = len(file_name)
                nombre_arch = file_name[:largo_file_name - 3]
            else:
                nombre_arch = file_name

            color_linea += 1
            if (nombre_arch == nombre_arch_ant):

                # sigo procesando un capitulo
                if ((file_what == "Peli") and (what_anterior == "Subt")) or ((file_what == "Subt") and (what_anterior == "Peli")):
                    # no piso estados
                    if not file_status[:3] == "***":
                        file_status = "*** OK"
                    if not status_anterior[:3] == "***":
                        status_anterior = "*** OK"

                # cambio de serie, se come el ultimo de la anterior
            if not (path_anterior == " "):
                # evito el primero en blanco
                guardo_en_control(self,path_anterior,serie_anterior,ext_anterior,status_anterior,what_anterior,color_linea)

        # ultimo capitulo

        color_linea += 1
        if not ( file_path == " "):
            # evito blanco
            guardo_en_control(self,file_path,file_name,file_extension,file_status,file_what,color_linea)

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        bot_sel = wx.Button(leftPanel, -1, 'Selec.todo', size=(100, -1))
        bot_des = wx.Button(leftPanel, -1, 'Deselec.todo', size=(100, -1))
        bot_switch = wx.Button(leftPanel, -1, 'Total / Parcial', size=(100, -1))


        bot_series = wx.Button(leftPanel, -1, 'Series', size=(100, -1))
        bot_1serie = wx.Button(leftPanel, -1, '1 serie', size=(100, -1))
        bot_seriesn = wx.Button(leftPanel, -1, 'Series nuevas', size=(100, -1))
        bot_1serien = wx.Button(leftPanel, -1, '1 serie nueva', size=(100, -1))
        bot_1peli = wx.Button(leftPanel, -1, '1 pelicula', size=(100, -1))

        bot_vose = wx.Button(leftPanel, -1, 'Marco [vose]', size=(100, -1))
        bot_espa = wx.Button(leftPanel, -1, 'Marco [esp]', size=(100, -1))
        bot_subtitulo = wx.Button(leftPanel, -1, 'Subtitulo', size=(100, -1))
        bot_borrar = wx.Button(leftPanel, -1, 'Borro', size=(100, -1))

        bot_apply = wx.Button(leftPanel, -1, 'Procesar', size=(100, -1))
        bot_final = wx.Button(leftPanel, -1, 'Fin', size=(100, -1))

        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=bot_sel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=bot_des.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, id=bot_switch.GetId())


        self.Bind(wx.EVT_BUTTON, self.OnSeries, id=bot_series.GetId())
        self.Bind(wx.EVT_BUTTON, self.On1Serie, id=bot_1serie.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSeriesN, id=bot_seriesn.GetId())
        self.Bind(wx.EVT_BUTTON, self.On1SerieN, id=bot_1serien.GetId())
        self.Bind(wx.EVT_BUTTON, self.On1Peli, id=bot_1peli.GetId())

        self.Bind(wx.EVT_BUTTON, self.OnVose, id=bot_vose.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnEspa, id=bot_espa.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSubtitulo, id=bot_subtitulo.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBorrar, id=bot_borrar.GetId())

        self.Bind(wx.EVT_BUTTON, self.OnApply, id=bot_apply.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnFin, id=bot_final.GetId())

        vbox2.Add(bot_sel, 0, wx.TOP, 5)
        vbox2.Add(bot_des)
        vbox2.Add(bot_switch)
        vbox2.Add((-1, 10))
        vbox2.Add(bot_series)
        vbox2.Add(bot_1serie)
        vbox2.Add(bot_seriesn)
        vbox2.Add(bot_1serien)
        vbox2.Add(bot_1peli)
        vbox2.Add((-1, 10))
        vbox2.Add(bot_vose)
        vbox2.Add(bot_espa)
        vbox2.Add(bot_subtitulo)
        vbox2.Add(bot_borrar)
        vbox2.Add((-1, 10))
        vbox2.Add(bot_apply)
        vbox2.Add((-1, 10))
        vbox2.Add(bot_final)

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

        format = "%Y%m%d"
        today = datetime.datetime.today()
        s = "c:\python27\log_"+today.strftime(format)+".txt"
        if os.path.isfile(s):
            self.log.LoadFile(s)

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

    def OnSwitch(self, event):

        if sigue_el_loop[1] == ["TOTAL"]:
            sigue_el_loop[1] = ["PARCIAL"]
            carpeta_inicial[1] = "PARCIAL: "+carpeta_inicial[1][7:]
        else:
            sigue_el_loop[1] = ["TOTAL"]
            carpeta_inicial[1] = "TOTAL: "+carpeta_inicial[1][9:]


        msg = str(sigue_el_loop[1])
        busyDlg = wx.BusyInfo(msg)
        time.sleep(3)
        busyDlg = None

        self.Close(True)
        self.Destroy()

    def OnSeries(self, event):
        carpeta_inicial[0] = default_path_series
        if sigue_el_loop[1] == ["TOTAL"]:
            carpeta_inicial[1] = "TOTAL: Procesando series"
        else:
            carpeta_inicial[1] = "PARCIAL: Procesando series"

        self.Close(True)
        self.Destroy()

    def On1Serie(self, event):
        carpeta_inicial[0] = default_path_series
        # guardo anteriores
        carpeta_ant_0 = carpeta_inicial[0]
        carpeta_ant_1 = carpeta_inicial[1]

        if sigue_el_loop[1] == ["TOTAL"]:
            carpeta_inicial[1] = "TOTAL: Procesando 1 serie"
        else:
            carpeta_inicial[1] = "PARCIAL: Procesando 1 serie"

        dir_dest = default_path_series
        # pido la carpeta
        dialog = wx.DirDialog(None, "Elija carpeta de la SERIE ",
        defaultPath = dir_dest, style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            carpeta_inicial[0] = dialog.GetPath()
        else:
            # rollback
            carpeta_inicial[0] = carpeta_ant_0
            carpeta_inicial[1] = carpeta_ant_1

        dialog.Destroy()
        self.Close(True)
        self.Destroy()

    def OnSeriesN(self, event):
        carpeta_inicial[0] = default_path_serien

        if sigue_el_loop[1] == ["TOTAL"]:
            carpeta_inicial[1] = "TOTAL: Procesando series nuevas"
        else:
            carpeta_inicial[1] = "PARCIAL: Procesando series nuevas"

        self.Close(True)
        self.Destroy()

    def On1SerieN(self, event):
        carpeta_inicial[0] = default_path_serien
        # guardo anteriores
        carpeta_ant_0 = carpeta_inicial[0]
        carpeta_ant_1 = carpeta_inicial[1]

        if sigue_el_loop[1] == ["TOTAL"]:
            carpeta_inicial[1] = "TOTAL: Procesando 1 serie nueva"
        else:
            carpeta_inicial[1] = "PARCIAL: Procesando 1 serie nueva"

        dir_dest = default_path_serien
        # pido la carpeta
        dialog = wx.DirDialog(None, "Elija carpeta de la SERIE NUEVA ",
        defaultPath = dir_dest, style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            carpeta_inicial[0] = dialog.GetPath()
        else:
            # rollback
            carpeta_inicial[0] = carpeta_ant_0
            carpeta_inicial[1] = carpeta_ant_1

        # falta el else
        dialog.Destroy()
        self.Close(True)
        self.Destroy()

    def On1Peli(self, event):
        carpeta_inicial[0] = default_path_pelis
        # guardo anteriores
        carpeta_ant_0 = carpeta_inicial[0]
        carpeta_ant_1 = carpeta_inicial[1]

        if sigue_el_loop[1] == ["TOTAL"]:
            carpeta_inicial[1] = "TOTAL: Procesando 1 pelicula"
        else:
            carpeta_inicial[1] = "PARCIAL: Procesando 1 pelicula"

        dir_dest = default_path_pelis
        # pido la carpeta
        dialog = wx.DirDialog(None, "Elija carpeta de la PELICULA ",
        defaultPath = dir_dest, style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            carpeta_inicial[0] = dialog.GetPath()
        else:
            # rollback
            carpeta_inicial[0] = carpeta_ant_0
            carpeta_inicial[1] = carpeta_ant_1

        dialog.Destroy()
        self.Close(True)
        self.Destroy()

    def OnVose(self, event):

        num = self.list.GetItemCount()
        for yy in range(num):
            if self.list.IsChecked(yy) and listado[yy].tipo == "Peli" and len(listado[yy].accion.strip()) == 0:
                self.list.SetStringItem(yy, 3, "[vose]")
                self.list.CheckItem(yy, False)
                listado[yy].accion = "[vose]"

    def OnEspa(self, event):
        num = self.list.GetItemCount()
        for yy in range(num):
            if self.list.IsChecked(yy) and listado[yy].tipo == "Peli" and len(listado[yy].accion.strip()) == 0:
                self.list.SetStringItem(yy, 3, "[esp]")
                self.list.CheckItem(yy, False)
                listado[yy].accion = "[esp]"

    def OnSubtitulo(self, event):
        num = self.list.GetItemCount()
        for yy in range(num):
            if self.list.IsChecked(yy) and listado[yy].tipo == "Peli" and len(listado[yy].accion.strip()) == 0:
                self.list.SetStringItem(yy, 3, "Subtitulo")
                self.list.CheckItem(yy, False)
                listado[yy].accion = "Subtitulo"

    def OnBorrar(self, event):
        num = self.list.GetItemCount()
        for yy in range(num):
            if self.list.IsChecked(yy):
                self.list.SetStringItem(yy, 3, "Borrar")
                self.list.CheckItem(yy, False)
                listado[yy].accion = "Borrar"

    def OnFin(self, event):

        format = "%Y%m%d"
        today = datetime.datetime.today()
        s = today.strftime(format)
        self.log.SaveFile("c:\python27\log_"+s+".txt")
        sigue_el_loop[0] = ["Final"]
        self.Close(True)
        self.Destroy()

    def OnApply(self, event):

        linea = Archivo
        num = self.list.GetItemCount()

        # primera pasada

        for ix in range(num):
            linea = listado[ix]

            if linea.accion == "Subtitulo":
                self.log.AppendText("Busco subtitulo para "+linea.capitulo+ "\n")

                sigo_dialogo = True

                barra_1 = linea.serie.find("\\", 20)
                barra_2 = linea.serie.find("\\", barra_1+1)
                esta_serie = linea.serie[barra_1+1:barra_2]

                if esta_serie in diccionario:
                    nro = diccionario[esta_serie]
                else:
                    el_titulo = 'Ingrese pagina de '+esta_serie
                    dlg = wx.TextEntryDialog(None, el_titulo,'Nro ', "0000")
                    if dlg.ShowModal() == wx.ID_OK:
                        nro = dlg.GetValue()
                        # guardo en diccionario
                        diccionario[esta_serie] = nro
                    else:
                        sigo_dialogo = False
                    dlg.Destroy()

                if sigo_dialogo:
                    ## despliego pag del nro
                    el_link = "http://www.tusubtitulo.com/show/"+nro
                    # dialog = MyBrowser(None, -1)
                    dialog = MyBrowser(None, wx.ID_ANY)
                    dialog.browser.LoadURL(el_link)
                    dialog.Show()

                    dlg = wx.FileDialog(
                        self, message="Subtitulo para "+linea.capitulo,
                        defaultDir="",
                        defaultFile="",
                        wildcard= "subtitulos (*.srt,*.sub)|*.srt;*.sub",
                        style=wx.OPEN | wx.CHANGE_DIR
                    )

                    # Show the dialog and retrieve the user response. If it is the OK response,
                    # process the data.
                    if dlg.ShowModal() == wx.ID_OK:
                        # This returns a Python list of files that were selected.
                        paths = dlg.GetPaths()
                        # guardo los datos ingresados
                        linea.archsub = paths[0]
                        listado[ix] = linea
                    else:
                        sigo_dialogo = False

                    # Destroy the dialog. Don't do this until you are done with it!
                    # BAD things can happen otherwise!
                    dlg.Destroy()
                    dialog.Destroy()

                    # si cancelaron, saco el indicador de subtitulo para la segunda pasada
                    if not sigo_dialogo:
                        linea.accion = " "
                        listado[ix] = linea


        # segunda pasada

        for ix in range(num):
            linea = listado[ix]
            if linea.accion == "[vose]":
                self.log.AppendText("Marco [vose] a "+linea.capitulo+ "\n")
                # extraigo las partes
                parte_a = os.path.join(linea.serie, linea.capitulo)
                parte_b = linea.extension
                # armo
                copia_origen = parte_a + parte_b
                copia_destino = parte_a+".[vose]"+parte_b
                # renombro archivo
                if not os.path.isfile(copia_destino):
                    shutil.move(copia_origen, copia_destino)

            elif linea.accion == "[esp]":
                self.log.AppendText("Marco [esp] a "+linea.capitulo+ "\n")
                # extraigo las partes
                parte_a = os.path.join(linea.serie, linea.capitulo)
                parte_b = linea.extension
                # armo
                copia_origen = parte_a + parte_b
                copia_destino = parte_a+".[esp]"+parte_b
                # renombro archivo
                if not os.path.isfile(copia_destino):
                    shutil.move(copia_origen, copia_destino)

            elif linea.accion == "Subtitulo":
                self.log.AppendText("Copio subtitulo para "+linea.capitulo+ "\n")
                parte_a = os.path.join(linea.serie, linea.capitulo)
                # armo
                copia_origen = linea.archsub
                parte_c, parte_b = os.path.splitext(copia_origen)
                copia_destino = parte_a+parte_b
                # copio
                if not os.path.isfile(copia_destino):
                    shutil.copy2(copia_origen, copia_destino)
                # borro en el origen
                os.chmod(copia_origen,stat.S_IWRITE)
                os.remove(copia_origen)

            elif linea.accion == "Borrar":
                # borro el archivo
                self.log.AppendText("Borro archivo "+linea.capitulo+ "\n")
                parte_a = os.path.join(linea.serie, linea.capitulo)
                parte_b = linea.extension
                # armo
                copia_origen = " "
                copia_destino = parte_a+parte_b
                # borro en destino
                if os.path.isfile(copia_destino):
                    os.chmod(copia_destino,stat.S_IWRITE)
                    os.remove(copia_destino)

            self.list.SetStringItem(ix, 3, " ")
            listado[ix].accion = " "

        format = "%Y%m%d"
        today = datetime.datetime.today()
        s = today.strftime(format)
        self.log.SaveFile("c:\python27\log_"+s+".txt")

        self.Close(True)
        self.Destroy()

def proceso_carpeta(carp, lista):

    # pongo cartel...
    msg = "Procesando archivos ..."
    busyDlg = wx.BusyInfo(msg)
    # time.sleep(5)
    # busyDlg = None

    contenido = os.listdir(carp)
    for ii in range(len(contenido)):

            item = contenido[ii]
            s = os.path.join(carp, item)
            if os.path.isfile(s):

                # marco los que no necesitan subs
                # pregunto por vose y [esp]
                # marco los contenidos con [vose] y [esp]

                if len(re.findall("vose", item, re.IGNORECASE)) > 0:
                    estado = "*** vose"
                elif len(re.findall("\[esp\]", item, re.IGNORECASE)) > 0:
                    estado = "*** espa"
                else:
                    estado = " "

                file_name, file_extension = os.path.splitext(item)

                if (file_extension == ".avi") or (file_extension == ".mp4") or (file_extension == ".mkv"):
                    que_es = "Peli"
                elif (file_extension == ".srt") or (file_extension == ".sub"):
                    que_es = "Subt"
                else:
                    que_es = " "

                lista.append([carp,item,estado,que_es])
            else:
                busyDlg = None
                proceso_carpeta(s, lista)
    busyDlg = None

def cargo_diccionario():
    handle = open("c:\python27\seriesynumeros.txt")
    for line in handle:
        line = line.rstrip()
        if len(line) > 0:
            posicion = line.find("|")
            clave = line[:posicion]
            numero = line[posicion+1:]
            diccionario[clave] = numero
    handle.close()

def guardo_diccionario():
    handle = open("c:\python27\seriesynumeros.txt","w")
    for key in diccionario:
        clave = key
        numero = diccionario[key]
        if len(numero.rstrip())  > 0:
            linea = clave+"|"+numero+"\n"
            handle.write(linea)
    handle.close()

app = wx.App(redirect=True)
carpeta_inicial = list()
carpeta_inicial.append("\\\\BUFALITO\\share02\\SERIES NUEVAS")
carpeta_inicial.append("TOTAL: Procesando series nuevas")

sigue_el_loop = list()
sigue_el_loop.append(["Sigue"])
sigue_el_loop.append(["TOTAL"])
# sigue_el_loop[0]: "Sigue" = loop principal
# sigue_el_loop[1]: "TOTAL" = todo, "PARCIAL" = lo que falta
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

    Repository(None, wx.ID_ANY, carpeta_inicial[1])
    app.MainLoop()

guardo_diccionario()
