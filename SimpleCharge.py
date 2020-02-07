import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random as rnd

class Particle:
    def __init__(self,charge,posx,posy,posz):
        self.posx = posx
        self.posy = posy
        self.posz= posz
        self.charge = charge
        
        
class Field: 
    
    def __init__(self):
        self.particles = []
    def generate_random_particle(self, charge_scale =1,pos_scale = 1, ammount=1):
        for i in range(ammount):
            charge = rnd.random() * charge_scale
            posx = rnd.random() * pos_scale
            posy = rnd.random()* pos_scale
            posz = rnd.random() * pos_scale
            particle = Particle(charge,posx,posy,posz)
            self.add_particle(particle)
        
        
    def add_particle(self,*args):
        for particle in args:
            try:
                if isinstance(particle,Particle):
                    self.particles.append(particle)
                else:
                    print("Dont add other objects other than particles!")
            except:
                print("something went wrong...maybe you tried adding an object thats not a particle?")
        
        
    def charge(self, q1,q2):
        
        #Simple calculations for x y  and z axis
        
        k = 9*(10**9)
        
        distancex= q2.posx-q1.posx
        distancey = q2.posy-q1.posy
        distancez = q2.posz-q1.posz
        distancexyz = (((distancex)**2)+((distancey)**2)+(distancez**2))**(1/2)
        
        #print(distancex,distancey,distancez)
    
        fx = (k*(q2.charge*q1.charge)/(distancexyz**2))*((q2.posx-q1.posx)/distancexyz)
    
        fy = (k*(q2.charge*q1.charge)/(distancexyz**2))*((q2.posy-q1.posy)/distancexyz)
        fz = (k*(q2.charge*q1.charge)/(distancexyz**2))*((q2.posz-q1.posz)/distancexyz)
        return fx,fy, fz
    def show_particles(self):
        fig = plt.figure()
        ax = Axes3D(fig)
        x=[]
        y=[]
        z=[]
        for particle in self.particles:
            x.append(particle.posx)
            y.append(particle.posy)
            z.append(particle.posz)
        
        ax.scatter(x, y, z)
        plt.show()
        
        
    def calculate_force(self, main_particle_pos):
        
        #Calculates the force applied for a particle using superposition principle
        
        main_particle = self.particles[main_particle_pos]

        fx=[]
        fy=[]
        fz=[]
        
        for particle in self.particles:
            if particle != main_particle:
                try:
                    x,y,z = self.charge(main_particle , particle)
                    fx.append(x)
                    fy.append(y)
                    fz.append(z)
                except:
                    print("Something wrong happened!, maybe main particle is overlapped with another one?")
            else:
                pass
        return sum(fx),sum(fy),sum(fz)
            
            



    
field = Field()  
micro = 10**(-6)
nano = 10**(-9)
cargelectron = (1.60217662*(10**(-19)))
"""
q1 = Particle(cargelectron,0,0,0)
q2=Particle(cargelectron, 5*10**(-19),4*10**(-19),5*10**(-19))
q3=Particle(cargelectron, 0,4*10**(-19),0)
field.add_particle(q1)
field.add_particle(q2)
field.add_particle(q3)
"""
"""
q1 = Particle(2*micro,0,0,0)
q2 = Particle(-4*micro,5*nano,0,0)
q3 = Particle(10*micro,5*nano,4*nano,0)
"""
q1= Particle(3*nano,2,2,2)
q2 = Particle(5*nano,2,7,9)
q3= Particle(3*nano,4,6,3)
q4 = Particle(5*nano,2,10,6)
q5= Particle(3*nano,8,3,2)
q6 = Particle(5*nano,2,1,7)
field.add_particle(q1,q2,q3,q4,q5,q6)
field.generate_random_particle(charge_scale =nano,pos_scale = 10, ammount=7)
field.show_particles()

print(field.calculate_force(0))
#print(charge(q1,q2))
    