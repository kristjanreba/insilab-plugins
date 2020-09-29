# Copyright Notice
# ================
#
# The PyMOL Plugin source code in this file is copyrighted, but you can
# freely use and copy it as long as you don't change or remove any of
# the copyright notices.
#
# ----------------------------------------------------------------------
# This PyMOL Plugin is Copyright (C) 2017 by Marko Jukic <marko.jukic@ffa.uni-lj.si>
#
#                        All Rights Reserved
#
# Permission to use, copy and distribute
# versions of this software and its documentation for any purpose and
# without fee is hereby granted, provided that the above copyright
# notice appear in all copies and that both the copyright notice and
# this permission notice appear in supporting documentation, and that
# the name(s) of the author(s) not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# THE AUTHOR(S) DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.  IN
# NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
# ----------------------------------------------------------------------


# -*- coding: utf-8 -*-
# ProBis_H2O
# written for python 2.7.x
# Not Yet Described at PyMOL wiki: /
# Author : Marko Jukic
# Date: October 2017
# License: chech http://insilab.org
# Version: 0.93
__author__ = "Marko Jukic"
__licence__ = "http://insilab.org"
__version__ = "0.93"


# Comments: Script is commented in Slovene language
#


import tkinter, sys, re, gzip, os, urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
import fileinput, pymol, tkinter.ttk, json, math, multiprocessing
import numpy as np
from pymol.cgo import *


import tkinter.messagebox
#tipicni python 2x tkFileDialog - v 3 je filedialog
from tkinter.filedialog import askopenfilename

from glob import glob
from ftplib import FTP
from collections import Counter
from itertools import groupby

# SCIKIT LEARN------------------------------------------------------------------
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
# /SCIKIR LEARN-----------------------------------------------------------------

# ---------------------------------------INITIALIZE-----------------------------


def __init__(self):

    """Add this Plugin to the PyMOL menu"""
    self.menuBar.addmenuitem('Plugin', 'command',
                             'ProBiS_H2O',
                             label = 'ProBiS H2O',
                             command = lambda: mainDialog(self.root))

red01 = '#ffe6e6'
red02 = '#ffcccc'
red03 = '#ffb3b3'
red04 = '#ff9999'
red05 = '#ff8080'
red06 = '#ff6666'
red07 = '#ff4d4d'
red08 = '#ff3333'
red09 = '#ff1a1a'
red10 = '#ff0000'

logo = """
iVBORw0KGgoAAAANSUhEUgAAAXgAAABeCAYAAAApHw85AAAAAXNSR0IArs4c6QAAAAlwSFlzAAAL
EwAACxMBAJqcGAAABCVpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6
eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYg
eG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4K
ICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlm
Zj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOmV4aWY9
Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIgogICAgICAgICAgICB4bWxuczpkYz0iaHR0
cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICAgICAgICAgIHhtbG5zOnhtcD0iaHR0
cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+CiAgICAgICAgIDx0aWZmOlJlc29sdXRpb25Vbml0
PjI8L3RpZmY6UmVzb2x1dGlvblVuaXQ+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjU8L3Rp
ZmY6Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOlhSZXNvbHV0aW9uPjcyPC90aWZmOlhSZXNv
bHV0aW9uPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgog
ICAgICAgICA8dGlmZjpZUmVzb2x1dGlvbj43MjwvdGlmZjpZUmVzb2x1dGlvbj4KICAgICAgICAg
PGV4aWY6UGl4ZWxYRGltZW5zaW9uPjM3NjwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAg
IDxleGlmOkNvbG9yU3BhY2U+MTwvZXhpZjpDb2xvclNwYWNlPgogICAgICAgICA8ZXhpZjpQaXhl
bFlEaW1lbnNpb24+OTQ8L2V4aWY6UGl4ZWxZRGltZW5zaW9uPgogICAgICAgICA8ZGM6c3ViamVj
dD4KICAgICAgICAgICAgPHJkZjpCYWcvPgogICAgICAgICA8L2RjOnN1YmplY3Q+CiAgICAgICAg
IDx4bXA6TW9kaWZ5RGF0ZT4yMDE2LTEwLTIwVDIyOjEwOjE4PC94bXA6TW9kaWZ5RGF0ZT4KICAg
ICAgICAgPHhtcDpDcmVhdG9yVG9vbD5QaXhlbG1hdG9yIDMuNS4xPC94bXA6Q3JlYXRvclRvb2w+
CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgqTTXc2
AABAAElEQVR4Ae2dCWAdVfX/78xb8rI2SdOm+74vlKUFClhA9h0FUUEQFHFF8YeouFbFDVF/bn9/
oIiCiICgoIgIArLvO4XSfW/atE2zv23m//nelxfSNMl7aZO02jntyczcuds79873njn33DvGBBRI
IJBAIIFAAv0rgfNvLC694M7B/VvIzrm7OwcFIYEEAgkEEggk0JcSiCWHHuglY1eahQsHFHMHtLC+
FFiQVyCBQAKBBP5TJBBxQ4ekU4WnTNy4X9VA1jkA+IGUdlBWIIFAAvucBGa+5/VosiV9vJ9ITk42
FR8ykAIIAH4gpR2UFUggkMA+J4Et4ZrJ6dbkXJPyQ146ckKbAJyBEEQA8AMh5aCMQAKBBPZZCSQS
qRMA9wovkTQRzztp4vn3DUUY/kAIJAD4gZByUEYggUAC+6QEqj70WGnUM+/xU55JptKmIBQeF/Pc
YwdKGAHAD5Skg3ICCQQS2OckUNiYOMykkgelAHeT9o3rO25RpOACYxZGB0IYAcAPhJSDMgIJBBLY
JyUQMua9XjIVMQ5Qi1GmtTVuKorChxcecdDBAyGQAOAHQspBGYEEAgnscxKIHP3gnNKQf0pLPGWM
w5wq/7c1xc3Q8sKSUZWx89Hi+x1/+72Afa5Vgx8cSCCQQCABJFA9KHRRLGSGNifaYBaQb2zxTMRJ
mbFDik83k6ZM729BBQDf3xIO8g8kEEhg35PA+HvGDisLn9kST5q0yQK8MUns8HXNCX/y6NJhFUPL
z+1vwQQA398SDvIPJBBIYB+SgG/924tGl3xgWIUztmY7k6tCWYU6Gc/IdVvjzqihITO+Onaeqbh2
TH8KJwD4/pRukHcggUAC+5gEQPGJ940eM8RcHHZ9s6URULcALxs8J/xf35DiNG3mTKkYGx1ZdVF/
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
TkSuQmCC
"""

def mainDialog(root=None):

    global master
    master = tkinter.Toplevel(root)
    master.title(' ProBiS H2O Plugin ')
    w_photo = tkinter.PhotoImage(data = logo)
    w = tkinter.Label(master, image = w_photo)
    w.image = w_photo
    w.pack()


# ------------------------------------- ttk NoteBook ---------------------------


    global nb
    global p1
    global p2
    global p3

    nb = tkinter.ttk.Notebook(master, height=320, width=430)
    style = tkinter.ttk.Style()
    style.configure("classicklook", foreground="black", background="#f2f1f0")

    p1 = tkinter.Frame(nb)
    p2 = tkinter.Frame(nb)
    p3 = tkinter.Frame(nb)


    nb.add(p1, text='define system', )
    nb.add(p2, text='cluster analysis', )
    nb.add(p3, text='    About/Help   ', )


    group = tkinter.LabelFrame(p1, text='define system')
    # group2 = Tkinter.LabelFrame(p2, text='ccluster analysis', bg = '#f2f1f0')


    nb.pack(padx=5, pady=5, fill=tkinter.BOTH, expand=1)
