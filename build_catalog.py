#!/usr/bin/python
'''
Program:
This is a program to build catalog by local star catalog.
step in concept:
    1.  get in the path of /home/Jacob975/demo/TAT_row_star_catalog/
    2.  read row star catalogs haven't been resolved, then resolve.
    3.  save result in path of /home/Jacob975/demo/TAT_star_catalog/
    4.  move row star catalogs to /home/Jacob975/demo/TAT_row_star_catalog/done/

    example of star catalog.

    # id : TAT279-29_7.tsv
    # HD id: 0000
    # HIB id: 0000
    # other famous star catalog id: 0000
    RAJ2000 DECJ2000        date    band    scope   method  count   instrument_mag  x_size  y_size
    278.7513        -28.8593        20170518        N_40s   TF      mdn     0.1295  2.2194  0.0000122       -0.0000227
    278.7508        -28.8592        20170518        R_100s  TF      mdn     0.1750  1.8922  0.0000117       -0.0000249 

Usage:
    $build_catalog.py   # you can run this code anywhere.

editor Jacob975
20170721
#################################
update log

    20170721 version alpha 1
        just write down the future of this code.
        no content, haha.

    20170726 version alpha 2
        1.  The code work properly.
        2.  There is still one thing haven't been comfirm 
            that how large is the error of position of stars. 
    20170731
        Localize for user Joseph
        1.path_of_data_source = "/home/Jacob975/demo/TAT_row_star_catalog/" >> path_of_data_source = "/home/Joseph/demo/TAT_row_star_catalog/"
        2.path_of_output = "/home/Jacob975/demo/TAT_star_catalog/" >> path_of_output = "/home/Joseph/demo/TAT_star_catalog/"
'''
from sys import argv
import numpy as np
import pyfits
import time
import glob
import os

def readfile(filename):
    file = open(filename)
    answer_1 = file.read()
    answer=answer_1.split("\n")
    while answer[-1] == "":
        del answer[-1]
    return answer

# This is used to read .tsv file
def read_tsv_file(file_name):
    f = open(file_name, 'r')
    data = []
    for line in f.readlines():
        # skip if no data or it's a hint.
        if not len(line) or line.startswith('#'):
            continue
        line_data = line.split("\t")
        data.append(line_data)
    f.close()
    return data

# read data from .tsv file 
# compare their RA and DEC with existing star catalog
# arrange them to proper cataglo
def resolve_data(data_list, date, band, scope, method):
    for data in data_list:
        if data[0] == "RAJ2000":
            continue
        if data[0] == "degree":
            continue
        local_RA = float(data[0])
        local_DEC = float(data[2])
        key_name = ""
        if local_DEC >= 0:
            key_name = "TAT{0:.0f}+{1:.0f}*".format(local_RA, local_DEC)
        elif local_DEC < 0:
            key_name = "TAT{0:.0f}{1:.0f}*".format(local_RA, local_DEC)
        star_catalog_list = glob.glob(key_name)
        success = 0
        if len(star_catalog_list) != 0:
            for star_name in star_catalog_list:
                star_property = read_tsv_file(star_name)
                ref_RA = float(star_property[2][0])
                ref_DEC = float(star_property[2][2])
                # determine that whether they are the same or not
                if local_RA - 0.0007 <= ref_RA and ref_RA <= local_RA + 0.0007: 
                    if local_DEC - 0.0007 <= ref_DEC and ref_DEC <= local_DEC + 0.0007:
                        append_page(data, star_name, date, band, scope, method)
                        success = 1
                        break
        if not success :
            create_page(data, len(star_catalog_list), date, band, scope, method)
    return 1

# create a new star catalog
def create_page(data, id_number, date, band, scope, method):
    row_RA = float(data[0])
    row_DEC = float(data[2])
    file_name = ""
    if row_DEC >= 0:
        file_name = "TAT{0:.0f}+{1:.0f}_{2}.tsv".format(row_RA, row_DEC, id_number)
    elif row_DEC < 0:
        file_name = "TAT{0:.0f}{1:.0f}_{2}.tsv".format(row_RA, row_DEC, id_number)
    result_file = open(file_name, "a")
    result_file.write("# id : {0}\n".format(file_name))
    result_file.write("# count and instrument_mag have been normalized by exptime = 1s\n")
    result_file.write("RAJ2000\te_RAJ2000\tDECJ2000\te_DECJ2000\tdate\tband\tscope\tmethod\tcount\te_count\tinst_mag\te_inst_mag\tXcoord\te_Xcoord\tYcoord\te_Ycoord\tsigma_x\te_sigma_x\tsigma_y\te_sigma_y\trotation\te_rotation\tbkg\te_bkg\n")
    result_file.write("degree\tdegree\tdegree\tdegree\tno_unit\tno_unit\tno_unit\tno_unit\tcount_per_sec\tcount_per_sec\tmag_per_sec\tmag_per_sec\tpixel\tpixel\tpixel\tpixel\tpixel\tpixel\tpixel\tpixel\tdegree\tdegree\tcount\tcount\n")
    result_file.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\t{17}\t{18}\t{19}\t{20}\t{21}\t{22}\t{23}".format(data[0], data[1], data[2], data[3], date, band, scope, method, data[8], data[9], data[10], data[11], data[4], data[5], data[6], data[7], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19]))
    result_file.close()

# append data to a existing star catalog
def append_page(data, TAT_id, date, band, scope, method):
    result_file = open(TAT_id, "a")
    result_file.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\t{17}\t{18}\t{19}\t{20}\t{21}\t{22}\t{23}".format(data[0], data[1], data[2], data[3], date, band, scope, method, data[8], data[9], data[10], data[11], data[4], data[5], data[6], data[7], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19]))
    result_file.close()

#--------------------------------------------
# main code
VERBOSE = 0
# measure times
start_time = time.time()
# get property from argv
list_name=argv[-1]
fits_list=readfile(list_name)

# path of data source
path_of_data_source = "/home/Joseph/demo/TAT_row_star_catalog/"
os.chdir(path_of_data_source)
row_star_catalog_list = glob.glob("*.tsv")
# path of output
path_of_output = "/home/Joseph/demo/TAT_star_catalog/"
os.chdir(path_of_output)
for name in row_star_catalog_list:
    # read a tsv file which haven't been prcoessed
    name_list = name.split("_")
    name_dir = "{0}{1}".format(path_of_data_source, name)
    temp_data = read_tsv_file(name_dir)
    date = name_list[1]
    band = "{0}_{1}".format(name_list[3], name_list[4])
    scope = name_list[0]
    method = name_list[-3]
    success = resolve_data(temp_data, date, band, scope, method)
    if success:
        os.rename(name_dir, "{0}done/{1}".format(path_of_data_source, name))
# measuring time
elapsed_time = time.time() - start_time
print "Exiting Main Program, spending ", elapsed_time, "seconds."
