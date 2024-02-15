import os 
import numpy as np
import sklearn.preprocessing as pp

os.chdir(os.path.dirname(os.path.realpath(__file__)) +  "/../data")  

def read_vector(fname):
  with open(fname) as f:
    data = f.read().split()
    return [float(x) for x in data]

def L1_scaler(v):
  sum = np.sum(v)
  return v/sum

def save_vector(v, fname):
  data = ""
  for i in v:
    data = data + str(i) + "\n"
  with open(fname, "w") as f:
    f.write(data)

scaler = L1_scaler

v1a = np.array(read_vector("benchmark3.txt"))
v1b = np.array(read_vector("benchmark3-b.txt"))

v1a = scaler(v1a)
v1b = scaler(v1b)



for i in range(0,11):
  t = i / 10
  save_vector(v1a*t + v1b*(1-t), f"interpolations/i1-{t:3.1f}.txt")

v2a = np.array(read_vector("benchmark0.txt"))
v2b = np.array(read_vector("benchmark3.txt"))

v2a = scaler(v2a)
v2b = scaler(v2b)

for i in range(0,11):
  t = i / 10
  save_vector(v2a*t + v2b*(1-t), f"interpolations/i2-{t:3.1f}.txt")
