//#define EIGENLIB			// uncomment to use Eigen linear algebra library
//#define NO_POINTER_INIT	// uncomment to disable pointer checking

#include "fun_head_fast.h"

// do not add Equations in this area

MODELBEGIN

EQUATION("basic")
/*
"Renda básica universal"
*/

v[0] = VL("basic",1);
v[1] = V("g_basic");
v[2] = (1+v[1])*(v[0]);

RESULT(v[2])

EQUATION("basic_total")
/*
Total expenditure with basic
*/

v[0] = V("basic");
v[1] = V("N");
v[2] = v[0]*v[1];

RESULT(v[2])



EQUATION("Q_fc")
/*
Full capacity output
*/

v[1] = VL("K_t",1); // Changed
v[2] = V("gamma");
v[3] = v[1]*v[2]; // Warning: supply constraint
v[4] = V("xi");
v[5] = V("N");
v[6] = v[4]*v[5]; // 'Warning: labor supply constraint'
v[7] = min(v[3],v[6]);

RESULT(v[7])


EQUATION("u_t")
/*
Capacity utilization equation
*/

v[0] = V("Q_t"); // WARNING: Trial to solve deadlock erros
v[1] = V("Q_fc"); // WARNING: Trial to solve deadlock erros
v[2] = v[0]/(v[1]);

if (v[2] >= 1) // Warning: supply constraint
{v[2] = 1;}
else {v[2] = v[2];}

if (v[2] < 0) // Warning: supply constraint
{v[2] = 0;}
else {v[2] = v[2];}


RESULT(v[2])



EQUATION( "I_t" )

	/*
	Firms' investment. Eq. (7)
	*/

	v[0] = V("alpha");				// Utilization gap coefficient
	v[1] = V("gamma"); 				// 
	v[2] = V("beta");					// Profit rate coefficient
	v[3] = V("pi");					// Profit-share
	v[4] = V("price_t");			// price in t. CHANGED: it is price_t insted price_t-1
	v[5] = VL("Q_t", 1);				// Total output in t-1
	v[6] = V("ud");
	v[7] = VL("K_t", 1);
	v[8] = (v[6]*v[7])/v[1];			// Qd
	v[9] = V("e");					// Valuation ratio coefficient
	v[10] = VL("Pe_t", 1);				// Stock price in t-1
	v[11] = VL("E_t", 1);				// Equity amount

	v[12] = (v[0]*v[1] + v[2]*v[3])*v[4]*v[5];// 1st term of I_t
	v[13] = -v[0]*v[1]*v[4]*v[8];			// 2nd term of I_t
	v[14] = v[9]*v[10]*v[11];			// 3rd term of I_t

	v[15] = v[12] + v[13] + v[14];		// Firm's investment

	if (v[15] < 0) 					// Garantees that firms' investment is non-negative
		v[15] = 0;
	else
		v[15] = v[15];

RESULT( v[15] )


EQUATION( "K_t" )

	/*
	Capital stock equation. K in t-1 + Eq. (8)
	*/
	
	v[0] = V("delta");			// Depreciation rate
	v[1] = VL("K_t", 1);			// Capital stock in t-1
	v[2] = V("I_t");				// Total investiment in t
	
	v[3] = (1 - v[0])*v[1] + v[2];	// Capital Stock in t

RESULT( v[3] )


EQUATION( "price_t" )

	/*
	Calculate the price. Eq (9)
	*/

	v[0] = V("mu");				// mark-up parameter
	v[1] = V("wbarocc");			// average wage of employed workers in t
	v[2] = V("xi");				// Labor-produtivity (Q/L)
	v[3] = (1+v[0])*(v[1]/v[2]);
	
RESULT( v[3] )


EQUATION( "psi" )

	/*
	Wage-share equation. Eq (10)
	*/

	v[0] = V("mu"); 			// mark-up parameter
	v[1] = 1/(1+v[0]); 

	PARAMETER //Transform the variable into a parameter. Effectively prevents the variable from being computed again, turning it into a parameter which are never computed.

RESULT( v[1] )


