SIGMA no assoc, no col: running...

real	0m18.722s
user	0m18.689s
sys	0m0.032s
RESULT not event(acceptB(B,A,x)) is false.
RESULT event(acceptB(B,A,x)) ==> event(initA(A,B,x)) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x)) ==> event(initB(B,A,x)) || event(Dishonest(A)) || event(Dishonest(B)) is true.
RESULT event(acceptB(B,A,x)) ==> event(initA(A,B',x)) || event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(sessionKeyA(B,A,x)) && attacker(x) ==> event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(sessionKeyB(B,A,x)) && attacker(x) ==> event(Dishonest(B)) || event(Dishonest(A)) is true.
\nSIGMA with assoc, no col: running...

real	0m27.768s
user	0m27.733s
sys	0m0.033s
RESULT not event(acceptB(B,A,x)) is false.
RESULT event(acceptB(B,A,x)) ==> event(initA(A,B,x)) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x)) ==> event(initB(B,A,x)) || event(Dishonest(A)) || event(Dishonest(B)) is true.
RESULT event(acceptB(B,A,x)) ==> event(initA(A,B',x)) || event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(sessionKeyA(B,A,x)) && attacker(x) ==> event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(sessionKeyB(B,A,x)) && attacker(x) ==> event(Dishonest(B)) || event(Dishonest(A)) is true.
\nSIGMA with assoc, with col: running...

real	0m17.079s
user	0m16.950s
sys	0m0.125s
RESULT not event(acceptB(B,A,x)) is false.
RESULT event(acceptB(B,A,x)) ==> event(initA(A,B,x)) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x)) ==> event(initB(B,A,x)) || event(Dishonest(A)) || event(Dishonest(B)) is false.
RESULT event(acceptB(B,A,x)) ==> event(initA(A,B',x)) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(sessionKeyA(B,A,x)) && attacker(x) ==> event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(sessionKeyB(B,A,x)) && attacker(x) ==> event(Dishonest(B)) || event(Dishonest(A)) is false.
\nSimplified IKE no assoc, no col: running...

real	0m6.379s
user	0m6.289s
sys	0m0.089s
RESULT event(acceptB2(B,A,sA)) ==> event(initA2(A,sA)) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptB(B,A,x,y,t,h)) ==> (event(initA(A,B',x',y',t',h')) && eq_hash(t,t')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT event(acceptB(B,A,x,y,t,h)) ==> (event(initA(A,B',x',y',t',h')) && eq_hash(h,h')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT not event(SanityA(true,x)) is false.
RESULT not event(SanityA(false,x)) is false.
RESULT not event(SanityB(true,x)) is false.
RESULT not event(SanityB(false,x)) is false.
\nSimplified IKE with assoc, no col: running...

real	0m6.811s
user	0m6.702s
sys	0m0.106s
RESULT event(acceptB2(B,A,sA)) ==> event(initA2(A,sA)) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptB(B,A,x,y,t,h)) ==> (event(initA(A,B',x',y',t',h')) && eq_hash(t,t')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT event(acceptB(B,A,x,y,t,h)) ==> (event(initA(A,B',x',y',t',h')) && eq_hash(h,h')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT not event(SanityA(true,x)) is false.
RESULT not event(SanityA(false,x)) is false.
RESULT not event(SanityB(true,x)) is false.
RESULT not event(SanityB(false,x)) is false.
\nSimplified IKE with assoc, with col: running...

real	3m9.842s
user	3m8.378s
sys	0m1.415s
RESULT event(acceptB2(B,A,sA)) ==> event(initA2(A,sA)) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptB(B,A,x,y,t,h)) ==> (event(initA(A,B',x',y',t',h')) && eq_hash(t,t')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT event(acceptB(B,A,x,y,t,h)) ==> (event(initA(A,B',x',y',t',h')) && eq_hash(h,h')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT not event(SanityA(true,x)) is false.
RESULT not event(SanityA(false,x)) is false.
RESULT not event(SanityB(true,x)) is false.
RESULT not event(SanityB(false,x)) is false.
\nIKE no assoc, no col: running...

real	0m15.157s
user	0m15.019s
sys	0m0.137s
RESULT event(acceptB(B,A,x,y)) ==> event(initA(A,B,x,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x,y)) ==> event(initB(B,A,x,y')) || event(Dishonest(A)) || event(Dishonest(B)) is true.
RESULT event(acceptB(B,A,x,y)) ==> event(initA(A,B',x,y')) || event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(acceptB(B,A,x,y)) ==> (event(initA(A,B,x,y')) && eq_hash(y,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x,y)) ==> (event(initB(B,A,x,y')) && eq_hash(y,y')) || event(Dishonest(A)) || event(Dishonest(B)) cannot be proved.
RESULT event(acceptB(B,A,x,y)) ==> (event(initA(A,B',x,y)) && eq_hash(y,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(sessionKeyA(B,A,k)) && attacker(k) ==> event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(sessionKeyB(B,A,k)) && attacker(k) ==> event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptB2(B,A,x,y,h)) ==> (event(initA2(A,B',x',y',h')) && eq_hash(h,h')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT not event(SanityA(x)) is false.
RESULT not event(SanityB(x)) is false.
\nIKE with assoc, no col: running...

real	0m22.033s
user	0m21.751s
sys	0m0.281s
RESULT event(acceptB(B,A,x,y)) ==> event(initA(A,B,x,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x,y)) ==> event(initB(B,A,x,y')) || event(Dishonest(A)) || event(Dishonest(B)) is true.
RESULT event(acceptB(B,A,x,y)) ==> event(initA(A,B',x,y')) || event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(acceptB(B,A,x,y)) ==> (event(initA(A,B,x,y')) && eq_hash(y,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x,y)) ==> (event(initB(B,A,x,y')) && eq_hash(y,y')) || event(Dishonest(A)) || event(Dishonest(B)) cannot be proved.
RESULT event(acceptB(B,A,x,y)) ==> (event(initA(A,B',x,y)) && eq_hash(y,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(sessionKeyA(B,A,k)) && attacker(k) ==> event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(sessionKeyB(B,A,k)) && attacker(k) ==> event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptB2(B,A,x,y,h)) ==> (event(initA2(A,B',x',y',h')) && eq_hash(h,h')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT not event(SanityA(x)) is false.
RESULT not event(SanityB(x)) is false.
\nIKE with assoc, with col: running...

real	3m6.363s
user	3m6.011s
sys	0m0.329s
RESULT event(acceptB(B,A,x,y)) ==> event(initA(A,B,x,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x,y)) ==> event(initB(B,A,x,y')) || event(Dishonest(A)) || event(Dishonest(B)) is true.
RESULT event(acceptB(B,A,x,y)) ==> event(initA(A,B',x,y')) || event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(acceptB(B,A,x,y)) ==> (event(initA(A,B,x,y')) && eq_hash(y,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptA(A,B,x,y)) ==> (event(initB(B,A,x,y')) && eq_hash(y,y')) || event(Dishonest(A)) || event(Dishonest(B)) cannot be proved.
RESULT event(acceptB(B,A,x,y)) ==> (event(initA(A,B',x,y)) && eq_hash(y,y')) || event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(sessionKeyA(B,A,k)) && attacker(k) ==> event(Dishonest(B)) || event(Dishonest(A)) is true.
RESULT event(sessionKeyB(B,A,k)) && attacker(k) ==> event(Dishonest(B)) || event(Dishonest(A)) is false.
RESULT event(acceptB2(B,A,x,y,h)) ==> (event(initA2(A,B',x',y',h')) && eq_hash(h,h')) || event(Dishonest(B)) || event(Dishonest(A)) cannot be proved.
RESULT not event(SanityA(x)) is false.
RESULT not event(SanityB(x)) is false.
\nAll log files:
LOG_ike_assoc.txt
LOG_ike_col.txt
LOG_ike_no.txt
LOG_ikeS_assoc.txt
LOG_ikeS_col.txt
LOG_ikeS_no.txt
LOG_sigma_assoc.txt
LOG_sigma_col.txt
LOG_sigma_no.txt
