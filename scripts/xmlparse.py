import xml.parsers.expat
from infoclientLib import InfoClient
import numpy as np

class MyXML:
        Parser = ""

        # prepare for parsing

        def __init__(self, xml_string):
                assert(xml_string != "")
                self.Parser = xml.parsers.expat.ParserCreate()
                self.xml_string = xml_string
                self.Parser.CharacterDataHandler = self.handleCharData
                self.Parser.StartElementHandler = self.handleStartElement
                self.Parser.EndElementHandler = self.handleEndElement

        # parse the XML file
  
        def parse(self):
                try:
                        self.Parser.Parse(self.xml_string)
                except:
                        print "ERROR: Can't open XML file!"
                        sys.exit(0)

         # will be overwritten w/ implementation specific methods

        def handleCharData(self, data): pass
        def handleStartElement(self, name, attrs): pass
        def handleEndElement(self, name): pass

class foo(MyXML):
    name = None
    roi = None
    tr = None
    data = None
    def handleStartElement(self,name,attrs):
        if name=='data':
            self.roi = attrs["roi"]
            self.tr = float(attrs["tr"])
            self.name = attrs["name"]
        
    def handleCharData(self, data): 
        #if self.so:
        #    self.sliceorder=data
        #    self.so = False
        self.data=float(data)
    def get(self):
        #self.SliceOrder = []
        #order = self.sliceorder.split(',')
        #for o in order:
        #    self.SliceOrder.append(int(o)-1)
        pass

class RT():
    ic = None
    data = {'active':[],'reference':[]}
    tr = {'active':[],'reference':[]}
    xml = []
    trial_type = {'active':[],'reference':[]}

    def __init__(self):
        self.ic = InfoClient('localhost', 15002, 'localhost', 15003)
        self.ic.add('roi-weightedave', 'active')
        self.ic.add('roi-weightedave','reference')
        self.ic.start()
        print "initialized new RT"

    def check(self,trial=None):
        self.xml = self.ic.check()
        data = {'active':[],'reference':[]}
        tr = {'active':[],'reference':[]}

        for s in self.xml:
            a = foo(s)
            a.parse()
            data[a.roi].append(a.data)
            tr[a.roi].append(a.tr)
            
        if trial:
            for key in data.keys():
                for i in range(0,len(data[key])-len(self.trial_type[key])):
                    self.trial_type[key].append(trial)
            #trials.append((trial,tr[-1]))
                
        self.data = data
        self.tr = tr
        return self.data, self.tr
    
    def save(self,filename='rt_data.npz'):
        np.savez(filename,data=self.data, xml = self.xml, tr = self.tr, trials = self.trial_type)
        return filename
        
    def close(self):
        self.ic.stop()
        #self.ic.remove(('roi-weightedave', 'active'))
        self.trial_type = []
        self.data = []
        self.name = []
        self.roi = []
        self.xml = []
        
if __name__=="__main__":
    
    import numpy as np
    S = np.load("parseme.npy")
    
    data = []
    for s in S:
        a = foo(s)
        a.parse()
        data.append(a.data)
    print data
    
    
