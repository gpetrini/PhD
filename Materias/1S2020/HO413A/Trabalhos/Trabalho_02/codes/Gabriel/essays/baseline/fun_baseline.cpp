//#define EIGENLIB			// uncomment to use Eigen linear algebra library
//#define NO_POINTER_INIT	// uncomment to disable pointer checking

#include "fun_head_fast.h"

// do not add Equations in this area

MODELBEGIN

// insert your equations here, between the MODELBEGIN and MODELEND words


//////////////////////////////////// Model Initialization //////////

EQUATION("N")
/*
Population
*/

v[0] = VL("N",1);
v[1] = V("gN"); // Population growth rate
v[2] = (1+v[1])*v[0];

RESULT(v[2])


EQUATION("psi")
/*
Wage-share equation. Eq (8)
*/

v[0] = V("mu"); // mark-up 
v[1] = (1)/(1+v[0]); 

RESULT(v[1])


EQUATION("pi")
/*
Profit-share equation. Eq (9)
*/

v[0] = V("mu"); // mark-up 
v[1] = (v[0])/(1+v[0]); 

RESULT(v[1])

EQUATION("g_it")
/*
???
*/

v[0] = V("gmin");
v[1] = V("gmax"); 
v[2] =  uniform(v[0], v[1]);

RESULT(v[2])

EQUATION("mult")
/*
Keynesian multiplier
*/

v[0] = V("b");
v[1] = V("xi");
v[2] = V("spsi");
v[3] = V("tau_y");
v[4] = V("psi");
v[5] = V("psi");
v[6] = V("Theta");
v[7] = V("pi");
v[8] = 1/((v[0]/v[1]) + 1 - (1-v[2])*(1-v[3])*(v[4]+v[6]*v[7]));
//v[8] = 1/(1 - (1-v[2])*(1-v[3])*(v[4]+v[6]*v[7])); // Trying to fix

RESULT(v[8])

EQUATION("minsal_t")
/*
Update salaries
*/

v[0] = VL("minsal_t", 1);
v[1] = V("pie"); 
v[2] =  v[0]*(1+v[1]);

RESULT(v[2])

EQUATION("w_last")
/*
Just for code consistency. Returns de last wage
*/

RESULT(VL("w_it", 1))

EQUATION("w_it")
/*
Updates wages and evaluates if it is below the minimum one
*/

v[0] = V("w_last");
v[1] = V("pie"); 
v[2] = V("g_it"); // g_it
v[3] = V("minsal_t");
v[4] = v[0]*(1+v[1]) + v[2]*v[3];

if (v[4] < v[3]) // Evaluates if current wages is below the minimum one
{v[4] = v[3];}
else {v[4] = v[4];}
v[5] = V("state_it");
v[4] = v[4]*v[5]; // If unemployed, w_it = 0

RESULT(v[4])


EQUATION("II_t")
/*
investment function component
*/

v[0] = V("Beta");
v[1] = VL("Pe_t",1);
v[2] = VL("E_t", 1);
v[3] = VL("price_t",1);
v[4] = VL("K_t",1);
v[5] = (v[0]*v[1]*v[2])/(v[3]*v[4]);

RESULT(v[5])

EQUATION("I_t")
/*
Firms' investment
*/

v[0] = V("I0");
v[1] = V("i0");
v[2] = V("a");
v[3] = VL("u_t",1);
v[4] = V("ud");
v[5] = VL("K_t",1);
v[6] = V("II_t");
v[7] = (v[0] + (v[2]*(v[3] - v[4])))/(v[4])*v[5] + v[6];

if (v[7] < 0) // Garantees that firms' investment is non-negative
	{v[7] = 0;}
else {v[7] = v[7];}

RESULT(v[7])

EQUATION("auton")
/*
equilibrium in goods market
*/

v[0] = V("I_t");
v[1] = VL("W_t",1);
v[2] = V("sigma");
v[3] = V("tau_w");
v[4] = VL("price_t",1);
v[5] = V("phi");
v[6] = VL("D_t",1);
v[7] = V("N");
v[8] = V("b");
v[9] = v[0] + v[1]*(1-v[2])*(1-v[3])/v[4] - v[5]*v[6]/v[4] + v[7]*v[8];

RESULT(v[9])

EQUATION("price_t")
/*
Price equation. Eq (4)
*/

