#!/usr/bin/env python3
"""
A script to plot up the battery level as it's charging.

Log output as 
%ts "%b %d %H:%M:%.S" < /dev/ttyACM0 >>feather_charge.log
(you might need to install "moreutils" to get ts, at least on Ubuntu)

and then run this script
"""

import argparse
from matplotlib import pyplot as plt
import pandas as pd

from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('filename', default='feather_charge.log', nargs='?')
parser.add_argument('--minvoltage', default=0, type=float)
parser.add_argument('--medwindow', default='1min')
args = parser.parse_args()


nyear = datetime.now().year

dtl = []
vs = []
with open(args.filename) as f:
    for line in f:
        lsplit = line.strip().split()
        if 'battery' not in lsplit:
            continue
        dts = ' '.join(lsplit[:3])
        dt = datetime.strptime(dts, '%b %d %H:%M:%S.%f')
        dtl.append(dt.replace(year=nyear))
        vs.append(float(lsplit[-1]))

df = pd.DataFrame({'voltage':vs},index=dtl)
df = df[df['voltage'] > args.minvoltage]


df.plot(alpha=.5, marker='.', lw=0, ms=2)

if args.medwindow != '0':
	meddf = df.rolling(args.medwindow).median().rename(columns={'voltage':args.medwindow+' median'})
	meddf.plot(ax=plt.gca())

plt.show()
