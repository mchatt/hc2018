import sys
import argparse
import time

class Car:
  def __init__(self):
    self.free = True
    self.position = [0,0]
    self.currentRide = None
    self.list_rides = []
    self.n = 0

  def __repr__(self):
    return str(len(self.list_rides))+' '+' '.join(str(self.list_rides))

  def one_step(self):
    if self.free or self.currentRide == None or self.n < self.currentRide.t1:
      return self

    else:
      self.n = self.n+1
      if self.position[0] != self.currentRide.x:
        if self.position[0] < self.currentRide.x:
          self.position = [self.position[0]+1, self.position[1]]
        else:
          self.position = [self.position[0]-1, self.position[1]]
      else:
        if self.position[1] < self.currentRide.y:
          self.position = [self.position[0], self.position[1]+1]
        else:
          self.position = [self.position[0], self.position[1]-1]
    return self

  def arrived(self):
    if not self.free and self.position == [self.currentRide.x, self.currentRide.y]:
      self.list_rides.append(self.currentRide.n)
      self.currentRide = None
      self.free = True

class Ride:
  def __init__(self, n, a, b, x, y, t1, t2):
    self.n = int(n)
    self.a = int(a)
    self.b = int(b)
    self.x = int(x)
    self.y = int(y)
    self.t1 = int(t1)
    self.t2 = int(t2)

  def __repr__(self):
    return "%d %d %d %d %d %d" % (self.a, self.b, self.x, self.y, self.t1, self.t2)

class State:
  '''
  Class representing the input data
  '''
  def __init__(self):
    self.R = 0
    self.C = 0
    self.nb_car = 0
    self.nb_rides = 0
    self.bonus = 0
    self.step = 0
    self.rides = []
    self.cars = None

  def parse(self, inputFile):
    with open(inputFile) as f:
      content = f.readlines()
      self.R, self.C, self.nb_car, self.nb_rides, self.bonus, self.step = [int(x) for x in content[0].split('\n')[0].split()]
      for i in range(self.nb_rides):
        tmp = content[i].split('\n')[0]
        self.rides.append(Ride(i, tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5]))
      self.cars = [Car() for i in range(self.nb_car)]
    return self
        
  def writefile(self, outfile):
    f = open(outfile, 'w')

    for s in self.cars:
      f.write(str(s)+"\n")
    f.close()


###################################################################################################


def compute(state):
  '''
  Implementation of the computing logic
  '''
  for i in range(state.step):
    # move the car in the map
    # if the car arrived to it destination, turn the free flag to True
    for c in state.cars:
      c.one_step()
      c.arrived()
    # assign a ride to a vehicle
    for c in state.cars:
      if c.free:
        c.currentRide = state.rides.pop(0)
        c.free = False
        # my_rides = sorted(state.rides, key=lambda x: 1, reverse=True)
        # best_ride = my_rides[0]
        # state.rides.remove(best_ride)
        # c.free = False
        # c.currentRide = best_ride

####################################################################################################


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', dest='inputfile', required=True, help='Path to input file')
  parser.add_argument('-o', '--outputfile', dest='outputfile', required=True, help='Path to output file')
  args = parser.parse_args()
  inputfile = args.inputfile
  outputfile = args.outputfile

  state = State().parse(inputfile)
  compute(state)
  state.writefile(outputfile)
