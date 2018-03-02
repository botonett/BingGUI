from github import Github
from appJar import gui
import os
import shutil
import fileinput
import time
from shutil import copyfile


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
            os.system('cd "{}"'.format("C:\\Users\\bing\\Desktop\\Bing2.0"))
            time.sleep(1)
            os.system('rmdir /S /Q "{}"'.format("C:\\Users\\bing\\Desktop\\Bing2.0\\bingUpdate"))
            time.sleep(1)
            os.system('git clone "{}"'.format("https://github.com/botonett/bingUpdate"))
            time.sleep(5)
            os.system("move.bat")
            updateCurrentVersion(serverVersion)
            time.sleep(1)
            app.queueFunction(app.setLabel, "title", "Update updater Sucessful!")
            return "Update updater Sucessful"
        else:
            return "No updater update Available"
    except Exception as e:
        print(str(e))
        return "An Error Has Occured While Attempting Update."

def getAccount():
    profile = []
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\gitAccount.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
    return profile[0],profile[1]

def getCurrentVersion():
    currentVersion = 0
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\updaterVersion.dat",'r') as curVer:
        for line in curVer:
            currentVersion = int(line.strip())
        curVer.close()
    return currentVersion

def updateCurrentVersion(version):
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\updaterVersion.dat",'w') as curVer:
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
    os.system("C:\\Users\\bing\\Desktop\\Bing2.0\\bingUpdate\\run2.bat")

