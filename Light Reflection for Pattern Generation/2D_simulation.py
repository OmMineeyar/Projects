import pygame
import sys
import math
import numpy as np
import math as mh
def reflected(incident_vector,normal):
        
        incident_vector = norm(incident_vector)
        normal=norm(normal)
        reflection_vector = incident_vector - 2 * np.dot(incident_vector, normal) * normal
        return reflection_vector
    
def magnitude(vector):
   return np.sqrt(np.dot(np.array(vector),np.array(vector)))

def norm(vector):
   return np.array(vector)/magnitude(np.array(vector))

class Laser:
    def __init__(self,coordinates,initial_direction):
        self.source=pygame.math.Vector2(coordinates)
        self.direction=pygame.Vector2(initial_direction)#.normalize()
    def draw(self,screen):
        pygame.draw.line(screen,'Blue',self.source,self.source + 100*self.direction)
        
class Mirror:

    def __init__(self,mid_point, normal_vec):
        self.pos = pygame.math.Vector2(mid_point)
        self.normal=pygame.Vector2(normal_vec)
        if normal_vec[1]==0:
            self.mirror_vector= pygame.Vector2(0,1)
        else:
            self.mirror_vector= pygame.Vector2(1/math.sqrt(1**2+((-1*normal_vec[0])/(normal_vec[1]))**2),(-1*normal_vec[0])/(normal_vec[1])/math.sqrt(1**2+((-1*normal_vec[0])/(normal_vec[1]))**2))
        self.endpoints=[self.pos + 10 * self.mirror_vector,self.pos- 10 * self.mirror_vector]
    def draw(self,screen):
        pygame.draw.line(screen,'Red',self.pos,self.pos + 10 * self.mirror_vector)
        pygame.draw.line(screen,'Red',self.pos,self.pos - 10 * self.mirror_vector)
    
pygame.init()

screen = pygame.display.set_mode((1400, 600+100))
pygame.display.set_caption("Mirror and Light Source")

M=[Mirror((0+50,150+50),(1,0)),Mirror((260+50,300+50),(0,-1)),Mirror((520+50,150+50),(-1,0))]
L=Laser((260+50,0+50),(-1.732,1))
print("First set of Mirrors and Laser")
print("Laser")
print((L.source-[50,50])/4,L.direction)
print("Mirrors & Angle")
for i in (0,1,2):
    print((M[i].pos-[50,50])/4,mh.acos(np.dot(M[i].normal,[1,0]))*180/3.141592653589793)

M2=[Mirror((0+50,150*3+50),(1.732/2,-1/2)), Mirror((260+50,150*4+50),(-1/2,-1.732/2))]
L2=Laser((0+50,150+50+1),(0,1))
print("2nd set of Mirrors and Laser")
print("Laser")
print((L2.source-[50,50])/4,L2.direction)
print("Mirrors & Angle")
for i in (0,1):
    print((M2[i].pos-[50,50])/4,mh.acos(np.dot(M2[i].normal,[1,0]))*180/3.141592653589793)

M3=[Mirror((520+50,450+50),(-1.732/2,-1/2))]
L3=Laser((520+50,150+50),(0,1))
print("3rd set of Mirrors and Laser")
print("Laser")
print((L3.source-[50,50])/4,L3.direction)
print("Mirrors & Angle")
print((M3[0].pos-[50,50])/4,mh.acos(np.dot(M3[0].normal,[1,0]))*180/3.141592653589793)

M4=[Mirror((260*3+50,150*2+50),((0,-1))),Mirror((260*4+50,150+50),((-1,0))),Mirror((260*3+50,0+50),((0,1)))]
L4=Laser((260*2+50,150+50),(1.732,1))
print("4th set of Mirrors and Laser")
print("Laser")
print((L.source-[50,50])/4,L4.direction)
print("Mirrors & Angle")
for i in (0,1,2):
    print((M4[i].pos-[50,50])/4,mh.acos(np.dot(M4[i].normal,[1,0]))*180/3.141592653589793)
    
M5=[Mirror((260*3+50,150*4+50),(-1/2,-1.732/2))]
L5=Laser((520+50,450+50),(1.732,1))
print("5th set of Mirrors and Laser")
print("Laser")
print((L5.source-[50,50])/4,L5.direction)
print("Mirrors & Angle")
print((M5[0].pos-[50,50])/4,mh.acos(np.dot(M5[0].normal,[1,0]))*180/3.141592653589793)

