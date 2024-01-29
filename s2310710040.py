"""Program to simulate and plot velocity and distance when braking

      Returns:
          PDF: PDF-File with the visualization
"""
import argparse
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import g

#setting up the parameters from powerpoint slides
DRY_CONCRETE = 0.5
WET_CONCRETE = 0.35
DRY_ICE = 0.15
WET_ICE = 0.08
AQUAPLANING = 0.05
DRY_GRAVEL = 0.35
DRY_SAND = 0.3

#preventing uncertain values (like string as input, but value must be float)
def check_float(value, default):
  """Check user-input to be a float; if not, sets a default float-value
  Args:
    value (input of concole): user-input to the system via the console
    default (float): default-value float for the calculations
  Returns:
    float: gives back the input if float, or default-value
  """
  try:
    valueasfloat = float(value)
    return valueasfloat
  except ValueError:
    print(f'Unvalid input {value},input must be float,default-value is set')
  return default

def check_road(value, default):
  """Check's if the user input is a valid Road-Type
    Args:
    value (input of console): user-input to the system via the console
    default (string): default-value string for the calculations
    Returns:
        string: gives back the input if valid string, or default-value
    """
  road_types = ['concrete', 'ice', 'water', 'gravel', 'sand']
  if value in road_types:
    return value
  else:
    print(f' Invalid Road_Type {value}, default-value is set to Concrete')
    return default

def check_condition(value, default):
  """Check's if the user input is a valid Road-Condition
    Args:
        value (input of console): user-input to the system via the console
        default (string): default-value string for the calculations
    Returns:
        string: gives back the input if valid string, or default-value
    """
  conditions = ['dry', 'wet', 'aquaplaning']
  if value in conditions:
    return value
  else:
    print(f' Invalid Condition {value}, default-value is set to dry')
    return default

#parse parameters as typed in from the user
parser = argparse.ArgumentParser(description = 'Setting the parameters')
parser.add_argument('Mass',
                    type = lambda x: check_float(x, 2000),
                    nargs = '?',
                    default = 2000,
                    help = 'Vehicle-Mass')
parser.add_argument('Road_Type', type = lambda x: check_road(x, 'concrete'),
                    nargs = '?',
                    default = 'concrete',
                    help = 'Road-Type, concrete, ice, water, gravel, sand!)')
parser.add_argument('Condition', type = lambda x: check_condition(x, 'dry'),
                    nargs = '?',
                    default = 'dry',
                    help = 'Condition, dry, wet, aquaplaning!')
parser.add_argument('velocity', type = lambda x: check_float(x, 27.5),
                    nargs = '?',
                    default = 27.5,
                    help = 'Velocity')
parser.add_argument('Steepness', type = lambda x: check_float(x, 0),
                    nargs = '?',
                    default = 0,
                    help = 'Steepness')
args = parser.parse_args()

angle_rad = math.radians(args.Steepness)

#defining the friction coefficient based on inputs
def friction_calculation():
  """Check's what friction-coefficient is the right one for calculating

  Returns:
    float: friction-coefficient for the chosen conditions
  """
  if args.Road_Type == 'concrete' and args.Condition == 'dry':
    friction_value = DRY_CONCRETE
  elif args.Road_Type == 'concrete' and args.Condition == 'wet':
    friction_value = WET_CONCRETE
  elif args.Road_Type == 'ice' and args.Condition == 'dry':
    friction_value = DRY_ICE
  elif args.Road_Type == 'ice' and args.Condition == 'wet':
    friction_value = WET_ICE
  elif args.Road_Type == 'water' and args.Condition == 'aquaplaning':
    friction_value = AQUAPLANING
  elif args.Road_Type == 'gravel' and args.Condition == 'dry':
    friction_value = DRY_GRAVEL
  elif args.Road_Type == 'sand' and args.Condition == 'dry':
    friction_value = DRY_SAND
  else:
    friction_value = DRY_CONCRETE
    print('Combination of Road-Type and Condition is not existing '
              'Road-Type is set to default value CONCRETE '
              'Condition is set to default value DRY')
    args.Road_Type = 'concrete'

  return friction_value

FRICTION = friction_calculation()

#setting up the forces
Fnorm = args.Mass * g * math.cos(angle_rad)    #Normal-Force with steepness
Ffriction = FRICTION * Fnorm              #Friction-Force

#implementing function
acceleration = Ffriction / args.Mass
time = np.linspace(0, (args.velocity / acceleration))
brakingvelocity = args.velocity - (acceleration * time)
brakingdistance = (1/2) * time * (2 * args.velocity - acceleration * time)

#calculating the exakt brakingdistance as last value from the list
brakdist = round(brakingdistance[-1], 2)

#calculating the acceleration
acc = round(acceleration, 2)

#calculating the exakt stopping time
stoptime = round(time[-1], 2)

#programming rule of thumb
thumbvelo = args.velocity * 3.6
snormal = (thumbvelo/10) * (thumbvelo/10)
sdanger = snormal * 1/2
sreaction = (thumbvelo/10) * 3

