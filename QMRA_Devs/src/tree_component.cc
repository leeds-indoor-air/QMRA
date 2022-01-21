#include "tree_component.h"

using namespace std;

TreeComponent::TreeComponent(const std::string& local_name)
  :local_name{local_name}{}

TreeComponent::~TreeComponent(){}

void TreeComponent::setAbsoluteAddress(const TreeComponent& parent_addr, relAddrType local_address)
{
  absolute_address = parent_addr.absolute_address;
  absolute_address.insert(absolute_address.end(), local_address);
  absolute_address.shrink_to_fit();
}


ostream& TreeComponent::printAbsoluteAddress(ostream& os) const
{
  vector<relAddrType>::const_iterator it{absolute_address.cbegin()};

  while(it != absolute_address.cend()) os << *(it++) << ",";

  return os;
}

//void panic(const string& s){ cout << "Panic! " << s << endl; exit(1); }

