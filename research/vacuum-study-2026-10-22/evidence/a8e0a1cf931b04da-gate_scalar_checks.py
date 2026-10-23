"""One bounded exact-rational check of written scalar inequalities; no field."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json

checks = []
def check(name, ok, detail):
    checks.append({'name': name, 'pass': bool(ok), 'detail': detail})

delta = F(1, 10**11)
taylor = F(9, 1000) * F(11, 140)**6 / 720
selection = F(1, 2**70)
epsilon = F(1, 500000)
raw = delta*(126240+480000*delta)
check('eta_upper_squared', F(273,1) < F(81,4)**2,
      'sqrt(273)<81/4 gives eta<9/100')
check('eta_lower_squared', F(273,1)>16**2,
      'sqrt(273)>16 gives eta>2/25')
check('Machin_width', F(16,513*5**513)+F(4,513*239**513)<F(1,2**1000),
      '256 terms; outward alternating-series remainder')
check('eta_width', F(273,2500)*F(25,4)+2 <3,
      'outer interval width less than3*2^-256')
check('trig_remainder', F(4**81,factorial(81))<F(1,2**160),
      'degree80 for both sin and cos on[-4,4]')
check('coefficient_selection_sum', F(6,2**76)<selection,
      'six coefficient errors below2^-76 each')
check('full_slope_radius', taylor+selection<delta,
      {'spatial':str(taylor),'selection':str(selection),'delta':str(delta)})
check('constitutive_factor', F(20,7)**2*F(21,5)<36,
      'A*t/sqrt(mD)<6')
constant = 6*400+12*F(18,1000)*400**2/4+12*F(3,10)*400**3/(4*500)
check('G_error_constant', constant==126240, str(constant))
check('G_error_bound', raw<epsilon, {'raw':str(raw),'epsilon':str(epsilon)})
screen = epsilon+4*epsilon**2
check('exact_screen_identity',screen==F(125001,62500000000),str(screen))
check('exact_screen',screen<1,str(screen))
loss = epsilon+8*epsilon**2+F(1,100000)
check('theta1_alpha_necessary_V_condition',loss<1,str(loss))
check('advisory_scale_only',epsilon/F(3,100)==F(1,15000),
      'Not a bound on combined event correction')
record={'scope':'Scalar rational identities in GATE-PROOF only; no coefficient array,field,mesh,matrix,eigen/native/projecttest',
        'checks':checks,'all_pass':all(c['pass'] for c in checks)}
Path(__file__).with_name('GATE-SCALAR-CHECKS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_pass':record['all_pass']}))
raise SystemExit(0 if record['all_pass'] else 1)
