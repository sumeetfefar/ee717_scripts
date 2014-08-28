import re
import os
import difflib
import csv
import signal
from contextlib import contextmanager

code_dir = "./Codes/"
extract_dir = "./Extract/"
refpath = "./Reference/"
csv_sheet = "Result.csv"

IOfiles = [("input100.txt","output100.txt"),("input1000.txt","output1000.txt"),("input10000.txt","output10000.txt")]
permanent_dirs = ["Reference","Answers"]


class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def CPP_correct(inputfile,outputfile):
	with open(inputfile, "r") as infile, open(outputfile, "w") as outfile:
		blind_copy = True
		bracket_search = False
		for line in infile:
			ms_to_us = re.findall('(.*?)(?=double runtime \= \(end \- start\)\/\(double\)\(CLOCKS_PER_SEC\/1000\)\;)', line)
			if ms_to_us != []:
				tmp = re.split('double runtime \= \(end \- start\)\/\(double\)\(CLOCKS_PER_SEC\/1000\)\;', line)
				# print tmp
				outfile.write(tmp[0]+"double runtime = (end - start)/(double)(CLOCKS_PER_SEC/1000000);" + tmp[1])
			elif blind_copy and not bracket_search:
				outfile.write(line)

			if re.search('(?<=main \(void\))', line) != None or re.search('(?<=main \()', line) != None or re.search('(?<=main\()', line) != None:
				# break
				bracket_count = line.count("{")-line.count("}")
				outfile.write("{\n")
				for i in IOfiles:
					outfile.write("\tinsertionSort(\""+i[0]+"\",\""+i[1]+"\");\n")	
				# outfile.write("\tinsertionSort(\"input100.txt\",\"output100.txt\");\n")
				# outfile.write("\tinsertionSort(\"input1000.txt\",\"output1000.txt\");\n")
				# outfile.write("\tinsertionSort(\"input10000.txt\",\"output10000.txt\");\n")
				outfile.write("\treturn 0;\n")
				outfile.write("}\n")
				blind_copy=False
				if(bracket_count==0):
					bracket_search = True

			if not blind_copy :
				if bracket_count >0 or bracket_search:
					bracket_count +=line.count("{") - line.count("}")
					if bracket_count>0:
						bracket_search = False
				else:
					blind_copy= True
			

	os.system("mv -f " + outputfile + " " + inputfile)

def findReadme(filepath):
	for subdir, dirs, files in os.walk(filepath):
		for rfile in files:
			# print rfile
			if("README" in rfile.upper()):
				return rfile
	return "Nil"
	

def CheckCorrect(filepath,rollno_from_filename):
	for subdir, dirs, files in os.walk("./Answers"):
		score = {}
		for answer_file in files:
			diff = difflib.SequenceMatcher(None, open(filepath+answer_file).readlines(), open("./Answers/"+answer_file).readlines())
			diff.get_matching_blocks()
			with open("./Answers/"+answer_file,"r") as ans_file:
				N = int(ans_file.readline().strip())
			with open(filepath+answer_file,"r") as ans_file:
				runtime = str(ans_file.readline().strip()) # Runtime in microseconds
			# print diff.matching_blocks, N, runtime
			correctOutput = 0
			for i in diff.matching_blocks:
					correctOutput += i[2]
			# print correctOut,"|", N
			score["input"+str(N)]=(N,correctOutput,runtime)

			# if (correctOutput != N):
			# 	print False
			# else:
			# 	print True
		try:
			Readme_filnename = findReadme(filepath)

			with open(filepath+Readme_filnename,"r") as ans_file:
				(rollno, Name) = ans_file.readline().replace("\t"," ").split(" ",1)
				(rollno, Name) = (rollno.strip(), Name.strip())
				# print Name, rollno

			with open(csv_sheet, 'a') as csvfile:
				str_csv = rollno +","+Name
				marks = 0
				for i in IOfiles:
					str_csv = str_csv +","+ str(score[i[0].split(".")[0]][1]/score[i[0].split(".")[0]][0]*10) +","+str(score[i[0].split(".")[0]][2])
					marks += (score[i[0].split(".")[0]][1]/score[i[0].split(".")[0]][0]*10)
				str_csv += "," + str(int(float(marks)/len(IOfiles)*10))
				csvfile.write(str_csv+"\n")
		except:
			with open(csv_sheet, 'a') as csvfile:
				str_csv = rollno_from_filename + "," + "<README not readable>"
				marks = 0
				for i in IOfiles:
					str_csv = str_csv +","+ str(score[i[0].split(".")[0]][1]/score[i[0].split(".")[0]][0]*10) +","+str(score[i[0].split(".")[0]][2])
					marks += (score[i[0].split(".")[0]][1]/score[i[0].split(".")[0]][0]*10)
				str_csv += "," + str(int(float(marks)/len(IOfiles)*10))
				csvfile.write(str_csv+"\n")

def modifyfilepath(filepath,rollno_filename):

	if(os.path.exists(filepath+rollno_filename.lower())):			
			
		Readme_filnename = findReadme(filepath)
		# print "mv " + filepath + Readme_filnename + " " + filepath + rollno_filename.lower()
		# print filepath, Readme_filnename
		if(os.path.isfile(filepath + Readme_filnename)):
			os.system("mv " + filepath + Readme_filnename + " " + filepath + rollno_filename.lower())

		filepath = filepath + rollno_filename.lower() + "/"
		# print filepath
		return modifyfilepath(filepath,rollno_filename.lower())

	elif(os.path.exists(filepath+rollno_filename.upper())):
		
		Readme_filnename = findReadme(filepath)
		
		if(os.path.isfile(filepath + Readme_filnename)):
			os.system("mv " + filepath + Readme_filnename + " " + filepath + rollno_filename.upper())

		# filepath = modifyfilepath(filepath,rollno_filename)
		filepath = filepath + rollno_filename.upper() + "/"
		# print filepath
		return modifyfilepath(filepath,rollno_filename.upper())
	else:
		return filepath


