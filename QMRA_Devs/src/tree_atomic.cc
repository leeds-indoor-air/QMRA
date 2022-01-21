#include "tree_atomic.h"

using namespace std;
using namespace adevs;

TreeAtomic::TreeAtomic(const std::string& n)
  :TreeComponent{n}
  ,Atomic<Envelope>{}
{}

TreeAtomic::~TreeAtomic()
{}
