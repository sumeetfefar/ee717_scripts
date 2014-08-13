#include<iostream>
#include<string>
#include<fstream>
#include<sstream>
#include<stdlib.h>
using namespace std;

void randArray(int N){
	ostringstream convert; 
	convert << N;
	
	
	ofstream outfile(("input"+convert.str()+".txt").c_str());
	outfile<<N<<endl;
	int randomNumber;
	for(int i=0; i<N; i++){	
		outfile<<rand()<<endl;
	}
}


main(){
	randArray(100);
	randArray(1000);
	randArray(10000);

	
}




