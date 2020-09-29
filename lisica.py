'''
Described at PyMOL wiki: http://www.pymolwiki.org/index.php/lisica
 
'''

import os
import stat
import urllib.request, urllib.error, urllib.parse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import zipfile
import tempfile
import shutil
import json
import sys
import platform
from distutils.dir_util import copy_tree
from tkinter import *
from tkinter.ttk import *
import webbrowser
import time
import tkinter.messagebox

from threading import Thread
import contextlib

HOME_DIRECTORY=os.path.expanduser('~')
LISICA_DIRECTORY=os.path.join(HOME_DIRECTORY,".lisicagui")
versionFile = os.path.join(LISICA_DIRECTORY, "version.txt")


class Configuration:
    def __init__(self):

        self.system = platform.system()
        self.machine = platform.machine()
        self.architecture = platform.architecture()
        import struct
        self.python_bit = 8 * struct.calcsize("P")
        self.python_version = platform.python_version_tuple()

    def is_os_64bit(self):
        if self.system == 'Windows':
            return platform.architecture()[0] == "64bit"
        else:
            return platform.machine().endswith('64')

    def exe_File(self):
        if self.system == 'Windows':
            if self.is_os_64bit():
                exe_filename = "LiSiCAx64.exe"
            else:
                exe_filename = "LiSiCAx86.exe"

        elif self.system == 'Linux':
            exe_filename = "lisica"
        else:
            print("The plugin might not be compatible with your machine")
            exe_filename = "lisica"
        return exe_filename
        
    
    
