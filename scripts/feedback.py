import numpy as np
from psychopy import visual
from graph_base import GraphBase, scale

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
    
    def plotFB(self, fb,fillColor=None):
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
        if frac < 1:
            color = 'black'
        elif (fb < thresh and arrow == 'up') or (fb>thresh and arrow=='down'):
            color = 'red'
        elif (fb >= thresh and arrow == 'up') or (fb<=thresh and arrow=='down'):
            color = 'green'
        if frac >= 1:
            frac = 1
        self.plotFB(fb*frac,color)
        self.plotThr(thresh)
    
        
    def _scaleY(self,X):
        y,a,b = scale(X)
        f = lambda pt: pt*a+b+self._pos[1]
        return f, a, b
        
    def _scaleX(self):
        a,b = self._size[0], self._pos[0]
        f = lambda pt: pt*self._size[0]+self._pos[0]
        return f, a, b

        
        
def get_feedback(fb,win,thresh=[0.0]):
    fb.append(fb[-1]+(-1 + np.random.rand(1)[0]*2)/50)
    pos = [-0.5,0]
    if fb[-1] < thresh[-1]:
        fixation=visual.ShapeStim(win,
                 vertices = ((0,0),(0,fb[-1]),(.1,fb[-1]),(.1,0)),
                 pos = pos,
                 fillColor="red")
    else:
        fixation=visual.ShapeStim(win,
                 vertices = ((0,0),(0,fb[-1]),(.1,fb[-1]),(.1,0)),
                 pos = pos,
                 fillColor="green")
    th = visual.ShapeStim(win,
                          vertices=((0,0),(0,thresh[-1]),
                                    (.1,thresh[-1]),(0.1,0)),
                          pos=pos,
                          lineColor="black")
    therm = visual.ShapeStim(win,
                             vertices=((0,-0.9),(0,.9),
                                       (0.1,.9),(0.1,-.9)),
                             pos=pos,
                             lineColor="white")
    zero = visual.TextStim(win,text="0.0",pos=[-0.6,0])
    zero.draw()
    if thresh[-1]:
        th_txt = visual.TextStim(win,'*',pos=[-0.6,thresh[-1]])
        th_txt.draw()
    fixation.draw()
    th.draw()
    therm.draw()
    return fb
    
    
if __name__== "__main__":
    win = visual.Window([800,600])
    
    t = ThermBase(win, [0.25,1],[-0.125,-0.5])
    t.plotFB(1.5,"green")
    t.plotThr(1.0)

    t.draw()
    win.flip()
