"""
zberman2, chansky2, based off of VishnuC's file converter
Python program which converts .byte.gz files to a summarized form.
"""
from multiprocessing import Pool
import os
import gzip
from csv import writer
import six

#python type code
read_mode, write_mode = ('r','w') if six.PY2 else ('rt','wt')

if six.PY2:
    from itertools import izip
    zp = izip
else:
    zp = zip

# Give path to gzip of .byte files
paths = ['/Volumes/My Passport/460_Data/train_gz/',
'/Users/benchansky/Desktop/460_malware_project/test_gz/']   
######needed to use an external hard drive
#because the data set is quite large ~200+gb



def convert(path):
    mod_path = path #+ '_gz/'
    Files = os.listdir(mod_path)
    byteFiles = [i for i in Files if '.bytes.gz' in i]
    consolidatedFile = path + '_converted.gz'
    
    with gzip.open(consolidatedFile, write_mode) as f:
        #prep header
        fw = writer(f)
        columns = ['filename', 'question_mark_counter']
        columns += ['TB_'+hex(i)[2:] for i in range(16**2)]
        fw.writerow(columns)
        converted = []
        for t, fname in enumerate(byteFiles):
            f = gzip.open(mod_path+fname, read_mode)
            twoByte = [0]*256
            question_mark_counter = 0
            for row in f:
                codes = row[:-2].split()[1:]
                question_mark_counter += codes.count('??')
                twoByteCode = [int(i,16) for i in codes if i != '??']  #change to two byte summary                                                  
                # Frequency calculation 
                for i in twoByteCode:
                    twoByte[i] += 1
                
            converted.append([fname[:fname.find('.bytes.gz')], question_mark_counter] \
                                    + twoByte)
                                    
            # console status indicator
            if (t+1)%100==0:
                print(t+1, 'files loaded for ', path)
                fw.writerows(converted)
                converted = []
                
        # Write remainder 
        if len(converted)>0:
            fw.writerows(converted)
            converted = []
    
    del Files, byteFiles, columns, mod_path, converted, f, fw, \
        twoByte, twoByteCode, consolidatedFile

#using two threads to process test and train at same time
if __name__ == '__main__':
    p = Pool(2)
    p.map(convert, paths)