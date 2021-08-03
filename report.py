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

print("The following report contains min,max,mean and standard dev \n")


print("Total time     : %12.3f  %12.3f  %12.3f  %12.3f"%(np.min(total),np.max(total),np.mean(total),np.std(total)))
print("I/O Time       : %12.3f  %12.3f  %12.3f  %12.3f"%(np.min(io),np.max(io) , np.mean(io) ,np.std(io)))
print("Samples/seconds: %12.3f  %12.3f  %12.3f  %12.3f"%(np.min(sps),np.max(sps) , np.mean(sps) ,np.std(sps)))
print("Bandwidth MB/s : %12.3f  %12.3f  %12.3f  %12.3f"%(np.min(bw),np.max(bw) , np.mean(bw) ,np.std(bw)))






