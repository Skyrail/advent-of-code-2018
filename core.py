import os
import requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

SESSION_COOKIE = os.environ.get('SESSION_COOKIE')
REMOTE = os.environ.get('REMOTE')
WORK_DIR = os.path.dirname(__file__)

class Core:
    day = 0
    dirPath = WORK_DIR
    dataPath = WORK_DIR
    execPath = WORK_DIR

    def __init__(self, day: int):
        """ Initialises the necessary file/folder setup for the given day """
        self.day = day
        self.dirPath = os.path.join(WORK_DIR, f'day{day}')
        self.dataPath = os.path.join(self.dirPath, f'day{day}.data')
        self.execPath = os.path.join(self.dirPath, f'day{day}.py')

        self.setupFolder()
        self.setupFiles()

    def setupFiles(self):
        """ Attempts to setup the files for the day (data and executable) """
        try:
            if(not os.path.isfile(self.dataPath)):
                open(self.dataPath, 'x')

            if(not os.path.isfile(self.execPath)):
                open(self.execPath, 'x')
        except:
            pass

    def setupFolder(self):
        """ Attempts to setup the day's folder """
        if(not os.path.isdir(self.dirPath)):
            os.mkdir(self.dirPath)

    def getCookies(self) -> dict:
        """ Retrieves the cookie suitable to send in a HTTP request """
        return dict(session=SESSION_COOKIE)

    def getInputAsArray(self) -> list:
        """ Gets the task inpurt as an array split by \n """
        return self.getInput().split('\n')

    def getInput(self) -> str:
        """ Gets the task input, if we already have it it'll retrieve the file version """
        if(not os.path.isfile(self.dataPath)):
            return self.getInputFromRemote()
        else:
            return self.getInputFromFile()

    def getInputFromRemote(self) -> str:
        """ Retrieves the task data from the AoC website """
        request = requests.get(REMOTE.format(self.day), cookies=self.getCookies())
        self.saveFile(request.text)
        return request.text
    
    def getInputFromFile(self) -> str:
        """ Retrieves the task data from our cached data file """
        file = open(self.dataPath, 'r')
        return file.read().strip()

    def saveFile(self, content: str):
        """ Saves a data file with the given content """
        file = open(self.dataPath, 'w')
        file.write(content)
