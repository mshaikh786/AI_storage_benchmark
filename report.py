import os
import numpy as np
import argparse 


parser = argparse.ArgumentParser(description='IO benchmarking report.')
parser.add_argument('--file', type=str, required=True,
                    help='filename with raw benchmark data')
args = parser.parse_args()
filename=args.file

f = open(filename,'r+')

buf = f.readlines()

io=list()
sps=list()
bw=list()
total=list()
for i in range(len(buf)):
 if "Time spent in I/O" in buf[i]:
    io.append(float(buf[i].strip().split()[4]))
 if "Samples read/second" in buf[i]:
    sps.append(float(buf[i].strip().split()[2]))
 if "Bandwidth" in buf[i]:
    bw.append(float(buf[i].strip().split()[6]))
 if "Total time" in buf[i]:
    total.append(float(buf[i].strip().split()[2]))

print(f"The following report contains min,max,mean and standard dev")

print(f"Total time:        {np.min(total):.3f} , {np.max(total):.3f} , {np.mean(total):.3f} ,  {np.std(total):.3f}")
print(f"I/O Time:          {np.min(io):.3f} , {np.max(io):.3f} , {np.mean(io):.3f} , {np.std(io):.3f}")
print(f"Samples/seconds:   {np.min(sps):.3f} , {np.max(sps):.3f}, {np.mean(sps):.3f} , {np.std(sps):.3f}")
print(f"Bandwidth MB/s:    {np.min(bw):.3f} , {np.max(bw):.3f} , {np.mean(bw):.3f}  , {np.std(bw):.3f}")




