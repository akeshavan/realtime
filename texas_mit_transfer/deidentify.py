from glob import glob
import os
from tempfile import mkdtemp
import dicom

def deidentify(srcdir,subject,session):
    print srcdir
    dcms = glob(os.path.join(srcdir,'*','*','*'))
    tmpdir = mkdtemp()
    outdir = os.path.join(tmpdir,subject,session)
    os.makedirs(outdir)
    for d in dcms:
        dcm = dicom.read_file(d,force=True)
        date, series, instance = dcm.InstanceCreationDate, dcm.SeriesNumber, dcm.InstanceNumber
        outfile = os.path.join(outdir,'%s-%s-%s.dcm'%(date,series,instance))
        cmd = "python parse.py %s %s"%(d,outfile)
        os.system(cmd)
    return tmpdir