EQUATION( "pi" )

	/*
	Profit-share equation. Eq (11)
	*/
	
	v[0] = V("mu"); 			// mark-up parameter
	v[1] = (v[0])/(1+v[0]); 

	PARAMETER //Transform the variable into a parameter. Effectively prevents the variable from being computed again, turning it into a parameter which are never computed.

RESULT( v[1] )


EQUATION( "A_t" )

	/*
	Retained profit. Eq. (12)
	*/
	
	v[0] = V("theta");			// Share of net profit distributed 
	v[1] = V("pi");				// Profit share
	v[2] = V("price_t");			// Price in t
	v[3] = V("Q_t");				//
	v[4] = V("i");				// Interest rate
	v[5] = VL("B_t", 1);			// Bonds in t-1

	v[6] = (1 - v[0])*(v[1]*v[2]*v[3] - v[4]*v[5]);

RESULT( v[6] )


EQUATION( "B_t" )

	/*
	Stock of Bonds. Bonds in t-1 + Eq. (13)
	*/

	v[0] = VL("B_t", 1);			// Bonds in t-1
	v[1] = V("debt_f");			// Share of investment funded by debt
	v[2] = V("I_t");				// Total investiment in t
	v[3] = V("A_t");				// Retained profits in t

	v[4] = v[0] + v[1]*(v[2] - v[3]);

RESULT( v[4] )


EQUATION( "E_t" )

	/*
	Equity stock. E_t in t-1 + Eq. (14)
	*/
	
	v[0] = VL("E_t", 1);			// Equities stock in t-1
	v[1] = V("debt_f");			// Share of investment funded by debt
	v[2] = V("I_t");				// Total investiment in t
	v[3] = V("A_t");				// Retained profits in t
	v[4] = V("Pe_t");				// Equities price in t

	v[5] = v[0] + (1 - v[1])*(v[2] - v[3])/(v[4]);
	
	if (v[5] <= 0)
		v[5] = 1;
	else
		v[5] = v[5];

RESULT( v[5] )


EQUATION( "Ytheta_t" )

	/*
	Managers' diposable income in t. Eq. (15)
	*/

	v[0] = V("theta");			// Parameter of firms' net profits shared with managers
	v[1] = V("pi");				// Profit-share
	v[2] = V("price_t");			// Price in t
	v[3] = V("Q_t");				//
	v[4] = V("i");				// Interest rate
	v[5] = VL("B_t", 1);			// Bonds in t-1

	v[6] = v[0]*(v[1]*v[2]*v[3] - v[4]*v[5]);

RESULT( v[6] )


EQUATION( "Ctheta_t" )

	/*
	Managers' consumption in t. Eq. (17)
	*/
 
     	v[0] = V("stheta");			// Propensity to save out of managers’ disposable income 
  	v[1] = V("theta");			// Parameter of firms' net profits shared with managers
 	v[2] = V("pi");				// Profit-share
  v[3] = V("price_t");		// Price in t
 	v[4] = VL("Q_t", 1);			//
 	v[5] = V("i");				// Interest rate
 	v[6] = VL("B_t", 1);			// Bonds in t-1
 	v[7] = V("sigmatheta");			// Propensity to save out of managers’ wealth
 	v[8] = VL("Wtheta_t", 1);		// Managers' wealth in t-1
 
 	v[9] = (1 - v[0])*v[1]*(v[2]*v[3]*v[4] - v[5]*v[6]) + (1 - v[7])*v[8];
 
RESULT( v[9] )


EQUATION( "Wtheta_t" )

	/*
	Managers' total wealth. Wtheta in t-1 + Eq. (18)
	*/

	v[0] = VL("Wtheta_t", 1);		// Managers' wealth in t-1
	v[1] = V("Stheta_t");			// Managers' total savings in t
	v[2] = V("G_t");				// Capital gain in t

	v[3] = v[0] + v[1] + v[2];

RESULT( v[3] )


EQUATION( "Stheta_t" )

	/*
	Managers' total saving.
	*/

	v[0] = V("Ytheta_t");			// Managers' diposable income in t
	v[1] = V("Ctheta_t");			// Managers' consumption in t

	v[2] = v[0] - v[1];

RESULT( v[2] )


