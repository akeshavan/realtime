import traits.api as traits
from traitsui.api import View, Item
from glob import glob
import os

subjects = [os.path.split(i)[1] for i in glob('/home/rt/subjects/*')]

class transfer_app(traits.HasTraits):
    subject_id = traits.Enum(subjects)
    action = traits.Enum("Transfer data to MIT",
                         "Transfer DVD to MIT",
                         "Fetch data from MIT")
    session = traits.Enum(1,2,3,4,5,6)

def check_CD_input(subject):
    print "Checking CD input"
    if not os.path.exists(os.path.join('/media',subject)):
        print ('cant find subject %s'%subject)
        possible_files = glob(os.path.join('/media','*/dicom'))
        if len(possible_files)==1:
            dcmdir = os.path.split(possible_files[0])[0]
            print "using %s"%dcmdir
            return dcmdir
        else:
            raise Exception('no dicoms available')
    else:
        return os.path.join('/media',subject)

def transfer_local_data(subject):
    cmd = 'rsync -r -e \"ssh -i /home/rt/.ssh/rt_texas\" ~/subjects/%s mtbi_texas@ba3:/mindhive/xnat/data/mTBI/texas/'%subject    
    print "transfering data from ~/subjects/%s"%subject
    return cmd

def transfer_DVD_data(subject,session):
    dcmdir = check_CD_input(subject)
    cmd1 = 'mkdir %s'%subject
    cmd2 = 'mkdir session%d'%(session-1)
    cmd3 = 'rsync -r -e \"ssh -i /home/rt/.ssh/rt_texas\" %s mtbi_texas@ba3.mit.edu:/mindhive/xnat/dicom_storage/mTBI/'%(subject)
    cmd4 = 'rsync -r -e \"ssh -i /home/rt/.ssh/rt_texas\" session%d mtbi_texas@ba3.mit.edu:/mindhive/xnat/dicom_storage/mTBI/%s'%(session-1,subject)
    for c in [cmd1,cmd2,cmd3,cmd4]:
        os.system(c)
    cmd = 'rsync -r -e \"ssh -i /home/rt/.ssh/rt_texas\" %s mtbi_texas@ba3.mit.edu:/mindhive/xnat/dicom_storage/mTBI/%s/session%d'%(dcmdir,subject,session-1)
    print "transferring DVD data"
    return cmd

def fetch_MIT_data(subject):
    cmd = 'rsync -r -e \"ssh -i /home/rt/.ssh/rt_texas\" mtbi_texas@ba3:/mindhive/gablab/rtfmri/mTBI/pilots/%s/mask ~/subjects/%s/\n'%(subject,subject)
    cmd += 'rsync -r -e \"ssh -i /home/rt/.ssh/rt_texas\" mtbi_texas@ba3:/mindhive/gablab/rtfmri/mTBI/pilots/%s/xfm ~/subjects/%s/'%(subject,subject)
    print "fetching MIT data"
    return cmd

def do_action(app):
    action = app.action
    subject = app.subject_id
    session = app.session

    if action=="Transfer data to MIT":
        cmd = transfer_local_data(subject)

    elif action=="Transfer DVD to MIT":
        cmd = transfer_DVD_data(subject,session)

    elif action=="Fetch data from MIT":
        cmd = fetch_MIT_data(subject)

    print cmd
    os.system(cmd)

if __name__=="__main__":
    app = transfer_app()
    app.configure_traits()
    do_action(app)
