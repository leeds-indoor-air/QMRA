#ifndef TREE_ATOM_H
#define TREE_ATOM_H

#include <limits>
#include <string>
#include <vector>
#include "adevs.h"
#include "debug.h"
#include "message.h"
#include "tree_component.h"


class TreeAtomic : public TreeComponent, public adevs::Atomic<Envelope>
{
public:
  TreeAtomic(const std::string& local_name);
  virtual ~TreeAtomic();
  
  void delta_int()=0;
  void delta_ext(double e, const adevs::Bag<Envelope>& xb)=0;
  void delta_conf(const adevs::Bag<Envelope>& xb)=0;
  void output_func(adevs::Bag<Envelope>& yb)=0;
  double ta()=0;
  void gc_output(adevs::Bag<Envelope>& g)=0;
};

#endif
