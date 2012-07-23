from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from nibabel import Nifti1Image, Nifti1Header, load
from nipype.algorithms.modelgen import spm_hrf
import pylab

 
def montage(X, colormap=pylab.cm.gist_gray):    
    from numpy import array,flipud,shape,zeros,rot90,ceil,floor,sqrt
    from scipy import io,reshape,size
    m, n, count = shape(X)    
    mm = int(ceil(sqrt(count)))
    nn = mm
    M = zeros((mm * m, nn * n))
    image_id = 0
    for j in range(mm):
        for k in range(nn):
            if image_id >= count: 
                break
            sliceM, sliceN = j * m, k * n
            M[sliceN:sliceN + n, sliceM:sliceM + m] = X[:, :, image_id]
            image_id += 1
    pylab.imshow(flipud(rot90(M)), cmap=colormap)
    pylab.axis('off')             
    return M

TR = 2.
offset = 30  # 30s baseline of rest
# define trial timing: arrows=30s, question=4s, smileyFB=2s, intertrial rest=12s
trial_timing_FB   = np.array([30,4,2,12])
trial_timing_noFB = np.array([30,4,0,14])
trial_start_TR    = 0
trial_end_TR      = (trial_timing_noFB[0]/TR).astype(int)

# define which runs have feedback
FB_runs = np.array([0,1,1,1,1,0])

dr = np.array([[1, 1, 0, 1, 0, 0],
      [0, 1, 1, 0, 0, 1],
      [0, 0, 1, 0, 1, 1],
      [1, 0, 0, 1, 1, 0],
      [1, 1, 0, 1, 0, 0],
      [0, 1, 1, 0, 0, 1]])

num_runs, num_trials = dr.shape

x,y,z = (64,64,32)
study_ref = '/home/rt/software/realtime/murfi/fakedata/xfm/study_ref.nii'
roi_mask = '/home/rt/software/realtime/murfi/fakedata/mask/roi.nii'
background_mask = '/home/rt/software/realtime/murfi/fakedata/mask/background.nii'

img = load(study_ref)
Data,Aff,Hdr = img.get_data(), img.get_affine(), img.get_header()
Hdr.set_data_dtype(np.int16)
roi_img = load(roi_mask)
roi_Data = roi_img.get_data()
mean = np.mean(Data)
for i in range(num_runs):
    if FB_runs[i]:
        tt = trial_timing_FB
        level = (2*dr[i]-1)*0.2*(i+1)
    else:
        level = 0.2*i*dr[i] + 0.2*i*(dr[i]-1) + 0.2*(np.cumsum(dr[i])*dr[i] + np.cumsum(1-dr[i])*(dr[i]-1))/6
        tt = trial_timing_noFB
    n_points = (offset + num_trials*np.sum(tt))/TR
    print n_points
    trial = np.zeros(np.sum(tt)/TR)
    trial[range(trial_start_TR,trial_end_TR)] = 1
    run_data = np.dot(trial[:,None], level[:,None].T)
    data = np.concatenate((np.zeros(offset/TR), run_data.T.ravel()))
    ## generate hrf_data, the response signal to trial blocks
    #####   4% signal based on looking at real brain data
    hrf_data = np.convolve(data, spm_hrf(TR))[0:len(data)]*0.04*mean  
    DataT = np.tile(Data[:,:,:,None],len(data))
    
    DataT[roi_Data==1,:] += np.tile(hrf_data[:,None],(DataT[roi_Data==1]).shape[0]).T

    noise = np.random.rand(DataT.shape[0],DataT.shape[1],DataT.shape[2],DataT.shape[3])*mean*.02  # 2% noise based on looking at real brain data
    DataT += noise

    myaff = Aff
    myaff[:3,3] = [-4,7,29]

    actimg = Nifti1Image(DataT.astype(np.int16), None, header=Hdr)
    actimg.get_header().set_xyzt_units('mm','sec')
    actimg.to_filename('run%d.nii'%(i+1))