EQUATION( "G_t" )

	/*
	Capital gain
	*/

	v[0] = V("Pe_t");				// Equity price in t
	v[1] = VL("Pe_t", 1);			// Equity price in t-1
	v[2] = VL("E_t", 1);			// Equity amount in t-1

	v[3] = v[2]*(v[0] - v[1]);

RESULT( v[3] )


//EQUATION( "Wtheta_total" )
//
//	/*
//	Managers' Total Wealth.
//	*/
//
//	v[0] = 0;
//	
//	CYCLE(cur, "Consumers")
//		{
//		v[1] = VS(cur, "Wtheta_t");
//		v[0] = v[0] + v[1];
//		}
//
//RESULT( v[0] )


EQUATION( "Mtheta_t" )

	/*
	Managers’ demand for money. Eq. (20)
	*/
	
	v[0] = V("Wtheta_t");
	v[1] = V("Pe_t");
	v[2] = V("E_t");
	
	v[3] = v[0] - v[1]*v[2];

RESULT( v[3] )


EQUATION( "state_b_it" )

	/*
	State of workers - borrow behavior. 1= borrowing; 0= not borrowing. Eqs. (21) and (22)
	*/
	
	v[0] = VL("Mw_t", 1);			// Each Workers' amount of money in t-1
	v[1] = V("Yw_t");				// Workers' disposable income in t
	v[2] = V("Cw_t");				// Workers' consumption in t
	
	if (v[0] + v[1] < v[2])			// Evaluates worker finance consumption with debt 
		v[2] = 1;				// If it is true, the worker is borrowing
	else
		v[2] = 0;				// If not, the worker doesn't borrow

RESULT( v[2] )


EQUATION( "Yw_t" )

	/*
	Workers' disposable income. Eq. (23)
	*/

	v[0] = V("w_it");				// Wage in t
	v[1] = V("i");				// Interest rate
	v[2] = VL("D_t", 1);			// Workers' debt in t-1
	v[3] = V("basic");

	v[3] = v[0] - v[1]*v[2] + v[3];

RESULT( v[3] )


EQUATION( "Sw" )

	/*
	Workers' savings. p. 7
	*/

	v[0] = V("Yw_t");				// Workers' disposable income in t
	v[1] = V("Cw_t");				// Workers' consumption in t
	
	v[2] = v[0] - v[1];

RESULT( v[2] )


EQUATION( "Sw_total" )

	/*
	Workers' Total savigns
	*/

	v[0] = 0;
	
	CYCLE(cur, "Consumer")
		{
		v[1] = VS(cur, "Sw");
		v[0] = v[0] + v[1];
		}

RESULT( v[0] )


EQUATION( "Ww_t" )

	/*
	Workers' wealth. Ww_1 in t-1 + Eq. (25)
	*/

	v[0] = VL("Ww_t", 1);			// Workers' wealth in t-1
	v[1] = V("Yw_t");				// Workers' disposable income in t
	v[2] = V("Cw_t");				// Workers' consumption in t

	v[3] = v[0] + v[1] - v[2];

	if(v[3] < 0)				// Evaluates if workers' wealth is negative
		v[3] = 0;				// If it is true, set wealth as 0
	else
		v[3] = v[3];

RESULT( v[3] )


EQUATION( "Ww_total" )

	/*
	Workers' Total Wealth.
	*/

	v[0] = 0;
	
	CYCLE(cur, "Consumer")
		{
		v[1] = VS(cur, "Ww_t");
		v[0] = v[0] + v[1];
		}

RESULT( v[0] )


EQUATION( "Mw_t" )

	/*
	Workers’ demand for money. Eqs. (27) and (28)
	*/
	
	v[0] = VL("Mw_t", 1);			// Each Workers' amount of money in t-1
	v[1] = V("Sw");				// Workers' savings in t
	
	v[2] = v[0] + v[1];

RESULT( v[2] )


EQUATION( "Mw_total" )

	/*
	Workers' Total demand for money. Eq. (29)
	*/

	v[0] = 0;
	
	CYCLE(cur, "Consumer")
		{
		v[1] = VS(cur, "Mw_t");
		v[0] = v[0] + v[1];
		}

RESULT( v[0] )


