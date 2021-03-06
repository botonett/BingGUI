import os
import sys
import shutil
import fileinput
import time
from shutil import copyfile
import sys
import pip
from random import randint
def update():
    try:
        with open("packages.txt",'r') as curVer:
            for line in curVer:
                pip.main(['install', line.strip()])
            curVer.close()
        return "Done"
    except Exception as E:
        print(str(E))
        return "Failed!"
updatePackage = update()
while(True):
    if((updatePackage == "Done") or (updatePackage == "Failed!")):
        break
    else:
        time.sleep(1)
print(updatePackage)
from unipath import Path
from github import Github
from appJar import gui

current_user = os.getlogin()
current_working_dir, filename = os.path.split(os.path.abspath(__file__))
home = Path(current_working_dir).parent
sys.path.append(home)
os.chdir(current_working_dir)
AccountG = ''
VMG = ''
HostG = ''
ReportG = ''
PCSeachG = ''
MobileSearchG = ''
ShutdownG = ''
updateProgress = 0

def primaryUpdate():
    try:
        global updateProgress
        updateProgress = updateProgress + 10
        account,password = getAccount() 
        #create a Github instance:
        serverVersion = 0
        g = Github(account, password)
        for repo in g.get_user().get_repos():
            if repo.name == "bingUpdate":
                temp =  repo.get_stats_contributors()
                updateProgress = updateProgress + 60
                while(temp == None):
                    time.sleep(2)
                    temp =  repo.get_stats_contributors()
                serverVersion =temp[0].total
        if(serverVersion != getCurrentVersion()):    
            app.thread(updateUpdater)
            app.thread(didyouknow)
        else:
            app.queueFunction(app.setLabel, "title", "No Update Is Available!")
            updateProgress = 100
            return "No updater update Available"
    except Exception as e:
        app.queueFunction(app.setLabel, "title", "Failed to update updater!")
        updateProgress = 100
        return "An Error Has Occured While Attempting Update."
def didyouknow():
    data = []
    with open("didyouknow.txt","r",encoding="utf-8") as dyn:
        for line in dyn:
            data.append(line.strip())
    app.queueFunction(app.setLabel, "title", "Updates Found. Installing Updates in the Background. BingGUI Will Restart Search Process Automatically!")
    time.sleep(6)
    counter = 0
    while(counter <= 20):
        app.queueFunction(app.setLabel, "title", str(data[randint(0, len(data)-1)]))
        time.sleep(6)
    
    
def updateUpdater():
    temp = os.system("update.bat")
    app.stop()

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

def tracker():
    #tracker for log deletion every 30 days
    tracker = 0;
    clear = False
    with open(home+"\\data\\tracker.dat", 'r') as tr:
        for line in tr:
            tracker= int(line.strip())
        tr.close()
    if (tracker == 60):
        with open(home+"\\data\\tracker.dat", 'w') as tr:
            tr.write('0')
            print('Tracker is 60')
            print('Tracker has been reset.')
            clear = True
            tr.close()
    else:
        with open(home+"\\data\\tracker.dat", 'w') as tr:
            tracker = tracker + 1
            tr.write(str(tracker))
            tr.close()
    #clear log  
    if(clear == True):
        with open(home+'\\data\\log.dat','w') as log:
            print('Log is Cleared') 
            log.write('Log Cleared')
            log.write('\n')
        log.close()

def logging(info):
    #time for log
    localtime = time.asctime(time.localtime(time.time()))
    #print time stamp into log
    with open(home+"\\data\\log.dat", "a") as log:
        #log.write('==================================================')
        #log.write('\n')
        log.write(str(localtime)+ ': ' + str(info))
        log.write('\n')
        #log.write('==================================================')
        #log.write('\n')

def updateMeter():
    if(updateProgress < 100):
        app.setMeter("update", updateProgress)

