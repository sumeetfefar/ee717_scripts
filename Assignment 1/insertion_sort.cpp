#include<iostream>
#include<string>
#include<fstream>
#include<ctime>
using namespace std;

// Read data from inputfile, perform Insertion Sort and wirte back result & runtime(milliseconds) into outputfile
void insertionSort(string inputfile, string outputfile){
	
	// Read Data from inputfile
	ifstream infile(inputfile.c_str());
	
	int N;
	infile>>N; // N = size of Array
	
	int inputArray[N], outputArray[N];
	for(int i=0; i<N; i++){
		infile>>inputArray[i];
	}
	
	// Record time before algorithm execution
	clock_t start,end;
	start = clock();
	
	
	// Insertion Sort Algorithm
	/*
	
		INSERT YOUR ALGORITHM CODE HERE
		* Input Array = inputArray
		* Output Array = outputArray
		* 
		* Run Insertion Sort Algorithm on 'inputArray' and store resultant sorted array in 'outputArray'
	
	*/
	
	
	// Record time after algorithm execution, and calculate time elapsed
	end = clock();
	double runtime = (end - start)/(double)(CLOCKS_PER_SEC/1000); //Runt time of algorithm in "Milliseconds"
	
	// Write runtime & Result(Sorted Array) into outputfile
	ofstream outfile(outputfile.c_str());
	outfile<<runtime<<endl;
	for(int i=0; i<N; i++){
		outfile<<outputArray[i]<<endl;
	}
}


main(){
	insertionSort("input100.txt","output100.txt");
	insertionSort("input1000.txt","output1000.txt");
	insertionSort("input10000.txt","output10000.txt");	
}



