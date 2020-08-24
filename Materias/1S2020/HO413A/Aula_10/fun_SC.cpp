//#define EIGENLIB			// uncomment to use Eigen linear algebra library
//#define NO_POINTER_INIT	// uncomment to disable pointer checking

#include "fun_head_fast.h"

// do not add Equations in this area

MODELBEGIN

// insert your equations here, between the MODELBEGIN and MODELEND words

EQUATION("ProdUsed")
/*
Produto usado pelo consumidor em t
*/

v[0] = V("IsBroken");

if ( v[0] == 0 )		// produto não quebrou?
	v[1] = VL("ProdUsed", 1);
else
	v[1] = V("Purchase");
	
RESULT( v[1] )


EQUATION("Purchase")
/*
Escolha de produto do usuário em t
*/

cur = RNDDRAW("Firm", "Visibility");
v[0] = VS(cur, "IdFirm");

V("InitTrade");			// garante que  Sales e NumLost tenha sido zerados
INCRS(cur, "Sales", 1);

RESULT( v[0] )


EQUATION("InitTrade")
/*
Inicializa o mercado a cada período t para Sales e NumLost
*/

CYCLE(cur, "Firm")
{
	WRITES(cur, "Sales", 0);
	WRITES(cur, "NumLost", 0);
}

RESULT( 1 )


EQUATION("IsBroken")
/*
Verifica se o produto atual quebrou ou não
*/

v[0] = VL("ProdUsed", 1);		// produto em uso
cur = SEARCH_CND("IdFirm", v[0]);		// ponteiro para a firma que produziu
v[1] = VS(cur, "BD");				// qualida do produto uso

if ( uniform(0, 1) < v[1] )		// o produto quebrou?
{
	v[2] = 1;
	
	V("InitTrade");			// garante que  Sales e NumLost tenha sido zerados
	INCRS(cur, "NumLost", 1);	// atualiz o número de clientes perdidos da firma
}
else
	v[2] = 0;

RESULT( v[2] )


EQUATION("NumUsers")
/*
Número líquido de usuários do produto da firma em t
*/

V("EndTrade");		// garatir que todos os usuários tenham escolhido em t

v[0] = VL("NumUsers", 1);	// número anterior de usuários
v[1] = V("Sales");				// vendas da firm em t
v[2] = V("NumLost");			// clientes perdidos em t

v[3] = v[0] + v[1] - v[2];

RESULT( v[3] )


EQUATION("EndTrade")
/*
Garante que todos os consumidores tenha escolhido produto em t
*/

CYCLE(cur, "Consumer")
	VS(cur, "ProUsed");

RESULT( 1 )


EQUATION("ms_user")
/*
Market share da firma em numero de usuários em t
*/

v[0] = V("NumUsers");
v[1] = V("TotalUsers");

v[2] = v[0] / v[1];

RESULT( v[2] )


EQUATION("Visibility")
/*
Visibilidade da firma em t
*/

v[0] = V("alpha");
v[1] = VL("ms_user", 1);

if ( v[1] == 0 )
	v[2] = 0;
else
	v[2] = pow( v[1], v[0] );

RESULT( v[2] )


EQUATION("Init")
/*
Inicializa o modelo
*/

cur = SEARCH("Demand");		// ponteiro para o pai dos objetos Consumer
v[0] = V("TotalUsers");		// quantidade de objetos Consumer
ADDNOBJS(cur, "Consumer", v[0] - 1);	// cria n-1 objetos

CYCLES(cur, cur1, "Consumer")
{
	v[1] = VS(cur1, "Purchase");
	WRITELS(cur1, "ProdUsed", v[1], T - 1);	// produto ativo em t=0
}

PARAMETER;			// transforma Init em parâmetro

RESULT( 1 )


MODELEND

// do not add Equations in this area

void close_sim( void )
{
	// close simulation special commands go here
}