M6=[Mirror((260*4+50,150*3+50),(-1.732/2,-1/2))]
L6=Laser((260*4+50,150+50),(0,1))
print("6th set of Mirrors and Laser")
print("Laser")
print((L6.source-[50,50])/4,L6.direction)
print("Mirrors & Angle")
print((M6[0].pos-[50,50])/4,mh.acos(np.dot(M6[0].normal,[1,0]))*180/3.141592653589793)

t2=1
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    M[0].draw(screen)
    M[1].draw(screen)
    M[2].draw(screen)
    for j in range(0,5):
        k=0
        for i in range(0,3):
            g=0
            rayOrigin = np.array(L.source)
            rayDirection = np.array(norm(L.direction))
            point1 = np.array(M[i].endpoints[0])
            point2 = np.array(M[i].endpoints[1])
            v1 = rayOrigin - point1
            v2 = point2 - point1
            if np.dot(rayDirection,M[i].normal)>0:
                continue
            v3 = np.array([-rayDirection[1], rayDirection[0]])
            v2dv3=np.dot(v2, v3)
            if v2dv3==0:
                continue
            t1 = np.cross(v2, v1) / np.dot(v2, v3)
            t2 = np.dot(v1, v3) / np.dot(v2, v3)
            if t1 > 0.0 and t2 >= 0.0 and t2 <= 1.0:
                k=k+1
                g=1
                pygame.draw.line(screen,'Blue',rayOrigin,rayOrigin + t1 * rayDirection)
                L.direction=reflected(rayDirection,M[i].normal)
                L.source=rayOrigin + t1 * rayDirection
                continue
        if k==0:
            pygame.draw.line(screen,'Blue',rayOrigin,rayOrigin + 1000 * rayDirection)
            continue
        
    M2[0].draw(screen)
    M2[1].draw(screen)
    for j in range(0,5):
        k=0
        for i in range(0,2):
            rayOrigin = np.array(L2.source)
            rayDirection = np.array(norm(L2.direction))
            point1 = np.array(M2[i].endpoints[0])
            point2 = np.array(M2[i].endpoints[1])
            v1 = rayOrigin - point1
            v2 = point2 - point1
            if np.dot(rayDirection,M2[i].normal)>0:
                continue
            v3 = np.array([-rayDirection[1], rayDirection[0]])
            v2dv3=np.dot(v2, v3)
            if v2dv3==0:
                
                continue
            t1 = np.cross(v2, v1) / np.dot(v2, v3)
            t2 = np.dot(v1, v3) / np.dot(v2, v3)
            if t1 > 0.0 and t2 >= 0.0 and t2 <= 1.0:
                k=k+1
                pygame.draw.line(screen,'Red',rayOrigin,rayOrigin + t1 * rayDirection)
                L2.direction=reflected(rayDirection,M2[i].normal)
                L2.source=rayOrigin + t1 * rayDirection
                continue
        if k==0:
            pygame.draw.line(screen,'Red',rayOrigin,rayOrigin + 1000 * rayDirection)
            continue
            
    M3[0].draw(screen)
    for j in range(0,5):
        k=0
        for i in range(0,1):
            rayOrigin = np.array(L3.source)
            rayDirection = np.array(norm(L3.direction))
            point1 = np.array(M3[i].endpoints[0])
            point2 = np.array(M3[i].endpoints[1])
            v1 = rayOrigin - point1
            v2 = point2 - point1
            if np.dot(rayDirection,M3[i].normal)>0:
                continue
            v3 = np.array([-rayDirection[1], rayDirection[0]])
            v2dv3=np.dot(v2, v3)
            if v2dv3==0:
                continue
            t1 = np.cross(v2, v1) / np.dot(v2, v3)
            t2 = np.dot(v1, v3) / np.dot(v2, v3)
            if t1 > 0.0 and t2 >= 0.0 and t2 <= 1.0:
                k=k+1
                pygame.draw.line(screen,'Green',rayOrigin,rayOrigin + t1 * rayDirection)
                L3.direction=reflected(rayDirection,M3[i].normal)
                L3.source=rayOrigin + t1 * rayDirection
                continue
        if k==0:
            pygame.draw.line(screen,'Green',rayOrigin,rayOrigin + 1000 * rayDirection)
            continue
        
    M4[0].draw(screen)
    M4[1].draw(screen)
    M4[2].draw(screen)
    for j in range(0,5):
        k=0
        for i in range(0,3):
            rayOrigin = np.array(L4.source)
            rayDirection = np.array(norm(L4.direction))
            point1 = np.array(M4[i].endpoints[0])
            point2 = np.array(M4[i].endpoints[1])
            v1 = rayOrigin - point1
            v2 = point2 - point1
            if np.dot(rayDirection,M4[i].normal)>0:
                continue
            v3 = np.array([-rayDirection[1], rayDirection[0]])
            v2dv3=np.dot(v2, v3)
            if v2dv3==0:
                continue
            t2_prev=t2
            t1 = np.cross(v2, v1) / np.dot(v2, v3)
            t2 = np.dot(v1, v3) / np.dot(v2, v3)
            
            if t1 > 0.0 and t2 >= 0.0 and t2 <= 1.0:
                k=k+1
                pygame.draw.line(screen,'Yellow',rayOrigin,rayOrigin + t1 * rayDirection)
                L4.direction=reflected(rayDirection,M4[i].normal)
                L4.source=rayOrigin + t1 * rayDirection
                continue
        if k==0:
            pygame.draw.line(screen,'Yellow',rayOrigin,rayOrigin + 1000 * rayDirection)
            continue
        
    M5[0].draw(screen)
    for j in range(0,5):
        k=0
        for i in range(0,1):
            rayOrigin = np.array(L5.source)
            rayDirection = np.array(norm(L5.direction))
            point1 = np.array(M5[i].endpoints[0])
            point2 = np.array(M5[i].endpoints[1])
            v1 = rayOrigin - point1
            v2 = point2 - point1
            if np.dot(rayDirection,M5[i].normal)>0:
                continue
            v3 = np.array([-rayDirection[1], rayDirection[0]])
            v2dv3=np.dot(v2, v3)
            if v2dv3==0:
                print("Hi" , i,j)
                continue
            t2_prev=t2
            t1 = np.cross(v2, v1) / np.dot(v2, v3)
            t2 = np.dot(v1, v3) / np.dot(v2, v3)
            
            if t1 > 0.0 and t2 >= 0.0 and t2 <= 1.0:
                k=k+1
                pygame.draw.line(screen,'Blue',rayOrigin,rayOrigin + t1 * rayDirection)
                L5.direction=reflected(rayDirection,M5[i].normal)
                L5.source=rayOrigin + t1 * rayDirection
                continue
        if k==0:
            pygame.draw.line(screen,'Blue',rayOrigin,rayOrigin + 1000 * rayDirection)
            continue
    M6[0].draw(screen)
    for j in range(0,5):
        k=0
        for i in range(0,1):
            rayOrigin = np.array(L6.source)
            rayDirection = np.array(norm(L6.direction))
            point1 = np.array(M6[i].endpoints[0])
            point2 = np.array(M6[i].endpoints[1])
            v1 = rayOrigin - point1
            v2 = point2 - point1
            if np.dot(rayDirection,M6[i].normal)>0:
                continue
            v3 = np.array([-rayDirection[1], rayDirection[0]])
            v2dv3=np.dot(v2, v3)
            if v2dv3==0:
                print("Hi" , i,j)
                continue
            t2_prev=t2
            t1 = np.cross(v2, v1) / np.dot(v2, v3)
            t2 = np.dot(v1, v3) / np.dot(v2, v3)
            
            if t1 > 0.0 and t2 >= 0.0 and t2 <= 1.0:
                k=k+1
                pygame.draw.line(screen,'Red',rayOrigin,rayOrigin + t1 * rayDirection)
                L6.direction=reflected(rayDirection,M6[i].normal)
                L6.source=rayOrigin + t1 * rayDirection
                continue
        if k==0:
            pygame.draw.line(screen,'Red',rayOrigin,rayOrigin + 1000 * rayDirection)
            continue
    pygame.display.update()
    pygame.time.Clock().tick(60)
pygame.quit()
sys.exit()
