#include "reservoir_collection.h"
#include <iostream>

using namespace std;

int f(double t, const double y[], double dydt[], void *params)
  {
    (void)(t); 
    gsl_spmatrix *Z = (gsl_spmatrix *) params;

    gsl_vector_const_view v = gsl_vector_const_view_array(y, Z->size1);
    gsl_vector_view out = gsl_vector_view_array(dydt, Z->size1);
    gsl_spblas_dgemv(CblasNoTrans, 1.0, Z, &v.vector, 0, &out.vector);

    return GSL_SUCCESS;
  };

Reservoirs::Reservoirs(size_t n, size_t nzmax)
  :current_time{0.0}
  ,m{gsl_spmatrix_alloc(n, n)}
  ,beta{gsl_spmatrix_alloc(n, n)}
  ,Q{gsl_spmatrix_alloc(n, 2)}
  ,Z_{gsl_spmatrix_alloc(n, n)}
  ,Z{gsl_spmatrix_alloc_nzmax(n, n, nzmax, GSL_SPMATRIX_CSR)}
  ,C{gsl_vector_alloc(n)}
  ,d{gsl_vector_alloc(n)}
  ,d_inv{gsl_vector_alloc(n)}
  ,sys{f, NULL, n, Z}
  ,dri{ gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rkf45, 1e-6, 1e-6, 0.0)}
{}

Reservoirs::Reservoirs(const char *C_in
		       ,const char *d_in
		       ,const char *m_in
		       ,const char *beta_in
		       ,const char *Q_in
		       ,size_t n)
  :current_time{0.0}
  ,m{gsl_spmatrix_alloc(n, n)}
  ,beta{gsl_spmatrix_alloc(n, n)}
  ,Q{gsl_spmatrix_alloc(n, 2)}
  ,Z_{gsl_spmatrix_alloc(n, n)}
  ,Z{gsl_spmatrix_alloc_nzmax(n, n, 3*n, GSL_SPMATRIX_CSR)}
  ,C{gsl_vector_alloc(n)}
  ,d{gsl_vector_alloc(n)}
  ,d_inv{gsl_vector_alloc(n)}
  ,sys{f, NULL, n, Z}
  ,dri{ gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rkf45, 1e-6, 1e-6, 0.0)}
{
  {
    FILE *f = fopen(C_in, "r");
    if(f)
      {
	gsl_vector_fscanf(f, C);
	fclose(f);
	cout << "C:" << endl;
	gsl_vector_fprintf(stdout, C, "%.2f");
      }
    else{cout << "C read fail" << endl; terminate(); }
    
    f = fopen(d_in, "r");
    if(f)
      {
	gsl_vector_fscanf(f, d);
	fclose(f);
	cout << "d:" << endl;
	gsl_vector_fprintf(stdout, d, "%.2f");
      }
    else{cout << "d read fail" << endl; terminate(); }
    
    f = fopen(m_in, "r");
    if(f)
      {
	m = gsl_spmatrix_fscanf(f);
	fclose(f);
	cout << "m:" << endl;
	gsl_spmatrix_fprintf(stdout, m, "%.2f");
	
      }
    else{cout << "m read fail" << endl; terminate(); }
    
    f = fopen(beta_in, "r");
    if(f)
      {
	beta = gsl_spmatrix_fscanf(f);
	fclose(f);
	cout << "beta:" << endl;
	gsl_spmatrix_fprintf(stdout, beta, "%.2f");
      }
    else{cout << "beta read fail" << endl; terminate(); }
    
    f = fopen(Q_in, "r");
    if(f)
      {
	Q = gsl_spmatrix_fscanf(f);
	fclose(f);
	cout << "Q:" << endl;
	gsl_spmatrix_fprintf(stdout, Q, "%.2f");
      }
    else{cout << "Q read fail" << endl; terminate(); }
  }

  //set d_inv

  for(size_t i = 0; i < n; ++i) gsl_vector_set(d_inv, i, 1.0 / gsl_vector_get(d, i) );

  calculate_Z();
}

