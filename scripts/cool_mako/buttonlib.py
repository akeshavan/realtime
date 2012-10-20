## buttonlib.py:
## ** helps handle json buttons (see json_template.py and processLib.py) 
## ** designed to work with MakoRoot objects (see mako_cherry.py)

import os
import time
import processLib as lib
import json_template as jlib

def btn_node(bid,j):
    """
    Helper designed for MakoRoot.formHandler().
    Returns a dict of button properties for the desired button.
    In: * bid (str), "x.y.z"
        * j (dict-like), MakoRoot.json
    Out: * node (dict-like), subnode of j, for that button
    """
    [v,s,p] = bid.split('.')
    return lib.get_node(j,['protocol',v,'steps',s,'parts',p])    

def sib_node(bid,j,z):
    """
    Button groups consist of sibling buttons. Get sibling z for the
    button bid.
    Returns a dict of button properties for the desired sibling button.
    In: * bid (str), eg "x.y.z"
        * j (dict-like), MakoRoot.json
        * z (int/str), indicating which sibling to return
    Out: * node (dict-like), subnode of j, for the sibling button
    """
    [v,s,p] = bid.split('.')
    return lib.get_node(j,['protocol',v,'steps',s,'parts',z])    


def timeStamp(node):  ## store time in epoch-secs + string
    tStamp = "%f"%time.time()  ## get time in seconds in the epoch
    timeReadable = time.strftime("%H:%M:%S--%m/%d/%Y",time.localtime(float(tStamp)))
    node['history'].append(tStamp)
    lib.set_here(node,'time',timeReadable)
    return  ### end timeStamp

def clearTimeStamp(node):
    lib.set_here(node,'time',"")
    return

def nameLogfile(node,subject,useInfo=None):
    """
    Out: absolute path where stdout/stderr logfile should go
    """
    # error check: useInfo has 'run','history'; node has 'action', 'id'
    if not useInfo:     ## allow us to (optionally) use a different btn's info
        useInfo=node    ## use this btn's info by default
    run = useInfo['run']
    timeStr = time.strftime("_%b%d_%H%M%S_",time.localtime(float(lib.get_node(useInfo,'history:-1'))))

    action = node['action']
    tab = int(lib.get_node(node,'id')[0])
    filename = str(run) + timeStr + action + '.log'
    return os.path.abspath(os.path.join(lib.SUBJS, subject, "session%d"%tab, filename))
    

def buttonReuse(node,newText):
    ## When a button has been pressed, (say to start something),
    ## rename it to the opposite function (say, to end the thing)
    if node.has_key('text'):
        node['text'] = newText
    else:
        print node
        raise KeyError("Can't reuse this button")
    return

def get_visit(info,j):
    if isinstance(info,str):   ## info is a buttonID, like v.s.p
        visit = int(info[0])
    elif isinstance(info,unicode):  ## also probably a buttonID?
        visit = int(info[0])
    elif isinstance(info,int):  ## info is just a visit number
        visit = info
    else:
        print "info in get_visit:", info
        raise TypeError("get_visit: Didn't expect a %s"%(type(info)))
    return lib.get_node(j, [jlib.FULLSTUDY,visit])

def getProgress(visitNode):
    return lib.get_node(visitNode, jlib.VPROGRESS)

def setProgress(bid,visitNode):
    lib.set_node(visitNode, bid, jlib.VPROGRESS)
    return

def visitBids(tab, j):
    vNode = get_visit(int(tab), j)
    vBids = []
    for s in range(0, len(vNode['steps'])):
        vBids.extend([str(p) for p in lib.get_node(vNode,"steps:%d:parts:*:id"%s)])
    return vBids

def enableOnly(j, tab, only=None):
    """
    only: 'first', None
    """
    vBids = visitBids(tab, j)
    if only == 'first':
        lib.set_here(btn_node(vBids.pop(0),j),'disabled', False)
    [lib.set_here(btn_node(bid,j), 'disabled', True) for bid in vBids]
    return

def enableNext(bid,j):
    [v,s,p] = bid.split(".")
    try:
        nextBtn = btn_node("%s.%s.%d"%(v,s,int(p)+1), j)
    except LookupError:  ## done with this step
        try:
            nextBtn = btn_node("%s.%d.%d"%(v,int(s)+1,0), j)
        except LookupError:  ## done with this visit
            vNode = get_visit(bid,j)
            lib.set_node(vNode,True, jlib.VCOMPLETE)
            return int(v)+1
    lib.set_here(nextBtn,'disabled', False)
    return int(v)