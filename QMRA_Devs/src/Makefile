gsl_incl=/home/cenlb/anaconda3/envs/doxygen/include/
gsl_lib=/home/cenlb/anaconda3/envs/doxygen/lib/
adevs_incl=../include/adevs-3.3/

all : test_person moving_infector static_infector

moving_infector : reservoir_collection.o moving_infector.o
	g++ -o ../moving_infector reservoir_collection.o moving_infector.o -lgsl -lgslcblas -L$(gsl_lib)

static_infector : reservoir_collection.o static_infector.o
	g++ -o ../static_infector reservoir_collection.o static_infector.o -lgsl -lgslcblas -L$(gsl_lib)

test_person : test_person.o person.o tree_atomic.o tree_component.o
	g++ -o ../test_person test_person.o person.o tree_atomic.o tree_component.o

moving_infector.o : moving_infector.cc reservoir_collection.h
	g++ -std=c++11 -c moving_infector.cc -I$(gsl_incl)

static_infector.o : static_infector.cc reservoir_collection.h
	g++ -std=c++11 -c static_infector.cc -I$(gsl_incl)

test_person.o : test_person.cc person.h
	g++ -std=c++11 -c test_person.cc -I$(adevs_incl)

reservoir_collection.o : reservoir_collection.cc reservoir_collection.h
	g++ -std=c++11 -c reservoir_collection.cc -I$(gsl_incl)

person.o : person.cc person.h debug.h message.h tree_atomic.h
	g++ -std=c++11 -c person.cc -I$(adevs_incl)

tree_atomic.o : tree_atomic.cc tree_atomic.h debug.h message.h tree_component.h
	g++ -std=c++11 -c tree_atomic.cc -I$(adevs_incl)

tree_component.o : tree_component.cc tree_component.h debug.h
	g++ -std=c++11 -c tree_component.cc -I$(adevs_incl)

clean :
	rm -f *.o *~
	rm -f ../moving_infector ../static_infector



#test_reservoirs : reservoir_collection.o test_reservoirs.o
#	g++ -o ../test_reservoirs reservoir_collection.o test_reservoirs.o -lgsl -lgslcblas -L$(gsl_lib)

#test_reservoirs.o : test_reservoirs.cc reservoir_collection.h
#	g++ -std=c++11 -c test_reservoirs.cc -I$(gsl_incl)