v[0] = V("mu");
v[1] = V("wbarocc");
v[2] = V("xi");
v[3] = (1+v[0])*(v[1]/v[2]);


RESULT(v[3])

EQUATION("inflation")
/*
Inflation rate
*/

v[0] = VL("price_t",1);
v[1] = V("price_t");
v[2] = (v[1]-v[0])/v[0];

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

EQUATION("Q_t")
/*
GDP level
*/

v[0] = V("auton");
v[1] = V("mult");
v[2] = V("Q_fc");
v[3] = v[0]*v[1]; 

if (v[3] > v[2]) { // WARNING: Supply constraint
	v[3] = v[2];
} else {
	v[3] = v[3];
	}

RESULT(v[3])


EQUATION("K_t")
/*
Capital stock equation
*/

v[0] = V("delta");
v[1] = VL("K_t",1);
v[2] = V("I_t");
v[3] = (1-v[0])*v[1] + v[2];

RESULT(v[3])

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

RESULT(v[2])

EQUATION("EL_t")
/*
employed workers
*/

v[0] = V("N");
v[1] = V("Q_t");
v[2] = V("xi");
v[3] = v[1]/v[2];
v[4] = min(v[0],v[3]);

RESULT(v[4])

EQUATION("numocc")
/*
Number of occupied workers
*/
RESULT(V("EL_t"))


EQUATION("numOfActiveWorkers_t")
/*
Number of active workers
*/
RESULT(V("numocc"))

EQUATION("sizeunemployed")
/*
sizeunemployed
*/

v[0] = V("N");
v[1] = V("numocc");
v[2] = v[0] - v[1];

RESULT(v[2])

EQUATION("Un_t")
/*
Just for consistency reasons
*/
RESULT(V("sizeunemployed"))

EQUATION("unemploymentRatio_t")
/*
Unemployment ratio
*/

v[0] = V("sizeunemployed");
v[1] = V("N");
v[2] = v[0]/v[1];

RESULT(v[2])

EQUATION("A_t")
/*

*/

v[0] = V("Theta");
v[1] = V("pi");
v[2] = V("price_t");
v[3] = V("Q_t");
v[4] = (1-v[0])*(v[1]*v[2]*v[3]);

RESULT(v[4])

EQUATION("Pe_t")
/*
Equities price
*/

v[0] = VL("E_t",1);
v[1] = VL("W_t",1);
v[2] = V("tau_w");
v[3] = V("lambda");
v[4] = VL("V_t",1);
v[5] = V("I_t");
v[6] = V("price_t");
v[7] = V("A_t");
v[8] = 1+exp(-v[3]*v[4]);

v[9] = (1/v[0])*(v[1]*(1-v[2])/v[8]) - v[5]*v[6] + v[7];

if(v[9] <= 0){v[9]=1;}
	else{v[9] = v[9];}

RESULT(v[9])

EQUATION("E_t")
/*
Equities stock volume
*/

v[0] = VL("E_t",1);
v[1] = V("I_t");
v[2] = V("price_t");
v[3] = V("A_t");
v[4] = V("Pe_t");
v[5] = v[0] + (v[1]*v[2] - v[3])/(v[4]);

if (v[5] <= 0) {v[5]=0;}
	else{v[5]=v[5];}

RESULT(v[5])

///////////////////////////////////////// GOVERNMENT /////////////////////

EQUATION("Tax")
/*
Government tax revenue
*/

v[0] = V("tau_y");
v[1] = V("psi");
v[2] = V("Theta");
v[3] = V("pi");
v[4] = V("price_t");
v[5] = V("Q_t");
v[6] = V("tau_w");
v[7] = VL("W_t",1);
v[8] = v[0]*(v[1]+v[2]*v[3])*v[4]*v[5] + v[6]*v[7];

RESULT(v[8])

EQUATION("B_t")
/*
government budget
*/

v[0] = VL("B_t",1);
v[1] = V("Tax");
v[2] = V("price_t");
v[3] = 0;

CYCLE(cur, "Government")
{
v[4] = VS(cur, "b_it");
v[3] = v[3] + v[4];
}
v[5] = v[3]*v[2];
v[6] = v[0] + v[1] - v[5];

RESULT(v[6])

EQUATION("V_t")
/*
Comment
*/

