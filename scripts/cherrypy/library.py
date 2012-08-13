import os
import getpass

def doMurfi(subject,visit,run):
    print "starting murfi ......................."
    os.chdir("/home/%s/subjects/%s/session%s"%(getpass.getuser(),subject,visit))
    foo = subprocess.Popen(["murfi","-f","scripts/run%s.xml"%run])
    history = "<ul><li> Started Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return foo, history
    
def endMurfi(proc,subject,visit,run):
    proc.kill()
    history = "<ul><li> Ended Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return history

def doServ(subject,visit,run):
    os.chdir("/home/%s/subjects/%s"%(getpass.getuser(),subject)
    foo = subprocess.Popen(["servenii4d","run%s.nii"%run,"localhost",os.environ["SCANNERPORT"],"2"])    
    self.history = "<ul><li> Served Fake Data for %s, visit %s, run %s</li></ul>"%(subject,visit,run)  
    return foo, history

def endServ(proc,subject,visit,run):
    proc.kill()
    history = "<ul><li> Stopped Fake Data for %s, visit %s, run %s</li></ul>"%(subject,visit,run)
    return history

def doStim(self,run=None):
    os.chdir("/home/%s/realtime"%getpass.getuser())
    foo = subprocess.Popen(["python", "mTBI_rt.py", subject, visit, '00%s'%run, '1'])    
    self.history = "<ul><li> Started Simulus for %s, visit %s, run %s</li></ul>"%(subject,visit,run)
    return foo, history
    