# ----------------------------- Water analysis TAB -----------------------------

    group.pack(fill='both', expand=1, padx=5, pady=5)
    # group2.pack(fill='both', expand=1, padx=5, pady=5)
    # INPUT on tab p1
    tkinter.Label(group, text='PDB ID:').grid(row=2, column=0)

    tkinter.Button(group, text="custom", command=custom_disk_file_get.load_file,
                    justify=tkinter.CENTER, padx=20).grid(row=2, column=5)

    global pdb_text
    pdb_text = tkinter.StringVar(master=group)
    pdb_text.set("protein")

    def clearme(event):
        pdb_text.set("")

    global entry_pdb_text
    entry_pdb_text = tkinter.Entry(group, textvariable=pdb_text, width=10)
    entry_pdb_text.bind("<Button-1>", clearme)
    entry_pdb_text.grid(row=2, column=1)
    entry_pdb_text.update()

    tkinter.Label(group, text='Analyze binding site (default)').grid(row=3, column=1)

    global bsite_vicinity_setting
    global entry_bsite_vicinity_setting
    bsite_vicinity_setting = tkinter.StringVar(master=group)

    entry_bsite_vicinity_setting = tkinter.Checkbutton(group,
                                    variable=bsite_vicinity_setting, onvalue="yes",
                                    offvalue="not", justify=tkinter.LEFT, padx=10)

    entry_bsite_vicinity_setting.grid(row=3, column=0)
    entry_bsite_vicinity_setting.select()
    entry_bsite_vicinity_setting.update()

    tkinter.Label(group, text='Define water as binding site').grid(row=4, column=1)

    global water_binding_setting
    global entry_water_binding_setting
    water_binding_setting = tkinter.StringVar(master=group)

    entry_water_binding_setting = tkinter.Checkbutton(group,
                                    variable=water_binding_setting, onvalue="yes",
                                    offvalue="not", justify=tkinter.LEFT, padx=10)

    entry_water_binding_setting.grid(row=4, column=0)
    entry_water_binding_setting.deselect()
    entry_water_binding_setting.update()

    tkinter.Label(group, text='Compare whole chain').grid(row=5, column=1)

    global whole_chain_setting
    whole_chain_setting = tkinter.StringVar(master=group)

    entry_whole_chain_setting = tkinter.Checkbutton(group,
                                variable=whole_chain_setting, onvalue="yes",
                                offvalue="not", justify=tkinter.LEFT, padx=10)

    entry_whole_chain_setting.grid(row=5, column=0)
    entry_whole_chain_setting.deselect()
    entry_whole_chain_setting.update()

    tkinter.Label(group, text='Debye-Waller correction').grid(row=6, column=1)

    global debye_waller_setting
    debye_waller_setting = tkinter.StringVar(master=group)

    entry_debye_waller_setting = tkinter.Checkbutton(group,
                                variable=debye_waller_setting, onvalue="yes",
                                offvalue="not", justify=tkinter.LEFT, padx=10)

    entry_debye_waller_setting.grid(row=6, column=0)
    entry_debye_waller_setting.deselect()
    entry_debye_waller_setting.update()

    tkinter.Label(group, text='Single aligned chain per PDB entry').grid(row=7, column=1)

    global num_entity_chains_setting
    num_entity_chains_setting = tkinter.StringVar(master=group)

    entry_num_entity_chains_setting = tkinter.Checkbutton(group,
                                    variable=num_entity_chains_setting,
                                    onvalue="yes", offvalue="not", justify=tkinter.LEFT, padx=10)

    entry_num_entity_chains_setting.grid(row=7, column=0)
    entry_num_entity_chains_setting.deselect()
    entry_num_entity_chains_setting.update()

    global seq_identity_value
    seq_identity_value = tkinter.StringVar(master=group)
    seq_identity_value.set('blastclust: 95')

    seq_identity_options = ['blastclust: 30',
                            'blastclust: 40',
                            'blastclust: 50',
                            'blastclust: 70',
                            'blastclust: 90',
                            'blastclust: 95',
                            'blastclust: 100',
                            'custom_cluster']

    seq_identity_menu = tkinter.OptionMenu(group, seq_identity_value, *seq_identity_options)
    seq_identity_menu.grid(row=8, column=1)


    tkinter.Label(group, text='Found').grid(row=9, column=0)

    global find_value
    find_value = tkinter.StringVar(master=group)
    find_value.set(" ")
    entry_find_value = tkinter.Entry(group, textvariable=find_value, width=25)
    entry_find_value.grid(row=9, column=1)
    entry_find_value.configure(state='disabled')
    entry_find_value.update()
    tkinter.Label(group, text='Select\nBINDING SITE\n/ CHAIN').grid(row=10, column=0)

    global binding_listbox

    binding_listbox_scrollbar = tkinter.Scrollbar(group, orient=tkinter.VERTICAL)

    binding_listbox = tkinter.Listbox(group, width=20, height=5,
                    yscrollcommand=binding_listbox_scrollbar.set, selectmode=tkinter.SINGLE)

    binding_listbox_scrollbar.config(command=binding_listbox.yview)
    binding_listbox_scrollbar.grid(row=10, column=2)
    binding_listbox.grid(row=10, column=1)
    binding_listbox.configure(state='normal')
    binding_listbox.update()
    bindng_listbox_scrollbar = tkinter.Scrollbar(binding_listbox, orient=tkinter.VERTICAL)


# GO baby
    tkinter.Button(group, text="Find", command=ClusterComplexManipulation.get_cluster_complexes,
                    justify=tkinter.CENTER, padx=30).grid(row=8, column=5)

    global enable_disable_download
    enable_disable_download = tkinter.Button(group, text="Download",
                                            command=ClusterComplexManipulation.download_complexes,
                                            justify=tkinter.CENTER, padx=13)

    enable_disable_download.grid(row=9, column=5)
    enable_disable_download.configure(state='disabled')
    global find_bsites
    find_bsites = tkinter.Button(group, text="Identify", command=BindingSites.get_binding_sites,
                                justify=tkinter.CENTER, padx=18)

    find_bsites.grid(row=10, column=5)
    find_bsites.configure(state='normal')

    tkinter.Button(p1, text="GO", command=h20Analysis.analyze_waters,
                    justify=tkinter.CENTER, padx=30).pack(side=tkinter.RIGHT)

    tkinter.Button(p1, text="SETUP DB", command=RSCB_contact.contact_rscb_pdb,
                    justify=tkinter.CENTER, padx=30).pack(side=tkinter.LEFT)



# -------------------------------Results TAB------------------------------------

    group5 = tkinter.LabelFrame(p2, borderwidth = 0, highlightthickness = 0)
    group5.pack(fill='both', expand=1, padx=5, pady=5)

    tkinter.Label(group5, text='Info:').pack(anchor = tkinter.W)
    global T1_text
    global T1
    T1_text = tkinter.StringVar(group5)
    T1_text.set(" ")

    s1 = tkinter.Scrollbar(group5)
    T1 = tkinter.Text(group5, height = 5)

    T1.focus_set()
    s1.pack(side="right", padx=2, pady=35, expand = False)
    T1.pack(side="left", padx=2, pady=8, expand = False)
    s1.config(command=T1.yview)
    T1.config(yscrollcommand=s1.set)
    T1.insert(tkinter.END, T1_text.get())
#-------------------

    group56 = tkinter.LabelFrame(p2, borderwidth = 0, highlightthickness = 0)
    group56.pack(fill='both', expand=1, padx=5, pady=1)

    tkinter.Label(group56, text='Calculated clusters, conservation;    keep selected display:').pack(side = tkinter.LEFT)

    global display_setting
    display_setting = tkinter.StringVar(master=group56)

    entry_display_setting = tkinter.Checkbutton(group56, variable=display_setting, onvalue="yes", offvalue="not")
    entry_display_setting.pack(side = tkinter.RIGHT,  ipadx=15, expand = False)
    entry_display_setting.deselect()
    entry_display_setting.update()


    group6 = tkinter.LabelFrame(p2, borderwidth = 0, highlightthickness = 0)
    group6.pack(fill='both', expand=1, padx=5, pady=1)

    global cluster_listbox
    cluster_listbox_scrollbar = tkinter.Scrollbar(group6, orient=tkinter.VERTICAL)

    cluster_listbox = tkinter.Listbox(group6, width=50, height=7,
                                    yscrollcommand=cluster_listbox_scrollbar.set,
                                    selectmode=tkinter.SINGLE)

    cluster_listbox_scrollbar.config(command=cluster_listbox.yview)
    cluster_listbox_scrollbar.pack(side="right", padx=2, pady=35, expand = False)
    cluster_listbox.pack(side="left", padx=2, pady=8, expand = False)
    cluster_listbox.configure(state='normal')
    cluster_listbox.update()
    cluster_listbox_scrollbar = tkinter.Scrollbar(cluster_listbox, orient=tkinter.VERTICAL)
#----------------------

    group7 = tkinter.LabelFrame(p2, borderwidth = 0, highlightthickness = 0)
    group7.pack(fill='both', expand=1, padx=1, pady=1)

    tkinter.Button(group7, text="display", command=pyMOLinterface.pyMOL_display_cluster,
                    justify=tkinter.CENTER, padx=10).pack(side=tkinter.RIGHT)
    tkinter.Button(group7, text="b-site", command=pyMOLinterface.pyMOL_bsite_cluster,
                    justify=tkinter.CENTER, padx=10).pack(side=tkinter.RIGHT)
    tkinter.Button(group7, text="contacts", command=pyMOLinterface.pyMOL_water_contacts,
                    justify=tkinter.CENTER, padx=10).pack(side=tkinter.RIGHT)
    tkinter.Button(group7, text="chain box", command=pyMOLinterface.pyMOL_chain_box,
                    justify=tkinter.CENTER, padx=10).pack(side=tkinter.RIGHT)
    tkinter.Button(group7, text="fetch/reset", command=pyMOLinterface.pyMOL_fetch_system,
                    justify=tkinter.CENTER, padx=10).pack(side=tkinter.RIGHT)




# -------------------------------HELP TAB---------------------------------------

    inserted_helper_text = '''
ProBiS H2O plugin is a PyMOL gui tool using ProBiS
for crystal complex water analysis.

* Konc,J., Depolli,M., Trobec,R., Rozman,K., Janezic,D.
Parallel-ProBiS: Fast parallel algorithm for local structural comparison of protein structures and binding sites. J. Comp. Chem., 2012, 33, 2199-2203.

* Konc,J. and Janezic,D.
ProBiS algorithm for detection of structurally similar protein binding sites by local structural alignment. Bioinformatics, 2010, 26, 1160-1168.

* Jukic,M., Ilas,J., Brvar,M., Kikelj,D., Cesar,J., Anderluh,M.
Linker-switch approach towards new ATP binding site inhibitors of DNA gyrase B. European Journal of Medicinal Chemistry, 2017, 125, 500-514.

If You need help contact us at:
marko.jukic@ffa.uni-lj.si
konc@cmm.ki.si






good luck!
'''


    s2 = tkinter.Scrollbar(p3)
    T2 = tkinter.Text(p3)



    s2.pack(side = "right", padx = 5, pady = 5, expand = False, fill = "y")
    T2.pack(side = "left", padx = 5, pady = 5, fill = "y")
    s2.config(command=T2.yview)
    T2.config(yscrollcommand=s2.set)
    T2.insert(tkinter.END, inserted_helper_text)
    T2.tag_add("bluetag", "2.0", "2.10")
    T2.tag_add("bluetag", "2.44", "2.50")
    T2.tag_add("violettag", "9.0", "9.6")
    T2.tag_config("bluetag", background="white", foreground="dodger blue")
    T2.tag_config("violettag", background="ivory2", foreground="dark violet")


# --------------------------------------------------- end main-loop ------------





# ----------------------------------------------------FUNCTIONS-----------------
class custom_disk_file_get:

    @staticmethod
    def load_file():
        fajlname = askopenfilename(filetypes=(("PDB files", "*.pdb"),
                                           ("All files", "*.*") ))
        if fajlname:
            try:
                print("File read.")
                print((str(fajlname)))
            except:
                tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                        message="File error or \nFile not Found! \nplease investigate!")
            pdb_text = str(fajlname)[-8:-4]
            entry_pdb_text.delete(0, tkinter.END)
            entry_pdb_text.insert(tkinter.INSERT, pdb_text)
            entry_pdb_text.update()