def checkProfileEntry():
    if(app.getEntry("Account") != ''):
        return True
    if(app.getEntry("Host") != ''):
        return True
    if(app.getEntry("VM#") != ''):
        return True
    if(app.getEntry("Report") != ''):
        return True
    if(app.getEntry("PCSeach") != ''):
        return True
    if(app.getEntry("MobileSearch") != ''):
        return True
    
def checkShutdown(Shutdown):
    if(str(app.getCheckBox("Shutdown after complete")) != Shutdown):
        return True

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def updateProfile(profile):
    app.after(0,app.queueFunction,app.setLabel, "title", "Updating user profile!")
    profile = []
    
    with open(home+"\\data\\profile.dat", 'r') as pf:
        for line in pf:
             profile.append(line.strip())
    with open(home+"\\data\\shutdown.dat", 'r') as pf:
        for line in pf:
             profile.append(line.strip())
        
    Account1 = profile[0].split("=")[1].strip()
    VM1 = profile[1].split("=")[1]
    Host1 = profile[2].split("=")[1]
    Report1 = profile[3].split("=")[1].strip()
    PCSeach1 = int(profile[4].split("=")[1])
    MobileSearch1 = int(profile[5].split("=")[1])
    Shutdown1 = profile[6]
    Account = ''
    VM = ''
    Host = ''
    Report = ''
    PCSeach = ''
    MobileSearch = ''
    Shutdown = ''
    Account = app.getEntry("Account")
    VM = app.getEntry("VM#")
    Host = app.getEntry("Host")
    Report =  app.getEntry("Report")
    PCSeach = app.getEntry("PCSeach")
    MobileSearch =  app.getEntry("MobileSearch")
    Shutdown = app.getCheckBox("Shutdown after complete")
    if(Account == '' or Host == '' or Report == '' or PCSeach == '' or MobileSearch == '' or VM == ''):
        app.after(0,app.queueFunction,app.setLabel, "title", "Updating fields with inputs!")
        if(Account == ''):
            Account = Account1
        if(Host == ''):
            Host = Host1
        if(Report == ''):
            Report = Report1
        if(PCSeach == ''):
            PCSeach = PCSeach1
        if(MobileSearch == ''):
            MobileSearch = MobileSearch1
        if(VM == ''):
            VM = VM1
    if(RepresentsInt(PCSeach) == False):
        app.after(0,app.queueFunction,app.setLabel, "title", "PC Search must be an integer ie. 32")
    elif(RepresentsInt(MobileSearch) == False):
        app.after(0,app.queueFunction,app.setLabel, "title", "Mobile Search must be an integer ie. 23")
    elif('@' not in Report or ' ' in Report):
        print(Report)
        app.after(0,app.queueFunction,app.setLabel, "title", "Report destination must be a valid email address.")
    elif('@' not in Account or ' ' in Account):
        print(Account)
        app.after(0,app.queueFunction,app.setLabel, "title", "Bing account must be a valid email address.")
    else:
        app.queueFunction(app.disableButton,"Begin Search")
        AccountG = Account
        VMG = VM
        HostG = Host
        ReportG = Report
        PCSeachG = PCSeach
        MobileSearchG = MobileSearch
        ShutdownG = Shutdown
        with open(home+"\\data\\profile.dat","w") as profile:
            profile.write("Account = " + str(Account))
            profile.write('\n')
            profile.write("VM# = "+str(VM))
            profile.write('\n')
            profile.write("Host = "+str(Host))
            profile.write('\n')
            profile.write("Report = "+str(Report))
            profile.write('\n')
            profile.write("PCSeach = "+str(PCSeach))
            profile.write('\n')
            profile.write("MobileSearch = "+str(MobileSearch))
            profile.write('\n')
            profile.write(str(Shutdown))
            profile.write('\n')
        profile.close()
        app.queueFunction(app.enableButton,"Begin Search")
        app.after(0,app.queueFunction,app.setLabel, "title", "Profile Updated Sucessfully! Click Begin Search to Continue!")
