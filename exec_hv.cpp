//g++ exec_hv.cpp -std=c++17 -lfmt -o exec_hv
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <fmt/core.h>


namespace fs = std::filesystem;
std::string getEnvVar( std::string const & key , std::string default_val)
{
    char * val = std::getenv( key.c_str() );
    return val == NULL ? default_val : std::string(val);
}

std::string exec_command(std::string command) {
   char buffer[128];
   std::string result = "";

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

std::string nadir_point(int nobjs) {
    std::string result;
    for (int i = 0; i < nobjs; ++i) {
        result += "1.1";
        if (i < nobjs - 1) {
            result += " ";
        }
    }
    return result;
}

double compute_hv(std::string filename, int nobjs) {
    std::vector<double> hv(2,0.0);    
    std::string WFG_PATH = getEnvVar("OPT4CAST_WFG_PATH", "./wfg");
    std::string nadir = nadir_point(nobjs);
    std::string s = exec_command(fmt::format("{} -q {} {}", WFG_PATH, filename, nadir));
    std::string delimiter = " ";
    size_t pos = 0;
    std::string token;
    int i =0;

    while ((pos = s.find(delimiter)) != std::string::npos) {
        token = s.substr(0, pos);
        hv[i]= stof(token);
        ++i;
        s.erase(0, pos + delimiter.length());
    }
    hv[i] = stof(s);

    return hv[0];
}


int main(int argc, char **argv) {
  int nobjs = 2;

  if (argc < 3 || argc > 3) {
    std::cerr<<fmt::format("Use: {} normalized_pareto_front number_of_objectives\n", argv[0]);
    exit(1);
  }
  nobjs = std::stoi(argv[2]);

  std::string filename = argv[1];

  if (!fs::exists(filename)) {
    std::cerr<<fmt::format("File:  does not exist\n", argv[1]);
    exit(1);
  }

  std::cout<<compute_hv(filename, nobjs) <<std::endl;
  return 0;

}
