#include <iostream>
#include <iomanip>
#include <fstream>
#include <deque>
#include <functional>
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

int main()
{
  Reservoirs res{"inputs/NoakesSleighF/C.in"
    ,"inputs/NoakesSleighF/d.in"
    ,"inputs/NoakesSleighF/m.in"
    ,"inputs/NoakesSleighF/beta.in"
    ,"inputs/NoakesSleighF/Q.in", 13};

  /*
  cout << endl;
  cout << "C vector:" << endl;
  gsl_vector_fprintf(stdout, res.C, "%.2f");

  cout << endl;
  cout << "d vector:" << endl;
  gsl_vector_fprintf(stdout, res.d, "%.2f");

  cout << endl;
  cout << "d_inv vector:" << endl;
  gsl_vector_fprintf(stdout, res.d_inv, "%.2f");

  cout << endl;
  cout << "m matrix:" << endl;
  gsl_spmatrix_fprintf(stdout, res.m, "%.2f");
  */
  cout << endl;
  cout << "beta matrix:" << endl;
  gsl_spmatrix_fprintf(stdout, res.beta, "%.2f");

  /*
  cout << endl;
  cout << "Q matrix:" << endl;
  gsl_spmatrix_fprintf(stdout, res.Q, "%.2f");

  cout << endl;
  cout << "Z_ matrix:" << endl;
  gsl_spmatrix_fprintf(stdout, res.Z_, "%.2f");
  */
  cout << endl;
  cout << "Z matrix:" << endl;
  gsl_spmatrix_fprintf(stdout, res.Z, "%.2f");
  
  ofstream timeout, filesout[19];
  
  timeout.open("outputs/time.out");
  filesout[0].open("outputs/1a.out"); //1
  filesout[1].open("outputs/1b.out"); 
  filesout[2].open("outputs/c1.out"); //3
  filesout[3].open("outputs/2a.out");
  filesout[4].open("outputs/2b.out"); //5
  filesout[5].open("outputs/c2.out");
  filesout[6].open("outputs/3a.out"); //7
  filesout[7].open("outputs/3b.out");
  filesout[8].open("outputs/c3.out"); //9
  filesout[9].open("outputs/exposure_1a.out"); //10
  filesout[10].open("outputs/exposure_1b.out"); //11
  filesout[11].open("outputs/exposure_2a.out"); //12
  filesout[12].open("outputs/infector_2b.out"); //12



  timeout << setprecision(5);
  filesout[1] << setprecision(7);
  filesout[2] << setprecision(7);

  res.set_m(12, 5, 1.0);
  res.advance(60.0, 0.01, timeout, filesout);

}
