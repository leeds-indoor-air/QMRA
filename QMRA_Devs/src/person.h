#ifndef PERSON_H
#define PERSON_H

#include <queue>
#include "adevs.h"
#include "debug.h"
#include "message.h"
#include "tree_atomic.h"

  
class Person : public TreeAtomic
{
 public:
  Person(const std::string& local_name);
  ~Person();
  
  void delta_int();
  void delta_ext(double e, const adevs::Bag<Envelope>& xb);
  void delta_conf(const adevs::Bag<Envelope>& xb);
  void output_func(adevs::Bag<Envelope>& yb);
  double ta();
  void gc_output(adevs::Bag<Envelope>& g);

  double time;
  
  typedef std::pair<double, Envelope> Action;
  std::priority_queue< Action, std::vector<Action>, std::greater<Action>> action_queue;

  void (*cough)();
};


#endif //PERSON_H
