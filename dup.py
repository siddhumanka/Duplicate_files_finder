import os, sys
import hashlib
from stat import *
from collections import defaultdict

class fil :
	def __init__(self, siz, file_h, name):
		self.size=siz
		self.file_hash=file_h
		self.name=name
	def keyfun(self):
		return self.size

group=defaultdict(list)
file_list=[]
def traverse(top):
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        try:
        	mode = os.stat(pathname)[ST_MODE]
	except OSError :
		print "Something went wrong while accessing file :"+pathname
        try:
	        if S_ISDIR(mode):
	            traverse(pathname)
	        elif S_ISREG(mode):
		    file_hash1=hashfile(pathname)
		    size1 = os.stat(pathname)[ST_SIZE]
		    file_list.append(fil(size1,file_hash1,pathname))
	        elif S_ISLNK(mode):
	            print "Skipped file : "+pathname
	except UnboundLocalError,OSError :
		print "Skipped file : "+pathname

def hashfile(path, blocksize = 65536):
	try:
    		afile = open(path, 'rb')
    		hasher = hashlib.md5()
    		buf = afile.read(blocksize)
   		while len(buf) > 0:
    			hasher.update(buf)
	 		buf = afile.read(blocksize)
		afile.close()
		return hasher.hexdigest()
	except IOError :
    		print "Skipped file : "+path

def sort():
	file_list.sort(key=fil.keyfun)

def grouping():
	chunk_list=[]
	print "Total number of files are : "+str(len(file_list))
	j=0
	for i in range(0,len(file_list)-1):
		if file_list[i].size == file_list[i+1].size:
			if file_list[i].size in group:
                		group[file_list[i].size].append(file_list[i+1])
            		else:
                		group[file_list[i].size] = [file_list[i]]
				group[file_list[i].size].append(file_list[i+1])
		else :
			group[file_list[i+1].size] = [file_list[i+1]]
	comparehash()

def comparehash() :
	for key in group.keys():
		for i in range(0,len(group[key])-1):
			print "-----------------------------------------------------------for size "+str(key)+"-------------------------------------------------------------------------"
			for j in range ((1+i),len(group[key])):
				if group[key][i].file_hash == group[key][j].file_hash:
					print group[key][i].name+"\n\t\t\t\t\t\t\tAND\n"+group[key][j].name+"\nARE DUPES\n"		
	k=1
	while (k==1):	
		rm_file=raw_input("Enter the duplicate file to be deleted or enter e to exit\n >>>>")
		if rm_file == 'e':
			k=0
		else:
			os.remove(rm_file)
			print "Successfully Deleted..."
	
if __name__ == '__main__':
	try :
	    traverse(sys.argv[1])
	except IndexError :
	    print "Please mention a directory as n arguement"    
	    sys.exit(0)
	sort()
    	grouping()
