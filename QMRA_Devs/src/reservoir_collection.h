#include <cstddef>
#include <fstream>
#include <algorithm>
#include <gsl/gsl_spmatrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_spblas.h>
#include <gsl/gsl_odeiv2.h>


//Convention: col 0 = ventilation, col 1 = decay

int f(double t, const double y[], double dydt[], void * params);

/**
 * \defgroup reservoir Reservoirs
 * 
 * \f[ d_i \frac{dC_i}{dt} = \sum_{j \neq i}^n m_{ji} C_j + \sum_{j \neq i}^n \beta_{ji} C_j - \sum_{k \neq i}^n \beta_{ik} C_i - Q_i C_i - \gamma_i C_i  \f]
 *
 * where
 *
 * 1. \f$ \mathbf{d} = (d_1, \ldots, d_n)\f$ are the <B> resservoir dimensions </B> (volumes or areas).  ''Reservoirs'' such as pulmonary and mucous membrane exposures, will have nominal dimension 1 unit.
 * 2. \f$ \mathbf{C} = (C_1, \ldots, C_n)\f$ are <B> concentrations </B> (pathogen units / unit area or volume).  For an infector, this is <B>viral load</B>, i.e., pathogen units per unit volume of resp. fluid, for an air zone, pathogen units per unit volume of air, for a surface, pathogen units per unit area, etc.
 * 3. \f$ (m_{ij}) \f$ is the <B> source matrix </B>.  E.g., infector \f$i\f$ breathing into an air zone \f$j\f$ with \f$m_{ij}\f$ being the <B>volume of resp.fluid exhaled by infector, per unit time</B> and \f$C_i\f$ is the <B>viral load</B> in pathogen units per volume.  Another example, a susceptible person\f$j\f$ is exposed to air in zone \f$ i\f$ and \f$m_{ij}\f$ is their <B>pulmonary rate</B>
 * 4. \f$ (\beta_{ij}) \f$ is the <B> mixing matrix </B> whose terms are the volume rates of mixing between reservoirs.  E.g., air mixing between zones and droplet deposition from air onto surfaces
 * 5. \f$Q_i\f$ and \f$\gamma_i\f$ are <B> sink terms </B>, resp. rates of ventilation and pathogen decay from reservoir \f$i\f$.
 *
 * I.e., \f[ \frac{d\mathbf{C}}{dt} = D^{-1} X \mathbf{C} \f]
 *
 * where \f$D = \text{diag}(d_1, \ldots, d_n)\f$ and
 *
 * \f[ X_{ij} = \left\{ \begin{array}{rl} \beta_{ji} + m_{ji} &i \neq j\\ -\sum_{k \neq i} \beta_{ik} - Q_i - \gamma_i & i = j\\ \end{array} \right. \f]
 */
struct Reservoirs
{

  /**
   * When using this constructor, d must be set first
   */
  Reservoirs(std::size_t n
	     ,std::size_t nzmax);

  Reservoirs(const char *C_in
	     ,const char *d_in
	     ,const char *m_in
	     ,const char *beta_in
	     ,const char *Q_in
	     ,std::size_t dimension);
  
  ~Reservoirs();

  double current_time;
  
  gsl_spmatrix *m, *beta, *Q, *Z_, *Z;
  gsl_vector *C, *d, *d_inv;

  gsl_odeiv2_system sys;
  gsl_odeiv2_driver *dri;

  void set_m(std::size_t i, std::size_t j, double val );
  void set_beta(std::size_t i, std::size_t j, double val );
  void set_Q(std::size_t i, std::size_t j, double val );

  double* _C(std::size_t i);
  const double* _C(std::size_t i) const;

  void set_d(std::size_t i, double val );

  double get_m(std::size_t i, std::size_t j) const;
  double get_beta(std::size_t i, std::size_t j) const;
  double get_Q(std::size_t i, std::size_t j) const;

  double get_d(std::size_t i) const;

  void calculate_Z();

  void advance(double t, double delta_t, std::ofstream& timeout, std::ofstream *fileouts);
  void advance(double t, std::ofstream& timeout, std::ofstream* fileouts);

  /**
   * Transfer `lambda_ij` * `dim` * `C[i]` to reservoir j and `lambda_ji` * `dim` * `C[j]` to reservoir i
   *
   * <B> No checking!!!! Assumptions </B>
   * 
   * 1. i and j are within range
   * 2. lambdas are not greater than 1 and not less than 0
   * 3. dim is not greater than d_i or d_j
   */
  void transfer(std::size_t i, std::size_t j, double lambda_ij, double lambda_ji, double dim);
  void increment_C(std::size_t i, double incr);
  void proportion_C(std::size_t i, double prop);
};
