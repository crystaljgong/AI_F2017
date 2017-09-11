#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cctype>
#include <iterator>


using namespace std;

int main () {
 
	string input="";
	getline(cin, input);

	istringstream iss(input);
	vector<string> results((istream_iterator<string>(iss)),
                                 istream_iterator<string>());

	

	if(results[0] == "Teach") {
		
		if(results[2] == "=") {
			//observeRootVar(results[1], results[3]);

		//} else if (results[2] == "->" && map.find(results[1]) == 'true') {
			//createNewRule(results[1], results[3]);

		} else {
			string s;
			vector<string>::iterator itr = results.begin();
			
			advance(itr, 4);
	
			
			while(itr != results.end()) {
				if(itr != results.end()-1) {
					s += *itr + " ";
				} else {
					s += *itr;
				}
				
				
				++itr;
			}
			cout<< s <<endl;
			

			//createNewVar(results[1], results[2], results[results.size()-1]);
		}

	} else if(results[0] == "List") {
		//List();

	} else if(results[0] == "Learn") {
		//Learn();

	} else if(results[0] == "Query") {
		//Query(results[1]);

	} else if(results[0] == "Why"){
		//Why(results[1]);
	} else {
		cout<<"Error"<<endl;
	}

  return 0;
}