class RSCB_contact:

    """PDB database server setup"""

    lista_cluster_fajlov = ["bc-30.out", "bc-40.out", "bc-50.out", "bc-70.out",
                            "bc-90.out", "bc-95.out", "bc-100.out"]


    @staticmethod
    def set_cluster_list(list):
        lista_cluster_fajlov = list

    @staticmethod
    def contact_rscb_pdb():

        # initial setup
        current_path = str(os.getcwd())
        if current_path == check_path:
            pass
        else:
            os.mkdir(check_path)
            os.chdir(check_path)


        """download fajlov"""
        print("Setting up the cluster database!")
        rscb_pdb_ftp_server = FTP("resources.rcsb.org")
        rscb_pdb_ftp_server.login()
        rscb_pdb_ftp_server.cwd('/sequence/clusters/')
        rscb_pdb_ftp_server.retrlines('LIST')
        for cluster_fajl in RSCB_contact.lista_cluster_fajlov:
            lokalni_fajl = open(str(cluster_fajl), 'wb')
            rscb_pdb_ftp_server.retrbinary('RETR ' + str(cluster_fajl), lokalni_fajl.write)
            lokalni_fajl.close

        rscb_pdb_ftp_server.quit()
        print(("Database setup finished" + "\t thx RCSB protein data bank"))

        if str(os.path.isfile("./.pro/probis")) == "False":
            os.system("mkdir ./.pro/")
            RSCB_contact.fetch_probis()
            os.system("mv ./probis ./.pro/")
        else:
            pass

        RSCB_contact.file_checks()
        return None

    # 	sys.exit() -crashes pymol sometimes ...
# BOMO IMPLEMENTIRALI KASNEJE
    # pymol_path = "./Probis_H2O_database/"

    @staticmethod
    def fetch_probis():
        urllib.request.urlretrieve ("http://insilab.org/files/probis-algorithm/probis", "probis")
        # + X + X + X :)

    @staticmethod
    def file_checks():
        """preveri ce imamo instalirano bazo"""
        print("\nProBis_H2O: setting up...")
        check = ""
        for fajl in RSCB_contact.lista_cluster_fajlov:
            print((fajl + " present " + str(os.path.isfile(fajl))))
            if str(os.path.isfile(fajl)) == "False":
                print("ProBiS_H2O: please setup DB of rscb cluster files")
                break
            else:
                check += "a"
        if check == "aaaaaaaaaaa":
            print("ProBis_H2O: Database OK")

        if str(os.path.isfile("./.pro/probis")) == "False":
            print("ProBiS_H2O: please download probis using setup DB button in plugin GUI")
        else:
            try:
                if os.access("./.pro/probis", os.X_OK) == True:
                    print("probis executable ok")
                else:
                    print("probis executable present but no permissions set")
                    print("Do not forget to set +x premission for probis in working directory: ")
                    print("pymol_working_dir/ProBiS_H20/.pro/probis")
            except:
                pass

# -------------------------------------------------file checks------------------

# initial setup
check_path = str(os.getcwd()) + "/Probis_H2O/"


if os.path.isdir(check_path) == False:
    print("please setup probis DB and Probis_H2O folder")
else:
    os.chdir(check_path)
    RSCB_contact.file_checks()



# ------------------------------------------------------------------------------

class ClusterComplexManipulation:
    """download and identification of cluster complexes from RCSB"""



    @staticmethod
    def get_cluster_unique_list(target_complex, ime_selekcije, sekvenca_id):
        #target complex: kater pdb
        #ime selekcije: "clusters" ali "bc-"
        #sekvenca katera je izbrana 50, 70, 90
        vzorec = re.compile(target_complex, re.IGNORECASE)
        # lista z linijami ki vsebujejo iskani protein
        line_list = []
        # lista z linijami ki so del clustra
        line_list_2 = []
        # lista samo z imeni proteinov - ni unique - lahko je vec verig ....
        cluster_list = []

        try:
            if ime_selekcije == "clusters":

                with open(ime_selekcije + sekvenca_id + ".txt", "rt") as infile:
                    for linenumber, line in enumerate(infile):
                        if vzorec.search(line) != None:
                            line_list.append(line.rstrip('\n'))
                    print("using cd-hit preclustering")
                    print("""
Cd-hit: a fast program for clustering and comparing large sets of
protein or nucleotide sequences, Weizhong Li & Adam Godzik (2006)
Bioinformatics, 22:1658-9.
                        """)
                    print(("Found entries in sequence file: ", line_list))
                    print("Examined cluster number: ")
                    print((line_list[0].split("\t")[0]))
                    examined_cluster = line_list[0].split("\t")[0]


                # kljucen ^ na zacetku - zacetek linije !!!
                vzorec_2 = re.compile("^" + examined_cluster + "\t", re.IGNORECASE)


                with open(ime_selekcije + sekvenca_id + ".txt", "rt") as infile:
                    for linenumber, line in enumerate(infile):
                        if vzorec_2.search(line) != None:
                            line_list_2.append(line.rstrip('\n'))


                    for linija in line_list_2:
                        a = linija.split("\t")[2][0:4]
                        cluster_list.append(a)
                    # make unique list set
                    global cluster_list_unique
                    cluster_list_unique = set(cluster_list)
                    print("\nComplexes: ")
                    print(cluster_list_unique)

                find_value.set(str(len(cluster_list_unique)) + " compl. in cluster no.:"
                                                                + str(line_list[0].split("\t")[0]))

                print(("Found num of entries in cluster: ", len(cluster_list_unique)))
                enable_disable_download.configure(state='active')
                binding_listbox.delete(0, tkinter.END)
                return None

            else:
                with open(ime_selekcije + sekvenca_id + ".out", "rt") as infile:
                    for linenumber, line in enumerate(infile):
                        if vzorec.search(line) != None:
                            line_list.append(line.rstrip('\n'))


                line_list_2 = line_list[0].split()
                for element in line_list_2:
                    cluster_list.append(element[0:4])

                global cluster_list_unique
                cluster_list_unique = set(cluster_list)
                print("\nComplexes: ")
                print(cluster_list_unique)

                find_value.set(str(len(cluster_list_unique)) + " compl. in blastclust cluster.")
                print("using blastclust pre-clustering")
                print("""
Basic local alignment search tool, S.F. Altschul, W. Gish, W. Miller,
E.W. Myers, & D.J. Lipman (1990) J. Mol. Biol. 215:403-410.
""")
                print(("Found num of entries in cluster: ", len(cluster_list_unique)))
                enable_disable_download.configure(state='active')
                binding_listbox.delete(0, tkinter.END)
                return None

        except:
            tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                    message="invalid PDB ID or \nDatabase File not Found! \nplease investigate!")
            print("Database File not Found!")




    @staticmethod
    def get_cluster_complexes():


        wh_chain_setting = whole_chain_setting.get()
        if wh_chain_setting == "yes":
            entry_bsite_vicinity_setting.configure(state='disabled')
            entry_water_binding_setting.configure(state='disabled')
        else:
            entry_bsite_vicinity_setting.configure(state='active')
            entry_water_binding_setting.configure(state='active')


        #try:

        target_complex = str(pdb_text.get())

        if len(target_complex) < 4:

            tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                            message="invalid PDB ID!")
        elif len(target_complex) > 4:
            tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                            message="invalid PDB ID!")
        else:

            # replaced by water definition in first stage
            # target_complex_chain = str(chain_id.get())
            if str(seq_identity_value.get()) == "custom_cluster":
                selected_sequence = "_custom"
                ClusterComplexManipulation.get_cluster_unique_list(target_complex, "clusters", selected_sequence)

            elif str(seq_identity_value.get()) == "blastclust: 100":
                selected_sequence = "100"
                ClusterComplexManipulation.get_cluster_unique_list(target_complex, "bc-", selected_sequence)

            elif "blastclust" in str(seq_identity_value.get()):
                selected_sequence = str(seq_identity_value.get())[12:14]
                ClusterComplexManipulation.get_cluster_unique_list(target_complex, "bc-", selected_sequence)

            else:
                selected_sequence = str(seq_identity_value.get())[19:21]
                # print("hello" + target_complex + target_complex_chain + selected_sequence)
                ClusterComplexManipulation.get_cluster_unique_list(target_complex, "clusters", selected_sequence)

        #except:
        #    tkMessageBox.showwarning(title='ProBiS H2O warning', parent=master,
        #                                message="Check all settings, \nplease investigate!")



    @staticmethod
    def download_complexes():

        #za PDBje ki niso dostoni a imajo svoj entry
        nedostopni_datoteka = open("unavailable_pdb_list.txt", "w")


        try:
            def get_files_2(fajl):
                # ah lepse to kasneje !!! za download individualnih ent fajlov
                lokalni_fajl = open(fajl, 'wb')
                ftp_wwpdb_server.retrbinary('RETR ' + fajl, lokalni_fajl.write)
                lokalni_fajl.close()
                # unzip

                with gzip.open(fajl, 'rb') as compressed_f:
                    lokalni_fajl_uncompressed = open(fajl_uncompressed, 'wb')
                    lokalni_fajl_uncompressed.write(compressed_f.read())
                    lokalni_fajl_uncompressed.close()
                # -----

            i = 1

            for kompleks in cluster_list_unique:

                try:
                    if os.path.isfile(str(kompleks).lower() + ".pdb"):
                        i += 1
                        ftp_wwpdb_server = FTP("ftp.wwpdb.org")
                        ftp_wwpdb_server.login()
                    else:
                        fajl = "pdb" + str(kompleks).lower() + ".ent.gz"
                        fajl_uncompressed = str(kompleks).lower() + ".pdb"
                        print(("Downloading complex " + str(i) + " out of " + str(len(cluster_list_unique))))
                        i += 1
                        ftp_wwpdb_server = FTP("ftp.wwpdb.org")
                        ftp_wwpdb_server.login()
                        ftp_wwpdb_server.cwd('/pub/pdb/data/structures/divided/pdb/' + str(kompleks[1:3]).lower() + "/")

                        get_files_2(fajl)
                except:
                    #i += 1
                    print(("removing complex: " + str(kompleks)))
                    nedostopni_datoteka.write(str(kompleks).lower() + "\n")
                    pass

            ftp_wwpdb_server.quit()
            print("Download of complexes finished")



            return None
        except:
            tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                        message="Check all settings, \nplease investigate!")

        nedostopni_datoteka.close()


