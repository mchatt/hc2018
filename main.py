import sys
import argparse
import time
import logging

def move_by_one(A, B):
  if A[0] != B[0]:
    if A[0] < B[0]:
      return [A[0]+1, A[1]]
    else:
      return [A[0]-1, A[1]]
  else:
    if A[1] < B[1]:
      return [A[0], A[1]+1]
    else:
      return [A[0], A[1]-1]

class Car:
  def __init__(self, i):
    self.i = int(i)
    self.free = True
    self.position = [0,0]
    self.currentRide = None
    self.toDest = False
    self.list_rides = []
    self.n = 0

  def __repr__(self):
    return str(len(self.list_rides))+' '+' '.join(map(str, self.list_rides))

  def one_step(self):
    logging.debug("%d, %s {{%s}}" % (self.i, self.position, self.currentRide))
    
    if self.free or self.currentRide == None:
      logging.debug("%d, I am free, loosing one step !!" % self.i)
      self.n = self.n+1
      return self
      
    if self.position == self.currentRide.origin and self.n < self.currentRide.t1:
      logging.debug("Arrived to origin but waiting for my ride")
      self.n = self.n+1
      return self

    if self.toDest:
      logging.debug("Driving to destination")
      self.position = move_by_one(self.position, self.currentRide.dest)
    else:
      logging.debug("Driving to origin of my ride")
      self.position = move_by_one(self.position, self.currentRide.origin)
      if self.position == self.currentRide.origin:
        self.toDest = True

    self.n = self.n+1
    return self

  def arrived(self):
    if not self.free and self.position == self.currentRide.dest:
      self.list_rides.append(self.currentRide.n)
      self.currentRide = None
      self.free = True

class Ride:
  def __init__(self, n, a, b, x, y, t1, t2):
    self.n = int(n)
    self.origin = [int(a), int(b)]
    self.dest = [int(x), int(y)]
    self.t1 = int(t1)
    self.t2 = int(t2)

  def __repr__(self):
    return "%s %s %d %d" % (self.origin, self.dest, self.t1, self.t2)

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
        tmp = content[i+1].split('\n')[0].split()
        self.rides.append(Ride(i, tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5]))
      self.cars = [Car(i) for i in range(self.nb_car)]
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
      # assign a ride to a vehicle
      if c.free and state.rides:
        c.currentRide = state.rides.pop(0)
        c.free = False
    # my_rides = sorted(state.rides, key=lambda x: 1, reverse=True)
    # best_ride = my_rides[0]
    # state.rides.remove(best_ride)
    # c.free = False
    # c.currentRide = best_ride


      c.one_step()
      c.arrived()

####################################################################################################


if __name__ == "__main__":
  logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', dest='inputfile', required=True, help='Path to input file')
  parser.add_argument('-o', '--outputfile', dest='outputfile', required=True, help='Path to output file')
  args = parser.parse_args()
  inputfile = args.inputfile
  outputfile = args.outputfile

  state = State().parse(inputfile)
  compute(state)
  state.writefile(outputfile)
