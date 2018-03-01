import sys
import argparse
import time

class Car:
  def __init__(self):
    self.free = True
    self.position = [0,0]
    self.currentRide = None
    self.list_rides = []

  def __repr__(self):
    return len(self.list_rides)+' '.join(self.list_rides)

  def one_step(self):
    if not self.free:
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
    self.n = n
    self.a = a
    self.b = b
    self.x = x
    self.y = y
    self.t1 = t1
    self.t2 = t2

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
        tmp = list(content[i].split('\n')[0])
        self.rides.append(Ride(i, tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5]))
      self.cars = [Car() for i in range(self.nb_car)]
    return self
        
  def writefile(self, outfile):
    f = open(outfile, 'w')
    for s in self.cars:
      f.write(str(s)+"\n")
    f.close()


###################################################################################################


def compute(inp):
  '''
  Implementation of the computing logic
  '''
  for i in range(inp.step):
    print(i)
    # move the car in the map

    # if the car arrived to it destination, turn the free flag to True

    # assign a ride to a vehicle


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