class BindingSites:
    """definiraj binding site"""

    bsite_unique_centers = []

    @staticmethod
    def get_binding_sites():

        wh_chain_setting = whole_chain_setting.get()
        if wh_chain_setting == "yes":
            entry_water_binding_setting.configure(state='disabled')
            entry_bsite_vicinity_setting.configure(state='disabled')
        else:
            entry_bsite_vicinity_setting.configure(state='active')
            entry_water_binding_setting.configure(state='active')
        try:
            binding_listbox.delete(0, tkinter.END)

            water_sel = water_binding_setting.get()
            chain_sel = whole_chain_setting.get()
            target_complex_2 = str(pdb_text.get()).lower()

            vzorec_2 = re.compile("^" + "ATOM\s+\d+")
            # pazi na naslednji * ali + v re
            vzorec_3 = re.compile("^" + "HETATM\s*\d+")
            vzorec_4 = re.compile("HOH")
            # VSE LISTE---------------------------------------------------------
            lista_za_heteroatome = []
            lista_za_atome = []
            lista_za_vode = []
            lista_binding_sites = []
            lista_water_binding_sites = []
            lista_verige = []
            lista_verige_konc = []
            warning_lista = []
            lista_verige_unique = []
            bsite_unique = []
            # podaj rezultate v tri glavne liste--------------------------------
            try:
                with open(target_complex_2 + ".pdb", "rt") as infile:
                    print((target_complex_2 + ".pdb"))
                    for linenumber, line in enumerate(infile):
                        if vzorec_3.search(line) != None:
                            if vzorec_4.search(line) != None:
                                lista_za_vode.append(line.rstrip('\n'))
                            else:
                                lista_za_heteroatome.append(line.rstrip('\n'))
                        if vzorec_2.search(line) != None:
                            lista_za_atome.append(line.rstrip('\n'))

                        else:
                            pass
            except OSError:
                print("File not found!, please investigate.")


            # VKLJUCITEV CHAIN VOD
            global lista_za_atome_xyzchain
            lista_za_atome_xyzchain = []

            for entry in lista_za_atome:
                test = []
                try:
                    entry2 = entry.split()
                    # ATOM    477  CG2 ILE A  78       6.540   0.762  34.941  1.00 13.42           C

                    test.append(entry2[6])
                    test.append(entry2[7])
                    test.append(entry2[8])
                    test.append(str(entry2[4]).upper())
                    lista_za_atome_xyzchain.append(test)
                except:
                    pass



            if water_sel == "not":
                for linija in lista_za_heteroatome:
                    #print(linija)
                    #naslednja linija je pomembna za korekturo "posebnih" pdb (4bqp, ...), to je ze 123 korektura...
                    if len(str(linija.split()[0])) > 6:
                        unique_binding_site = str(linija.split()[2]) + "." + (str(linija.split()[3]))[1:] + "." + (str(linija.split()[3]))[0]
                        lista_binding_sites.append(unique_binding_site)
                        # prostorska definicija bsite
                        bsite_unique.append([unique_binding_site, linija.split()[4], linija.split()[5], linija.split()[6]])
                    #naslednja linija je za korekturo "posebnih" pdb (1h00)
                    #primer:
                    #HETATM 2280  C22BFCP A1400       3.795  28.597   6.010  0.50 44.76           C
                    elif len(str(linija.split()[2])) > 6:
                        unique_binding_site = (str(linija.split()[2]))[-3:] + "." + (str(linija.split()[3]))[1:] + "." + (str(linija.split()[3]))[0]
                        lista_binding_sites.append(unique_binding_site)
                        # prostorska definicija bsite
                        bsite_unique.append([unique_binding_site, linija.split()[4], linija.split()[5], linija.split()[6]])
                    #naslednja linija je za korekturo "posebnih" pdb (2v5z, 1l2s)
                    #primer:
                    #HETATM 8040  O2P FAD B1497      26.808 129.360   7.718  1.00 27.99           O
                    elif len(str(linija.split()[4])) > 1:
                        unique_binding_site = (str(linija.split()[3]))[-3:] + "." + (str(linija.split()[4]))[1:] + "." + (str(linija.split()[4]))[0]
                        lista_binding_sites.append(unique_binding_site)
                        # prostorska definicija bsite
                        bsite_unique.append([unique_binding_site, linija.split()[5], linija.split()[6], linija.split()[7]])

                    else:
                        unique_binding_site = str(linija.split()[3]) + "." + str(linija.split()[5]) + "." + str(linija.split()[4])
                        lista_binding_sites.append(unique_binding_site)
                        # prostorska definicija bsite
                        bsite_unique.append([unique_binding_site, linija.split()[6], linija.split()[7], linija.split()[8]])
            else:
                for linija in lista_za_vode:
                    #naslednja linija je pomembna za korekturo "posebnih" pdb (4bqp, ...), to je ze 123 korektura...
                    if len(str(linija.split()[0])) > 6:
                        unique_binding_site = str(linija.split()[2]) + "." + (str(linija.split()[3]))[1:] + "." + (str(linija.split()[3]))[0]
                        lista_binding_sites.append(unique_binding_site)
                        bsite_unique.append([unique_binding_site, linija.split()[4], linija.split()[5], linija.split()[6]])
                    else:
                        unique_binding_site = str(linija.split()[3]) + "." + str(linija.split()[5]) + "." + str(linija.split()[4])
                        lista_binding_sites.append(unique_binding_site)
                        bsite_unique.append([unique_binding_site, linija.split()[6], linija.split()[7], linija.split()[8]])

            # priprava bsite ---------------------------------------------------
            # ok grupiranje ker zelimo UNIQUE
            for key, group in groupby(bsite_unique, lambda x: x[0]):
                bsx = []
                bsy = []
                bsz = []
                for el in group:
                    bsx.append(float(el[1]))
                    bsy.append(float(el[2]))
                    bsz.append(float(el[3]))

                # name of bsite, axerage x, average y, average z, min x, max x, min y, max y, min z, max z
                BindingSites.bsite_unique_centers.append([key, sum(bsx)/len(bsx), sum(bsy)/len(bsy), sum(bsz)/len(bsz), min(bsx), max(bsx), min(bsy), max(bsy), min(bsz), max(bsz)])

            # priprava vode-----------------------------------------------------
            for linija in lista_za_vode:
                temp = []
                if len(str(linija.split()[0])) > 6:
                    water_binding_sites = str(linija.split()[2]) + "." + (str(linija.split()[3]))[1:] + "." + (str(linija.split()[3]))[0]
                    lista_water_binding_sites.append(water_binding_sites)
                else:
                    water_binding_sites = str(linija.split()[3]) + "." + str(linija.split()[5]) + "." + str(linija.split()[4])
                    lista_water_binding_sites.append(water_binding_sites)
            # debug:
            # print(lista_water_binding_sites)

            # priprava ostalo---------------------------------------------------
            for linija in lista_za_atome:
                atom_site = []
                try:
                    atom_site.append(str(linija.split()[4]))
                    atom_site.append(int(linija.split()[5]))
                    lista_verige.append(atom_site)
                except:
                    pass

            # priprava verige---------------------------------------------------
            for key, group in groupby(lista_verige, lambda x: x[0]):

                temp_group = []
                residue_number = 0

                for el in group:

                    # TO JE ZA STETJE UNIKATNIH AK OSTANKOV
                    if el not in temp_group:
                        temp_group.append(el)
                    else:
                        pass

                    # uporbljeno za opcijo kjer se steje unikatne AK ostanke
                    ins_str = str(temp_group[-1][0]) + " chain with " + str(len(temp_group)) + " residues"
                    # ins_str = str(temp_group[-1][0]) + " chain with " + str(temp_group[-1][1]) + " residues"


                lista_verige_konc.append(ins_str)
                # print ins_str

            # debug line :
            # print lista_verige_konc

            # resevanje prolematicnih pdbjev - naj preveri uporabnik
            # v bodoce mogoce avtomatsko
            #-------------------------------------------------------------------
            if chain_sel == "not":

                for chainelement in lista_verige_konc:
                    if float(chainelement.split()[3]) < 30.0:
                        temp_str = "ONLY " + str(chainelement.split()[3]) + " resiues found in chain " + str(chainelement.split()[0])
                        # problemi v warning listi
                        warning_lista.append(temp_str)
                    else:
                        pass

                if len(warning_lista) >= 1:
                    tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                            message="\n".join(warning_lista) + "\n" +
                                            "Try to compare whole chains instead of individual binding sites at the short chain location.")
                else:
                    pass

                if water_sel == "not":
                    for entry in sorted(list(set(lista_binding_sites))):
                        binding_listbox.insert(0, entry)
                else:
                    for entry in sorted(list(set(lista_binding_sites))):
                        binding_listbox.insert(0, entry)
                    for entry in sorted(list(set(lista_water_binding_sites))):
                        binding_listbox.insert(0, entry)

            else:
                for entry in lista_verige_konc:
                    binding_listbox.insert(0, entry)

            return None
        # flow out except-------------------------------------------------------
        except:
            tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                    message="invalid PDB ID or \nDatabase File not Found! \n\nplease investigate!")
            print("Database File not Found!")
            print((sys.exc_info()))
        # class end


# report lista 1----------------------------------------------------------------
report_list_1 = []
report_list_2 = []
report_list_1.append("ProBiS H2O REPORT file")
report_list_1.append("-" * 25 + "\n\n")
# ------------------------------------------------------------------------------

