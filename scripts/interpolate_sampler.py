import os 
import numpy as np

os.chdir(os.path.dirname(os.path.realpath(__file__)) +  "/..")  

def create_rankfile(ranks):
    out = ""
    for i in range(len(ranks)):
        out += f"rank {i}=localhost slot={ranks[i]}\n"
    with open("rankfile", "w") as f:
        f.write(out)

def run_test(vsize, iter, core_map, bmark, out_file, label):
        create_rankfile(core_map)
        exit_status = os.system(
            f"mpirun -rf rankfile build/softmax data/{bmark}.txt {vsize} {iter} {label} 1>> results/{out_file}.txt 2>> results/{out_file}_error.txt"
        )
        if exit_status != 0:
            os.system(
                f'echo "FAILED: {label} {bmark} WITH: {exit_status}" >> results/{out_file}_failures.txt'
            )

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

v1a = np.array(read_vector("data/benchmark0.txt"))
v1b = np.array(read_vector("data/benchmark5.txt"))

v1a = scaler(v1a)
v1b = scaler(v1b)

divisions = 100

test_name = "test18"

simple_maps = [
    ("1-p",[0]),
    ("1-e",[8]),
    ("2-p",[i for i in range(2)]),
    ("2-e",[i+8 for i in range(2)]),
    ("4-p",[i for i in range(4)]),
    ("4-e",[i+8 for i in range(4)]),
    ("8-p",[i for i in range(8)]),
    ("8-e",[i+8 for i in range(8)]),
]

# for label, mapping in simple_maps:
#   run_test(1000000000, 10, mapping,"benchmark0", test_name , label)

for i in range(8):
  run_test(10000000, 100, [j for j in range(i+1)],"benchmark0", test_name , f'{i+1}-p')
for i in range(8):
  run_test(10000000, 100, [j+8 for j in range(i+1)],"benchmark0", test_name , f'{i+1}-e')

temp_file = "interpolations/i3-temp"
maps = [i for i in range(16)]
ratios = [
    1,
    1.1**23,
    7,
    # 6.8,
    # 6,
    # 5,
    # 6.2,
    # 6.4,
    # 6.6,
  ]

# for ratio in ratios:
#   for i in range(8):
#     save_vector([ratio for j in range(i+1)] + [1 for j in range(i+1)], f"data/{temp_file}.txt")
#     run_test(10000000, 100, [j for j in range(i+1)] + [j+8 for j in range(i+1)], temp_file, test_name, f"{(i+1)*2}-p+e-{ratio:.2f}")
# for i in range(divisions+1):
#   ratio = 1.1**(i + 1)
#   save_vector([ratio for j in range(8)] + [1 for j in range(8)], f"data/{temp_file}.txt")
#   run_test(1000000000, 10, maps, temp_file, test_name, f"log1.1={i+1:.3f}")
