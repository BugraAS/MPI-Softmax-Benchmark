import os 

os.chdir(os.path.dirname(os.path.realpath(__file__)) +  "/../results")  

arr = ["benchmark0","benchmark1","benchmark2"]

out_file = "test1"

if not os.path.isdir("../results"):
      os.mkdir("../results") 

#     for j in arr_var:
for i in arr: 
       exit_status = os.system(f"mpirun --map-by core -np 16 ../build/softmax ../data/{i}.txt 1000000 500 1>> {out_file}.txt 2>> {out_file}_error.txt");
       if(exit_status != 0):
              os.system(f'echo "FAILED: {i} WITH: {exit_status}" >> test1_failures.txt')
