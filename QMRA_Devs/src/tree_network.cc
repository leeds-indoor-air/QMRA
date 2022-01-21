#include "tree_network.h"

using namespace std;
using namespace adevs;

TreeNetwork::TreeNetwork(const std::string& name)
  :Network<Envelope>{}
  ,TreeComponent{name}
  ,routing_table{map<relAddrType, adevs::Devs<Envelope>*>{}}
{}

TreeNetwork::TreeNetwork(const std::string& name, TreeNetwork* parent)
  :Network<Envelope>{}
  ,TreeComponent{name}
  ,routing_table{map<relAddrType, adevs::Devs<Envelope>*>{}}
{
  parent->addTreeComponent(this);
}
   
TreeNetwork::~TreeNetwork()
{}

void TreeNetwork::getComponents(Set<Devs<Envelope>*>& c)
{
  map<relAddrType, adevs::Devs<Envelope>*>::const_iterator it{routing_table.cbegin()}, itend{routing_table.cend()};

  for(; it != itend; ++it) c.insert(it->second);
}

void TreeNetwork::addTreeComponent(Devs<Envelope>* comp)
{
  if(TreeComponent *tc = dynamic_cast<TreeComponent*>(comp))
    {
      relAddrType l = routing_table.size();
      
      routing_table.insert( {l, comp} );
      comp->setParent(this);
      tc->setAbsoluteAddress(*this, l);
    }
  else;//otherwise either complain or ignore, haven't decided.
}


void TreeNetwork::constructTranslationTable(map<string, vector<relAddrType>>& table
					    , const string& root)

{
  table.insert( {root, {}} );
  TreeComponent *tcp;
  auto it = routing_table.cbegin(), itend = routing_table.cend();
  for(; it != itend; ++it)
    {
      if(tcp = dynamic_cast<TreeComponent*>(it->second))
	{
	  table.insert( {root + tcp->getLocalName()
	      ,tcp->getAbsoluteAddress()} );
	  if(TreeNetwork *tnp = dynamic_cast<TreeNetwork*>(it->second))
	    tnp->constructTranslationTable(table, root + tcp->getLocalName());
	}
    }
}


void TreeNetwork::route(const Envelope& value
			,Devs<Envelope>* model
			,Bag<Event<Envelope> >& r)
{
  if( value->address[0] == INT16_MAX ) route_cascade_down(value, model, r);
  else route_to_dest(value, model, r);
}

void TreeNetwork::route_cascade_down(const Envelope& value
				     ,Devs<Envelope>* model
				     ,Bag<Event<Envelope> >& r)
{
  map<relAddrType, Devs<Envelope>*>::const_iterator it{routing_table.cbegin()}, itend{routing_table.cend()};
  if(model == this->getParent())
    {
      for(; it != itend; ++it)
	{
	  Event<Envelope> ev{it->second, value};
	  r.insert(ev);
	}
    }
  else
    {
      for(; it != itend; ++it)
	{
	  if(it->second == this) continue;
	  Event<Envelope> ev{it->second, value};
	  r.insert(ev);
	}
      
    }
}

void TreeNetwork::route_to_dest(const Envelope& value
				,Devs<Envelope>* model
				,Bag<Event<Envelope> >& r)
{
  /*
    value = either absolute destination address, e.g., "/A/B/C/D"
    or relative address, e.g., "C/D"
  */

  /* We change value's innards (its std::string)*/
  //string s, *dest = static_cast<string*>(value); //pntr->Message ----> pntr->std::string
  relAddrType s;
  TreeAddress *dest = static_cast<TreeAddress*>(value);
  Devs<Envelope>* m;
  Event<Envelope> ev;

/*
  are we still seeking HDCA?
  i.e. does destination begin with '/'?
*/
#ifdef TREE_NET__DEBUG  
  cout << "\nTop of route_to_dest.\n"
       << "Current node: ";
  for(relAddrType r : getAbsoluteAddress()) cout << r << ",";
  cout << " (" << getLocalName() << ")" << endl;

#endif
  if( !value->address_is_relative ) //yes
    {
#ifdef TREE_NET__DEBUG
      cout << "Destination is absolute" << endl;
#endif
      /* 
	 is this node the HDCA? - i.e. is node address an initial substring of destination?
      */
      if( !hdca(dest->address) )//no, pass upwards?
	{
#ifdef TREE_NET__DEBUG
	  cout << "not HDCA" << endl;
#endif
	  m = this->getParent();
	  ev.model = m;
	  ev.value = value;
	  r.insert(ev);
	  return;
        }
      else
	{
	  dest->address_is_relative = true;
	  for(size_t i{0}; i < getAbsoluteAddress().size(); ++i) dest->address.pop_back();
#ifdef TREE_NET__DEBUG
	  cout << "Current node address ";
	  for( relAddrType r : getAbsoluteAddress() ) cout << r << ",";
	  cout << " (" << getLocalName() << ")";
	  cout << " is HDCA.  New destination addr: ";
	  for( relAddrType r : dest->address ) cout << r << ",";
	  cout << endl;
#endif
	}
    }
  
  //we've now found HDCA and we just pass downwards using relative address
#ifdef TREE_NET__DEBUG
  cout << "Destination is relative" << endl;
#endif
  /*
    Put initial segment of dest up to and including first '/'
    (or whole string if there is no '/') into s, leaving 
    remainder in dest
  */
  
  s = dest->address.back();
  dest->address.pop_back();
  
#ifdef TREE_NET__DEBUG
  cout << "s: " << s << " dest: ";
  for( relAddrType r : dest->address ) cout << r << ",";
	  cout << endl;
#endif
  
  map<relAddrType,Devs<Envelope>*>::iterator it = routing_table.find(s);
  
  if(it == routing_table.end()) {cout << "panic!" << endl; terminate();} //not there? For now, panic!
  else m = it->second;
  
  ev.model = m;
  ev.value = value;
  r.insert(ev);
  return;
}

bool TreeNetwork::hdca(const vector<relAddrType>& addr)
{
  size_t i{0};
  
  if( getAbsoluteAddress().size() > addr.size() ) return false;
  else
    {     
      while( i < getAbsoluteAddress().size() )
	{
	  if( getAbsoluteAddress()[i] == addr[i] ) ++i;
	  else return false;
	}
      return true;
    }
}
