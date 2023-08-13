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

double compute_hv(std::string filename) {
    std::vector<double> hv(3, 0.0);    
    std::string WFG_PATH = getEnvVar("OPT4CAST_WFG_PATH", "./wfg");
    std::string s = exec_command(fmt::format("{} -q {} 1.1 1.1 1.1", WFG_PATH, filename));
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

    //std::cout<<"current hv: "<<current_hv[0]<<" raw hv: "<<hv_raw_pf<<std::endl;
    //if (hv_raw_pf * (1.0-pct_hv_to_exit) < current_hv[0] ){
    //    return true;
    //}
    return hv[0];
}


int main(int argc, char **argv) {
  std::vector<double> min(3, 0.0);    
  std::vector<double> max(3, 1.0);    

  if (argc < 2) {
    std::cerr<<fmt::format("Use: {} normalized_pareto_front\n", argv[0]);
    exit(1);
  }

  if (argc > 6) {
    min[0] = std::stoi(argv[3]);
    min[1] = std::stoi(argv[4]);
    max[0] = std::stoi(argv[5]);
    max[1] = std::stoi(argv[6]);
  }

  std::string filename = argv[1];

  if (!fs::exists(filename)) {
    std::cerr<<fmt::format("File:  does not exist\n", argv[1]);
    exit(1);
  }

  std::cout<<compute_hv(filename) <<std::endl;
    //printf("\n Enter the Raw HV of the Pareto front: ");
    //scanf("%lf", &hv_raw_pf);
    //printf("\n Enter the PCT HV to Exit: ");
    //scanf("%lf", &pct_hv_to_exit);
  return 0;

}