EQUATION( "D_t" )

	/*
	Workers' debt derived from Eq. (26)
	*/

	v[0] = VL("D_t", 1);			// Workers' debt in t-1
	v[1] = V("Sw");				// Workers' savings in t
	v[2] = VL("Mw_t", 1);			// Each Workers' amount of money in t-1

	v[3] = v[0] - (v[1] + v[2]);

RESULT( v[4] )


EQUATION( "D_total" )

	/*
	Workers' TOTAL debt derived from Eq. (30)
	*/

	v[0] = 0;
	
	CYCLE(cur, "Consumer")
		{
		v[1] = VS(cur, "D_t");
		v[0] = v[0] + v[1];
		}

RESULT( v[0] )


EQUATION( "Cw_t" )

	/*
	Workers' consumption. Eq. (31)
	*/

	v[0] = V("spsi");				// Propensity to save out of workers' income
	v[1] = V("w_it");				// Wage in t
	v[2] = V("eta");				// Sensitivity to workers’ relative income
	v[3] = V("wbarocc");			// Average wage of employed workers in t-1
	v[4] = V("sigmapsi");			// Propensity to save out of workers' wealth
	v[5] = VL("Ww_t", 1);			// Workers' wealth in t-1

	v[6] = (1 - v[0])*v[1] + v[2]*(v[3] - v[1]) + (1 - v[4])*v[5];

	if(v[6] < 0)				// Evaluates if workers' consumption is negative
		v[6] = 0;				// If it is true, set as 0
	else
		v[6] = v[6];

RESULT( v[6] )


EQUATION( "Cw_total" )

	/*
	Workers' Total Consumption. Eq. (32)
	*/

	v[0] = 0;
	
	CYCLE(cur, "Consumer")
		{
		v[1] = VS(cur, "Cw_t");
		v[0] = v[0] + v[1];
		}

RESULT( v[0] )


EQUATION( "Wfinance" )

	/*
	Financial sector wealth. From Eq. (33)
	*/

	v[0] = V("i");				// interest rate
	v[1] = VL("D_total", 1);		// Workers' TOTAL debt in t-1
	v[2] = VL("B_t", 1);			// Bonds in t-1
	v[3] = VL("Wfinance", 1);		// Financial sector wealth in t-1
	
	v[4] = v[3] + v[0]*(v[1] + v[2]);

RESULT( v[4] )


EQUATION( "Q_t" )

	/*
	Goods market equilibrium. Eq. (34)
	*/

	v[0] = V("alpha");
	v[1] = V("gamma");
	v[2] = V("beta");
	v[3] = V("pi");
	v[4] = VL("price_t", 1);
	v[5] = VL("Q_t", 1);
	v[6] = V("ud");
	v[7] = VL("K_t", 1);
	v[8] = V("sigmapsi");
	v[9] = VL("Mw_t", 1);
	v[10] = VL("D_t", 1);
	v[11] = V("stheta");
	v[12] = V("theta");
	v[13] = V("i");
	v[14] = VL("B_t", 1);
	v[15] = V("sigmatheta");
	v[16] = VL("Wtheta_t", 1);
	v[17] = V("e");
	v[18] = VL("Pe_t", 1);
	v[19] = VL("E_t", 1);
	v[20] = V("spsi");
	v[21] = V("eta");
	v[22] = V("psi");
	v[23] = V("wbarocc");
	v[24] = V("xi");
	v[25] = (v[6]*v[7])/v[1];				// Qd

	v[26] = (v[0]*v[1] + v[2]*v[3])*v[4]*v[5];	// F 1st term
	v[27] = -v[0]*v[4]*v[25];				// F 2nd term
	v[28] = (1 - v[8])*(v[9] - v[10]);			// F 3rd term
	v[29] = -(1 - v[11])*v[12]*v[13]*v[14];		// F 4th term
	v[30] = (1 - v[15])*v[16];				// F 5th term
	v[31] = v[17]*v[18]*v[19];				// F last term

	v[32] = v[26]+v[27]+v[28]+v[29]+v[30]+v[31];	// F t-1
	
	v[33] = v[4]*(1 - (1 - v[20] - v[21])*v[22] - (1 - v[11])*v[12]*v[3]) - (v[21]*v[23])/v[24];
	
	v[0] = V("basic_total");

	v[34] = (v[32] + v[0])/v[33];
	
	/*
	v[0] = V("Cw_total");			// Total workers' consumption in t
	v[1] = V("Ctheta_t");			// Managers' consumption in t
	v[2] = V("I_t");				// Investment in t
	v[4] = V("price_t");

	v[3] = (v[0] + v[1] + v[2])/v[4];
	*/

