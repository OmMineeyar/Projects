import math as mh
import numpy as nap
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs
from panda3d.core import LVecBase3f
from panda3d.core import NodePath

def distance(point1,point2):
    point1 = nap.array(point1)
    point2 = nap.array(point2)
    temp = point1 - point2
    sum_sq = nap.dot(temp.T, temp)
    return(nap.sqrt(sum_sq))

def angle(vector1,unit_vector):
    k=nap.arccos(nap.dot(vector1,unit_vector)/mh.sqrt(nap.dot(vector1,vector1)))
    k=360*k/(2*3.14)
    return k

def nap_vec(vector):
    vector=nap.array(vector)
    return LVecBase3f(vector[0],vector[1],vector[2])

def magnitude(vector):
   return nap.sqrt(nap.dot(nap.array(vector),nap.array(vector)))

def norm(vector):
   return nap.array(vector)/magnitude(nap.array(vector))

def cross(x1,y1):
    x1=nap.array(x1)
    y1=nap.array(y1)
    k= nap.cross(x1,y1)
    return k

def line_plane_intersection(laser_source, laser_direc,M):
    laser_source=nap.array(laser_source)
    laser_direc=nap.array(laser_direc)
    inval=[1000 ,1000,1000]
    if nap.dot(M.normal, laser_direc)!=0:
        t = nap.dot(M.normal, (M.pos_np - laser_source)) / nap.dot(M.normal, laser_direc)
        
        if t>=0:
            intersection_point = laser_source + t * laser_direc
            k=M.pos_np-intersection_point
        
            inval=nap.array(inval)
            if(abs(nap.dot(k,M.endvectors[0]))<1 and abs(nap.dot(k,M.endvectors[1]))<1):
                return intersection_point
            else:
                return inval
        else:
            return inval
    else:
        return inval

class Mirror:
    def __init__(h,mid_point, angle,X_axis_rotation,screen):
        h.pos_np = nap.array(mid_point)
        #h.pos_np = nap.array(mid_point)
        h.pos=nap_vec(h.pos_np)
        #h.normal=nap.array(normal_vec)
        h.angle=angle
        h.screen=screen
        if X_axis_rotation==0:
            Z=nap.array((0,0,1))
            normal_vec=[mh.sin(2*mh.pi*h.angle/360),-mh.cos(2*mh.pi*h.angle/360),0]
            mirror_plane_Z=cross(Z,normal_vec)
            mirror_plane_Z=norm(mirror_plane_Z)
            h.endvectors=[Z,mirror_plane_Z]
            h.normal=nap.array(normal_vec)
            #print(h.normal)
            h.angles=(h.angle,0,0)
        else:
            X=LVecBase3f(1,0,0)
            normal_vec=[0,mh.sin(2*mh.pi*h.angle/360),-mh.cos(2*mh.pi*h.angle/360)]
            mirror_plane_X=cross(X,normal_vec)
            mirror_plane_X=norm(mirror_plane_X)
            h.endvectors=[X, mirror_plane_X]
            h.normal=nap.array(normal_vec)
            # print(h.normal)
            h.angles=(0,-h.angle,0)
    def draw(h):
        mirror=h.screen.loader.loadModel("models/box")
        v=[0.5*mh.cos(2*mh.pi*h.angle/360),0.5*mh.sin(2*mh.pi*h.angle/360),0.5]
        v=nap.array(v)
        mirror.setPos(nap_vec(h.pos_np-v))
        mirror.setScale(1, 0.06,1)
        mirror.setHpr(h.angles)
        mirror.reparentTo(h.screen.render)
        
def isequal(vector1,vector2):
    if(vector1[0]==vector2[0] and vector1[1]==vector2[1] and vector1[2]==vector2[2]):
        return True
    else:
        return False

class Laser:
    def __init__(self,coordinates,initial_direction):
        self.source=LVecBase3f(coordinates)
        self.direction=LVecBase3f(initial_direction)       
            
def reflect_ray(ray_direction, M):

    ray_direction = norm(ray_direction)
    M.normal = norm(M.normal)
    reflection_direction = ray_direction - 2 * nap.dot(ray_direction, M.normal) * M.normal
    #print(M.normal)
    return reflection_direction