Reservoirs::~Reservoirs()
{
  gsl_spmatrix_free(m);
  gsl_spmatrix_free(beta);
  gsl_spmatrix_free(Q);
  gsl_spmatrix_free(Z_);
  gsl_spmatrix_free(Z);

  gsl_vector_free(C);
  gsl_vector_free(d);
  gsl_vector_free(d_inv);
  
}




void Reservoirs::set_m(size_t i, size_t j, double val )
{
  /**
   * m(i,j) term appears at (j,i) under a positive sign
   */
  double current_val = gsl_spmatrix_get(m, i, j);
  gsl_spmatrix_set(m, i, j, val);
  
  if(gsl_spmatrix_ptr(Z_, j, i) != NULL)
    *gsl_spmatrix_ptr(Z_, j, i) += val - current_val;
    
  else
    gsl_spmatrix_set(Z_, j, i, val);
   
  gsl_spmatrix_csr(Z, Z_);
  gsl_spmatrix_scale_rows(Z, d_inv);
}


void Reservoirs::set_beta(size_t i, size_t j, double val )
{
  /**
   * beta(i,j) term appears in two places:
   * 1. (j,i) under a positive sign
   * 2. at (i, i) under a negative sign
   */
  double current_val = gsl_spmatrix_get(beta, i, j);
  gsl_spmatrix_set(beta, i, j, val);
  
  //1.
  if(gsl_spmatrix_ptr(Z_, j, i) != NULL)
    *gsl_spmatrix_ptr(Z_, j, i) += val - current_val;
  
  else gsl_spmatrix_set(Z_, j, i, val);
  
  //2.
  if(gsl_spmatrix_ptr(Z_, i, i) != NULL)
    *gsl_spmatrix_ptr(Z_, i, i) += current_val - val;
    
  else gsl_spmatrix_set(Z_, i, i, -val);
    
  
  gsl_spmatrix_csr(Z, Z_);
  gsl_spmatrix_scale_rows(Z, d_inv);
}

void Reservoirs::set_Q(size_t i, size_t j, double val )
{
  /**
   * Q term appears at (i,i) under a negative sign
   */
  double current_val = gsl_spmatrix_get(Q, i, j);
  gsl_spmatrix_set(Q, i, j, val);
  

  if(gsl_spmatrix_ptr(Z_, i, i) != NULL)
    *gsl_spmatrix_ptr(Z_, i, i) += current_val - val;
   
  else
    gsl_spmatrix_set(Z_, i, i, -val);
    
  gsl_spmatrix_csr(Z, Z_);
  gsl_spmatrix_scale_rows(Z, d_inv);
}

void Reservoirs::set_d(size_t i, double val )
{
  gsl_vector_set(d, i, val);
  gsl_vector_set(d_inv, i, 1.0 / val);
  calculate_Z();
}

double Reservoirs::get_m(size_t i, size_t j) const {return gsl_spmatrix_get(m, i, j);}
double Reservoirs::get_beta(size_t i, size_t j) const {return gsl_spmatrix_get(beta, i, j);}
double Reservoirs::get_Q(size_t i, size_t j) const {return gsl_spmatrix_get(Q, i, j);}


double Reservoirs::get_d(std::size_t i) const {return gsl_vector_get(d, i);}

double* Reservoirs::_C(size_t i){ return gsl_vector_ptr(C, i);}
const double* Reservoirs::_C(size_t i) const {cout << "const ptr" << endl; return gsl_vector_const_ptr(C, i);}

