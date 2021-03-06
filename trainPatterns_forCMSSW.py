import sys, os
import numpy as np
import matplotlib.pyplot as plt
from stationsObjects import*
import copy
import pickle

# Input variable
if len(sys.argv) < 2 :
    print("Please tell me which MB you want to train the patterns for: MB or MB4")
    print("")
    print("python trainPatterns_forCMSSW.py MB1")
    print("python trainPatterns_forCMSSW.py MB2")
    print("python trainPatterns_forCMSSW.py MB3")
    print("python trainPatterns_forCMSSW.py MB4")
    sys.exit()

MB_input = sys.argv[1]
print("MB to use: " + MB_input)

# Maximum slope allowed for a pattern (mmax is the atan of the phi angle)
mmax = 0.3

allPatterns = []
allSeeds    = [] #Naming convention is [SLdown, SLup, diff in units of halfs of cell width] == [SLup, SLdown, -diff]

# Choose which MB use for training,
# considering those defined in stationsObjects.py

if MB_input == "MB1_left":
    MB_train   = MB1_left
    MB_train_f = MB1f_left
    output_file_name = "trainedPatterns_MB1_left.pck"
elif MB_input == "MB1_right":
    MB_train   = MB1_right
    MB_train_f = MB1f_right
    output_file_name = "trainedPatterns_MB1_right.pck"

elif MB_input == "MB2_left": 
    MB_train   = MB2_left
    MB_train_f = MB2f_left
    output_file_name = "trainedPatterns_MB2_left.pck"
elif MB_input == "MB2_right": 
    MB_train   = MB2_right
    MB_train_f = MB2f_right
    output_file_name = "trainedPatterns_MB2_right.pck"

elif MB_input == "MB3": 
    MB_train   = MB3
    MB_train_f = MB3f
    output_file_name = "trainedPatterns_MB3.pck"

elif MB_input == "MB4_left": 
    MB_train   = MB4_left
    MB_train_f = MB4f_left
    output_file_name = "trainedPatterns_MB4_left.pck"
elif MB_input == "MB4": 
    MB_train   = MB4
    MB_train_f = MB4f
    output_file_name = "trainedPatterns_MB4.pck"
elif MB_input == "MB4_right": 
    MB_train   = MB4_right
    MB_train_f = MB4f_right
    output_file_name = "trainedPatterns_MB4_right.pck"
    
else:
    raise ValueError("Please revise input")
    
# Generate all sets of semilayer-semilayer patterns

#################################################
### Starting from correlated sets of patterns ###
#################################################

#################################################
# Starting point: each layer of SL1 (l_in_sl1), 
# first cell (starting from left or right), 
# both lateralities, positive and negative slope 

for lat in [0.25, 0.75]:
    for slope in [0, -1]:
        for l_in_sl1 in range(0, 4):
            print("")
            print("Layer in SL1 = {}".format(l_in_sl1))
            x0 = MB_train.layers[l_in_sl1].DTlist[0].xmin + MB_train.layers[l_in_sl1].DTlist[0].width*lat
            y0 = MB_train.layers[l_in_sl1].DTlist[0].ymin + MB_train.layers[l_in_sl1].DTlist[0].height/2.

            # Final point: each layer of SL3: consider all valid cells and both lateralities
            for l_in_sl3 in reversed(range(4, 8)):
                print("Layer in SL3 = {}".format(l_in_sl3))
                for d in MB_train_f.layers[l_in_sl3].DTlist:
                    # just to keep slopes separated
                    if slope == 0  and d.idx < 0: continue
                    if slope == -1 and d.idx > 0: continue
                    # Consider both lateralities
                    for semicell in [0.25, 0.75]:
                        xf = d.xmin + semicell*d.width
                        if abs(xf - x0) < 0.1*d.width: 
                            m = 100000
                        else:
                            yf = d.ymin + d.height/2.
                            m = (yf - y0)/(xf - x0)
                        if abs(m) < mmax:  continue
                        mm = Muon(x0, y0, m)
                        if slope == -1:
                            mm.color = "k-"
                        MB_train_f.checkIn(mm)
                        if (l_in_sl3 == 7 and l_in_sl1 == 3):
                            mm.plot()        
                        if abs(m) > mmax:
                            allPatterns.append(mm.getPattern())
                            allSeeds.append([l_in_sl1, l_in_sl3, d.idx - MB_train.layers[l_in_sl1].DTlist[0].idx])


#################################################
### And now the uncorrelated sets of patterns ###
#################################################

# And now uncorrelated in SL1

#################################################
# Starting point: each layer of SL1 (l_in_sl1), 
# first cell (starting from left or right), 
# both lateralities, positive and negative slope 

