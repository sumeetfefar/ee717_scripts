import re
import os


with open("insertion_sort.cpp", "r") as infile, open("insertion_sort.cpp.tmp", "w") as outfile:
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
	outfile.write("\tinsertionSort(\"input100.txt\",\"output100.txt\");\n")
	outfile.write("\tinsertionSort(\"input1000.txt\",\"output1000.txt\");\n")
	outfile.write("\tinsertionSort(\"input10000.txt\",\"output10000.txt\");\n")
	outfile.write("\treturn 0;\n")
	outfile.write("}\n")

os.system("mv -f insertion_sort.cpp.tmp insertion_sort.cpp")