class UpdateCheck:

    def __init__(self):
        self.firstVersionURL = "http://insilab.org/files/lisica-plugin/version.txt"
        self.firstArchiveURL = "http://insilab.org/files/lisica-plugin/archive.zip"
        self.currentVersion=""
        self.latestVersion = ""


    def installationFailed(self):
        global running, status
        status = "failed"
        running = False

    def deleteTmpDir(self):
        try:
            shutil.rmtree(self.tmpDir)
            print("deleted temporary ", self.tmpDir)
        except:
            print("error : could not remove temporary directory")


    def createTmpDir(self):
        try:
            self.tmpDir= tempfile.mkdtemp()
            print("created temporary ", self.tmpDir)
        except:
            print("error : could not create temporary directory")
            self.installationFailed()
        self.zipFileName=os.path.join(self.tmpDir, "archive.zip")

    def downloadInstall(self):
        try:
            print("Fetching plugin from the git server")
            urlcontent = urlopen(self.firstArchiveURL, timeout=5)
            zipcontent = urlcontent.read()
            LiSiCAzipFile = open(self.zipFileName, 'wb')
            LiSiCAzipFile.write(zipcontent)
        except HTTPError as e1:
            print("HTTP Error:", e1.code, e1.reason)
            self.installationFailed()
        except URLError as e2:
            print("URL Error:", e2.reason)
            self.installationFailed()
        except Exception as e:
            print("Error: download failed, check if http://insilab.org website is up...")
            self.installationFailed()
        finally:
            try:
                LiSiCAzipFile.close()
            except:
                pass
            try:
                urlcontent.close()
            except:
                pass

    def extractInstall(self):
        # this must be called before import LisicaGUI, otherwise
        # rmtree will fail on NFS systems due to open log file handle
        try:
            with contextlib.closing(zipfile.ZipFile(self.zipFileName, "r")) as LiSiCAzip:
                for member in LiSiCAzip.namelist():
                    masterDir = os.path.dirname(member)
                    break
                LiSiCAzip.extractall(self.tmpDir)
            # copy new
            copy_tree(os.path.join(self.tmpDir, masterDir, ".lisicagui"), LISICA_DIRECTORY)
        except:
            print("installation of lisicagui failed")
            self.installationFailed()

    def firstUpgrade(self):
        return not os.path.isdir(LISICA_DIRECTORY)


    def upgrade(self):

        #try:
        #    shutil.rmtree(LISICA_DIRECTORY)
        #except Exception, e:
        #    print e

        self.createTmpDir()
        self.downloadInstall()
        self.extractInstall()
        self.deleteTmpDir()

        # add executable properties
        configure=Configuration()
        exe_filename=configure.exe_File()
        exe_path=os.path.normpath(os.path.join(LISICA_DIRECTORY,"bin",exe_filename))
        st = os.stat(exe_path)
        os.chmod(exe_path, st.st_mode | stat.S_IEXEC)

        sys.path.append(os.path.normpath(os.path.join(LISICA_DIRECTORY, "modules")))

        self.writeToVersionTxt(self.latestVersion)

        print("Upgrade finished successfully!")
        global running, status
        status = "start"
        running = False

    #
    # read current version of probis from version.txt file
    #
    def findCurrentVersion(self):

        if os.path.isfile(versionFile):
            with open(versionFile, 'r') as myFile:
                lines = myFile.readlines()
            if len(lines) == 1:
                self.currentVersion = lines[0].strip()
            else:
                date = lines[len(lines)-1].split('\t')[2]
                t = time.strftime("%d/%m/%Y")

                tmpTime1 = date.split('/')
                tmpTime2 = t.split('/')
                if int(tmpTime2[2]) > int(tmpTime1[2]) or int(tmpTime2[1]) > int(tmpTime1[1]) or int(tmpTime2[0]) > int(tmpTime1[0])+15:
                    self.currentVersion = lines[0].strip()
                else:
                    self.currentVersion = (lines[len(lines)-1].split('\t')[0]).strip()


    #
    # get info about latest version
    #
    def findLatestVersion(self):
        try:
            # from insilab git server
            versionFile = urllib.request.urlopen(self.firstVersionURL, timeout=5)
            self.latestVersion = versionFile.read().strip()
            
            if len(self.latestVersion) > 6:
                self.latestVersion = ""
                
            print("l1 = ", self.latestVersion)

        except HTTPError as e1:
            print("HTTP Error:", e1.code, e1.reason)
        except URLError as e2:
            print("URL Error:", e2.reason)
        except Exception as e:
            print("URL Error: Is Insilab webpage (http://insilab.org) down?")


    #
    # yes or no update window
    #
    def updateWindow(self):

        self.window=Tk()
        self.window.title("Software Update")

        frame = Frame(self.window)
        frame.pack()

        Label(frame, text="A new LiSiCA GUI version is available. Do you want to update?", anchor=CENTER).pack(pady=(20,10), padx=30, fill=BOTH, expand=1)


        versionFrame = Frame(self.window)
        versionFrame.pack(fill=BOTH, expand=1, padx=15, pady=(0,10))

        Label(versionFrame, text="Current version: ").grid(column=0, row=0, sticky=W, padx=(30,0), pady=(10,0))
        Label(versionFrame, text="Latest version: ").grid(column=0, row=1, sticky=W, padx=(30,0), pady=(0,10))

        Label(versionFrame, text=self.currentVersion).grid(column=1, row=0, sticky=W, padx=10, pady=(10,0))
        Label(versionFrame, text=self.latestVersion).grid(column=1, row=1, sticky=W, padx=10, pady=(0,10))
        Label(versionFrame, text="For more information about software update, go to:", font=("Times",10)).grid(column=0, columnspan=2, row=3, padx=30)
        urlLabel = Label(versionFrame, text="http://www.insilab.org/lisica", font=("Times",10),foreground="blue",underline=True)
        urlLabel.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=30, sticky=W)
        urlLabel.bind("<Button-1>", self.open_url)

        self.checkRemindMe = 0
        Checkbutton(self.window, command=self.setCheckRemindMe, text="Do not ask me again").pack(fill=BOTH, expand=1, padx=60)

        buttonsFrame = Frame(self.window)
        buttonsFrame.pack(fill=BOTH, expand=1, padx=30, pady=(10,20))
        Button(buttonsFrame, text='Cancel', command=self.cancelButton).grid(row=0, column=0, padx=(200, 20), pady=(0,10))
        Button(buttonsFrame, text='Update', command=self.updateButton).grid(row=0, column=1, pady=(0,10))

        self.window.bind('<Return>', self.updateButton)
        self.window.protocol('WM_DELETE_WINDOW', self.cancelButton)

        self.window.mainloop()



    def open_url(self, e):
        try:
            webbrowser.open_new(r"http://www.insilab.org/lisica")
        except:
            print("Error: Could not open the website.")

    def setCheckRemindMe(self):
        if self.checkRemindMe == 0:
            self.checkRemindMe = 1
        else:
            self.checkRemindMe = 0

    def cancelButton(self):
        if self.checkRemindMe  == 1:
            self.writeToVersionTxt(self.latestVersion, True)
        self.window.quit()


    def updateButton(self, event=None):
        global status
        status = "update"
        self.window.quit()


    #
    # write to version.txt file
    #
    def writeToVersionTxt(self, version, reminder=False):

        if reminder:
            with open(versionFile, 'a') as myfile:
                myfile.write(version+"\t later \t"+time.strftime("%d/%m/%Y")+"\n")

        else:
            with open(versionFile, 'w') as myfile:
                myfile.write(version+"\n")


