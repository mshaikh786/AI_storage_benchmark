#!/usr/bin/env python3 
import time
total=time.time()
import torch
from torchvision import datasets,transforms
import numpy as np
import os, subprocess as sb
import argparse

mod_load_t = time.time() -total

parser = argparse.ArgumentParser(description='data loader benchmark')
parser.add_argument('--num_workers', type=int, default=1,
                    help='Number of PyTorch threads using multiprocessing to run the I/O task along with data transformation.')
parser.add_argument('--dataDir', type=str, required=True, 
                    help='Path to training data.')
parser.add_argument('--batch_size', type=int, default=32, 
                    help='Batch size.')
parser.add_argument('--reps', type=int, default=1, 
                    help='Repeats of the train loop')
args = parser.parse_args()

print("Starting with %s worker threads" % args.num_workers)
tdir = args.dataDir
print("Using Tiny ImageNet 200 classes")
tdata = datasets.ImageFolder(tdir,transform=transforms.ToTensor())
os_time=0.0
for rep in range(args.reps):
    #Clear cache before running a rep
    os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches')
    os_time += (time.time() - total)
    print("Rep %s" %rep)
    dloader = torch.utils.data.DataLoader(tdata,batch_size=args.batch_size,
                                          num_workers=args.num_workers,
                                          pin_memory=True)
    num_batches=len(dloader)
    inputs=list()
    labels=list()
    batch_time=0.0
    indx=0
    mega_bytes=0
    
    
    end = time.time()
    for i, (data,target) in enumerate(dloader):
      batch_time += (time.time() - end)
      mega_bytes += (data.nelement() * data.element_size())
      indx += 1
      end=time.time()
    io_time = batch_time 
    data_vol = int((
        sb.run(['du','-sb', tdir],stdout=sb.PIPE)).
        stdout.decode('utf8').strip().
        split()[0])
    os_time += (time.time() - total)
    mega_bytes = mega_bytes/(1024*1024)
    print("Hostname %s " % os.getenv('HOSTNAME'))
    print(f'Batch size: {dloader.batch_size:.3f}')
    print(f'Total time: {(time.time() - total):.3f}')
    print(f'Time in loading modules {mod_load_t:.3f} seconds')
    print(f'Time spent in I/O: {io_time:.3f} seconds')
    print(f'Time spent running OS commands: {os_time:.3f} seconds')
    print(f'Total samples: {len(tdata.imgs)}')
    print(f'Samples read/second: {len(tdata.imgs)/io_time:.3f}')
    print(f'Data : {data_vol/(1024*1024)} MBytes , Bandwidth: {data_vol/1024/1024/io_time} MBytes/s')