void Reservoirs::calculate_Z()
{
  size_t n = Z_->size1;

  gsl_vector *row_sums = gsl_vector_alloc(n);

  {
    gsl_vector *ones = gsl_vector_alloc(n);
    gsl_vector_set_all(ones, 1.0);
    gsl_spblas_dgemv(CblasNoTrans, 1.0, beta, ones, 0.0, row_sums);
    gsl_vector_free(ones);
  }

  {
    gsl_vector *ones = gsl_vector_alloc(2);
    gsl_vector_set_all(ones, 1.0);
    gsl_spblas_dgemv(CblasNoTrans, 1.0, Q, ones, 1.0, row_sums);
    gsl_vector_free(ones);
  }

  for(size_t i=0; i < n; ++i)
    if(gsl_vector_get(row_sums, i) != 0) gsl_spmatrix_set(Z_, i, i, -gsl_vector_get(row_sums, i));

  for(size_t i=0; i < n; ++i)
    for(size_t j=0; j < n; ++j)
      {
	if(i == j) continue;
	if( gsl_spmatrix_get(beta, j, i) + gsl_spmatrix_get(m, j, i) != 0 )
	  gsl_spmatrix_set(Z_, i, j, gsl_spmatrix_get(beta, j, i) + gsl_spmatrix_get(m, j, i));
      }
      

  gsl_spmatrix_csr(Z, Z_);
  gsl_spmatrix_scale_rows(Z, d_inv);

  gsl_vector_free(row_sums);
}


void Reservoirs::advance(double t, double delta_t, ofstream& timeout, ofstream* fileouts)
{
  double end_time = current_time + t;
  timeout << current_time << endl;
  
  for(size_t p = 0; p < Z->size1; ++p)
	    {
	      if( fileouts + p == nullptr ) continue;
	      *(fileouts + p) << gsl_vector_get(C, p) << endl;
	    } 

  while( current_time + delta_t < end_time )
    {
      int status = gsl_odeiv2_driver_apply(dri
					   ,&current_time
					   ,current_time + delta_t
					   ,C->data);
      
      if( status != GSL_SUCCESS )
	{
	  printf ("error, return value=%d\n", status);
          break;
	}
      else
	{
	  timeout << current_time << endl;
	  for(size_t p = 0; p < Z->size1; ++p)
	    {
	      if( fileouts + p == nullptr ) continue;
	      *(fileouts + p) << gsl_vector_get(C, p) << endl;
	    }
	}

    }

  //one last time
  int status = gsl_odeiv2_driver_apply(dri
				       ,&current_time
				       ,end_time
				       ,C->data);

  if( status != GSL_SUCCESS ) printf ("error, return value=%d\n", status);
  else
    {
      timeout << current_time << endl;
      for(size_t p = 0; p < Z->size1; ++p)
	{
	  if( fileouts + p == nullptr ) continue;
	  *(fileouts + p) << gsl_vector_get(C, p) << endl;
	}
    }
}


void Reservoirs::advance(double t, ofstream& timeout, ofstream* fileouts)
{
  timeout << current_time << endl;
  for(size_t p = 0; p < Z->size1; ++p)
	    {
	      if( fileouts + p == nullptr ) continue;
	      *(fileouts + p) << gsl_vector_get(C, p) << endl;
	    }
  
  int status = gsl_odeiv2_driver_apply(dri, &current_time, current_time + t, C->data);
      
  if( status != GSL_SUCCESS ) printf ("error, return value=%d\n", status);
}


void Reservoirs::transfer(size_t i,size_t j, double lambda_ij, double lambda_ji, double dim)
{
  double load_ij, load_ji;

  load_ij = lambda_ij * dim * *_C(i);
  load_ji = lambda_ji * dim * *_C(j);

  *_C(i) += (load_ji - load_ij) / gsl_vector_get(d, i);
  *_C(j) += (load_ij - load_ji) / gsl_vector_get(d, j);
}


void Reservoirs::increment_C(size_t i, double incr)
{
  *_C(i) = max(0.0, *_C(i) + incr);
}

void Reservoirs::proportion_C(size_t i, double prop)
{
  *_C(i) *= prop;
}
