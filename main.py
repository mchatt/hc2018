import sys
import argparse
import time

class Input:
  '''
  Class representing the input data
  '''
  def __init__(self):
    self.R = 0
    self.C = 0
    self.L = 0
    self.H = 0
    self.M = []

  def parse(self, inputFile):
    with open(inputFile) as f:
      content = f.readlines()
      self.R, self.C, self.L, self.H = [int(x) for x in content[0].split('\n')[0].split()]
      for i in range(1, len(content)):
        self.M.append(list(content[i].split('\n')[0]))
    return self

  def __str__(self):
    p = ''
    for x in self.M:
      p += str(x) + '\n'
    return '%d %d %d %d\n%s' % (self.R, self.C, self.L, self.H, p)


class Output:
  '''
  Class representing the output data
  '''
  def __init__(self):
    self.paires = [] #list of slices

  def __str__(self):
    p = 'print Output {%d}\n' % len(self.paires)
    for x in self.paires:
      p += str(x) + '\n'
    return p

  def formatOutput(self, outputFile):
    f = open(outputFile, 'w')
    f.write('%d\n' % len(self.paires))
    for p in self.paires :
      f.write(' '.join([str(x) for x in p]))
    f.close()


###################################################################################################


def compute(inp):
  '''
  Implementation of the computing logic
  '''
  res = Output()

  def findSlices(inp, startingPoint, slices):
    print('startingPoint', startingPoint)
    print('slices', slices)
    if startingPoint == [inp.R-1, inp.C-1]:
      return slices
    m = 0
    t = 0
    for i in range(inp.R-startingPoint[0]):
      for j in range(2*i+1):
        l = i+startingPoint[0] if (j <= i+1) else 2*i-j
        c = j+startingPoint[1] if (j <= i+1) else i+1
        if l >= inp.R or c >= inp.C:
          continue
        if inp.M[l][c] == 'M':
          m = m+1
      else:
          t = t+1
      if m >= inp.L and m >= inp.L:
          return findSlices(inp, [startingPoint[0],c+1], slices + [[startingPoint, [l, c]]])

    return slices

  res.paires = findSlices(inp, [0,0], [])

  return res



####################################################################################################


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', dest='inputfile', required=True, help='Path to input file')
  parser.add_argument('-o', '--outputfile', dest='outputfile', required=True, help='Path to output file')
  args = parser.parse_args()
  inputfile = args.inputfile
  outputfile = args.outputfile

  inp = Input().parse(inputfile)
  output = compute(inp)
  output.formatOutput(outputfile)
