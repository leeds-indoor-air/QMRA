#ifndef MESSAGE_H
#define MESSAGE_H

#include <string>
#include <stdlib.h>
#include <vector>
#include "adevs.h"
#include "debug.h"

struct TreeAddress
{
  /* address is loaded in back-to-front for ease of popping by route method */
  TreeAddress(const Address& addr, bool relative)
    :address{std::vector<relAddrType>{}}
    ,address_is_relative{relative}
  {
    std::vector<relAddrType>::const_reverse_iterator rit, ritend;
    for(rit = addr.crbegin(), ritend = addr.crend(); rit != ritend; ++rit)
      address.push_back(*rit);
  }
  Address address;
  bool address_is_relative;
};

struct Message;

typedef Message* Envelope;

struct Message : TreeAddress
{
  Message(const Address& destination)
    :TreeAddress{destination, false}{}
  virtual void change_state(double e, adevs::Devs<Envelope>*) const=0;
  virtual ~Message(){};
};

struct ping : Message
{
  double payload;

  ping(const std::vector<relAddrType>& destination);
  void change_state(double e, adevs::Devs<Envelope>*) const;
  ~ping();
};

#endif //MESSAGE_H