for lat in [0.25, 0.75]:
    for slope in [0, -1]:
        for l_in_sl1 in range(0, 4):
            print("")
            print("Lower layer in SL1 = {}".format(l_in_sl1))
            x0 = MB_train.layers[l_in_sl1].DTlist[0].xmin + MB_train.layers[l_in_sl1].DTlist[0].width*lat
            y0 = MB_train.layers[l_in_sl1].DTlist[0].ymin + MB_train.layers[l_in_sl1].DTlist[0].height/2.

            # Final point: each layer of SL1 (excluding the one from where we start), 
            # considering all valid cells and both lateralities
            for l_in_sl1_up in reversed(range(l_in_sl1 + 1, 4)):
                print("Upper layer in SL1 = {}".format(l_in_sl1_up))
                for d in MB_train_f.layers[l_in_sl1_up].DTlist:
                    # just to keep slopes separated
                    if slope == 0  and d.idx < 0: continue
                    if slope == -1 and d.idx > 0: continue
                    # Consider both lateralities
                    for semicell in [0.25, 0.75]:
                        xf = d.xmin + semicell*d.width
                        if abs(xf - x0) < 0.1*d.width: 
                            m = 100000
                        else:
                            yf = d.ymin + d.height/2.
                            m = (yf - y0)/(xf - x0)
                        if abs(m) < mmax:  continue
                        mm = Muon(x0,y0, m)
                        if m < mmax: 
                            mm.color = "k-"
                        MB_train_f.checkIn(mm)
                        # mm.plot()        
                        if abs(m) > mmax:
                            allPatterns.append(mm.getPattern())
                            allSeeds.append([l_in_sl1, l_in_sl1_up, d.idx - MB_train.layers[l_in_sl1].DTlist[0].idx])


# Starting from uncorrelated in SL3

#################################################
# Starting point: each layer of SL3 (l_in_sl3), 
# first cell (starting from left or right), 
# both lateralities, positive and negative slope 

for lat in [0.25, 0.75]:
    for slope in [0, -1]:
        for l_in_sl3 in range(4, 8):
            print("")
            print("Lower layer in SL3 = {}".format(l_in_sl3))
            x0 = MB_train.layers[l_in_sl3].DTlist[0].xmin + MB_train.layers[l_in_sl3].DTlist[0].width*lat
            y0 = MB_train.layers[l_in_sl3].DTlist[0].ymin + MB_train.layers[l_in_sl3].DTlist[0].height/2.

            # Final point: each layer of SL3 (excluding the one from where we start), 
            # considering all valid cells and both lateralities
            for l_in_sl3_up in reversed(range(l_in_sl3 + 1, 8)):
                print("Upper layer in SL3 = {}".format(l_in_sl3_up))
                for d in MB_train_f.layers[l_in_sl3_up].DTlist:
                    # just to keep slopes separated
                    if slope == 0  and d.idx < 0: continue
                    if slope == -1 and d.idx > 0: continue
                    # Consider both lateralities
                    for semicell in [0.25, 0.75]:
                        xf = d.xmin + semicell*d.width
                        if abs(xf - x0) < 0.1*d.width: 
                            m = 100000
                        else:
                            yf = d.ymin + d.height/2.
                            m = (yf - y0)/(xf - x0)
                        if abs(m) < mmax:  continue
                        mm = Muon(x0,y0, m)
                        if m < mmax: 
                            mm.color = "k-"
                        MB_train_f.checkIn(mm)
                        # mm.plot()        
                        if abs(m) > mmax:
                            allPatterns.append(mm.getPattern())
                            allSeeds.append([l_in_sl3, l_in_sl3_up, d.idx - MB_train.layers[l_in_sl3].DTlist[0].idx])


# Plots, printouts, and save
listPatterns = []

for i in range(len(allPatterns)):
      listPatterns.append(Pattern(allSeeds[i], allPatterns[i]))
      # print "---------------------------------"
      # print allSeeds[i], allPatterns[i]
      # print "---------------------------------"

print("Patterns: ", len(listPatterns))

pick = open(output_file_name, "wb") 
pickle.dump(listPatterns, pick)

"""
overlaps = 0
for i in range(len(listPatterns)):
    for j in range(len(listPatterns)):
        if listPatterns[i].isEqual(listPatterns[j]): overlaps += 1

#print [i.overlap for i in listPatterns]
print overlaps
"""

#print listPatterns[0].overlapsw

MB_train_f.plot()

plt.axis([-100, 100, -5, 30])
plt.xlabel("z/cm")
plt.ylabel("r/cm")
plt.show()

