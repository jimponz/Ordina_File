import os,shutil

def create_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

def move_ext_to_dirs(path):
    cont = 0
    totalSize = 0
    for f in os.listdir(path):
        if not os.path.isdir(os.path.join(path,f)):
            filename,fileext = os.path.splitext(f)
            if fileext != ".lnk" and fileext != "" and fileext != ".ini" and fileext != ".crdownload":
                if f != "ORDINA_FILE.py" and f != "ORDINA_FILE.exe" :
                    totalSize += os.stat(os.path.join(path,f)).st_size
                    ordpath = os.path.join(path,"ORDINATI")
                    create_dir(ordpath)
                    create_dir(os.path.join(ordpath,fileext[1:]))
                    newpath = os.path.join(ordpath,fileext[1:],f)
                    shutil.move(os.path.join(path,f),newpath)
                    cont += 1
    print("\nSpostati " + str(cont) + " files ("+ str(round(totalSize/1024/1024, 2)) + " Mb)"+" in " + dire)                             
    

home = os.path.expanduser('~')
dire = os.path.join(home,"Desktop")
#move_ext_to_dirs(dire)

dire = os.path.join(home,"Documents")
#move_ext_to_dirs(dire)

dire = os.path.join(home,"Downloads")
#move_ext_to_dirs(dire)

move_ext_to_dirs(os.getcwd())

input("\nPremi INVIO per uscire")