v[0] = V("Theta");
v[1] = V("pi");
v[2] = V("price_t");
v[3] = V("Q_t");
v[4] = V("Pe_t");
v[5] = V("E_t");
v[6] = (v[0]*v[1]*v[2]*v[3])/(v[4]*v[5])

RESULT(v[6])



///////////////////////////////////// WORKERS /////////////////////////

EQUATION("y_it")
/*
disposable income of the workers
*/

v[0] = V("tau_y");
v[1] = V("w_it");
v[2] = VL("theta_it",1);
v[3] = V("Theta");
v[4] = V("pi");
v[5] = V("price_t");
v[6] = V("Q_t");
v[7] = V("ibar");
v[8] = VL("d_it",1);
v[9] = V("b_it");
v[10] = (1-v[0])*(v[1]+v[2]*v[3]*v[4]*v[5]*v[6]) - v[7]*v[8] + v[9]*v[5];

RESULT(v[10])

EQUATION("temp")
/*
savings of the workers
*/

v[0] = V("y_it");
v[1] = V("c_it");
v[3] = v[0] - v[1];

RESULT(v[3])

EQUATION("theta_it")
/*
Comment
*/

v[0] = V("W_it");
v[1] = V("W_t");
v[2] = v[0]/v[1];

RESULT(v[2])

EQUATION("E_it")
/*
Comment
*/

v[0] = V("theta_it");
v[1]=V("E_t");
v[2] = v[0]*v[1];

RESULT(v[2])

EQUATION("m_it")
/*
Comment
*/

v[0] = V("W_it");
v[1] = V("Pe_t");
v[2] = V("E_it");
v[3] = v[0] - v[1]*v[2];

RESULT(v[3])

EQUATION("c_it")
/*
Consumption
*/

v[0] = V("spsi");
v[1] = V("tau_y");
v[2] = V("w_it");
v[3] = VL("theta_it",1);
v[4] = V("Theta");
v[5] = V("pi");
v[6] = V("price_t");
v[7] = V("Q_t");
v[8] = V("eta");
v[9] = V("wb");
v[10]= V("sigma");
v[11]=V("tau_w");
v[12]=VL("W_it",1);
v[13]=V("b_it");
v[14]=V("phi");
v[15]=VL("d_it",1);
v[16] = (1-v[0])*(1-v[1])*(v[2] + v[3]*v[4]*v[5]*v[6]*v[7] + v[8]*(v[9]-v[2])) + (1-v[10])*(1-v[11])*v[12] + v[13]*v[6] - v[14]*v[15];

if(v[16] < 0){
v[16] = 0;} else {
	v[16]=v[16];}

RESULT(v[16])


EQUATION("state_b_it")
/*
Comment
*/

v[0] = V("temp");

if (v[0] <= 0) {
	v[1] = 1;} else {
	v[1]=0;}

RESULT(v[1])

EQUATION("numOfBorrowWorkers_t")
/*
Number of borrow workers
*/

v[0] = 0;

CYCLE(cur, "Goods")
	{
	v[1] = VS(cur, "state_b_it");
	v[0] = v[0] + v[1];
	}

RESULT(v[0])


EQUATION("shareOfBorrWorkers_t")
/*
Share of Borrowers
*/

v[0] = V("numOfBorrowWorkers_t");
v[1] = V("N");
v[2] = v[0]/v[1];

RESULT(v[2])


EQUATION("numOfNonBorrowWorkers_t")
/*
Number of non-borrow workers
*/

v[0] = V("numOfBorrowWorkers_t");
v[1] = V("N");
v[2] = v[1] - v[0];

RESULT(v[2])

EQUATION("shareOfNonBorrWorkers_t")
/*
Share of Non-Borrowers
*/

v[0] = V("numOfNonBorrowWorkers_t");
v[1] = V("N");
v[2] = v[0]/v[1];

RESULT(v[2])


EQUATION("state_it")
/*
the state of worker i at time t (Inactive =0,Active=1)
*/

v[0] = 0; // Min
v[1] = V("N"); //Max
v[2] = V("EL_t"); // i to be evaluated
v[3] = uniform_int(v[0], v[1]);

if (v[3]>= v[2]){ // Simular to: If agent is drawed out of employed range, Inactive = 0
	v[4] = 0;
	} else {
	v[4] = 1;}

RESULT(v[4])

