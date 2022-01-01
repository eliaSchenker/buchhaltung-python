import os

class SaveLoadUtil:
    @staticmethod
    def getSavePath():
        homePath = os.path.expanduser('~')
        buchhaltungPath = homePath + "/Documents/Buchhaltung/"
        if not os.path.exists(buchhaltungPath):
            os.makedirs(buchhaltungPath)
        return buchhaltungPath
    @staticmethod
    def loadFile(fileName):
        filePath = SaveLoadUtil.getSavePath() + fileName
        #Check if the file exists
        if os.path.exists(filePath):
            with open(filePath, 'r', encoding="UTF-8") as f:
                return f.read().splitlines()
        else:
            #If the file doesn't exist, create it and return an empty array
            open(filePath, 'a').close()
            return []
    @staticmethod
    def saveFile(fileName, lines):
        with open(SaveLoadUtil.getSavePath() + fileName, 'w', encoding="UTF-8") as f:
            f.writelines(lines)