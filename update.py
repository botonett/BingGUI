from github import Github
from appJar import gui
import os
import shutil
import fileinput
import time
from shutil import copyfile
from unipath import Path
import sys

current_user = os.getlogin()
current_working_dir, filename = os.path.split(os.path.abspath(__file__))
home = Path(current_working_dir).parent
sys.path.append(home)
os.chdir(current_working_dir)

def primaryUpdate():
    try:
        account,password = getAccount() 
        #create a Github instance:
        serverVersion = 0
        g = Github(account, password)
        for repo in g.get_user().get_repos():
            if repo.name == "bingUpdate":
                temp =  repo.get_stats_contributors()
                while(temp == None):
                    time.sleep(2)
                    temp =  repo.get_stats_contributors()
                serverVersion =temp[0].total
        if(serverVersion != getCurrentVersion()):  
            #os.system('rmdir /S /Q "{}"'.format(directory))
            os.system('cd "{}"'.format(home))
            time.sleep(1)
            os.system('rmdir /S /Q "{}"'.format(home + "\\bingUpdate"))
            time.sleep(1)
            os.system('git clone "{}"'.format("https://github.com/botonett/bingUpdate"))
            time.sleep(5)
            os.system("move " + current_working_dir+"\\bingUpdate " + home)
            updateCurrentVersion(serverVersion)
            time.sleep(1)
            return "Update updater Sucessful"
        else:
            return "No updater update Available"
    except Exception as e:
        print(str(e))
        return "An Error Has Occured While Attempting Update."

def getAccount():
    profile = []
    with open(home+ "\\data\\gitAccount.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
    return profile[0],profile[1]

def getCurrentVersion():
    currentVersion = 0
    with open(home+"\\data\\updaterVersion.dat",'r') as curVer:
        for line in curVer:
            currentVersion = int(line.strip())
        curVer.close()
    return currentVersion

def updateCurrentVersion(version):
    with open(home+"\\data\\updaterVersion.dat",'w') as curVer:
        curVer.write(str(version))
        curVer.close()

if __name__ == "__main__":
    update = primaryUpdate()
    while(True):
        if((update != "Update updater Sucessful") or (update != "No updater update Available") or (update != "An Error Has Occured While Attempting Update.")):
            break
        else:
            time.sleep(1)
    print(update)
    from subprocess import call
    #call(["CScript.exe", "C:\\Users\\bing\\Desktop\\Bing2.0\\script.vbs"])
    os.system(home+"\\bingUpdate\\run2.bat")