class h20Analysis:
    """collect, prepare, cluster, analyze, display, crystal h20 data"""

    @staticmethod
    def analyze_waters():
        global SELECTED_SITE
        global SELECTED_SITE_CHAIN
        # NUM CPU:
        try:
            processors_available_local = str(multiprocessing.cpu_count())
        except:
            processors_available_local = "1"
        # NUM_CPUS //

        nova_datoteka = open("report_" + str(pdb_text.get()).lower() + ".txt", "w")
        nova_datoteka.close()


        # za eno ali vec verig na primerjan protein
        one_or_multiple = num_entity_chains_setting.get()
        # get setting on superposition starting point analysis
        bsite_space_check = bsite_vicinity_setting.get()

        chain_sel = whole_chain_setting.get()
        vzorec_3 = re.compile("^" + "HETATM\s+\d+")
        vzorec_3_supp = re.compile("^" + "HETATM\d\d\d\d\d\s+")
        examined_list_unique = []
        examined_list = list(cluster_list_unique)
        target_complex_2 = str(pdb_text.get()).lower()

        # to je za 1j4h kjer nastopajo nedosegljivi pdb-ji ki imajo svoje
        # entrije v bazi pdb: npr: 5GKY
        # za njih bomo tvorili bazo: unavailable_pdb_list.txt datoteka
        # ki se nahaja v delovnem okolju

        with open('unavailable_pdb_list.txt', 'r') as f:
            removed_list = f.read().splitlines()
        removed_list.append(target_complex_2.lower())



        for element in examined_list:
            if str(element).lower() not in removed_list:
                examined_list_unique.append(str(element).lower())
            else:
                pass

        try:
            bsite_selection = str(binding_listbox.get(binding_listbox.curselection()))
            chain_selection = str(binding_listbox.get(binding_listbox.curselection()))[-1]
            whole_chain_compare_selection = str(binding_listbox.get(binding_listbox.curselection()))[0]
        except:
            tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                    message="invalid selection \n\nplease select b-site or chain!")
            return None

        if bsite_space_check == "yes":
            for element in BindingSites.bsite_unique_centers:
                if element[0] == bsite_selection:
                    SELECTED_SITE = element
                    SELECTED_SITE_CHAIN = str(chain_selection).upper()

        if bsite_space_check == "not":
            for element in BindingSites.bsite_unique_centers:
                if element[0] == bsite_selection:
                    SELECTED_SITE = element
                    SELECTED_SITE_CHAIN = str(chain_selection).upper()

        if str(chain_sel) == "yes":
            SELECTED_SITE = []
            SELECTED_SITE.append("no binding site used in analysis")
            SELECTED_SITE_CHAIN = str(whole_chain_compare_selection).upper()

        else:
            pass


        #report 2,3,4,5,6,7,8,9, 10
        report_list_1.append("\n\n\nExamined complex: " + target_complex_2)
        report_list_1.append("Whole chain setting used: " + str(chain_sel))
        if str(chain_sel) == "yes":
            report_list_1.append("Whole chain selection: " + whole_chain_compare_selection)
            report_list_1.append("Binding site selection: / (not used)")
            report_list_1.append("Chain selection: " + whole_chain_compare_selection)
        else:
            report_list_1.append("Whole chain selection: / (not used)")
            report_list_1.append("Binding site selection: " + bsite_selection)
            report_list_1.append("Chain selection: " + chain_selection)


        report_list_1.append("Used PDB clusters with: " + str(seq_identity_value.get()) + " %")
        report_list_1.append("Unique structures in identified cluster: " + str(examined_list) + "\n\n\n")






        if chain_sel == "not":
    # for probis 2.4.7
            os.system("./.pro/probis -ncpu " + processors_available_local
                        + " -extract -bsite " + bsite_selection + " -dist 3.0 -f1 "
                        + target_complex_2 + ".pdb -c1 " + chain_selection
                        + " -srffile " + target_complex_2 + ".srf")
    # for probis 2.4.2
    #     os.system("./probis -extract -bsite " + bsite_selection + " -dist 3.0 -f1 " + target_complex_2 + ".pdb -c1 " + chain_selection + " > " + target_complex_2 + ".srf")
        else:
            os.system("./.pro/probis -ncpu " + processors_available_local
                        + " -extract -f1 " + target_complex_2 + ".pdb -c1 "
                        + whole_chain_compare_selection + " -srffile "
                        + target_complex_2 + ".srf")


        master_chain_list = []

        open("./srfs.txt", 'w').close()
        prot_list = []

        print("aaaaaa")
        print(examined_list_unique)

        for element in examined_list_unique:
            unique_chain_list = []
            # print element
            try:
                with open(element + ".pdb", "rt") as infile:
                    for linenumber, line in enumerate(infile):
                        if vzorec_3.search(line) != None:

                            unique_chain = str(line.rstrip('\n').split()[4])
                            if len(unique_chain) == 1:
                                unique_chain_list.append(unique_chain)
                            elif len(unique_chain) == 2:
                                #4WUC primer
                                #: HETATM 2976 NA  A NA A 403       8.964  15.893 -17.028  0.50 27.84          NA
                                unique_chain = str(line.rstrip('\n').split()[5][0])
                                unique_chain_list.append(unique_chain)
                            else:
                                # naslednja linija [4][0] je za primer PDBJA: 4BRI
                                # HETATM 5862  O2G UNP A1393      60.198   4.590  12.738  1.00 13.14           O
                                # klasicen PDB:
                                # HETATM 2769  N1  ARU A   1      35.314  25.889  32.623  1.00 60.17           N
                                unique_chain = str(line.rstrip('\n').split()[4][0])
                                unique_chain_list.append(unique_chain)

                        elif vzorec_3_supp.search(line) != None:
                                # tretji problematicen primer: PDB ID: 4BRP
                                # HETATM11092 BR    BR A1394      19.400 -62.788  -5.889  1.00 49.48          BR
                            unique_chain = str(line.rstrip('\n').split()[3][0])
                            unique_chain_list.append(unique_chain)
                        else:
                            pass


                unique_chain_list = list(set(unique_chain_list))
                master_chain_list.append(unique_chain_list)

                for chain_id in unique_chain_list:
                    # zacasna lista of unwanted
                    unwanted_chain = [1, "1", 2, "2", 3, "3", 4, "4", 5, "5", 6, "6", 7, "7", 8, "8", 9, "9"]

                    if chain_id in unwanted_chain:
                        pass

                    else:
                        # for probis 2.4.2
                        # os.system("./probis -extract -f1 " + element + ".pdb -c1 " + chain_id + " > " + element + chain_id + ".srf")
                        # for probis 2.4.7
                        os.system("./.pro/probis -ncpu " + processors_available_local
                                    + " -extract -f1 " + element + ".pdb -c1 "
                                    + chain_id + " -srffile " + element + chain_id + ".srf")

                        # print("./probis -compare -super -f1 " + target_complex_2 + ".srf -c1 " + chain_selection + " -f2 " + element + chain_id + ".srf -c2 " + chain_id)
                        srf_fajl = open("./srfs.txt", 'a')
                        srf_fajl.write(element + chain_id + ".srf " + chain_id + "\n")
                        srf_fajl.close()
                        prot_list.append(element + " " + chain_id)

                        pass
            except OSError:
                print("Database File not Found!, please investigate.")
    # ---------debug line-----------------------------------------------------------
        #print (master_chain_list) PAZI NA NASLEDNJO LINIJO
        srf_fajl.close()
    ##############################
        os.system("rm ./*.rota.pdb")
        os.system("rm ./AAA_NOSQL.nosql")
    ##############################

        if chain_sel == "not":
            # for probis 2.4.2
            # os.system("./probis -surfdb -local -sfile srfs.txt -f1 " + target_complex_2 + ".srf -c1 " + chain_selection)
            # for probis 2.4.7
            os.system("./.pro/probis -ncpu " + processors_available_local
                        + " -surfdb -local -sfile srfs.txt -f1 "
                        + target_complex_2 + ".srf -c1 "
                        + chain_selection + " -nosql AAA_NOSQL.nosql")

            # get json of alignmnts for comparison of chains
            os.system("./.pro/probis -ncpu " + processors_available_local
                        + " -results -f1 " + target_complex_2 + ".pdb -c1 "
                        + chain_selection + " -nosql AAA_NOSQL.nosql -json AAA_NOSQL.json")
        else:
            os.system("./.pro/probis -ncpu " + processors_available_local
                        + " -surfdb -sfile srfs.txt -f1 " + target_complex_2
                        + ".srf -c1 " + whole_chain_compare_selection + " -nosql AAA_NOSQL.nosql")

            os.system("./.pro/probis -ncpu " + processors_available_local
                        + " -results -f1 " + target_complex_2 + ".pdb -c1 "
                        + whole_chain_compare_selection + " -nosql AAA_NOSQL.nosql -json AAA_NOSQL.json")

        for element in prot_list:
            if chain_sel == "not":
                # for probis 2.4.2
                # print (element.split(" ")[0] + " ----  " + element.split(" ")[1])
                # os.system("./probis -align -alno 0 -f1 " + target_complex_2 + ".pdb -c1 " + chain_selection + " -f2 " + element.split(" ")[0] + ".pdb -c2 " + element.split(" ")[1])
                # for probis 2.4.7
                # -bkeep - DODANO NA NOVO
                os.system("./.pro/probis -ncpu " + processors_available_local
                        + " -align -bkeep -alno 0 -nosql AAA_NOSQL.nosql -f1 "
                        + target_complex_2 + ".pdb -c1 " + chain_selection
                        + " -f2 " + element.split(" ")[0] + ".pdb -c2 "
                        + element.split(" ")[1])
            else:
                os.system("./.pro/probis -ncpu " + processors_available_local
                        + " -align -bkeep -alno 0 -nosql AAA_NOSQL.nosql -f1 "
                        + target_complex_2 + ".pdb -c1 "
                        + whole_chain_compare_selection + " -f2 "
                        + element.split(" ")[0] + ".pdb -c2 " + element.split(" ")[1])

        print("Rotas done ... (alignment 0 !)")


        # correction of multiple or one chain per protein allignment
        aligned_unique = []
        aligned_discard = []
        helper = []
        if str(one_or_multiple) == "yes":
            with open("AAA_NOSQL.json") as json_fajl:
                z_data = json.load(json_fajl)
            for aligned in z_data:
                if str(aligned["pdb_id"]) in helper:
                    aligned_discard.append(str(aligned["pdb_id"]) + str(aligned["chain_id"]))
                else:
                    helper.append(str(aligned["pdb_id"]))
                    aligned_unique.append(str(aligned["pdb_id"]) + str(aligned["chain_id"]))

            if chain_sel == "not":
                for discarded in aligned_discard:
                    os.system("rm ./" + target_complex_2 + chain_selection
                                + "_" + str(discarded) + ".0.rota.pdb")
            else:
                for discarded in aligned_discard:
                    os.system("rm ./" + target_complex_2
                                + whole_chain_compare_selection
                                + "_" + str(discarded) + ".0.rota.pdb")

        else:
            pass



        # ----------------START WATER COLLECTION------------------------------------

        # vzorci vod v PDB

        # linija1 = "HETATM 3315  O   HOH A 653       6.657   0.611  50.201  1.00 22.92           O"
        # linija2 = "HETATM 6180  O   HOH A1063      46.720   3.111  27.787  1.00 51.91           O"
        # linija3 = "HETATM 3046  O  AHOH A 562      19.114  37.882  -1.866  0.50 24.61           O"
        # linija4 = "HETATM 3047  O  BHOH A 562      20.241  36.438  -1.021  0.50 30.54           O"
        # linija5 = "HETATM11839  O   HOH A2001      45.529  16.939  64.867  1.00 20.76           O"

        PDB_master_file_list = []
        imena_fajlov = glob("*.rota.pdb")
        # ZADNJI JE KOMPLEKS
        imena_fajlov.append(target_complex_2 + ".pdb")
        #print(imena_fajlov)

        vzorec_water_mining1 = re.compile("^" + "HETATM\s+\d+\s+\S+\s+" + "HOH" + "\s+\D\s+\d+\s+") # ok za linijo 1
        vzorec_water_mining2 = re.compile("^" + "HETATM\s+\d+\s+\S+\s+" + "HOH" + "\s+\D\d{4}\s+") # ok za linijo 2
        vzorec_water_mining3 = re.compile("^" + "HETATM\s+\d+\s+\S+\s+" + "\wHOH" + "\s+\D\s+\d+\s+") # ok za linijo 3,4
        vzorec_water_mining4 = re.compile("^" + "HETATM\d+\s+\S+\s+" + "HOH" + "\s+\D\d{4}\s+") # za linijo 5

    # VZOREC ZA END MODELA: VSAK *.rota.pdb ima MODEL2 zacetni kompleks
        vzorec_water_only_model_1 = re.compile("^" + "ENDMDL")
        # DEBUG LINE
        # print(imena_fajlov)

        for ime_fajla in imena_fajlov:
            # print (ime_fajla)
            lista_h2o = []
            with open(ime_fajla, 'r') as brani_fajl:
                for linija in brani_fajl:
                    if vzorec_water_mining1.search(linija) != None:
                        voda = linija.split()
                        voda.append(ime_fajla)
                        # print voda
                        lista_h2o.append(voda)

                    elif vzorec_water_mining2.search(linija) != None:
                        voda = linija.split()
                        voda.insert(5, voda[4][1:])
                        voda[4] = voda[4].strip("1234567890")
                        voda.append(ime_fajla)
                        lista_h2o.append(voda)

                    elif vzorec_water_mining3.search(linija) != None:
                        voda = linija.split()
                        voda[3] = voda[3][1:]
                        voda.append(ime_fajla)
                        lista_h2o.append(voda)

                    elif vzorec_water_mining4.search(linija) != None:
                        voda = linija.split()
                        voda.insert(4, voda[3][1:])
                        voda[3] = voda[3].strip("1234567890")
                        voda.insert(1, voda[0][6:])
                        voda[0] = voda[0].strip("1234567890")
                        voda.append(ime_fajla)
                        lista_h2o.append(voda)
                    # naslednja linija je kljucna zaradi 2 modelov v *.rota.pdb
                    elif vzorec_water_only_model_1.search(linija) != None:
                        break

                    else:
                        pass
                PDB_master_file_list.append(lista_h2o)





        # ----debug-----------------------------------------------------------------
        # print (PDB_master_file_list)
        MASTER_h2o_list = []
        fajl_list = []

        for PDB_water_fajl in PDB_master_file_list:
            try:
                for het, stev, atom, molekula, veriga, zapor, x, y, z, occ, R, atom2, fajl in PDB_water_fajl:

                    test = []
                    # test.append(het), test.append(stev), test.append(x), test.append(y), test.append(z)
                    test.append(x), test.append(y), test.append(z), test.append(fajl), test.append(R), test.append(zapor)
                    MASTER_h2o_list.append(test)
                    fajl_list.append(fajl)
            except (RuntimeError, TypeError, NameError, ValueError):
                pass

        entities = int(len(set(fajl_list)))
        #print ("AAA")
        #print (set(fajl_list))

        # naslednja linija je debug line
        # print (MASTER_h2o_list)
        T1.delete(1.0, tkinter.END)
        T1_text.set("Master water list includes %r molecules\n" % (len(MASTER_h2o_list)))
        # REPORT list 11,12
        report_list_1.append(str(find_value.get()) + " (sequence identity pre-cluster)")
        report_list_1.append("Master water list includes %r waters" % (len(MASTER_h2o_list)))

        T1.insert(tkinter.END, T1_text.get())
        T1_text.set("Superimposed chains: %r\n" % (entities))
        T1.insert(tkinter.END, T1_text.get())

        # print "Master lista vod narejena in vsebuje %r vod" % (len(MASTER_h2o_list))
        print("writing H2O master list")
        nova_datoteka = open("master_water_list.txt", "w")
        for tocka in MASTER_h2o_list:
            nova_datoteka.write("%s\n" % tocka)
        nova_datoteka.close()
        print("done...")
        nb.select(p2)

        # DBSCAN formatting-----------------------------------------------------

        # binding site clustering
        # BindingSites.bsite_unique_centers
        master_bsite_lista_vod = []
        master_bsite_lista_vod_koordinata_x = []
        master_bsite_lista_vod_koordinata_y = []
        master_bsite_lista_vod_koordinata_z = []

        master_lista_vod = []
        master_lista_vod_koordinata_x = []
        master_lista_vod_koordinata_y = []
        master_lista_vod_koordinata_z = []

        # POPRAVA VOD DA NE SEGAJO IZVEN CHAINA

        correction_x = []
        correction_y = []
        correction_z = []
        for element in lista_za_atome_xyzchain:
            if SELECTED_SITE_CHAIN == element[3]:
                correction_x.append(float(element[0]))
                correction_y.append(float(element[1]))
                correction_z.append(float(element[2]))

        global atom_max_x
        global atom_min_x
        global atom_max_y
        global atom_min_y
        global atom_max_z
        global atom_min_z

        atom_max_x = max(correction_x) + 4
        atom_min_x = min(correction_x) - 4
        atom_max_y = max(correction_y) + 4
        atom_min_y = min(correction_y) - 4
        atom_max_z = max(correction_z) + 4
        atom_min_z = min(correction_z) - 4

        global boundingBox

        boundingBox = [LINEWIDTH, 2.0, BEGIN, LINES,
                COLOR, float(1), float(0), float(0),

                VERTEX, atom_min_x, atom_min_y, atom_min_z,       #1
                VERTEX, atom_min_x, atom_min_y, atom_max_z,       #2

                VERTEX, atom_min_x, atom_max_y, atom_min_z,       #3
                VERTEX, atom_min_x, atom_max_y, atom_max_z,       #4

                VERTEX, atom_max_x, atom_min_y, atom_min_z,       #5
                VERTEX, atom_max_x, atom_min_y, atom_max_z,       #6

                VERTEX, atom_max_x, atom_max_y, atom_min_z,       #7
                VERTEX, atom_max_x, atom_max_y, atom_max_z,       #8


                VERTEX, atom_min_x, atom_min_y, atom_min_z,       #1
                VERTEX, atom_max_x, atom_min_y, atom_min_z,       #5

                VERTEX, atom_min_x, atom_max_y, atom_min_z,       #3
                VERTEX, atom_max_x, atom_max_y, atom_min_z,       #7

                VERTEX, atom_min_x, atom_max_y, atom_max_z,       #4
                VERTEX, atom_max_x, atom_max_y, atom_max_z,       #8

                VERTEX, atom_min_x, atom_min_y, atom_max_z,       #2
                VERTEX, atom_max_x, atom_min_y, atom_max_z,       #6


                VERTEX, atom_min_x, atom_min_y, atom_min_z,       #1
                VERTEX, atom_min_x, atom_max_y, atom_min_z,       #3

                VERTEX, atom_max_x, atom_min_y, atom_min_z,       #5
                VERTEX, atom_max_x, atom_max_y, atom_min_z,       #7

                VERTEX, atom_min_x, atom_min_y, atom_max_z,       #2
                VERTEX, atom_min_x, atom_max_y, atom_max_z,       #4

                VERTEX, atom_max_x, atom_min_y, atom_max_z,       #6
                VERTEX, atom_max_x, atom_max_y, atom_max_z,       #8

                END
        ]


        # ----------------------------------------------------------------------

        # cluster TESTING
        # mlv_datoteka = open("random_water_list5.txt", "r")
        mlv_datoteka = open("master_water_list.txt", "r")
        for linija in mlv_datoteka:
            vmesna_lista = []
            linija2 = linija.replace("[", "")
            linija3 = linija2.replace("]", "")
            linija4 = linija3.replace(" ", "")
            linija5 = linija4.replace("'", "")
            linija_lista = linija5.split(",")
            x = float(linija_lista[0])
            y = float(linija_lista[1])
            z = float(linija_lista[2])

            vmesna_lista.append(x)
            vmesna_lista.append(y)
            vmesna_lista.append(z)

            if bsite_space_check == "yes" and chain_sel == "not":

                # print("drugo mesto")
                # print(lista_za_atome_xyzchain)

                if SELECTED_SITE[4] - 4 <= vmesna_lista[0] <= SELECTED_SITE[5] + 4:
                    if SELECTED_SITE[6] - 4 <= vmesna_lista[1] <= SELECTED_SITE[7] + 4:
                        if SELECTED_SITE[8] - 4 <= vmesna_lista[2] <= SELECTED_SITE[9] + 4:
                            master_bsite_lista_vod.append(vmesna_lista)
                            x2 = float(vmesna_lista[0])
                            master_bsite_lista_vod_koordinata_x.append(x2)
                            y2 = float(vmesna_lista[1])
                            master_bsite_lista_vod_koordinata_y.append(y2)
                            z2 = float(vmesna_lista[2])
                            master_bsite_lista_vod_koordinata_z.append(z2)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

            if bsite_space_check == "not" and chain_sel == "not":
                if atom_min_x <= vmesna_lista[0] <= atom_max_x:
                    if atom_min_y <= vmesna_lista[1] <= atom_max_y:
                        if atom_min_z <= vmesna_lista[2] <= atom_max_z:
                            master_lista_vod_koordinata_x.append(x)
                            master_lista_vod_koordinata_y.append(y)
                            master_lista_vod_koordinata_z.append(z)
                            master_lista_vod.append(vmesna_lista)

            if chain_sel == "yes":
                if atom_min_x <= vmesna_lista[0] <= atom_max_x:
                    if atom_min_y <= vmesna_lista[1] <= atom_max_y:
                        if atom_min_z <= vmesna_lista[2] <= atom_max_z:
                            master_lista_vod_koordinata_x.append(x)
                            master_lista_vod_koordinata_y.append(y)
                            master_lista_vod_koordinata_z.append(z)
                            master_lista_vod.append(vmesna_lista)
            else:
                pass


        mlv_datoteka.close()
        # naslednja linija je samo za debug namen (odkomentiraj po potrebi)
        # print(master_bsite_lista_vod)
        # /DBSCAN formatting----------------------------------------------------

        def display_cluster_info(mlist, mlist_x, mlist_y, mlist_z):

            x_dim = max(mlist_x) - min(mlist_x)
            y_dim = max(mlist_y) - min(mlist_y)
            z_dim = max(mlist_z) - min(mlist_z)

            system_volume = round(x_dim * y_dim * z_dim)

            T1_text.set("System volume is: %d cubic A\n" % (system_volume))
            T1.insert(tkinter.END, T1_text.get())
            # report list 13,14,15
            report_list_1.append("System volume is: %d cubic A\n" % (system_volume))
            report_list_1.append("IDENTIFIED CLUSTERS: \n")
            report_list_1.append("-" * 25)


            def calculate_clusters(lista, sample_size):
                lista_np_array = np.array(lista)
                db3D = DBSCAN(eps=0.9, min_samples=sample_size).fit(lista_np_array)
                labels3D = db3D.labels_

                # print(labels3D)

                # Number of clusters in labels, ignoring noise if present.
                n_clusters_3D = len(set(labels3D)) - (1 if -1 in labels3D else 0)

                return int(n_clusters_3D)


            cluster_listbox.delete(0, tkinter.END)
            start_population = 2
            clus_num = calculate_clusters(mlist, start_population)
            cluster_collate_list = []
            max_population = 0

            while clus_num >= 1:

                consv = round((float(start_population)/float(entities)), 2)
                # limita ena je overloaded ker je lahko teoreticno prisotnih vec molekul vode na istem mestu v istem kristalu
                # glede na to da je smisel tega orodja v eksperimentalnih podatkih bi bile taksne vode na lokaciji manjsi od 1 A
                # nesmiselne in korigirane s strani kristalografa
                # zato lahko komot v skrajno nenavadno ali eksp-nekorigiranem primeru vrednost consv presega 1
                # taksne primere tukaj reduciramo na vrednost 1 kar pomeni, da je voda na tej lokaciji nastopa v vseh eksperimentalnih entitetah
                if consv > 1:
                    consv = 1.0
                else:
                    pass

                # za report list------------------------------------------------
                text_consv = int(round(consv*10)) * "*"
                st = 10 - len(text_consv)
                text_consv += st * " "
                # print consv
                if str(clus_num) == "1":
                    text = (str(clus_num) + " cluster with " + str(start_population)
                            + " H2O molecules. " +  "consv. " + str(consv))
                else:
                    text = (str(clus_num) + " clusters with " + str(start_population)
                            + " H2O molecules. " +  "consv. " + str(consv))
                num_spaces = 55 - len(text)
                report_list_1.append(text +  + num_spaces * " " + "[" + text_consv + "]")
                # REPORT LIST APPEND--------------------------------------------

                cluster_collate_list.append([clus_num, start_population, text])
                start_population += 1
                clus_num = calculate_clusters(mlist, start_population)
                max_population = start_population

            temp_collate = []
            for cluster_num, start_population, list_text in reversed(cluster_collate_list):

                if cluster_num not in temp_collate:

                    cluster_listbox.insert(tkinter.END, list_text)
                    temp_collate.append(cluster_num)
                else:
                    pass





            for i, listbox_entry in enumerate(cluster_listbox.get(0, tkinter.END)):

                if 0.9 <= float(listbox_entry.split()[7]):
                    cluster_listbox.itemconfig(i, {'bg':red10})
                elif 0.8 <=float(listbox_entry.split()[7]) < 0.9:
                    cluster_listbox.itemconfig(i, {'bg':red09})
                elif 0.7 <=float(listbox_entry.split()[7]) < 0.8:
                    cluster_listbox.itemconfig(i, {'bg':red08})
                elif 0.6 <=float(listbox_entry.split()[7]) < 0.7:
                    cluster_listbox.itemconfig(i, {'bg':red07})
                elif 0.5 <=float(listbox_entry.split()[7]) < 0.6:
                    cluster_listbox.itemconfig(i, {'bg':red06})
                elif 0.4 <=float(listbox_entry.split()[7]) < 0.5:
                    cluster_listbox.itemconfig(i, {'bg':red05})
                elif 0.3 <=float(listbox_entry.split()[7]) < 0.4:
                    cluster_listbox.itemconfig(i, {'bg':red04})
                elif 0.2 <=float(listbox_entry.split()[7]) < 0.3:
                    cluster_listbox.itemconfig(i, {'bg':red03})
                elif 0.1 <=float(listbox_entry.split()[7]) < 0.2:
                    cluster_listbox.itemconfig(i, {'bg':red02})
                else:
                    cluster_listbox.itemconfig(i, {'bg':red01})

            # report list  15
            report_list_1.append("-" * 25)
            max_pop_text = "Maximum occupied cluster contains %d H2O molecules \n binding site: %s" % (max_population - 1, SELECTED_SITE[0])
            T1_text.set(max_pop_text)
            T1.insert(tkinter.END, T1_text.get())
            report_list_1.insert(10, max_pop_text)

        if chain_sel == "yes":
            display_cluster_info(master_lista_vod, master_lista_vod_koordinata_x,
                                master_lista_vod_koordinata_y, master_lista_vod_koordinata_z)
        else:
            if bsite_space_check == "yes":
                display_cluster_info(master_bsite_lista_vod, master_bsite_lista_vod_koordinata_x,
                                    master_bsite_lista_vod_koordinata_y, master_bsite_lista_vod_koordinata_z)
            else:
                display_cluster_info(master_lista_vod, master_lista_vod_koordinata_x,
                                    master_lista_vod_koordinata_y, master_lista_vod_koordinata_z)






        # cleanup
        os.system("rm ./*.ent.gz")
        os.system("rm ./*.srf")
        os.system("rm ./*.rota.pdb")
        os.system("rm ./AAA_NOSQL*")
        os.system("rm ./query.json")
        os.system("rm ./info.json")
        os.system("rm ./srfs.txt")

        return None

