#!/usr/bin/env python3
import sys
import os
import math
import argparse

debug_p = False

def getBaseN(nodes, mpn):
    return int(math.sqrt((((mpn * 0.80) * nodes) * 1024 * 1024) / 8))


def getNFromNb(baseN, nb):
    factor = int(baseN/nb)
    if (factor % 2) != 0:
        factor -= 1
    return int(nb * factor)


def getGrid(nodes, ppn):
    cores = nodes * ppn
    sqrt_cores = int(math.sqrt(cores))
    factors = []
    for num in range(2, sqrt_cores+1):
        if (cores % num) == 0:
            factors.append(num)

    if len(factors) == 0:
        factors.append(1)

    diff = 0
    keep = 0
    for f in factors:
        if diff == 0:
            diff = cores - f
        if keep == 0:
            keep = f
        tmpDiff = cores - f
        if tmpDiff < diff:
            diff = tmpDiff
            keep = f

    return (keep, int(cores/keep))


def calchpl(nodes=1, cpn=48, mpn=192000, nb=192, outfile='HPL.dat'):
    global debug_p

    baseN = getBaseN(nodes, mpn)
    realN = getNFromNb(baseN, nb)
    pQ = getGrid(nodes, cpn)

    if debug_p:
        print('DEBUG')
        print('baseN = {}'.format(baseN))
        print('realN = {}'.format(realN))
        print('pQ = {}'.format(pQ))
        print('nb = {}'.format(nb))
        print('outfile = {}'.format(outfile))
        print('')

    contents = ''
    contents += 'HPLinpack benchmark input file\n'
    contents += 'Innovative Computing Laboratory, University of Tennessee\n'
    contents += 'HPL.out      output file name (if any) \n'
    contents += '6            device out (6=stdout,7=stderr,file)\n'
    contents += '1            # of problems sizes (N)\n'
    contents += str(realN) + '         Ns\n'
    contents += '1            # of NBs\n'
    contents += str(nb) + '           NBs\n'
    contents += '0            PMAP process mapping (0=Row-,1=Column-major)\n'
    contents += '1            # of process grids (P x Q)\n'
    contents += str(pQ[0]) + '            Ps\n'
    contents += str(pQ[1]) + '            Qs\n'
    contents += '16.0         threshold\n'
    contents += '1            # of panel fact\n'
    contents += '2            PFACTs (0=left, 1=Crout, 2=Right)\n'
    contents += '1            # of recursive stopping criterium\n'
    contents += '4            NBMINs (>= 1)\n'
    contents += '1            # of panels in recursion\n'
    contents += '2            NDIVs\n'
    contents += '1            # of recursive panel fact.\n'
    contents += '1            RFACTs (0=left, 1=Crout, 2=Right)\n'
    contents += '1            # of broadcast\n'
    contents += '1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)\n'
    contents += '1            # of lookahead depth\n'
    contents += '1            DEPTHs (>=0)\n'
    contents += '2            SWAP (0=bin-exch,1=long,2=mix)\n'
    contents += '64           swapping threshold\n'
    contents += '0            L1 in (0=transposed,1=no-transposed) form\n'
    contents += '0            U  in (0=transposed,1=no-transposed) form\n'
    contents += '1            Equilibration (0=no,1=yes)\n'
    contents += '8            memory alignment in double (> 0)\n'
    contents += '##### This line (no. 32) is ignored (it serves as a separator). ######\n'
    contents += '0                               Number of additional problem sizes for PTRANS\n'
    contents += '1200 10000 30000                values of N\n'
    contents += '0                               number of additional blocking sizes for PTRANS\n'
    contents += '40 9 8 13 13 20 16 32 64        values of NB\n'

    with open(outfile, 'w') as f:
        f.write(contents)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Debugging output')
    parser.add_argument('-n', '--nodes', type=int, default=1, help='Number of nodes; default 1')
    parser.add_argument('-c', '--cores-per-node', type=int, default=48, help='Number of cores per node; default 48')
    parser.add_argument('-m', '--memory-per-node', type=int, default=192000, help='Memory per node in MB; default 192000')
    parser.add_argument('-b', '--block-size', type=int, default=192, help='Block size (NB); default 192')
    parser.add_argument('-o', '--output-file', default='HPL.dat', help='Output file name; default "HPL.dat"')
    args = parser.parse_args()

    debug_p = args.debug

    calchpl(args.nodes, args.cores_per_node, args.memory_per_node, args.block_size, args.output_file)