def internetOn():
        try:
            urllib.request.urlopen('http://www.google.com',timeout=1)
            return True
        except:
            pass
        return False


def showManualDlInfo():
    tkinter.messagebox.showinfo("Installation failed.", "To download and manually install LiSiCA GUI please visit our website http://www.insilab.org/lisica/download.php .")
    #pass

def run():

    print("Initialising LiSiCA ...")

    global running, updateObj, status
    status = "start"

    try:
        sys.path.remove('')
    except:
        pass

    updateObj = UpdateCheck()

    if updateObj.firstUpgrade():
        if not internetOn():
            status = "no-internet"
        else:
            updateObj.findLatestVersion()
            updateObj.upgrade()
    else:
        updateObj.findCurrentVersion()

        if internetOn():
            updateObj.findLatestVersion()

            if updateObj.currentVersion == "UPDATE NOW":
                updateObj.upgrade()

            elif updateObj.latestVersion != updateObj.currentVersion:
                status = "check-update"

    running = False


class FuncThread(Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        Thread.__init__(self)

    def run(self):
        self._target(*self._args)


class Logo(Frame):

    def __init__(self, parent, txt):
        Frame.__init__(self, parent)

        self.parent = parent

        # move window to center
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.parent.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.parent.geometry("%dx%d+%d+%d" % (size + (x, y)))

        s = Style()
        s.configure("My.TFrame", background='#BFBFBF')

        frame=Frame(self.parent, style="My.TFrame")
        frame.pack(fill=BOTH, expand=1)

        raw_data = """R0lGODlhgACAAOf/ACUAAyoBABUAWDUCADwBAA0OCwoGZBcPB0cCABoPEDEKAzkMBB0UFVQGABYXFRUXJxcPdCkPQxoPgB0a
                      ElcKDRcVYBscGmIKAD0VBEMTCSQdFDMbEl0RAiUeK0gYCCEjIU0YEnAPD1MbCikcfiQcmywmIR4dpTAmGCcaqi4Ww2UZBSgl
                      TlkfCGEcFSkrKDMhcTcnKk8jDEQlGSoikmwdAywsLysmbi0rOFsiC0sjOzctHVMmEEkkR1EmHjMuKk8oFCsg0CgjxWUkClwn
                      FC4vTislujAyLy8mslUpLGwnBWUnIncmADgvZS4rrDw0KmYrFDY3M1IrYDouiVcxH0E3JXYrAEI2MkQ1Rks2Ki0t3GwvEnop
                      J3EuFGwwGW4xDqkeJHUxCTw9O3swBHUxEZolHbQeHmU1I38yAMAcIDgy33M1GNAaInw2B3k1GkQ9a4I1CkNDQX03EFs/MHc5
                      Gzs262A/K0c2zkhBZlZCO05FOjo493U8IoM8FU9JQ4A/HEVEoHRCKktMSYdAGIRCGHNGLfYhJ4xDHFBRTYNHIVNRVWhOQpFH
                      GZBHIF1USYlNJlhMwVtTc5VLI4ZPMGpWPlhZVn5SOpZNK5tQKHpZRF5gXYtXNF1an2pffGRlY4tdQnBkVJVdOWpnX35mWmNg
                      6mllv4ppU5RoRIZrWXZwZ3luhJZsU3V3dIt1W4h2Z5p1WZV6Z35/fYR+d4WAc5Z9b5mGbqOEZpWJZqSIdY6NipOKraCNfZqR
                      l6KTfJ2UhaeUeK+XfJublKebia6chqSau6udmq2jhKOkoamklrOhl7CkjLKmlK+ourSrkrerjLSumrStpq2vrLuunLyykrq0
                      oLy1p8K1o7q2tcC3ncK5n8S5msG6pr67rMS+qca9tsq9q8fBrcrBp8DCv8fBwMrEsMfGvdDHrdPGs8/JtNLMt9zMtNvNu9PO
                      ztjSvdbTxNXTyt/XvN/Yw9fZ097ay97Z19/bzN/f3OTg0d3j5ejk1e/o1Ojq5+/s3PDy7/fz5Pr8+f///yH+EUNyZWF0ZWQg
                      d2l0aCBHSU1QACH5BAEKAP8ALAAAAACAAIAAAAj+AP8JHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNq3Mixo8ePIEOKHEmy
                      pMmTKFOqXMmypcuXMGPKnEmzps2bOHPq3Mmzp8+fQIMKHUq0qNGjSJMqXcq0qdOnNuPwGcTTkCE+PvlcNcTIUqSaVgXxWSTI
                      ZxxNtTwh4mrJEkxHkRgZQmSqlqayPeNEisYN2StNhiJdusQykmFEkl4h83bNEda8fH6dQ4eO2y1PXAd/lehWIqNLVj350kbZ
                      3C0+b36+MTVOnbt27boJM+Vo0eDOCdtaGsy7N2GFbRnRDdYN9mtypt6A+QlG0LV28OjBg9fOXDJVtW8bbNt7t+/v2y3+CVel
                      zBz06NSvoQYKRkwtdNHpyZN3XJmr7L8N796v+/Yl799tFokliyCiCjLjtOPOfPRIh04tYiwHlBiOJChPg9JRh0431/HmHXff
                      XTKgV/8B6N8ljriiDDfoQHehPQ22w40kYlQRVBVi/IKOO/FpOI43ybgCymf9tSWYYUgi6dWAR4r4XySg1JKMNuTABs989KEj
                      TI1DLQHKNy3C1s6Gs13SFXeMJKnmmnGJyGYki1hiijAsWjkmN5pwKRSOwoxDDjrndDONK4sYsggjiKap5iJxIclomooaFqma
                      cjHiyjTf/InOOMKAsURRS5hCDTfcUCOMJloZWmiirCIK5yL+hcZ6KCOHwkprq7SSJYgmxWhDKjWmLJFEUUmwEYwzzvCCyBuC
                      WOVsrbcaKq2z1D5rla20ViuIIG8goguyvnh61BKeJENLHGy8wQcfzVZbaLXUDmKVvO7Ca8i226LrBy3JeLIEDeOywUocYrDB
                      xrrsbntvswwLMsggWkVsiLypprrwvfeuKxYf6YrhBytsfIqUGCSTbLBU7CaMb8JTXYXwyxFHjO/ML7PRXskiH1WyyQfD7PPP
                      6v4sNMJvGMxGjSTnDOrOBRtc9NCoRf3G1FNLHTTQqBnNtNJELVEjjmAY/UYcUx9ctNMGo0b2IOnyQfbYqI1dNNVxn330zmcM
                      axT+yTjynC7VRceBiCaeaIJIuk6XbfbbZyPiiSeSIILu2EaH3fcZXAt1Bt88o/s2G5IEI846pIsTjCRoH5w42WBIosvopFuj
                      C+pG28y0jaBuXnLtcscxyzr3BC/8PeSo8je6apPNhiviDC/8Oq/UfjPOR+nuNxtkizHLPM7r4/0965QC+BttlK3KOt6nP/w8
                      rWg9vZ5FiWE99k6L4Qn6wosDDC6xPHOPPuJAHeOm5glx6GMdz+gFKnCBv/+tg0aVkx/8iCJBkoHhDNiLAxiIkT59GCMW4hCH
                      EzTQCHHwgxjjm9ozAAiMdXRDBxpwgjH4kT5dhM1gJcPcUaqAwabJrVv+JtQHP54BDH7MIw8n0EAMm+eJt6GrFPewxgzdgUQY
                      luAZNORHN+agtbslxWRNM9gZJDEPfvDjHrgQYix0QAUdwBAL80DG31S4DlQIERVspIIPTtAHIfLjgU0L2+a+eLSToYsNnriH
                      GZ8RC3/MQw5UiCQVkhiLdSzrDeSaxydiYcQ8SNKNJbCGP4xIo0OSDClVSGUY0eaJevDDH8DwASqC0UY2+sAHffAB9M5QtFmI
                      owQ+iAUwasnGRpQAGKOcR57QVTC+4e4nSehbyW5WOzFIwh6vBIYSNXCCbnKTGHXEhRzfMIZqxOIA2+zmCXRwjHks0B/+WAcg
                      cHi3naUSKNL+nGbtzrAHccDTGBPYpkCB4Q5U9KEb5eODOPqAToEqsYWfMMYou0GwQnLua11iWjPTBQZkvNIaE5jAAUZ6gAL4
                      IA9WKEAo+bAERIC0ACQdaQGc0AcnTMCf/AhG08TgtSos4Z5FGQRPNUoyU7iyHiWAqQZK4AQqoCIWfVDEJ64xC1fUAhmNyCoW
                      sOCEEkyACk5QqSuV2TevLcFrSJFGLRDBU596jaeDeEY7yNGLXiDjGtXwRjfM4Q10pCMd3egGZYqTjsGOQxvPIEYvYjELesxj
                      GpJAl0/PEAdT/IIZRvFGORjzC1MgYhCDU8UvmpHX1qjDSux4x3mmw1oesXY6sGH+BzzYwQ51dMMb2tDGNYTxi18IoxncGIc5
                      pkEUb/wVHebgq261odlyoEMdsn2tdKZL3QbFB0PoyRBr36GOdJgDuX397l/LMZRq/PW86VAHZZ6rDnW8lrUYim+D8CHf+qLn
                      te+YLW3be97uakMoxvWuOdLbXtrS9r3ZrW996StfBL/WwPDobjrKcVzi/kQZuiVuOfj7jnSk9sPRfS+MsGsPeMBoxPYo8XTy
                      q+J3pFa/tD0vef9xjWtIoyjgQO95DQzh91bXxNeVDjtSbGIex1jHE57wNZCCjXI4+clJJrCREYyhFGP3vUbmr4wn/ORsMNnJ
                      4ABHOcL8ZCf71cM9fq/+PBw8W/3KuMzNLXM5mmGUZIQZG9nIczP2LI08k5nC0E0zm/Nr4O6COcx5zkaNs4GNMIf5xkXhhTB8
                      QemDULoZ2RAzZQrcZjbzWL1jzkYzKn2QZiSjGcoQBkns8RJaNEPMzkWzbA8cXSOn4xxjbgYvbKGSfQxkH6z+Rz7wMZ2WeGAS
                      xWj0OGKNDiPz+K+4Bgc2ilGKIaAEHvjYh6/3kY9+aNvb+8CHsTGggDoUoxrjEPNk2CFrdjwXUOgIdTEw4QERWLsk9tC2vsG9
                      D34Pm9gpYQELRJCBBSAbG8v+RjnOwfDjFvYc6QbHNJpRCoE/wQtaWLW+N87xb/eDHim5+BP+cPAERSjiFM1o9DfAoXCGM3wc
                      4/jGyrHRjFYoQhSA8EIc4uAFkWS7Hh3neD7yAWyVjGEMXvDDK2zRik+4utEsd/Q3Ih7midMCE63QBS80wQY/DGIMH6HH0Ike
                      dI7jY9gpGcPO+XCLZCAjGLrIOjOwQXepg0MbdJfGqEVxCl0ggxm/cIzbOmKPbOPj8EPX9+HDrfjDwwMlY2jDzl3hjGhMIxrK
                      iHsxmCENbEyD7qDHhjSkUQxbfEIXyrB8NGiBsDZoRB6Hj73sZR/u2dM3JTqPAyiYMY1q5HYawZiFLYox+uIbvxmlxwQtgjGN
                      3zvDFeri+UWwbfvqVz/FuN/5IHz+0Xtf5TYaurDF8JvB+eIzA/m+YIUodBGN3GqjGtNIhiXcFgeLDFk+KcZH4fVv/djDCB0p
                      AQYapAqWl1vecIDaoAy00AqSJgqKUAd1oAitUAy+YHqzgAzMhYDVEA2vIBVxoDcSwQ7SkWLykGImeIIoaIIglxJJoC/JQA58
                      cYDe8CPVIAyt0AoyAAAHAAA8CAB1YAui8ArBcA3c4A3RQA7foA3ToAyOgD0SEhHcwFryQFslWGImaGImWIIXQh3ngHtHYwrz
                      EA+woA0w5w3m8CPRcAtYAAAK0IYBoAA8OAmsEAzRMIPfAAvxUA/vFw2uYDQg6BCEMA3s0A7jQAu0cCX+awZkCIYl08EOJIEG
                      BQEGAkgLwBAO/GAMygBzyWUO2hAMZvCGbRiKAKAIdKhZ0TBD4kAMv1cMbAMGwwKJDgEIwUULgPAE0sBmDgYdjjgShYAGITAQ
                      SRAhiJAMznAM4QANYYAKZBgPz9AXihCKbTgAbYgL7rAN04AKYQAN4fAMefV+zpAnbJAEIYAGhdAQT4AJt0AIWvAEryAmrAUd
                      qwVb7eBuJVEGvgiMkmgKzuB7lBAGLmABlGCJH6QNtEBu0BgAVjBD4UAJFuACYZAJZfh+g4Ij4ogGZcAQXbAHe6AGaqAFgCCI
                      gygmIikmBgaAG8EP4YAQIUABFDAQVQAGVfD+Cs2nDYfgAjVQAH0QC7CQCc5QDtNwCgapAAuABaeQCbAAVQVQAy5wCArnDdyg
                      hLxwNFXAARTwiwdhif8ACHOwlVupBbTgcs1GW/PobICyEfoADPEQDoeAEF9AEKnEBrwgDb6CCh/gAsHwXTGnXocVDKIwCScn
                      DNVQDQOGDsHgAx+ACmWIW9NQDH6QSjTQlgdxCOEQD8CgD57AlXNQCd/ADLwAJgZGDu62Xi+3EdBQD+GwCpSQED7gllUQB8Iw
                      k4lgBOXxXezFX8p1DWJGYPwVDUaQCGe4WbqlDIiQSjGwmghBCasQDvXwCnOwB22wB7zgCpUwDS53DuRQnS73DR3+AQtwQAlG
                      gBCBEAYf4JJV4AfK0HzLoAc2IFzrVWD7xWMuVmjqZQN6sAy35ZTT8I2pVAJhEAgI4QOUAAeigJmVQAhmoAxIKHPYeQ7fcA7/
                      5RGBYAQOcBBhAAdQYAEu2VK8NwxpAASpsImbBl3vMKIkSqKFVlipAAR0MAwH+JTfuAQsYAFQAAdhYBA/4ABGEAhy0Jx7MAdq
                      sAevWQyswAwK2qAM+g3O8BGHYAQ10JAdQBB/AAcu8AEOMKX/4FOIwAzDQAd6QAJuwJ5+9VyzRaIrBg8jul/q5QYkoAcrip/O
                      UAkb4AIOUJdw8AcEAQP/WANGgAdb2QbNyQqsQAhPwAr+3CBzhrpyIGGaFlAABfABNmACaRAEaZAFT8qoH6CUcGAEWHAHdBAE
                      RYACTJBc7cluqTWiZmqi+1VYTIACRRAEdHAHoWAE/lgDJYABBfAPHZAFkZoGJmADJbABDGAB4RANlcCVe6AFWiCT0zAq31Co
                      SfoR/AAMmVAQJqAHRQABBlAQBeACEWoBNfACnFABEjAD1CCq6YVmJWqq8dle6kANMyABFZAKL9CkOeoCGEADKjAQBgABRaAH
                      JsADXeCjXUAJReQKxuoKtOAJxUANyzp6IAEN0IALBlEERxAE2WoQRuACLpAAqDANw5ALmzADgaANtPlX8VmqZyqf3xAIM7D+
                      CbnAorJQly7gA0nwh/9gAEFwBFLQBRypBnNgBrgADbOwlT9qBmagC9PweZglEnCAEBIAAQnBAAkwBXSYgS5gBFCACuZwDu7w
                      DOVgYCaKDs/gDrWFClCQsWf4I96ACg5gAYSwBPlKED0AASPAsxzpo3NQB3Lgp1vZBYTwLfm5tCuRBSmQEFZQAkLAfbnVC6EQ
                      oQ4QkPUADb3gngbWC6W5kDgaCKEQDGrLDb1gBHAwBjTAAQTxBEOQAkfQBXbrs2rQBj5LtIDAd6f2EkSwAoZbAiygrNrAuBmb
                      AHCwCrCAC8rAroHGDs6AC7CwCnCQAFcbCr0QkZ8LB0kwugPxBKb+SwRX0LPaS7Q+2wXIagvJABNQ4AIJEQY+4AGV4AzNxwyB
                      8AFQcJecSBrqRbztxVyUEQxQ8AGBwAxq6wyyIKsqELf/YL1aMAQuYAXam8AcqbpagAkxAQeBAAUTahAQbARTGwy7QAqjIAWh
                      AHOauF7rda7HVRrmEApSMAqkQAzcELM5CgekOwRD8ATrqAFQEAh4YLc4zLNmgKwzEQZhYAS3ahA/LKFG0ASPQAdZQALTcFua
                      KKog/MTIlVzcQAJZQAeP0ARELKs9EMMELAMFIKthoLpizMA8HBNlsAZbYAQW4AAOUAMjMBB64AZyWgAK0AGQSgckcAekMoMz
                      uIkgSpv+yeXBMHcHJEAHvHoDh2ABDOACbmAHPBAFOWADNcDGFuADW/AFZEAG65hxM9GLFLAGBPEAreqvQCABA9EAAYwCqgwJ
                      GahX5bBswuXHmwjLHgwJqowCysAMwSAEDSACEAAE1eqpHbADMTwEaEAB5GgT9njMBzGpKCAABcEBF4AETAAJvtfKB9jEsZy2
                      goyAnMAEu4B5mNAADRDDEYACupoD1lvM/4DMFmkTK4kQJCABplwQDSDNpVB51+wrRZjNgvzPnfuU2hANzvAKHNDLpju3EjAC
                      MGwQVSkUQVDP9swBKvAKzBAN17zHMvgjZai2TinQShgNzKALLUDOBCEBQdD+FE0AtQdxzyowC8ygvvssgx9N06QC0pfnDLrw
                      BA2AAAUBAU3QFBeaEOTcAq2gDJU3k973lKTCz+4nkdFwDLTQAj5tEDLKFDRKvgmBAPeMCcEQ00mr1E/tfmHtDMyQDKXQAASw
                      AAfhkE2rFIEQCFd7ECKwAANAAFz9BK0QDMdQeZYX1r0Hf89A0MeQDK1gBgSw1hkgAgL8Dxkb10cRufrQCeMbkBJLEEkgBARn
                      13jdAEpQCrpADEiNLASNLM6gDMnQC6dgBggwAAuQASCgAkLABXqDCwvpAlDQCfpQmkNxicYAC4waCPEQrQIhBE/ABVwgBEMg
                      Ah7A2Z1tBphwCsvpFwzUHXeYYAYgQACuvdhDMNvIzQVdUETxEAiMCgvGMENDgQurYBAQO8BHd3TI/QSaDQIFpwADcNd4DQL6
                      Td/aHQADgAH1Ztxc0AbI3QZjYAbtXRCrcNlL8QRH1wYQHuFqwAXyvdkBcOEYjuE9uAAgIOAR/uFtMAV18ARQUbptwAcnjuIS
                      PnIZAIcAoOE8eOEvHgBsmAEk17ofvi4QDnYlLhBDgOMQ3gXWiwMeMAA9GOMzTuMZ/uI9OACLbdwB+5yuS+I9PhBD0AL3BhIt
                      gOVV3uVe/uVgHuZiPuZkXuZmfuZonuZqvuYVERAAOw=="""

        photo=PhotoImage(master=self, data=raw_data)
        display=Label(frame, image=photo, background="#BFBFBF")
        display.image=photo
        display.pack(ipady=10, ipadx=50, fill=BOTH)

        Label(frame, text=txt, anchor=E, font = "Fixedsys 10 bold").pack(ipady=0, ipadx=0, fill=BOTH)

        global running
        running = True

        if txt == "Starting Software ":
            t = FuncThread(run)
        else:
            global updateObj
            #shutil.rmtree(LISICA_DIRECTORY)
            t = FuncThread(updateObj.upgrade)
        t.daemon = True
        t.start()

        while running:
            self.parent.update_idletasks()
            self.parent.update()

        self.parent.destroy()


def main():
    root = Tk()
    root.overrideredirect(1)
    root.geometry("250x170")
    Logo(root, "Starting Software ")

    global updateObj, status

    if status == "no-internet":
        #pass
        tkinter.messagebox.showinfo("Communication Error", "No Internet connection available. Please make sure that your device is connected to the Internet.")

    if status == "check-update":
        status = "start"
        updateObj.updateWindow()
        updateObj.window.destroy()
        if status == "update":
            root = Tk()
            root.overrideredirect(1)
            root.geometry("250x170")
            Logo(root, "Updating Software ")

    if status == "start":
        print("Python version: "+platform.architecture()[0])
        sys.path.append(os.path.normpath(os.path.join(LISICA_DIRECTORY, "modules")))
        del status, updateObj # remove global variables
        import LisicaGUI
        LisicaGUI.main()

    elif status == "failed":
        showManualDlInfo()


def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command', 'LiSiCA', label='LiSiCA', command=lambda s=self: main())
