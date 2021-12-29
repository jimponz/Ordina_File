import os,shutil

class File:
    path = ""
    size = 0

    def format_bytes(self,size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return str(round(size,2)) + " " + power_labels[n]+'B'

    def __init__(self,path):
        if os.path.isfile(path):
            self.path = path
            self.size = os.stat(path).st_size

    def __str__(self):
        return "\nPath: " + self.path + "\nSize: " + self.format_bytes(self.size)


class OrdinaFile:
    path = ""
    listOfFiles = []
    file_exclusions = []
    message = ""

    def __init__(self, path):
        if os.path.isdir(path):
            self.path = path
            self.file_exclusions = ["", ".lnk", ".ini", ".crdownload"]
            self.message = "OrdinaFile inizializzato!"
            #self.move_ext_to_dirs(self.path)
        else:
            self.path = path
            self.file_exclusions = ["", ".lnk", ".ini", ".crdownload"]
            message = "Il percorso fornito non è valido!"
            self.message = message
            print(message)
            return None

    def __str__(self):
        return "\nPath: " + self.path + "\nFile_exclusions: " + str(self.file_exclusions) + "\nMessage: " + str(self.message)

    def create_dir(self, dirname):
        try:
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
        except Exception as ex:
            message = "Si è verificata un eccezione in create_dir!\n" + str(ex)
            self.message = message
            print(message)
            return self

    def analyze_dir(self):
        """serve per analizzare una cartella e caricare i file da spostare, senza spostarli"""
        cont = 0
        totalSize = 0
        self.listOfFiles = []
        dest = ""
        try:
            for file in os.listdir(self.path):
                if not os.path.isdir(os.path.join(self.path,file)):
                    filename, fileext = os.path.splitext(file)
                    if fileext not in self.file_exclusions:
                        if file != "ORDINA_FILE.py" and file != "ORDINA_FILE.exe":
                            totalSize += os.stat(os.path.join(self.path, file)).st_size

                            dest = os.path.join(self.path, "ORDINATI")
                            #newpath = os.path.join(dest, fileext[1:], file)

                            self.listOfFiles.append(os.path.join(self.path, file))
                            cont += 1

            message = "Vorrei spostare " + str(cont) + " files (" + File.format_bytes(self, totalSize) + ")"\
                      + " in " + dest
            self.message = message
            print(message)
            return self

        except Exception as ex:
            message = "Si è verificata un eccezione in analyze_dir!\n" + str(ex)
            self.message = message
            print(message)
            return self

    def move_to_dirs(self):
        """sposta i file ottenuti da analyze_dir"""
        cont = 0
        totalSize = 0
        moved_files = []
        ordpath = ""
        try:
            for path in self.listOfFiles:
                file = os.path.split(path)[-1]
                filename, fileext = os.path.splitext(file)
                totalSize += os.stat(os.path.join(self.path, file)).st_size

                ordpath = os.path.join(self.path, "ORDINATI")
                self.create_dir(ordpath)
                self.create_dir(os.path.join(ordpath, fileext[1:]))

                src = os.path.join(self.path, file)
                dest = ordpath + "\\" + fileext[1:] + "\\" + file

                res = shutil.move(src, dest)
                if res:
                    moved_files.append(res)

            message = "Spostati " + str(len(moved_files)) + " files (" + File.format_bytes(self,
                        totalSize) + ")" + " in " + ordpath
            self.message = message
            return moved_files

        except Exception as ex:
            message = "Si è verificata un eccezione in move_ext_to_dirs!\n" + str(ex)
            self.message = message
            print(message)
            return self

    # def move_ext_to_dirs(self, path):
    #     cont = 0
    #     totalSize = 0
    #     try:
    #         for file in os.listdir(path):
    #             if not os.path.isdir(os.path.join(path,file)):
    #                 filename,fileext = os.path.splitext(file)
    #                 if fileext not in self.file_exclusions:
    #                     if file != "ORDINA_FILE.py" and file != "ORDINA_FILE.exe" :
    #                         totalSize += os.stat(os.path.join(path,file)).st_size
    #                         ordpath = os.path.join(path,"ORDINATI")
    #                         self.create_dir(ordpath)
    #                         self.create_dir(os.path.join(ordpath,fileext[1:]))
    #                         newpath = os.path.join(ordpath,fileext[1:],file)
    #
    #                         shutil.move(os.path.join(path,file),newpath)
    #
    #                         cont += 1
    #
    #         message = "Spostati " + str(cont) + " files (" + File.format_bytes(self, totalSize) + ")" + " in " + path
    #         self.message = message
    #         print(message)
    #         return self
    #
    #     except Exception as ex:
    #         message = "Si è verificata un eccezione in move_ext_to_dirs!\n" + str(ex)
    #         self.message = message
    #         print(message)
    #         return self


## USAGE

#home = os.path.expanduser('~')
#dire = os.path.join(home,"Desktop")

#res = OrdinaFile(dire)
#print(res)