RESULT( v[34] )


EQUATION( "Pe_t" )

	/*
	Equities price from financial market equilibrium. Eq. (35)
	*/
	
	v[0] = VL("E_t", 1);			// Equity amount in t-1
	v[1] = VL("Wtheta_t", 1);		// Managers' total wealth in t-1
	v[2] = V("lambda");			// Positive coefficient
	v[3] = VL("G_t", 1);			// Capital gain in t-1
	v[4] = V("debt_f");			// Share of investment funded by debt
	v[5] = V("I_t");				// Total investiment in t
	v[6] = V("A_t");				// Retained profit in t
	v[7] = 1 + exp(-v[2]*v[3]);
	
	v[8] = (1/v[0])*((v[1]/v[7]) - (1 - v[4])*(v[5] - v[6]));
	
	if(v[8] <= 0)
		v[8] = 1;
	else
		v[8] = v[8];

RESULT( v[8] )


EQUATION( "M_TOTAL" )

	/*
	Total money in the system
	*/
	
	v[0] = V("Wtheta_t");			// Managers' demand for money in t
	v[1] = V("Mw_total");			// Workers' total demand for money in t

	v[2] = v[0] + v[1];
	
RESULT( v[2] )


EQUATION( "EL_t" )

	/*
	Number of employed workers
	*/
	
	v[0] = V("N");				// Total numbers of workers
	v[1] = V("Q_t");				// Output in t
	v[2] = V("xi");				// Labor productivity
	v[3] = round(v[1]/v[2]);		// Round of output-labor productivity ratio

	v[4] = min(v[0],v[3]);

	if (v[4] <= 0)
		v[4] = 1;

RESULT( v[4] )


EQUATION( "size_unemp" )

	/*
	Number of unemployed workers
	*/
	
	v[0] = V("N");				// Total numbers of workers
	v[1] = V("EL_t");				// Number of employed workers
	v[2] = v[0] - v[1];

RESULT( v[2] )


EQUATION( "UnRate" )

	/*
	Unemployment rate
	*/
	
	v[0] = V("N");				// Total numbers of workers
	v[1] = V("size_unemp");			// Number of employed workers

	v[2] = v[1]/v[0];

RESULT( v[2] )


EQUATION( "wbarocc" )

	/*
	Average wage of employed workers
	*/

	v[0] = 0;
	
	CYCLE( cur, "Consumer")
		{
		v[1] = VLS(cur, "w_it", 1);
		v[0] = v[0] + v[1];
		}					// Calculate the sum of wage of employed workers

	v[2] = VL("EL_t", 1);			// Number of employed workers

	v[3] = v[0]/v[2];

RESULT( v[3] )


EQUATION( "Yw_total" )

	/*
	Workers' Total disposable income
	*/

	v[0] = 0;
	
	CYCLE( cur, "Consumer" )
		{
		v[1] = VS(cur, "Yw_t");
		v[0] = v[0] + v[1];
		}

RESULT( v[0] )


EQUATION( "minsal_t" )

	/*
	Update minimum salaries.
	*/
	
	v[0] = VL("minsal_t", 1); 		// minsal in t-1
	v[1] = V("inflation");			// Inflation rate
	
	if (v[1] > 0)
		v[2] = v[0]*(1 + v[1]); 		// minimun salary in t
	else
		v[2] = v[0];

RESULT( v[2] )


EQUATION( "w_last" )

	/*
	Just for code consistency. Returns de last wage of wich worker.
	*/
	
	v[0] = VL("w_it", 1);
	
RESULT( v[0] )


EQUATION( "inflation" )

	/*
	Inflation rate
	*/
	
	v[0] = VL("price_t",1);
	v[1] = V("price_t");
	v[2] = (v[1]-v[0])/v[0];

