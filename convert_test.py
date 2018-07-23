#!/usr/bin/python
import sys
import re


argvs = sys.argv
argc = len(argvs)

if (argc < 2):
    print "type an input"
    sys.exit();

filename = argvs[1];
fp = open(filename, "r");
lines = fp.read().split("\n")

# converts Dirac format to BAGEL format

tag = "**"  
large = "  Large"  
small = "  Small"  
stop = "Spin-free"
flag_lar = 0
plus_minus = "+"
flag_pm = 0
symbol_obital=""
atom = ""

atom += "{\n"

numbers = []

for i in range(0,len(lines)):
    ll = lines[i]
    if (len(ll) >= len(stop) and ll[0:len(stop)] == stop):
        if (len(numbers) > 0):
          m = len(numbers[0])
          for p in range(1,m):
            atom += "      \"prim\" : ["
            for q in numbers:
              atom += q[0] + ", "
            atom = atom[:-2] + "],\n"
            atom += "      \"cont\" : ["
            atom += "["
            for q in numbers:
              atom += q[p] + ", "
            atom = atom[:-2] + "],\n"
            atom = atom[:-2] + "]\n"
            atom += "    }, {\n"
            atom += "      \"angular\" : \"" + symbol_obital + "\",\n"
          atom = atom[:-27]
          atom += "\n  ]"
          numbers=[]
        break
    # search for the large or small
    if (len(ll) >= len(large) and ll[0:len(large)] == large):
        flag_lar = 1
    elif(len(ll) >= len(small) and ll[0:len(small)] == small):
        flag_lar = 0
    elif (len(ll) >= len(tag) and ll[0:len(tag)] == tag):
        if (len(numbers) > 0):
          m = len(numbers[0])
          for p in range(1,m):
            atom += "      \"prim\" : ["
            for q in numbers:
              atom += q[0] + ", "
            atom = atom[:-2] + "],\n"
            atom += "      \"cont\" : ["
            atom += "["
            for q in numbers:
              atom += q[p] + ", "
            atom = atom[:-2] + "],\n"
            atom = atom[:-2] + "]\n"
            atom += "    }, {\n"
            atom += "      \"angular\" : \"" + symbol_obital + "\",\n"
          atom = atom[:-27]
          atom += "\n  ],\n"
          numbers=[]
        # then go to the next atom
        if (i != len(lines)-2 ):
          if (len(numbers) > 0):
            atom += ",\n"
          numbers = []
          atom += "  \"" + lines[i][3:5].strip(" ") + "\" : [\n" ##
          #nextskip = 1                                          ##
    elif (flag_lar and len(ll) >= 29 and ll[0:5] == "     ") :   ##
        if (len(ll) == 0): continue
        # if buffer is used, flash
        if (ll[29] == plus_minus):
          flag_pm = 1
        else:
          flag_pm = 0
        if (flag_pm and len(numbers) > 0):
          m = len(numbers[0])
          for p in range(1,m):
            atom += "      \"prim\" : ["
            for q in numbers:
              atom += q[0] + ", "
            atom = atom[:-2] + "],\n"
            atom += "      \"cont\" : ["
            atom += "["
            for q in numbers:
              atom += q[p] + ", "
            atom = atom[:-2] + "],\n"
            atom = atom[:-2] + "]\n"
            atom += "    }, {\n"
            atom += "      \"angular\" : \"" + symbol_obital + "\",\n"
          atom = atom[:-23]
          numbers=[]
        elif (flag_pm) :
          atom += "    {\n"
        if (flag_pm) :
          symbol_obital = ll[28].lower()
          atom += "      \"angular\" : \"" + symbol_obital + "\",\n"
    elif (flag_pm and flag_lar and ll[0:3] == "   "):
        if (len(ll) == 0): continue
        tmp = ll[5:].split()
        numbers.append(tmp)

atom += "\n\
}"
atom = atom.replace("D-", "E-")
atom = atom.replace("D+", "E+")
atom = atom.replace("d-", "E-")
atom = atom.replace("d+", "E+")

fp2 = open(filename + ".json", "w");
fp2.write(atom)
fp2.close()
fp.close()
