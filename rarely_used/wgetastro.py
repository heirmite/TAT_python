#!/usr/bin/python
'''
Program:
This is a easier way to download lots of result of coordinates from nova.astrometry.net and correspond to original images.
method: $wgetastrom [original list] [job numbers]
original list:	The list of imgaes you upload to nova.astrometry.net.
job numbers:	THe list of images which is created by nova.astrometry.net, you can easily see them on corresponding result pages.
editor Jacob975 
20170118 version beta 1
##############################
update log

alpha 1:    20170117:
    the program can run properly, but I haven't put it in alias.

beta 1:     20170118:
    the program con run, include alias and explaination.
    But the program can not detect Is the input type is correct or not, 
    as well as preventing itself from type error.
'''   

from sys import argv

originallistname = argv[1]
jobnumberlistname = argv[2]

def readfile(filename):
    file = open(filename)
    answer_1 = file.read()
    answer=answer_1.split("\n")
    return answer

def readfileplus(filename):
    file = open(filename)
    answer_1 = file.read()
    answer=answer_1.split("subDARK.fits\n")
    return answer

def printlist(array):
    for i in range(len(array)):
        print array[i]

originallist = readfileplus(originallistname)
jobnumberlist = readfile(jobnumberlistname)


file = open('download','w')
for i in range(len(originallist)-1) :
    temp="wget 'http://nova.astrometry.net/new_fits_file/" + jobnumberlist[i] + "' -O " + originallist[i] + "subDARK_r_3s_w.fits\n"
    print temp
    file.write(temp)
file.close()


