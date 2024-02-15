import os

os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/..")

bmarks = [
    "benchmark0",
    "benchmark1",
    "benchmark2",
    "benchmark3",
    "benchmark3-b",
    "benchmark4",
    "benchmark4-b",
]
bmarks_interpolated = [
    "i1-0.0",
    "i1-0.1",
    "i1-0.2",
    "i1-0.3",
    "i1-0.4",
    "i1-0.5",
    "i1-0.6",
    "i1-0.7",
    "i1-0.8",
    "i1-0.9",
    "i1-1.0",
    "i2-0.0",
    "i2-0.1",
    "i2-0.2",
    "i2-0.3",
    "i2-0.4",
    "i2-0.5",
    "i2-0.6",
    "i2-0.7",
    "i2-0.9",
    "i2-0.8",
    "i2-1.0",
]

if not os.path.isdir("../results"):
    os.mkdir("../results")

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


test_name = "test7"

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

for label, mapping in simple_maps:
  run_test(10000000, 100, mapping,"benchmark0", test_name , label)

core_maps = [
    [i for i in range(16)],
]

for mapping in core_maps:
  for bmark in bmarks:
    run_test(10000000, 100, mapping, bmark, test_name, "bmark-n")
  for bmark in bmarks_interpolated:
    run_test(10000000, 100, mapping, f"interpolations/{bmark}", test_name, "bmark-i")