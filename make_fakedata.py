from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from nibabel import Nifti1Image, Nifti1Header, load
from nipype.algorithms.modelgen import spm_hrf
import pylab

subjDir = '/home/rt/subjects/pilot14/'

 
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

#x,y,z = (64,64,32)
study_ref = subjDir + 'xfm/study_ref.nii'
roi_mask = subjDir + 'mask/roi.nii'
background_mask = subjDir + 'background.nii'

from nipy import load_image
from nipy.core.image.image_spaces import xyz_affine
from nipy.algorithms.registration import resample

def adjust_affine(aff, shape, target_shape):
    b = np.zeros((4, 4))
    b[:, 3] = aff[:, 3]
    for i in range(3):
        c = float(shape[i] - 1) / float(target_shape[i] - 1)
        b[0:3, i] = c * aff[0:3, i]
    return b

def change_vox(t_shape, img):
    t_aff = adjust_affine(xyz_affine(img), img.shape, t_shape)
    img2 = resample(img, reference=(t_shape, t_aff))
    zooms = np.asarray(img.header.get_zooms())*np.asarray(img.shape)/np.asarray(t_shape)
    return img2, t_aff, zooms

t_shape = (64, 64, 32)
img, Aff, zooms  = change_vox(t_shape, load_image(study_ref))
zooms = zooms.tolist() + [2.]
Data = img.get_data()
roi_Data  = change_vox(t_shape, load_image(roi_mask))[0].get_data()
#mean = np.mean(Data)
for i in range(num_runs):
    if FB_runs[i]:
        level = 0.2*i*dr[i] + 0.2*i*(dr[i]-1) + 0.2*(np.cumsum(dr[i])*dr[i] + np.cumsum(1-dr[i])*(dr[i]-1))/6
        tt = trial_timing_noFB
    else:
        tt = trial_timing_FB
        level = (2*dr[i]-1)*0.2*(i+1)
    n_points = (offset + num_trials*np.sum(tt))/TR
    print n_points
    trial = np.zeros(np.sum(tt)/TR)
    trial[range(trial_start_TR,trial_end_TR)] = 1
    run_data = np.dot(trial[:,None], level[:,None].T)
    data = np.concatenate((np.zeros(offset/TR), run_data.T.ravel()))
    ## generate hrf_data, the response signal to trial blocks
    #####   4% signal based on looking at real brain data
    hrf_data = np.convolve(data, spm_hrf(TR))[0:len(data),None]
    plt.plot(hrf_data)
 #   Data[roi_Data==1][:,None].T
    DataT = np.tile(Data[:,:,:,None], len(data))
    noise = .1*np.random.rand(*DataT.shape)*DataT  # 2% noise based on looking at real brain data
#    plt.plot((DataT[roi_Data==1,:]).T)
    DataT[roi_Data==1,:] = DataT[roi_Data==1,:] + (DataT[roi_Data==1,:] * hrf_data.T)
    DataT += noise
#    plt.plot((DataT[roi_Data==1,:]).T)
#    plt.plot(np.mean(DataT[roi_Data==1,:], axis=0))

    myaff = Aff
    myaff[:3,3] = [-4,7,29]

    DataT = DataT/np.max(np.abs(DataT))*8000
    actimg = Nifti1Image(DataT.astype(np.int16), Aff)
    actimg.get_header().set_xyzt_units('mm','sec')
    actimg.get_header().set_zooms(zooms)
    actimg.get_header().set_data_dtype(np.int16)
    actimg.to_filename('run%d.nii'%(i+1))
    plt.show()
