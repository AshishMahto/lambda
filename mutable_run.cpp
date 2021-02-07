#include <iostream>
#include <vector>
#include <assert.h>
#include <fstream>
#include <string>

using namespace std;

vector<int> stackTrace = {};

void run(string inp) {
vector<int> instrs{6,2,5,0,6,2,0,6,2,1,6,11,0,6,2,1,6,11,0,6,2,1,8,5,6,2,5,6,2,1,8,5,5,5,1,8,5,5,5,6,5,6,6,2,1,6,10,9,6,2,0,6,2,0,1,6,11,0,6,2,1,6,11,0,6,2,1,8,5,6,2,5,6,2,1,8,5,5,6,2,5,1,8,5,5,5,6,5,6,6,2,1,6,10,9,6,2,0,6,2,0,5,1,6,2,1,11,6,2,0,6,2,1,6,2,1,6,2,6,0,6,2,5,8,5,5,6,2,5,6,2,1,6,2,1,6,10,9,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,5,6,2,1,6,2,1,6,2,1,10,10,6,6,2,6,0,6,2,5,6,2,1,6,2,0,6,2,1,6,2,0,6,2,0,6,2,1,10,6,6,2,6,0,6,2,5,6,0,6,2,5,6,2,1,10,0,6,2,1,6,11,0,1,8,5,5,6,2,5,6,2,1,6,2,1,6,10,9,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,7,6,6,2,6,0,6,2,5,8,5,6,2,5,6,2,6,0,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,3,5,6,0,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,0,6,2,6,3,-1};

 // for literals
vector<int> lits{4,0,232,0,1,0,0,19,0,0,1,0,0,1,0,0,1,0,0,19,0,0,0,4,1,0,8,1,0,0,0,2,9,383,0,0,2,2,3,0,2,1,18,0,0,362,0,0,1,0,0,19,0,0,0,1,0,0,1,0,0,1,0,0,19,0,0,0,4,1,0,10,1,0,0,0,2,9,19,0,383,0,0,2,2,3,0,2,1,18,0,0,315,0,0,1,0,0,19,0,0,9,0,1,0,0,0,19,0,0,1,0,0,19,0,0,2,0,123,0,1,0,335,0,2,4,18,0,383,18,0,0,19,0,0,272,0,0,0,1,0,42,0,1,0,24,0,1,0,13,0,1,0,0,0,57,17,0,0,1,0,0,1,0,0,0,0,128,2,0,175,0,1,0,330,17,0,0,19,0,0,2,0,0,19,0,0,1,0,0,18,0,0,0,128,4,0,202,0,1,0,303,207,0,1,0,206,19,0,0,0,0,16,0,0,1,0,0,0,0,2,4,4,0,341,4,0,0,15,0,0,176,0,0,43,1,54,4,35,7,31,10,78,13,116,16,32,19,28,22,1,25,47,28,84,31,25,34,26,37,123,40,69,43,102,46,50,49,65,52,21,55,16,17,0,280,0,1,0,268,0,4,19,0,84,19,0,0,0,78,0,1,0,111,0,1,0,32,0,1,0,115,0,1,0,105,0,1,0,99,0,1,0,101,0,1,0,32,0,1,0,102,0,1,0,111,0,1,0,114,0,1,0,32,0,1,0,121,0,1,0,111,0,1,0,117,0,1,0,32,0,1,0,58,0,1,0,40,0,1,0,0,0,1,0,19,0,41,0,0,67,0,1,0,111,0,1,0,114,0,1,0,114,0,1,0,101,0,1,0,99,0,1,0,116,0,1,0,33,0,1,0,0,0,1,0,9,0,0};

vector<int> flag{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

vector<int> box {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

  box.insert(box.end(), inp.rbegin(), inp.rend());

  int sz = instrs.size();

  int flagPtr = 0;

  for (int instrPtr = 0; instrs[instrPtr] != -1;) {
    int i = instrs[instrPtr];

    if (instrPtr == -1) {
      cout << "dat = " << lits[instrPtr] << endl << endl;

      cout << "flag = ";
      for (auto e : flag) cout << e << ",";
      cout << endl << endl;

      cout << "box  = ";
      for (auto e : box) cout << e << ",";
      cout << endl << endl << endl;
    }

    if (i == 0) {
      flag[flagPtr] = box.back();
      box.pop_back();

    } else if (i == 1) {
      box.push_back(flag[flagPtr]);

    } else if (i == 2) {
      flagPtr -= box.back();
      while (flagPtr < 0) flagPtr += 20;
      flagPtr = flagPtr % 20;
      box.pop_back();

    } else if (i == 3) {
      flagPtr = (flagPtr + box.back()) % 20;
      box.pop_back();

    } else if (i == 4) {
      instrPtr -= lits[instrPtr] + 1;

    } else if (i == 5) {
      instrPtr += lits[instrPtr] - 1;

    } else if (i == 6) {
      box.push_back(lits[instrPtr]);

    } else if (i == 7) {
      int j = -1 - lits[instrPtr];
      while (j < 0) j += box.size();
      box.push_back(box[j % box.size()]);

    } else if (i == 8) {
      if (box.back() == 0) ++instrPtr;
      box.pop_back();

    } else if (i == 9) {
      instrPtr += box.back() - 1;
      box.pop_back();

    } else if (i == 10) {
      int smol = box.back();
      box.pop_back();
      int big = box.back();
      box.pop_back();
      box.push_back(big + smol);

    } else if (i == 11) {
      int smol = box.back();
      box.pop_back();
      int big = box.back();
      box.pop_back();
      box.push_back(big - smol);
    }

    ++instrPtr;
    while (instrPtr < 0) instrPtr += instrs.size();
    instrPtr = instrPtr % instrs.size();
  }

  for (int j = 0; j < 20; ++j) {
    cout << char(flag[(flag.size() + flagPtr - j) % 20]);
  }
}

int main() {
  string inp = "y";
  run(inp);
  return 0;
}
