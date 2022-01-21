#include "debug.h"
#include "message.h"
#include "toy.h"

using namespace std;
using namespace adevs;

ping::ping(const std::vector<relAddrType>& destination)
  :Message{destination}
{

#ifdef MESSAGE__DEBUG
  cout << "ping constructor called" << endl;
#endif
}

ping::~ping()
{
#ifdef MESSAGE__DEBUG
  cout << "ping destructor called" << endl;
#endif
}

void ping::change_state(double e, Devs<Envelope>* model) const
{
  Toy *ty = dynamic_cast<Toy*>(model);
  ty->received = true;
}
