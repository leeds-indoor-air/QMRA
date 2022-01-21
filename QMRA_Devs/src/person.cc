#include "person.h"

using namespace std;
using namespace adevs;

Person::Person(const string& local_name)
  :TreeAtomic{local_name}
  ,time{0.0}
  ,action_queue{}
  {}

Person::~Person(){}

void Person::delta_int(){}
void Person::delta_ext(double e, const Bag<Envelope>& xb){}
void Person::delta_conf(const adevs::Bag<Envelope>& xb){}
void Person::output_func(adevs::Bag<Envelope>& yb){}
double Person::ta(){return DBL_MAX;}
void Person::gc_output(adevs::Bag<Envelope>& g){}




