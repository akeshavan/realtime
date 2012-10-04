import numpy as np
from psychopy import visual
from graph_base import GraphBase, scale
import time

class ThermBase(GraphBase):
    def __init__(self,win,size=[1,1],pos=[0,0],scale=range(-3,4)):
        """
        Inputs
        ------
        win : visual.Window object
        size : size of graph
        pos : position of graph
        """

        self._pos = pos
        self._size = size
        self._win = win
        self.objects = []

        self._draw_axis()
        
        _, ay,by = self._scaleY(scale)
        _, ax,bx = self._scaleX()
        self._draw_axis_labels(scale,by)
        
        self.affine = np.array([[ax,0.,bx],[0.,ay,by+self._pos[1]],[0.,0.,1.]])
        self.T = lambda x,y : tuple(np.dot(self.affine,[x,y,1.])[:2].tolist())
    
    def plotFB(self, fb,fillColor=None,thresh=None):
        if not thresh ==None:
            FB = visual.ShapeStim(self._win,
                                      closeShape=True,
                                      vertices= (self.T(0,thresh),
                                                        self.T(0,fb),
                                                        self.T(1,fb),
                                                        self.T(1,thresh)),
                                                        fillColor = fillColor)
            
        else:
            FB = visual.ShapeStim(self._win,
                                      closeShape=True,
                                      vertices= (self.T(0,0),
                                                        self.T(0,fb),
                                                        self.T(1,fb),
                                                        self.T(1,0)),
                                                        fillColor = fillColor)
                                                        
        self.objects.append(FB)
    
    def plotThr(self,thr):
        TH =  visual.ShapeStim(self._win,
                                      closeShape=False,
                                      vertices= (self.T(0,thr),
                                                        self.T(1,thr)), lineColor='black')
                                      
        self.objects.append(TH)
        
        thTxt = visual.TextStim(self._win,'*',pos=[self._pos[0]+self._size[0]+0.1,self.T(0,thr)[1]])
        self.objects.append(thTxt)
        
    def plot(self,fb,thresh,arrow='up',frame=20,maxframe=20):
        
        frac = float(frame)/float(maxframe)
        color = 'black'
    
        if frac >= 1:
            frac = 1.0
        
            if (fb < thresh and arrow == 'up') or (fb>thresh and arrow=='down'):
                color = 'red'
            
            elif (fb >= thresh and arrow == 'up') or (fb<=thresh and arrow=='down'):
                color = 'green'
        
        self.plotFB((fb-thresh)*frac+thresh,color,thresh)
        self.plotThr(thresh)
    
        
    def _scaleY(self,X):
        y,a,b = scale(X)
        f = lambda pt: pt*a+b+self._pos[1]
        return f, a, b
        
    def _scaleX(self):
        a,b = self._size[0], self._pos[0]
        f = lambda pt: pt*self._size[0]+self._pos[0]
        return f, a, b


def extract(rt,dr,mask='active'):
    trials = np.asarray(rt.trial_type[mask])
    data = np.asarray(rt.data[mask])
    try:
        if (trials==dr).any():
            return data[trials==dr].tolist()
        else:
            print "feedback.py: No matching trials"
            return []
    except:
        print "Exception in feedback.py: No matching trials."
        return []


def get_feedback(rt,dr,window=4):
    fb = np.mean(extract(rt,dr,'active')[-window:])-np.mean(extract(rt,dr,'reference')[-window:])
    return fb
    
def get_target(FB,dr,hist=None):
    trg = FB[dr] 
    if hist:
        trg += hist[dr]
    return np.median(trg[-6:])
    
    
if __name__== "__main__":
    win = visual.Window([800,600])
    
    t = ThermBase(win, [0.25,1],[-0.125,-0.5])
    for i in range(0,21):
        t.plot(0.5,1.0,'up',i,20)
        t.draw()
        win.flip()
