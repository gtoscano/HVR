#include <iostream>
#include <stdexcept>
#include <stdio.h>
#include <string>
#include <vector>

using namespace std;

string exec(string command) {
   char buffer[128];
   string result = "";

   // Open pipe to file
   FILE* pipe = popen(command.c_str(), "r");
   if (!pipe) {
      return "popen failed!";
   }

   // read till end of process:
   while (!feof(pipe)) {

      // use buffer to read and add to result
      if (fgets(buffer, 128, pipe) != NULL)
         result += buffer;
   }

   pclose(pipe);
   return result;
}

int main() {
    string s = exec("./wfg -q pop_sample.txt 1.1 1.1 1.1 1.1 1.1 1.1 1.1 1.1");
    std::string delimiter = " ";
    std::vector<double> fx;    
    size_t pos = 0;
    std::string token;
    while ((pos = s.find(delimiter)) != std::string::npos) {
        token = s.substr(0, pos);
	fx.emplace_back(stof(token));
        s.erase(0, pos + delimiter.length());
    }
    fx.emplace_back(stof(s));
    for ( auto &val : fx) {
	    std::cout<<val<<"\n";
    }
}