def clear():
    app.queueFunction(app.removeEntry,"Account")
    app.queueFunction(app.removeEntry,"VM#")
    app.queueFunction(app.removeEntry,"Host")
    app.queueFunction(app.removeEntry,"Report")
    app.queueFunction(app.removeEntry,"PCSeach")
    app.queueFunction(app.removeEntry,"MobileSearch")
    app.queueFunction(app.removeButton,"Update Profile")
    app.queueFunction(app.removeButton,"Begin Search")
    app.queueFunction(app.setLabel, "title", "Search Process Is Starting...")
def search():
    app.thread(clear)
    app.thread(search2)
def search2():
    import sys
    sys.path.append(home+"\\bingAuto")
    #from subprocess import call
    #call(["python", "C:\\Users\\bing\\Desktop\\Bing2.0\\script.vbs"])

    shutdown = str(app.getCheckBox("Shutdown after complete"))
    app.queueFunction(app.disableCheckBox,"Shutdown after complete")
    with open(home+"\\data\\shutdown.dat", 'w') as pf:
        pf.write(str(shutdown))
    
    app.queueFunction(app.removeCheckBox,"Shutdown after complete")
    if(shutdown == "True"):
        app.after(12,app.queueFunction,app.setLabel, "title", "Your computer will shutdown automatically!")
    else:
        app.after(12,app.queueFunction,app.setLabel, "title", "Your computer will remain on after search is done!")
    if(True):
        time.sleep(2)
        app.after(10,app.queueFunction,app.setLabel, "title", "Have a good day :) GUI out!")
    
    if(True):
        time.sleep(2)
        app.after(10,app.queueFunction,app.stop)
    from subprocess import call
    #call(["python", "C:\\Users\\bing\\Desktop\\Bing2.0\\bingAuto\\bingAuto.py"])
    os.system(home+"\\bingAuto\\bingAuto.py")

    