RESULT( v[2] )


EQUATION( "g_it" )

	/*
	Uniformly distributed shocks with mean zero in the wages.
	Suggestion: set to consider the shock's amplitude.
	*/
	
	v[0] = V("gmin");
	v[1] = V("gmax"); 
	v[2] =  uniform(v[0], v[1]);

RESULT( v[2] )


EQUATION( "state_it" )

	/*
	State of worker i at time t (Inactive=0, Active=1)
	*/
	
	v[1] = V("N"); 				// Max
	v[2] = VL("EL_t", 1); 			// Number of employed worker in t-1
	v[3] = uniform_int(0, v[1]);
	
	if (v[3] >= v[2])				// If agent is drawed out of employed range, Inactive = 0
		v[4] = 0;
	else
		v[4] = 1;

RESULT( v[4] )


EQUATION( "w_it" )

	/*
	Updates wages by worker, evaluates wich one is below the minimum and set them to it.
	*/
	
	v[0] = V("w_last");			// salary in t-1
	v[1] = V("inflation");			// Inflation rate
	v[2] = V("g_it");
	v[3] = V("minsal_t");			// minimun salary in t
	v[4] = v[0]*(1 + v[1])*(1 + v[2]); 	// current wage. Salary in t-1 updated by inflation and the shock (g_it)
	
	if (v[4] < v[3]) 				// Evaluates if current wages is below the minimum one.
		v[4] = v[3]; 			// If it is true, then set the wage as minimum.

	v[5] = V("state_it");
	v[4] = v[4]*v[5]; 			// If unemployed, w_it = 0

RESULT( v[4] )


EQUATION( "W" )

	/*
	Total Wealth, workers and managers
	*/

	v[0] = V("Ww_total");
	v[1] = V("Wtheta_t");

	v[2] = v[0] + v[1];

RESULT( v[2] )


EQUATION( "Yf_t" )

	/*
	Financial sector income. Eq. (33)
	*/

	v[0] = V("i");				// Interest rate
	v[1] = VL("D_t", 1);			// Workers' debt in t-1
	v[2] = VL("B_t", 1);			// Bonds in t-1

	v[3] = v[0]*(v[1] + v[2]);

RESULT( v[3] )


EQUATION( "M_t" )

	/*
	Amount of money
	*/
	
	v[0] = V("W");				// Total wealth in t
	v[1] = V("Pe_t");				// Equity price in t
	v[2] = V("E_t");				// Amount of equity in t

	v[3] = v[0] - v[1]*v[2];

RESULT(v[3])


EQUATION( "numOfBorrowWorkers_t" )

	/*
	Number of Borrowers
	*/
	
	v[0] = 0;
	
	CYCLE(cur, "Consumer")
		{
		v[1] = VS(cur, "state_b_it");
		v[0] = v[0] + v[1];
		}

RESULT( v[0] )


EQUATION( "shareOfBorrWorkers_t" )

	/*
	Share of Borrowers
	*/
	
	v[0] = V("numOfBorrowWorkers_t");	// Number of borrowers
	v[1] = V("N");				// Total number of workers

	v[2] = v[0]/v[1];

RESULT( v[2] )


EQUATION( "numOfNonBorrowWorkers_t" )

	/*
	Number of non-borrower workers
	*/
	
	v[0] = V("numOfBorrowWorkers_t");	// Number of non-borrowers
	v[1] = V("N");				// Total number of workers

	v[2] = v[1] - v[0];

RESULT( v[2] )


EQUATION( "shareOfNonBorrWorkers_t" )

	/*
	Share of Non-Borrowers
	*/
	
	v[0] = V("numOfNonBorrowWorkers_t");	// Number of non-borrowers
	v[1] = V("N");				// Total number of workers

	v[2] = v[0]/v[1];

RESULT( v[2] )


EQUATION( "Y_total" )

	/*
	Total income
	*/

	v[0] = V("Yw_total");			// Workers' total income
	v[1] = V("Ytheta_t");			// Managers' wealth

	v[2] = v[0] + v[1];

RESULT( v[2] )



MODELEND

// do not add Equations in this area

void close_sim( void )
{
	// close simulation special commands go here
}
