# MPI benchmark using softmax

Create build folder
```bash
mkdir build
```

Configure project.  
```bash
cmake -Ssrc -Bbuild
```

Compile the project
```bash
cmake --build build --config Release --target all
```

Run
```bash
mpirun build/softmax [benchmark-file] [size-of-vector] [number-of-iterations] [label]
```
