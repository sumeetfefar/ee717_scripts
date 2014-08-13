import re
import os
import difflib
import csv

code_dir = "./Codes/"
extract_dir = "./Extract/"
refpath = "./Reference/"
csv_sheet = "Result.csv"

IOfiles = [("input100.txt","output100.txt"),("input1000.txt","output1000.txt"),("input10000.txt","output10000.txt")]
permanent_dirs = ["Reference","Answers"]


def CPP_correct(inputfile,outputfile):
	with open(inputfile, "r") as infile, open(outputfile, "w") as outfile:
		for line in infile:
			ms_to_us = re.findall('(.*?)(?=double runtime \= \(end \- start\)\/\(double\)\(CLOCKS_PER_SEC\/1000\)\;)', line)
			if ms_to_us != []:
				tmp = re.split('double runtime \= \(end \- start\)\/\(double\)\(CLOCKS_PER_SEC\/1000\)\;', line)
				# print tmp
				outfile.write(tmp[0]+"double runtime = (end - start)/(double)(CLOCKS_PER_SEC/1000000);" + tmp[1])
			else:
				outfile.write(line)

			if re.search('(?<=int main \(void\))', line) != None:
				break
		outfile.write("{\n")
		for i in IOfiles:
			outfile.write("\tinsertionSort(\""+i[0]+"\",\""+i[1]+"\");\n")	
		# outfile.write("\tinsertionSort(\"input100.txt\",\"output100.txt\");\n")
		# outfile.write("\tinsertionSort(\"input1000.txt\",\"output1000.txt\");\n")
		# outfile.write("\tinsertionSort(\"input10000.txt\",\"output10000.txt\");\n")
		outfile.write("\treturn 0;\n")
		outfile.write("}\n")
	os.system("mv -f " + outputfile + " " + inputfile)


def CheckCorrect(filepath):
	for subdir, dirs, files in os.walk("./Answers"):
		score = {}
		for answer_file in files:
			diff = difflib.SequenceMatcher(None, open(filepath+answer_file).readlines(), open("./Answers/"+answer_file).readlines())
			diff.get_matching_blocks()
			with open("./Answers/"+answer_file,"r") as ans_file:
				N = int(ans_file.readline().strip())
			with open(filepath+answer_file,"r") as ans_file:
				runtime = int(ans_file.readline().strip()) # Runtime in microseconds
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
		with open(filepath+"README.txt","r") as ans_file:
			(rollno, Name) = ans_file.readline().split(" ",1)
			(rollno, Name) = (rollno.strip(), Name.strip())
			# print Name, rollno

		with open(csv_sheet, 'a') as csvfile:
			str_csv = rollno +","+Name
			for i in ["input100","input1000","input10000"]:
				str_csv = str_csv +","+ str(score[i][1]/score[i][0]*10) +","+str(score[i][2])
			csvfile.write(str_csv+"\n")

def userEvaluate(rollno_file):
	fileinfo = rollno_file.split(".")
	rollno = fileinfo[0]
	filepath = extract_dir+fileinfo[0]+"/"
	original_dir = os.getcwd()
	try:
		os.system("cp " + refpath + "* " + filepath)
		os.chdir(filepath)
		CPP_correct("insertion_sort.cpp", "insertion_sort.cpp.tmp")
		os.system("make")
		os.system("./insertion_sort")
		os.chdir(original_dir)
		CheckCorrect(filepath)
	except Exception, e: print "Error : " + rollno + " | " + str(e)
		


# ********* Scripts Starts here *********

for subdir, dirs, files in os.walk(code_dir):
	for dir_name in dirs:
		os.system("rm -rf "+code_dir + dir_name)

if(os.path.isfile(csv_sheet)):
	os.system("rm " + csv_sheet)		
if(os.path.exists(extract_dir)):
	os.system("rm -r " + extract_dir)

os.system("mkdir " + extract_dir)


for subdir, dirs, files in os.walk(code_dir):
	for rollno_file in files:
		print rollno_file
		fileinfo = rollno_file.split(".")
		if(fileinfo[1]=="zip"):
			os.system("unzip " + code_dir +rollno_file + " -d " + extract_dir)
			userEvaluate(rollno_file)
		elif(fileinfo[1]=="tar"):
			os.system("tar -xvf " + code_dir +rollno_file + " -C " + extract_dir)
			userEvaluate(rollno_file)

os.system("rm -r " + extract_dir)