class MyGame(ShowBase):
    def __init__(self):
        #super().__init__()
        self.environ = loader.loadModel("models/panda")
        self.SetupCam()
        self.environ.reparentTo(render)
        self.environ.setScale(0.25,0.25,0.25)
        self.environ.setPos(22,-6,14)
        self.accept('c',self.ShowCamPos)
        self.accept('c-up',self.HideCamPos)
        
        
        
    def SetupCam(self):
        base.camera.setX(22)
        base.camera.setY(-6)
        base.camera.setZ(14)
        
    def ShowCamPos(self):
#        position = environ.getPos()
        x=base.camera.getX()
        y=base.camera.getY()
        z=base.camera.getZ()
        self.title = OnscreenText(text = str(x)+":"+str(y)+":"+str(z),style=1,fg=(1,1,0,1),pos=(0,0), scale = 0.07)
        M=[Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self),Mirror((0,10,0),(0),(0),self)]
        for i in range (0,50):
            if(i<5):
                M[i]=Mirror((0,10*i+10,10*i),(5*i+45),(i%2),self)
            elif(i<10):
                M[i]=Mirror((0,10*(i-5)+10,2),(5*(i-5)+45),(i%2),self) 
            elif(i<15):
                M[i]=Mirror((0,10*(i-10)+10,4),(5*(i-10)+45),(i%2),self)
            elif(i<20):
                M[i]=Mirror((0,10*(i-15)+10,6),(5*(i-15)+45),(i%2),self)
            elif(i<25):
                M[i]=Mirror((0,10*(i-20)+10,8),(5*(i-20)+45),(i%2),self)
            elif(i<30):
                M[i]=Mirror((5,10*(i-25)+10,0),(5*(i-25)+45),(i%2),self)
            elif(i<35):
                M[i]=Mirror((5,10*(i-30)+10,2),(5*(i-30)+45),(i%2),self)
            elif(i<40):
                M[i]=Mirror((5,10*(i-35)+10,4),(5*(i-35)+45),(i%2),self)
            elif(i<45):
                M[i]=Mirror((5,10*(i-40)+10,6),(5*(i-40)+45),(i%2),self)
            elif(i<50):
                M[i]=Mirror((5,10*(i-45)+10,8),(5*(i-45)+45),(i%2),self)   
        
        M[20]=Mirror((0,10,8),(45),(0),self)
        
        M[21]=Mirror((0,20,8),(-45),(1),self)
        M[1]=Mirror((0,20,0),(45),(1),self)
        
        M[26]=Mirror((5,20,0),(45),(1),self)
        for i in range(0,50):
            M[i].draw()
        laser_source=[-2,10,8]
        laser_direction=[1,0,0]
        laser_source=nap.array(laser_source)
        line=LineSegs()
        inval=[1000 ,1000,1000]
        #laser_source=nap.array(laser_source)
        #laser_direction=nap.array(laser_direction)
        d =  [1000] * 50
        for j in range(0,6):
            pos=laser_source
            direction=laser_direction
            for i in range(0,50):
                if(not(isequal(line_plane_intersection(pos,direction,M[i]) ,nap.array(inval)))):
                    d[i]=(distance(laser_source,M[i].pos_np),line_plane_intersection(pos,direction,M[i]),reflect_ray(direction,M[i]))
                    print("PANCHOD",line_plane_intersection(pos,direction,M[i]),i,distance(laser_source,M[i].pos_np))
                else:
                    d[i]=(1000,(1000,1000,1000),(1000,1000,1000))
            d = [(x[0], tuple(item for item in x[1] if not isinstance(item, str)), tuple(item for item in x[2] if not isinstance(item, str)) if len(x) > 2 else x[2]) for x in d]        
            d=sorted(d,key=lambda tup: tup[0])          
            print(d,'\n')
            line.moveTo(nap_vec(pos))
            f=0
            while(f<50):
                if(d[f][0]>1):
                    line.drawTo(nap_vec(d[f][1]))
                    break
                else:
                    f=f+1
            print(f)
            line.setThickness(1)
            node = line.create()
            np = NodePath(node)
            np.reparentTo(render)
            laser_source=nap_vec(d[f][1])
            laser_direction=nap_vec(d[f][2])
            #print(laser_direction)
        #M[0].draw()
game=MyGame()
game.run()