def userEvaluate(rollno_filename):

	
	filepath = extract_dir+rollno_filename+"/"
	original_dir = os.getcwd()
	print("Extract Done")
	try:
		
		filepath = modifyfilepath(filepath,rollno_filename)

		os.system("cp " + refpath + "* " + filepath)

		if not (os.path.isfile(filepath+"Makefile")):
			os.system("cp Makefile " + filepath)
			
		os.chdir(filepath)
		

		CPP_correct("insertion_sort.cpp", "insertion_sort.cpp.tmp")
		os.system("make")

		

		# try:
		# 	with time_limit(1):
		os.system("./insertion_sort")
		os.chdir(original_dir)
		# except TimeoutException, e:
		# 	Readme_filnename = findReadme(filepath)
		# 	print filepath, Readme_filnename
		# 	try:
		# 		with open(filepath+Readme_filnename,"r") as ans_file:
		# 			(rollno, Name) = ans_file.readline().replace("\t"," ").split(" ",1)
		# 			(rollno, Name) = (rollno.strip(), Name.strip())
		# 	except Exception, p:
		# 		Name = "<README not readable>"
		# 		print str(p)
		# 	print "Error : " + rollno_filename + " | " + str(e)
		# 	os.chdir(original_dir)
		# 	with open(csv_sheet, 'a') as csvfile:
		# 		str_csv = rollno_filename + "," + Name
		# 		for i in IOfiles:
		# 			str_csv = str_csv +","+ "0" +","+"-"
		# 		str_csv += "," + "0" + ","+str(e)
		# 		csvfile.write(str_csv+"\n")

		os.chdir(original_dir)
		print "Checking Correctness"
		CheckCorrect(filepath,rollno_filename)
	except Exception, e: 
		Readme_filnename = findReadme(filepath)
		print filepath, Readme_filnename
		try:
			with open(filepath+Readme_filnename,"r") as ans_file:
				(rollno, Name) = ans_file.readline().replace("\t"," ").split(" ",1)
				(rollno, Name) = (rollno.strip(), Name.strip())
		except Exception, p:
			Name = "<README not readable>"
			print str(p)
		print "Error : " + rollno_filename + " | " + str(e)
		os.chdir(original_dir)
		with open(csv_sheet, 'a') as csvfile:
			str_csv = rollno_filename + "," + Name
			for i in IOfiles:
				str_csv = str_csv +","+ "0" +","+"-"
			str_csv += "," + "0" + ","+str(e)
			csvfile.write(str_csv+"\n")		
		


# ********* Scripts Starts here *********

for subdir, dirs, files in os.walk(code_dir):
	for dir_name in dirs:
		os.system("rm -rf "+code_dir + dir_name)

if(os.path.isfile(csv_sheet)):
	os.system("rm " + csv_sheet)

with open(csv_sheet, 'a') as csvfile:
	str_csv = "Roll No." + "," + "Name" + "," + "N=100 input" + "," + "N=100 runtime" + "," + "N=1000 input" + "," + "N=1000 runtime" + "," + "N=10000 input" + "," + "N=10000 runtime" + "," + "Total Marks" + "," + "Error (if any)" 
	csvfile.write(str_csv+"\n")		

if(os.path.exists(extract_dir)):
	os.system("rm -r " + extract_dir)

os.system("mkdir " + extract_dir)

unchecked=[]
for subdir, dirs, files in os.walk(code_dir):
	for rollno_file in files:
		
		fileinfo = rollno_file.split(".")
		if(fileinfo[-1]=="zip"):
			rollno_filename = rollno_file.rsplit(".",1)[0].split("_")[-1].strip()
			print rollno_filename + "$"
			print "unzip " + "'" + code_dir + rollno_file + "'" + " -d " + extract_dir + rollno_filename
			try:
				os.system("unzip " + "'" + code_dir +rollno_file + "'" + " -d " + extract_dir +rollno_filename)
				userEvaluate(rollno_filename)
			except:
				unchecked.append((rollno_filename,rollno_file))

		elif(fileinfo[-2]=="tar"):
			rollno_filename = (rollno_file.rsplit(".",2)[0].split("_"))[-1].strip()
			print rollno_filename+"$"
			print "tar -xvf " + "'" + code_dir + rollno_file + "'" + " -C " + extract_dir + rollno_filename
			try:
				os.system("mkdir "+ extract_dir + "/" + rollno_filename)
				os.system("tar -xvf " + "'" + code_dir + rollno_file + "'" + " -C " + extract_dir + rollno_filename)
				userEvaluate(rollno_filename)
			except:
				unchecked.append((rollno_filename,rollno_file))
			
		elif(fileinfo[-1]=="rar"):
			rollno_filename = (rollno_file.rsplit(".",1)[0].split("_"))[-1].strip()
			print rollno_filename+"$"
			print "unrar e -r -o- " + "'" + code_dir + rollno_file + "' " + extract_dir + rollno_filename
			try:
				os.system("mkdir "+ extract_dir + "/" + rollno_filename)
				os.system("unrar e -r -o- " + "'" + code_dir + rollno_file + "' " + extract_dir + rollno_filename)
				userEvaluate(rollno_filename)
			except:
				unchecked.append((rollno_filename,rollno_file))
		else:
			unchecked.append((rollno_filename,rollno_file))
# os.system("rm -r " + extract_dir)