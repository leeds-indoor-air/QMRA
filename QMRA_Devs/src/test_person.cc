#include <iostream>
#include "person.h"

using namespace std;
using namespace adevs;

ping::ping(
	   const vector<relAddrType>& destination
	   )
  :Message(destination)
{}

ping::~ping(){}

void ping::change_state(double e, Devs<Envelope>*) const
{}

Address a{0,0};

ping p1(a), p2(a), p3(a);

int main()
{

  Person harry("harry");

  harry.action_queue.push( {1.0, &p1} );
  harry.action_queue.push( {0.1, &p2} );

  cout << get<0>(harry.action_queue.top()) << endl;

  harry.action_queue.pop();

  cout << get<0>(harry.action_queue.top()) << endl;

  harry.action_queue.push( {0.8, &p3} );

  cout << get<0>(harry.action_queue.top()) << endl;
}
