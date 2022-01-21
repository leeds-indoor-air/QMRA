#include <exception>
#include <iostream>
#include "debug.h"

using namespace std;

void panic(const string& s)
{
  cout << "\nPanic!\n" << s << endl;
  terminate();
}