def profile():
    global updateProgress
    while(updateProgress != 100):
        time.sleep(1)
    profile = []
    newInfo = False
    try:
        with open(home+"\\data\\profile.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
        with open(home+"\\data\\shutdown.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
        app.queueFunction(app.setLabel, "title", "Getting Current User Profile...")
        app.queueFunction(app.removeMeter,"update")
        
        """
        Account = profile[0].split(' ')[2]
        VM = profile[1].split(' ')[2]
        Host = profile[2].split(' ')[2]
        Report = profile[3].split(' ')[2]
        PCSeach = profile[4].split(' ')[2]
        MobileSearch = profile[5].split(' ')[2]
        Shutdown = profile[6].split(' ')[2]
        """
        Account = profile[0]
        VM = profile[1]
        Host = profile[2]
        Report = profile[3]
        PCSeach = profile[4]
        MobileSearch = profile[5]
        Shutdown = profile[6]
        
    except Exception as e:
        print(e)
        logging(e)
        app.queueFunction(app.setLabel, "title", "No current profile found.")
        Account = 'Enter Bing Account'
        VM = 'Enter Virtual Machine Name'
        Host = 'Enter Host Name'
        Report = 'Enter Report Destination'
        PCSeach = 'Enter PC Search Amount'
        MobileSearch = 'Enter Mobile Search Amount'
        Shutdown = 'True'
        newInfo = True
    """
    app.queueFunction(app.addEntry,"Account",1,0,2)
    app.queueFunction(app.setEntryDefault,"Account",Account)
    app.queueFunction(app.setEntryTooltip,"Account","Current Bing Account")
    app.queueFunction(app.addEntry,"VM#",2,0,2)
    app.queueFunction(app.setEntryDefault,"VM#",VM)
    app.queueFunction(app.setEntryTooltip,"VM#","Virtual Machine Name")
    app.queueFunction(app.addEntry,"Host",3,0,2)
    app.queueFunction(app.setEntryDefault,"Host",Host)
    app.queueFunction(app.setEntryTooltip,"Host","Current host machine")
    app.queueFunction(app.addEntry,"Report",4,0,2)
    app.queueFunction(app.setEntryDefault,"Report",Report)
    app.queueFunction(app.setEntryTooltip,"Report","Current report destination")
    app.queueFunction(app.addEntry,"PCSeach",5,0,2)
    app.queueFunction(app.setEntryDefault,"PCSeach",PCSeach)
    app.queueFunction(app.setEntryTooltip,"PCSeach","Current PC Search per session")
    app.queueFunction(app.addEntry,"MobileSearch",6,0,2)
    app.queueFunction(app.setEntryDefault,"MobileSearch",MobileSearch)
    app.queueFunction(app.setEntryTooltip,"MobileSearch","Current Mobile Search per seassion")
    app.queueFunction(app.addCheckBox,"Shutdown after complete",7,1,1)
    """
    app.addEntry("Account",1,0,2)
    app.setEntryDefault("Account",Account)
    app.setEntryTooltip("Account","Current Bing Account")

    app.addEntry("VM#",2,0,2)
    app.setEntryDefault("VM#",VM)
    app.setEntryTooltip("VM#","Virtual Machine Name")

    app.addEntry("Host",3,0,2)
    app.setEntryDefault("Host",Host)
    app.setEntryTooltip("Host","Current host machine")

    app.addEntry("Report",4,0,2)
    app.setEntryDefault("Report",Report)
    app.setEntryTooltip("Report","Current Report destination")

    app.addEntry("PCSeach",5,0,2)
    app.setEntryDefault("PCSeach",PCSeach)
    app.setEntryTooltip("PCSeach","Current PC Search per session")

    app.addEntry("MobileSearch",6,0,2)
    app.setEntryDefault("MobileSearch",MobileSearch)
    app.setEntryTooltip("MobileSearch","Current Mobile Search per seassion")
    app.addButton("Begin Search", search ,8,1,1)
    app.hideButton("Begin Search")
    app.addButton("Update Profile", updateProfile,8,0,1)
    app.hideButton("Update Profile")
    app.addCheckBox("Shutdown after complete",7,1,1)
    if(Shutdown == "True"):
        app.queueFunction(app.setCheckBox,"Shutdown after complete")
    app.queueFunction(app.setLabel, "title", "Profile collection completed!")
    #time.sleep(2)
    counter = 10
    
    while(counter >= 0):
        time.sleep(1)
        app.setLabel( "title", "Searching will begins in " + str(counter) + " seconds!")
        if(checkProfileEntry() == True or newInfo == True):
            newInfo = True
            break
        #Begin Search Process
        if(counter == 0):
             search()
        counter -= 1
    
    if(newInfo):
        #app.queueFunction(app.setLabel, "title", "Detected new lable!")
        app.showButton("Update Profile")
        app.showButton("Begin Search")
        app.after(0,app.queueFunction,app.setLabel, "title", "Click update profile when complete! Or begin search to keep current profile.")
    
      

#def checkStop():
#    return app.yesNoBox("Confirm Exit", "Are you sure you want to exit the application?")


if __name__ == "__main__":
    
    # create a GUI variable called app
    app = gui("Bing Auto 2.0", "800x400")
    #app.setStopFunction(checkStop)
    app.setSticky("news")
    app.setExpand("both")
    app.addLabel("title", "Checking for update",0,0,2)
    app.addMeter("update",1,0,2)
    app.setMeterFill("update", "light green")
    app.setTransparency(99)
    app.setResizable(canResize=True)
    app.setLocation("CENTER")
    app.createRightClickMenu("rightMenu", showInBar=False)
    app.thread(primaryUpdate)
    app.registerEvent(updateMeter)
    app.thread(profile)
    # start the GUI
    app.go()
    
    