EQUATION("b_it")
/*
Unemployment benefit
*/

v[0] = V("b"); // Benefit value
v[1] = V("state_it"); // employment state
v[2] = v[0]*(1-v[1]);

RESULT(v[2])

EQUATION("ynet_it")
/*
disposable income of employed workers
*/

v[0] = V("state_it");
v[1] = V("y_it");
v[2] = v[0]*v[1];

RESULT(v[2])

EQUATION("tru_it")
/*
Comment
*/

v[0] = V("mm");
v[1] = VL("W_it",1);
v[2] = V("tau_w");
v[3] = V("Pe_t");
v[4] = VL("Pe_t",1);
v[5] = VL("E_it",1);
v[6] = V("temp");
v[7] = VL("d_it",1);
v[8] = v[0]*v[1]*(1-v[2])+(v[3] - v[4])*v[5] + v[6] - v[7];

RESULT(v[8])

EQUATION("W_it")
/*
Comment
*/

v[0] = V("tru_it");
v[1] = VL("W_it",1);
v[2] = V("tau_w");
v[3] = V("Pe_t");
v[4] = VL("Pe_t",1);
v[5] = VL("E_it",1);
v[6] = V("temp");
v[7] = VL("d_it",1);
v[8] = V("mm");

if(v[0] > 0) {
	v[9] = v[1]*(1-v[2]) + (v[3] - v[4])*v[5] + v[6] - v[7];
	} else {
	v[9] = v[1]*(1-v[2])*(1-v[8]);
	}

RESULT(v[9])

EQUATION("hru_it")
/*
Comment
*/

v[0] = VL("d_it",1);
v[1] = V("mm");
v[2] = VL("W_it",1);
v[3] = V("tau_w");
v[4] = V("Pe_t");
v[5] = VL("Pe_t",1);
v[6] = VL("E_it",1);
v[7] = V("temp");
v[8] = v[0] - v[1]*v[2]*(1-v[3]) - (v[4]-v[5])*v[6] - v[7];

RESULT(v[8])

EQUATION("d_it")
/*
Comment
*/

v[0] = V("hru_it");

if(v[0] > 0){
	v[1] = v[0];	
	} else { v[1] = 0;}

RESULT(v[1])



/////////////////////// AGGREGATIVE EQUATIONS ///////////////////////


EQUATION("C_t")
/*
Aggregate comsumption
*/

v[0] = 0;

CYCLE(cur, "Consumers")
	{
	v[1] = VS(cur, "c_it");
	v[0] = v[0] + v[1];
	}

RESULT(v[0])

EQUATION("W_t")
/*
Total Wealth
*/

v[0] = 0;

CYCLE(cur, "Consumers")
	{
	v[1] = VS(cur, "W_it");
	v[0] = v[0] + v[1];
	}

RESULT(v[0])

EQUATION("Savings")
/*
Aggregate Savings
*/

v[0] = 0;

CYCLE(cur, "Consumers")
	{
	v[1] = VS(cur, "temp");
	v[0] = v[0] + v[1];
	}

RESULT(v[0])

EQUATION("Y_t")
/*
Total income
*/

v[0] = 0;

CYCLE(cur, "Consumers")
	{
	v[1] = VS(cur, "y_it");
	v[0] = v[0] + v[1];
	}

RESULT(v[0])

EQUATION("wb")
/*
Average wage
*/

v[0] = 0;
v[1] = V("N");

CYCLE(cur, "Consumers")
	{
	v[2] = VS(cur, "w_it");
	v[0] = v[0] + v[2];
	}

RESULT(v[0]/v[1])

EQUATION("wbarocc")
/*
Average wage of occupied
*/

v[0] = 0;
v[1] = V("numocc");

CYCLE(cur, "Consumers")
	{
	v[2] = VS(cur,"state_it");
	v[3] = VS(cur, "w_it");
	v[4] = v[2]*v[3];
	v[0] = v[0] + v[4];
	}

RESULT(v[0]/v[1])


EQUATION("D_t")
/*
Total debt
*/

v[0] = 0;

CYCLE(cur, "Banks")
	{
	v[1] = VS(cur, "d_it");
	v[0] = v[0] + v[1];
	}

RESULT(v[0])


MODELEND

// do not add Equations in this area

void close_sim( void )
{
	// close simulation special commands go here
}