class pyMOLinterface:
    """use wonderful pyMol for visualisation of collected results"""
    """thanks! Warren L. DeLano!"""

    @staticmethod
    def pyMOL_water_contacts():

        target_complex_3 = str(pdb_text.get()).lower()
        # za H-bond mejno razdajo kar 4 A
        pymol.cmd.do("select protein, polymer and %s" % (target_complex_3))
        pymol.cmd.do("select ligand, organic and %s" % (target_complex_3))
        pymol.cmd.do("select conserved_waters, H2O*")
        pymol.cmd.do("select donors, (elem n,o and (neighbor hydro)) and %s" % (target_complex_3))
        pymol.cmd.do("select acceptors, (elem o or (elem n and not (neighbor hydro))) and %s" % (target_complex_3))
        pymol.cmd.do("distance prot_acceptors, (protein and acceptors), conserved_waters, 4.0")
        pymol.cmd.do("distance prot_donors, (protein and donors), conserved_waters, 4.0")
        pymol.cmd.do("distance ligand_acceptors, (ligand and acceptors), conserved_waters, 4.0")
        pymol.cmd.do("distance ligand_donors, (ligand and donors), conserved_waters, 4.0")
        pymol.cmd.do("distance inter_conserved_H2O, conserved_waters, conserved_waters, 4.0")
        pymol.cmd.do("delete donors")
        pymol.cmd.do("delete acceptors")
        pymol.cmd.do("set dash_color, magenta")
        pymol.cmd.do("set dash_gap, 0.2")
        pymol.cmd.do("set dash_length, 0.2")
        pymol.cmd.do("set dash_round_ends, on")
        pymol.cmd.do("set dash_width, 3")



    @staticmethod
    def pyMOL_fetch_system():

        target_complex_3 = str(pdb_text.get()).lower()
        # print(target_complex_3)

        pymol.cmd.do("delete all")
        pymol.cmd.do("fetch %s" % (target_complex_3))
        pymol.cmd.do("center %s" % (target_complex_3))
        pymol.cmd.do("center %s" % (target_complex_3))
        pymol.cmd.do("hide everything, %s" % (target_complex_3))
        pymol.cmd.do("show cartoon, %s" % (target_complex_3))
        pymol.cmd.do("set cartoon_color, %s" % ("white"))
        pymol.cmd.do("hide lines, all")
        pymol.cmd.do("util.cbag")
        pymol.cmd.do("show surface, %s" % (target_complex_3))
        pymol.cmd.do("set transparency, 0.9")
        pymol.cmd.do("set surface_color, %s" % ("white"))
        pymol.cmd.do("show sticks, organic")
        pymol.cmd.do("color blue, organic")
        pymol.cmd.do("select %s_waters, resn hoh" % (target_complex_3))
        pymol.cmd.do("show nonbonded, %s_waters" % (target_complex_3))
        pymol.cmd.deselect()


    @staticmethod
    def pyMOL_chain_box():
        pymol.cmd.load_cgo(boundingBox, "box")

    @staticmethod
    def pyMOL_bsite_cluster():
        # display binding sites of clusters
        pymol.cmd.do("select bsites, H2O* around 6")
        pymol.cmd.do("select byres bsites")
        pymol.cmd.do("show sticks, byres bsites")
        pymol.cmd.do("util.cbay byres bsites")
        pymol.cmd.do("set_bond stick_radius, 0.1, byres bsites")
        pymol.cmd.do("select sele, name ca and byres bsites")
        pymol.cmd.do("label sele,\"%s-%s\" % (resn,resi)")
        pymol.cmd.do("set label_size, 18")
        pymol.cmd.do("set label_font_id, 7")
        pymol.cmd.do("show sticks, organic")
        pymol.cmd.do("color blue, organic")
        pymol.cmd.do("util.cnc organic")
        pymol.cmd.do("set_bond stick_radius, 0.25, organic")

    @staticmethod
    def pyMOL_display_cluster():

        display_clusters_setting = display_setting.get()
        bsite_space_check = bsite_vicinity_setting.get()
        chain_sel = whole_chain_setting.get()

        # za korekcijo in pogled R faktorja
        debye_waller_check = debye_waller_setting.get()

        # DBSCAN formatting-----------------------------------------------------

        # binding site clustering
        # BindingSites.bsite_unique_centers
        master_bsite_lista_vod = []
        master_bsite_lista_vod_koordinata_x = []
        master_bsite_lista_vod_koordinata_y = []
        master_bsite_lista_vod_koordinata_z = []
        master_lista_vod = []
        master_lista_vod_koordinata_x = []
        master_lista_vod_koordinata_y = []
        master_lista_vod_koordinata_z = []
        # za Debye Waller
        master_bsite_lista_atom_iso_displacement = []
        master_lista_atom_iso_displacement = []
        # master_lista_names = []
        master_bsite_lista_info = []
        master_lista_info = []

        mlv_datoteka = open("master_water_list.txt", "r")
        for linija in mlv_datoteka:
            vmesna_lista = []
            linija2 = linija.replace("[", "")
            linija3 = linija2.replace("]", "")
            linija4 = linija3.replace(" ", "")
            linija5 = linija4.replace("'", "")
            linija_lista = linija5.split(",")
            x = float(linija_lista[0])
            y = float(linija_lista[1])
            z = float(linija_lista[2])
            B = float(linija_lista[4])
            if B < 0:
                B = 0
            info = str(linija_lista[3]) + " location: " + str(linija_lista[5].strip("\n"))


            # anizotropni displcement bomo implementirali v V2 hopefully
            # + 1.4 je zaradi r H2O
            isotropni_displacement = math.sqrt(B/(8*((math.pi)**2))) + 1.4


            # master_lista_names.append(ime)


            vmesna_lista.append(x)
            vmesna_lista.append(y)
            vmesna_lista.append(z)



            if bsite_space_check == "yes" and chain_sel == "not":
                if SELECTED_SITE[4] - 4 <= vmesna_lista[0] <= SELECTED_SITE[5] + 4:
                    if SELECTED_SITE[6] - 4 <= vmesna_lista[1] <= SELECTED_SITE[7] + 4:
                        if SELECTED_SITE[8] - 4 <= vmesna_lista[2] <= SELECTED_SITE[9] + 4:
                            master_bsite_lista_vod.append(vmesna_lista)
                            x2 = float(vmesna_lista[0])
                            master_bsite_lista_vod_koordinata_x.append(x2)
                            y2 = float(vmesna_lista[1])
                            master_bsite_lista_vod_koordinata_y.append(y2)
                            z2 = float(vmesna_lista[2])
                            master_bsite_lista_vod_koordinata_z.append(z2)
                            master_bsite_lista_atom_iso_displacement.append(isotropni_displacement)
                            master_bsite_lista_info.append(info)

            if bsite_space_check == "not" and chain_sel == "not":
                if atom_min_x <= vmesna_lista[0] <= atom_max_x:
                    if atom_min_y <= vmesna_lista[1] <= atom_max_y:
                        if atom_min_z <= vmesna_lista[2] <= atom_max_z:
                            master_lista_vod_koordinata_x.append(x)
                            master_lista_vod_koordinata_y.append(y)
                            master_lista_vod_koordinata_z.append(z)
                            master_lista_vod.append(vmesna_lista)
                            master_lista_atom_iso_displacement.append(isotropni_displacement)
                            master_lista_info.append(info)

            if chain_sel == "yes":
                if atom_min_x <= vmesna_lista[0] <= atom_max_x:
                    if atom_min_y <= vmesna_lista[1] <= atom_max_y:
                        if atom_min_z <= vmesna_lista[2] <= atom_max_z:
                            master_lista_vod_koordinata_x.append(x)
                            master_lista_vod_koordinata_y.append(y)
                            master_lista_vod_koordinata_z.append(z)
                            master_lista_vod.append(vmesna_lista)
                            master_lista_atom_iso_displacement.append(isotropni_displacement)
                            master_lista_info.append(info)


            else:
                pass

        # /DBSCAN formatting----------------------------------------------------

        # BSITE LOKALNO ALI GLOBALNO NA VERIGI
        if bsite_space_check == "yes" and chain_sel == "not":
            master_lista_vod = master_bsite_lista_vod
            master_lista_atom_iso_displacement = master_bsite_lista_atom_iso_displacement
            master_lista_info = master_bsite_lista_info
        else:
            pass

        mlv_datoteka.close()


        try:
            # example:
            # 2 clusters with 14 H2O molecules consv. 0.67
            cluster_selection = int(cluster_listbox.get(cluster_listbox.curselection()).split()[3])
            consv_of_cluster = float(cluster_listbox.get(cluster_listbox.curselection()).split()[7])

            # print (cluster_selection)
            # report list
            report_list_1.append("\nBinding site info (name, avg x, y, z, min x, max x, min y, max y, min z, max z; box 4 A around extremes): \n" + str(SELECTED_SITE))
            report_list_1.append("\nExamined cluster with " + str(cluster_selection) + " H2O molecules\n")
            report_list_1.append("-" * 25)

        except:
            tkinter.messagebox.showwarning(title='ProBiS H2O warning', parent=master,
                                    message="please select clusters to display")
            return

        db3D = DBSCAN(eps=0.9, min_samples=cluster_selection).fit(np.array(master_lista_vod))
        labels3D = db3D.labels_

        #debug line:
        #print(labels3D)

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_3D = len(set(labels3D)) - (1 if -1 in labels3D else 0)

        i = 0
        clustri_tock = []
        tocke = []
        for element in labels3D:
            temp = []
            if element != -1:
                temp.append(master_lista_vod[i])
                temp.append(element)
                temp.append(master_lista_atom_iso_displacement[i])
                temp.append(master_lista_info[i])
                # temp.append(master_lista_names[i])
                # report list
                report_list_1.append(temp)
                tocke.append(temp)
                # report list

            else:
                pass
            i += 1


        if debye_waller_check == "not":

            if display_clusters_setting == "not":
                pymol.cmd.do("delete H2O*")
            else:
                pass

            for element in list(set(labels3D)):
                cluster_temp = []
                # print element
                for sub_element in tocke:
                    if sub_element[1] == element:
                        cluster_temp.append(sub_element[0])

                # print cluster_temp


                try:
                    # k_means_test = KMeans(n_clusters = 1).fit(cluster_temp)
                    # print ("means je ")
                    # print (k_means_test.cluster_centers_[0])
                    # koordinate = k_means_test.cluster_centers_[0][0]
                    print(cluster_temp[0][0])

                    pymol.cmd.do("set_color clus_color, [%f, %f, %f]" % (1.0, (1.0 - consv_of_cluster), (1.0 - consv_of_cluster)))

                    pymol.cmd.do("pseudoatom H2O_clus-%d_%.2f, vdw=1, color=clus_color, pos=[%f, %f, %f]" % (element, consv_of_cluster, cluster_temp[0][0], cluster_temp[0][1], cluster_temp[0][2]))
                    pymol.cmd.do("show spheres, H2O_clus-%d*" % (element))
                    # pymol.cmd.do("pseudoatom H2O_mined_cluster %d, vdw=1, color=tv_blue, pos=[%f, %f, %f]" % (cluster_selection, element[0][0], element[0][1], element[0][2]))
                except IndexError:
                    pass

        else:


            pymol.cmd.do("delete H2O*")
            pymol.cmd.do("delete iso_disp")

            for element in list(set(labels3D)):
                cluster_temp = []
                # print element
                for sub_element in tocke:
                    if sub_element[1] == element:
                        sub_element[0].append(sub_element[2])
                        cluster_temp.append(sub_element[0])

                # print (cluster_temp)


                try:

                    print(cluster_temp[0][0])
                    pymol.cmd.do("pseudoatom H2O_clus, vdw=1, color=red, pos=[%f, %f, %f]" % (cluster_temp[0][0], cluster_temp[0][1], cluster_temp[0][2]))
                    pymol.cmd.do("show spheres, H2O_clus")


                    for tocka in cluster_temp:
                        print(tocka)
                        pymol.cmd.do("pseudoatom iso_disp, vdw=%f, color=red, pos=[%f, %f, %f]" % (cluster_temp[0][3], cluster_temp[0][0], cluster_temp[0][1], cluster_temp[0][2]))

                    pymol.cmd.do("show dots, iso_disp")

                except IndexError:
                    pass


        # report on cluster
        nova_datoteka = open("report_" + str(pdb_text.get()).lower() + ".txt", "w")
        for linija in report_list_1:
            nova_datoteka.write("%s\n" % linija)
        nova_datoteka.close()
        print("report created...")

# thanks Janez for Support!