sstop = snormal + sreaction
sstop_danger = sdanger + sreaction

sstop_list = np.linspace(0, sstop)
sstop_danger_list = np.linspace(0, sstop_danger)

stoppingtime_normal = sstop / (thumbvelo / 3.6)
stoppingtime_danger = sstop_danger / (thumbvelo / 3.6)

timeintsstop = np.linspace(0, stoppingtime_normal, len(sstop_list))
timeintsstopdanger = np.linspace(0, stoppingtime_danger, len(sstop_danger_list))

#setting up the plots
fig, axs = plt.subplots(2, 3, figsize = (15, 8))
axs[0, 0].plot(time, brakingvelocity, color = 'orange')
axs[0, 0].set_title('\n\nVelocity')
axs[0, 0].set_xlabel('Time in s')
axs[0, 0].set_ylabel('Velocity in m/s')
axs[0, 0].grid(True, which = 'major')
axs[0, 0].text(0.5, 0.5,
    f' Initial-Velocity: {round(args.velocity, 2)}m/s \n\
    Braking-Time: {stoptime} s',
    fontsize = 12,
    color = 'white',
    bbox = {'facecolor': 'darkgreen', 'alpha': 0.7},
    ha = 'center',
    va = 'center',
    transform = axs[0, 0].transAxes)

axs[0, 1].plot(time, brakingdistance, color = 'red')
axs[0, 1].set_title('\n\nDistance')
axs[0, 1].set_xlabel('Time in s')
axs[0, 1].set_ylabel('Distance in m')
axs[0, 1].grid(True, which = 'major')
axs[0, 1].text(0.5, 0.5,
    f' Braking-Distance: {brakdist} m \n Braking-Time: {round(time[-1], 2)} s',
    fontsize = 12,
    color = 'white',
    bbox = {'facecolor': 'darkgreen', 'alpha': 0.7},
    ha = 'center', va = 'center',
    transform = axs[0, 1].transAxes)

axs[0, 2].text(0.5, 0.5,
    f' Your parameters for the plots: \n\n\
    Velocity: {args.velocity} m/s \n\n\
    Mass: {args.Mass} kg \n\n\
    Type of road: {args.Road_Type} \n\n\
    Condition: {args.Condition} \n\n\
    Friction-Coefficient: {FRICTION} \n\n\
    Angle of surface: {args.Steepness} degrees \n\n\
    Acceleration: -{acc} m/s^2',
    fontsize = 12,
    color = 'white',
    bbox = {'facecolor': 'darkgreen', 'alpha': 0.7},
    ha = 'center', va = 'center')
axs[0, 2].axis('off')

axs[1, 0].plot(timeintsstop, sstop_list, color = 'red')
axs[1, 0].grid(True, which = 'major')
axs[1, 0].set_title('\n\nDistance Rule of Thumb normal')
axs[1, 0].set_xlabel('Time in s')
axs[1, 0].set_ylabel('Distance in m')
axs[1, 0].text(0.5, 0.5,
    f' Braking-Distance: {round(sstop, 2)} m \n\
        Braking-Time: {round(timeintsstop[-1], 2)} s',
    fontsize = 12,
    color = 'white',
    bbox = {'facecolor': 'darkgreen', 'alpha': 0.7},
    ha = 'center',
    va = 'center',
    transform = axs[1, 0].transAxes)

axs[1, 1].plot(timeintsstopdanger, sstop_danger_list, color = 'red')
axs[1, 1].grid(True, which = 'major')
axs[1, 1].set_title('\n\nDistance Rule of Thumb danger')
axs[1, 1].set_xlabel('Time in s')
axs[1, 1].set_ylabel('Distance in m')
axs[1, 1].text(0.5, 0.5, f' Braking-Distance: {round(sstop_danger, 2)} m \n\
    Braking-Time: {round(timeintsstopdanger[-1], 2)} s',
    fontsize = 12,
    color = 'white',
    bbox = {'facecolor': 'darkgreen', 'alpha': 0.7},
    ha = 'center',
    va = 'center',
    transform = axs[1, 1].transAxes)

axs[1, 2].axis('off')
axs[1, 2].text(0.5, 0.5,
    ' Hint: The Rule of thumb does not consider \n\n\
    the mass of the vehicle,\n\n\
    the road-condition, \n\n\
    the type of the road,\n\n\
    the steepness of the road!',
    fontsize = 12,
    color = 'white',
    bbox = {'facecolor': 'darkgreen', 'alpha': 0.7},
    ha = 'center',
    va = 'center')

#saving the plots
plt.tight_layout()
plt.suptitle('Visualizing of the braking velocity and\
    braking distance of a vehicle',
    fontsize = 16,
    color = 'blue')
plt.savefig(
    f'Mass_{args.Mass}_Road_{args.Road_Type}_Condition_{args.Condition}'
    f'_V0_{args.velocity}_Angle{args.Steepness}.pdf'
)
print('Plots have been saved!')

#visualising the plots
plt.show()
