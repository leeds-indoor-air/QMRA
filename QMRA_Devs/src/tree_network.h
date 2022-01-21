#ifndef TREENET_H
#define TREENET_H

#include <string>
#include <map>
#include <exception>
#include <iostream>
#include "adevs.h"
#include "debug.h"
#include "message.h"
#include "tree_atomic.h"

class TreeNetwork : public TreeComponent, public adevs::Network<Envelope>
{
public:
  TreeNetwork(const std::string& local_name);
  TreeNetwork(const std::string& local_name, TreeNetwork* parent);
  virtual ~TreeNetwork();

  void getComponents(adevs::Set<adevs::Devs<Envelope>*>& c);
  
  virtual void route(const Envelope& value
		     ,adevs::Devs<Envelope>* model
		     ,adevs::Bag<adevs::Event<Envelope> >& r);

  void route_to_dest(const Envelope& value
		     ,adevs::Devs<Envelope>* model
		     ,adevs::Bag<adevs::Event<Envelope> >& r);

  void route_cascade_down(const Envelope& value
			  ,adevs::Devs<Envelope>* model
			  ,adevs::Bag<adevs::Event<Envelope> >& r);

  void addTreeComponent(adevs::Devs<Envelope>* comp);

  void constructTranslationTable(std::map<std::string, std::vector<relAddrType>>& table)
  {
    constructTranslationTable(table, getLocalName());
  }

  std::map<relAddrType, adevs::Devs<Envelope>*> routing_table;
  void constructTranslationTable(std::map<std::string, std::vector<relAddrType>>& table
				 ,const std::string& root);

  bool hdca(const std::vector<relAddrType>& addr);

};


#endif //TREENET_H

