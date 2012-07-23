from psychopy import visual
import numpy as np
import time

class GraphBase(object):
    def __init__(self,win,size=[1,1],pos=[0,0]):
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

    def draw(self,flip=False):
        for obj in self.objects:
            obj.draw()
        if flip:
            self._win.flip()

    def _draw_axis(self):
        verts = ((0,0),(0,self._size[1]),
                 (self._size[0],self._size[1]),(self._size[0],0))
        axis = visual.ShapeStim(self._win,
                                pos=self._pos,
                                vertices=verts,
                                name="axis")
        self.objects.append(axis)

    def plot(self,X):
        x = np.linspace(0,self._size[0],float(len(X)))
        y,a,b = scale(X)
        y=y*self._size[1]
        self._draw_axis_labels(X,b)
        for i, p in enumerate(y):
            pt = visual.Circle(self._win,
                               radius=0.01,
                               pos=[x[i]+self._pos[0],
                                    p+self._pos[1]])
            self.objects.append(pt)
            if i:
                ln = visual.ShapeStim(self._win,
                                      closeShape=False,
                                      vertices= ((x[i-1]+self._pos[0],
                                                  y[i-1]+self._pos[1]),
                                                 (x[i]+self._pos[0],
                                                  y[i]+self._pos[1])))
                self.objects.append(ln)

    def _draw_axis_labels(self,X,b):
        if np.min(X)<0 and np.max(X)>0:
            #drawing the line for 0
            y0 = b*self._size[1]

            verts = ((0+self._pos[0],
                         y0+self._pos[1]),
                        (self._size[0]+self._pos[0],
                         y0+self._pos[1]))
            z = visual.ShapeStim(self._win,
                                 closeShape=False,
                                 vertices=verts)
            self.objects.append(z)
            zero = visual.TextStim(self._win,text="0",
                pos = [verts[0][0]-0.1,verts[0][1]])
            self.objects.append(z)
            self.objects.append(zero)
        #minX = visual.TextStim(self._win,text='%1.1f'%np.min(X),
        #                       pos=[self._pos[0]-0.1,self._pos[1]])
        #self.objects.append(minX)
        #maxX = visual.TextStim(self._win,text='%1.1f'%np.max(X),
        #    pos=[self._pos[0]-0.1,self._pos[1]+self._size[1]])
        #self.objects.append(maxX)

def scale(X):
    a = 1./float(np.max(X)-np.min(X))
    b = -np.ones(len(X))*np.min(X)*a
    y= np.asarray(X)*a + b
    return y, a ,b[0]

if __name__== "__main__":
    win = visual.Window([800,600])

    x=np.linspace(0,2*np.pi,100)
    y = np.sin(x)-np.ones(x.shape)*0.5

    for i in range(2,x.shape[0]):
        a = GraphBase(win,pos=[-0.25,-0.5],size=[1,.5])
        a.plot(y[:i].tolist())
        a.draw(True)
        time.sleep(1)

