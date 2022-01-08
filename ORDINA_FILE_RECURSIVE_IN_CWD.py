import os,shutil

def create_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

def move_ext_to_dirs(path):
    
    cont = 0
    totalSize = 0
    #for f in os.listdir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                complete_path = os.path.join(root, file)
                if not os.path.isdir(complete_path):
                    filename,fileext = os.path.splitext(file)
                    if fileext != ".lnk" and fileext != "" and fileext != ".ini" and fileext != ".crdownload":
                        if file != "ORDINA_FILE_AUTO_DOUBLECLICK.py" and file != "ORDINA_FILE.exe" :
                            totalSize += os.stat(complete_path).st_size
                            ordpath = os.path.join(path,"ORDINATI")
                            create_dir(ordpath)
                            create_dir(os.path.join(ordpath, fileext[1:]))
                            newpath = os.path.join(ordpath, fileext[1:], file)
                            shutil.move(complete_path, newpath)
                            cont += 1
            except Exception as ex:
                print("\nSi è verificata un'eccezione con il file:", complete_path)
                print(str(ex))
    print("\nSpostati " + str(cont) + " files ("+ str(round(totalSize/1024/1024, 2)) + " Mb)"+" in " + dire)                             
    

home = os.path.expanduser('~')
dire = os.path.join(home,"Desktop")
#move_ext_to_dirs(dire)

dire = os.path.join(home,"Documents")
#move_ext_to_dirs(dire)

dire = os.path.join(home,"Downloads")
#move_ext_to_dirs(dire)

dire = os.getcwd()
move_ext_to_dirs(dire)

input("\nPremi INVIO per uscire")
