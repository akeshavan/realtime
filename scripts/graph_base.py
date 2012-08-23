from psychopy import visual
import numpy as np
import time

class GraphBase(object):
    def __init__(self,win,size=[1,1],pos=[0,0],maxrange=None):
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
        self.maxrange = maxrange
        self._draw_axis()
       
    def get_affine(self,scale,drawlabel=True,abs_minmax=None): 
        _, self.ay,self.by = self._scaleY(scale)
        _, self.ax,self.bx = self._scaleX()
        self._draw_axis_labels(scale,self.by,True,abs_minmax=abs_minmax,height=0.05) 
        self.affine = np.array([[self.ax/self._size[0],0.,self.bx],[0.,self.ay*self._size[1],self.by*self._size[1]+self._pos[1]],[0.,0.,1.]])
        self.T = lambda x,y : tuple(np.dot(self.affine,[x,y,1.])[:2].tolist())

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


    def bar(self,X,abs_minmax=None):
        x = np.linspace(0,self._size[0],float(len(X)+1))
        self.get_affine(X,abs_minmax = abs_minmax)
        self._draw_xlabels(X,self.by)
        #y,a,b = scale(X)
        #y=y*self._size[1]
        #self._draw_axis_labels(X,b)
        for i, p in enumerate(X):
            pt = visual.ShapeStim(self._win, closeShape=True,
                               vertices=(self.T(x[i],0),
                                         self.T(x[i],p),
                                         self.T(x[i+1],p),
                                         self.T(x[i+1],0)), 
                               fillColor='white',
                               lineColor='black')
            self.objects.append(pt)
           
    def _scaleY(self,X):
        y,a,b = scale(X,self.maxrange)
        f = lambda pt: pt*a+b+self._pos[1]
        return f, a, b
        
    def _scaleX(self):
        a,b = self._size[0], self._pos[0]
        f = lambda pt: pt*self._size[0]+self._pos[0]
        return f, a, b

    def _draw_axis_labels(self,X,b,draw_minmax=False,abs_minmax=None,height=None):
        if abs_minmax==None:
            print "abs_minmax", abs_minmax
            min_ = np.min(X)
            max_ = np.max(X)
        else:
            min_ = abs_minmax[0]
            max_ = abs_minmax[1]
        print min_, max_
        if min_<=0 and max_>0:
            print "drawing 0"
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
                pos = [verts[0][0]-0.1,verts[0][1]],height=height)
            self.objects.append(z)
            self.objects.append(zero)
        if draw_minmax:
            if not min_ >= 0:
                minX = visual.TextStim(self._win,text='%d'%min_,
                                   pos=[self._pos[0]-0.1,self._pos[1]],height=height)
                self.objects.append(minX)
            maxX = visual.TextStim(self._win,text='%d '%max_+'%',
                pos=[self._pos[0]-0.1,self._pos[1]+self._size[1]],height=height)
            self.objects.append(maxX)
    
    def _draw_xlabels(self,X,b):
        xr = range(1,len(X)+1)
        y0 = b*self._size[1]
        Step = float(self._size[0])/float(len(X))
        for label in xr:
            step = label*Step-0.5*Step
            l = visual.TextStim(self._win,text="%d"%label,
                pos = [self._pos[0]+step,y0+self._pos[1]-0.05],height=0.05)
            self.objects.append(l)

    def add_title(self,title,height=0.1):
        T = visual.TextStim(self._win,text="%s"%title,
                pos = [self._pos[0]+self._size[0]/2,self._size[1]+self._pos[1]+0.05],height=height)
        self.objects.append(T)


def scale(X, maxrange=None):
    if not maxrange:
        a = 1./float(np.max(X)-np.min(X))
        b = -np.ones(len(X))*np.min(X)*a
    else:
        a = 1./float(maxrange[1]-maxrange[0])
        b = -np.ones(len(X))*maxrange[0]*a
    y= np.asarray(X)*a + b
    return y, a ,b[0]

if __name__== "__main__":
    win = visual.Window([800,600])
    downgraph = GraphBase(win,size=[0.75,0.5], pos=[0.2, 0],maxrange=[0,3])
    upgraph = GraphBase(win,size=[0.75,0.5], pos=[-0.8,0],maxrange=[0,3])
    upgraph.bar([1,2,3],abs_minmax=[0,100])
    upgraph.add_title('Successful Ups',0.075)
    upgraph.draw()
    downgraph.bar([2,1,0],abs_minmax=[0,100])
    downgraph.add_title('Successful Downs',0.075)
    downgraph.draw()
    win.flip()
    """
    x=np.linspace(0,2*np.pi,100)
    y = np.sin(x)-np.ones(x.shape)*0.5

    #for i in range(2,x.shape[0]):
    a = GraphBase(win,pos=[-0.75,-0.5],size=[0.5,0.5])
    a.bar(range(-5,5))
    a.draw(True)
    #    time.sleep(1)
    """

