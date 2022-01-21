#ifndef TREE_ADDR_H
#define TREE_ADDR_H

#include <vector>
#include <string>
#include <iostream>
#include "debug.h"

/* Impl...
  1. absolute_address = {} => not connected
*/

/**
 * \defgroup tree Tree addressing
 */
class TreeComponent
{
public:
  TreeComponent(const std::string& local_name);
  ~TreeComponent();
  
  const std::string& getLocalName() const {return local_name;}
  const std::vector<relAddrType>& getAbsoluteAddress() const {return absolute_address;}
  std::ostream& printAbsoluteAddress(std::ostream& os) const;
  void setAbsoluteAddress(const TreeComponent& parent_addr, relAddrType local_address);
  
private:
  std::string local_name;
  std::vector<relAddrType> absolute_address;
};


#endif //TREE_MODEL_H


