import platform


class SaveLoadUtil:
    @staticmethod
    def getSavePath():
        import os
        homePath = os.path.expanduser('~')
        buchhaltungPath = homePath + "/Documents/Buchhaltung/"
        if not os.path.exists(buchhaltungPath):
            os.makedirs(buchhaltungPath)
        return buchhaltungPath
    @staticmethod
    def loadFile(fileName):
        with open(SaveLoadUtil.getSavePath() + fileName, 'r') as f:
            return f.readlines()
    @staticmethod
    def saveFile(fileName, lines):
        with open(SaveLoadUtil.getSavePath() + fileName, 'w') as f:
            f.writelines(lines)