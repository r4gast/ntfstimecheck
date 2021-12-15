
import os
import platform
import time
import sys
import getopt
import stat
import csv

Final_List = []

def get_timestamps(file_path):
    if platform.system() == 'Windows':
      fileStatsObj = os.stat(file_path)
      creationTime = time.ctime(fileStatsObj[stat.ST_CTIME])
      modifiedTime = time.ctime(fileStatsObj[stat.ST_MTIME])
      accessTime = time.ctime(fileStatsObj[stat.ST_ATIME])
      timestamps = {'filename':file_path,'creation':creationTime,'modification':modifiedTime,'access':accessTime}
      return timestamps

def find_copiedfile(timestamps_dict):

    print("FileName:\t\t" + timestamps_dict['filename'])
    print("Creation Date Time:\t" + timestamps_dict['creation'])
    print("Last Modification Time:\t" + timestamps_dict['modification'])


    if (timestamps_dict['modification'] < timestamps_dict['creation']):
        print("Result:\t\t\tCreation date could not be newer than Last Modification date, Possible Copied File!\n")
        description = "YES"
    else:
        print("Result:\t\t\tNo Clue about File Copy Operation!\n")
        description = "NO"

    data = [timestamps_dict['filename'],timestamps_dict['creation'],timestamps_dict['modification'],description]
    Final_List.append(data)

def main(argv):
    singlefile = ''
    directory = ''
    outputfile = ''

    try:
        opts,args = getopt.getopt(argv,"hf:d:o:")
    except getopt.GetoptError:
        print("timeanalysis.py -f INPUT_FILE | -d INPUT_DIRECTORY")
        sys.exit(2)

    for opt,arg in opts:
        if opt == '-h':
            print("timeanalysis.py -f INPUT_FILE |  -d INPUT_DIRECTORY")

        elif opt in ("-f"):
            singlefile =  arg
            single(singlefile)

        elif opt in ("-d"):
            directory = arg
            wdirectory(directory)

def single(singlefilename):
        singlefilenamee = singlefilename.replace("/","//")
        result = get_timestamps(singlefilename)
        find_copiedfile(result)

def wdirectory(directoryname):
    directoryname =  directoryname.replace("/","//")
    directory_list = os.listdir(directoryname)

    for member in range(len(directory_list)):
        fullpath = directoryname + directory_list[member]
        result = get_timestamps(fullpath)
        find_copiedfile(result)


    header = ['FileName','CreationDate','Last Modification Date','Copy OR Volume File Move Operation']
    with open('TimeAnalysisResult.csv','ab') as f:
            writer =  csv.writer(f)
            writer.writerow(header)
            writer.writerows(Final_List)


if __name__ == "__main__":
   main(sys.argv[1:])
