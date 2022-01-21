#include <iostream>
#include <iomanip>
#include <fstream>
#include "reservoir_collection.h"

/**
passive TreeAtomic to wrap

Z matrix:

Keep m, beta, q & Q as internal state of Z matrix
Accepts requests to change terms by index then re-calculates Z

Reservoirs:
(d_i, C_i)

Continuous evolution of C via ode solver

Discrete changes to C: C += incr, C*= multipl, transfer(lam1, lam2, dimension), by index
*/
using namespace std;

//gsl_spmatrix *m, *beta, *q, *Q;
//gsl_spmatrix *Z_, *Z;


int main()
{
  Reservoirs res(5, 4);
  
  
  res.set_beta(1, 2, 0.05);
  res.set_beta(2, 3, 0.01);
  res.set_beta(2, 1, 0.02);
  res.set_m(2, 4, 0.001);
  
  res.set_Q(1, 0, .12);
  *res._C(0) = 1000;

  res.set_d(0, 1.0); //nominal dimension
  res.set_d(1, 1.0);
  res.set_d(2, 1.0);
  res.set_d(3, 1.0);
  res.set_d(4, 1.0); //nominal dimension

  ofstream timeout, filesout[5];

  
  timeout.open("time.out");
  filesout[1].open("Air_A.out");
  filesout[2].open("Air_B.out");
  filesout[3].open("Sur_X.out");
  filesout[4].open("Susc.out");
  
  timeout << setprecision(5);
  filesout[1] << setprecision(7);
  filesout[2] << setprecision(7);
  filesout[3] << setprecision(7);
  filesout[4] << setprecision(7);

  res.advance(5.0, 0.01, timeout, filesout);
  //Buonanno - voiced counting, standing
  //c_v * c_i * IR[activity_level] * 1e6 * NV[respiratory_activity]
  res.set_m(0, 1, 1e10 * 0.54 * 1e6 * 1.3863104870030406e-12);
  res.advance(10.0, 0.01, timeout, filesout);
  res.set_m(0, 1, 0.00);
  res.advance(10.0, 0.01, timeout, filesout);
  res.proportion_C(1, 2.0);
  res.advance(30.0, 0.01, timeout, filesout);
  res.transfer(1, 2, 0.0, 0.9, 0.2);
  res.advance(60.0, 0.01, timeout, filesout);
}
