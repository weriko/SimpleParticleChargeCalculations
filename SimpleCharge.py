import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random as rnd
import time
#TODO: just use numpy?

class Particle:
    def __init__(self,charge, mass, posx,posy,posz, name = None):
        self.posx = posx
        self.posy = posy
        self.posz= posz
        self.charge = charge
        self.force_applied = 0
        self.velocity = 0
        self.mass = mass
        self.acceleration = 0
        self.name = name
    def __str__(self):
        return f"\n\n{------self.name}   x:{self.posx}   y:{self.posy}   z:{self.posz}   velocity:{self.velocity}   acceleration:{self.acceleration}   force:{self.force_applied}"
        
        
class Field: 
    
    def __init__(self, precision = 1):   #Precision reduces movement of all particles, so each frame can calculate everything correctly
        self.particles = []
        self.precision = precision
        self.particle_counter = 0
        self.time = 0
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
                if isinstance(particle , Particle):
                    #Adds particle number if it doesnt have a name
                    if not particle.name:
                        particle.name= self.particle_counter
                    self.particle_counter += 1
                    self.particles.append(particle)
                else:
                    print("Dont add other objects other than particles!")
            except:
                print("something went wrong...maybe you tried adding an object thats not a particle?")
        
        
    def charge(self, q1,q2):
        
        #Simple calculations for x y  and z axis
        
        k = 9*(10**9)
        epsilon = 10**(-70)#To prevent 0 division
        
        distancex= q2.posx-q1.posx
        distancey = q2.posy-q1.posy
        distancez = q2.posz-q1.posz
        distancexyz = (((distancex)**2)+((distancey)**2)+(distancez**2))**(1/2)+epsilon
        
        #print(distancex,distancey,distancez)
        
    
        fx = -(k*(q2.charge*q1.charge)/(distancexyz**2))*((q2.posx-q1.posx)/distancexyz)
    
        fy = -(k*(q2.charge*q1.charge)/(distancexyz**2))*((q2.posy-q1.posy)/distancexyz)
        fz = -(k*(q2.charge*q1.charge)/(distancexyz**2))*((q2.posz-q1.posz)/distancexyz)
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
        
        
    def calculate_force_single(self, main_particle_pos):
        
        #Calculates the force applied for a single particle using superposition principle
        
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
        return [sum(fx),sum(fy),sum(fz)]
    
    def calculate_force_global(self):
        #Now calculates the force applied to all particles in a given moment
        
        particle_data ={}
        
        for i,particle in enumerate(self.particles):
            
            #particle_data[particle.name].append(self.calculate_force_single(i))
            particle.force_applied = self.calculate_force_single(i)
            
    def calculate_acceleration_global(self):
        
        for particle in self.particles:
            particle.acceleration = list(map(lambda x: x/particle.mass, particle.force_applied))
        
    def calculate_velocity_global(self):
        for particle in self.particles:
            particle.velocity = list(map(lambda x: x , particle.acceleration))
            
            
    def update_particle_positions(self):
        self.time +=1
        for particle in self.particles:
            
            particle.posx += particle.velocity[0] *  (1/self.precision)

            particle.posy += particle.velocity[1]  * (1/self.precision)
            particle.posz += particle.velocity[2]  * (1/self.precision)
            
    def simulate(self, frame_amount):#TODO
        frames=[]
        for frame in range(frame_amount):
                field.calculate_force_global()
                field.calculate_acceleration_global()
                field.calculate_velocity_global()
                field.update_particle_positions()
                
            
 
        
        
            
        
            
            



#Some testing    
field = Field(1000)  
d = 10**(-1)#deci
c = 10**(-2)#centi
m = 10**(-3)#milli
u = 10**(-6)#micro
n = 10**(-9)#nano
p = 10**(-12)#pico

nano= n
default_charge = (1.60217662*(10**(-19))) 


#charge, mass, posx,posy,posz, name

q1= Particle(default_charge,1*nano*nano*nano,6,10,6)
q2 = Particle(5*nano,1*nano,2,7,9)
q3= Particle(3*nano,1*nano,4,6,3)
q4 = Particle(5*nano,1*nano,2,10,6)
q5= Particle(3*nano,1*nano,8,3,2)
q6 = Particle(5*nano,1*nano,2,1,7)
q7= Particle(-3*nano,1*nano,3,2,2)
q8 = Particle(-5*nano,1*nano,4,7,9)
q9= Particle(-3*nano,1*nano,5,6,3)
q10 = Particle(-default_charge,  1*nano*nano*nano  , 2,2,2)
q11= Particle(-3*nano,1*nano,7,3,2)
q12 = Particle(5*nano,1*nano,0,1,7)
field.add_particle(q1,q10)

#field.generate_random_particle(charge_scale =nano,pos_scale = 10, ammount=70)
field.show_particles()

#print(field.calculate_force_single(0))
field.calculate_force_global()
field.calculate_acceleration_global()
field.calculate_velocity_global()
field.update_particle_positions()
field.show_particles()

for i in range(100000):
    time.sleep(0.0125)
    field.calculate_force_global()
    field.calculate_acceleration_global()
    field.calculate_velocity_global()
    field.update_particle_positions()
    if i%100==0:
        print(q1)
        print(q10)
        time.sleep(0.5)
    field.show_particles()
 


#print(charge(q1,q2))
    