#!/usr/bin/python3
# coding=utf-8

from tkinter import *
from tkinter.filedialog import askdirectory
import os
import re

class unapkg():
    def __init__(self):
# 指定目录
        root = Tk()
        root.withdraw()
        self.dirs = []
        self.indir = askdirectory(title="选择微信小程序的路径")
        self.indir = self.indir.replace("/","\\")
        self.outdir = askdirectory(title="存储位置")
        self.outdir = self.outdir.replace("/","\\")
        for dirs in os.walk(self.indir):
            self.dirs.append(dirs)
        self.filename = []
        for filename in self.dirs[0][1]:
            if re.match('wx',filename) != None:
                self.filename.append(filename)
        
        
# 解码
    def decode(self):
        exepath = os.getcwd() + "\\model\\decode\\main.exe"
        self.path = []
        for filename in self.filename:
            if os.listdir(self.indir + '\\' + filename)[0] != "":
                # 子包
                if len(os.listdir(self.indir + '\\' + filename + "\\" + os.listdir(self.indir + "\\" + filename)[0])) > 1:
                    os.mkdir(self.outdir + "\\" + filename)
                    for wxapkg_name in os.listdir(self.indir + '\\' + filename + "\\" + os.listdir(self.indir + "\\" + filename)[0]):
                        filepath = self.indir + '\\' + filename + "\\" + os.listdir(self.indir + "\\" + filename)[0] + "\\" + wxapkg_name
                        cmd = exepath + " -wxid " + filename + ' -in "' + filepath + '" -out ' + self.outdir + "\\" + filename + "\\" + wxapkg_name
                        os.system(cmd)
                else:
                    filepath = self.indir + '\\' + filename + "\\" + os.listdir(self.indir + "\\" + filename)[0] + "\__APP__.wxapkg"
                    cmd = exepath + " -wxid " + filename + ' -in "' + filepath + '" -out ' + self.outdir + "\\" + filename + ".wxapkg"
                    os.system(cmd)
# 反编译    
    def decompile(self):
        exepath = os.getcwd() + "\\model\\decompile\\bingo.bat"
        # for filename in os.listdir(self.outdir):
        #     if re.match('wx',filename) != None:
        #         cmd = exepath + " " + self.outdir + "\\" + filename +" && " + "del " + self.outdir + "\\" + filename
        #         os.system(cmd)
        for wxapkg in os.listdir(self.outdir):
            if re.match('wx',wxapkg) != None:
                # print(os.path.isdir(self.outdir + "\\" + wxapkg))
                if os.path.isdir(self.outdir + "\\" + wxapkg) == True:
                    # 子包
                    for filename in os.listdir(self.outdir + "\\"+wxapkg):
                        if filename != "__APP__.wxapkg":
                            cmd = exepath + " " + self.outdir + "\\" + wxapkg + "\\" + filename + " -s "+ self.outdir + "\\" + wxapkg + "\\__APP__.wxapkg"
                            os.system(cmd)
                        else:
                            cmd = exepath + " " + self.outdir + "\\" + wxapkg + "\\" + "__APP__.wxapkg"
                            os.system(cmd)
                        os.remove(self.outdir + "\\" + wxapkg + "\\" + filename)
                else:
                    cmd = exepath + " " + self.outdir + "\\" + wxapkg + " && del " + self.outdir + "\\" + wxapkg
                    os.system(cmd)
                
        os.system("explorer /root," + self.outdir) 
if __name__ == '__main__':
    wxapkg = unapkg()
    wxapkg.decode()
    wxapkg.decompile()
    
