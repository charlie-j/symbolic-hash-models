dnl (* [WARNING] Following rules are kept to reproduce per-flattening strategy results of SIGMA but the new noFlat and withFlat functions defined in MDH_lib.m4 should be used now.*)
dnl (******* 4 arguments *)
dnl (*** 4 arguments with one being a pair (position-2): *)
ifdef(`3-2',`(* 3-2 *)
otherwise  forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring; MDH( (x1,x2,(x3,x4),x5) ) = H(x5,H(x4,H(x3,H(x2,H(x1,NIL)))))')dnl
ifdef(`4-2',`(* 4-2 *)
otherwise  forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring; MDH( (x1,x2,x3,(x4,x5)) ) = H(x5,H(x4,H(x3,H(x2,H(x1,NIL)))))')dnl
ifdef(`2-2',`(* 2-2 *)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring; MDH( (x1,(x2,x3),x4,x5) ) = H(x5,H(x4,H(x3,H(x2,H(x1,NIL)))))')dnl
ifdef(`1-2',`(* 1-2 *)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring; MDH( ((x1,x2),x3,x4,x5) ) = H(x5,H(x4,H(x3,H(x2,H(x1,NIL)))))')dnl
dnl
dnl (*** 4 arguments with one being a triple (position-3): *)
ifdef(`4-3',`(* 4-3 *)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring,x6:bitstring; MDH( (x1,x2,x3,(x4,x5,x6)) ) = H(x6,H(x5,H(x4,H(x3,H(x2,H(x1,NIL))))))')dnl
ifdef(`3-3',`(* 3-3 *)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring,x6:bitstring; MDH( (x1,x2,(x3,x4,x5),x6) ) = H(x6,H(x5,H(x4,H(x3,H(x2,H(x1,NIL))))))')dnl
ifdef(`2-3',`(* 2-3 *)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring,x6:bitstring; MDH( (x1,(x2,x3,x4),x5,x6) ) = H(x6,H(x5,H(x4,H(x3,H(x2,H(x1,NIL))))))')dnl
ifdef(`1-3',`(* 1-3 *)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring,x6:bitstring; MDH( ((x1,x2,x3),x4,x5,x6) ) = H(x6,H(x5,H(x4,H(x3,H(x2,H(x1,NIL))))))')dnl
dnl 
dnl (*** 4 arguments with 2 being a pair (positionX-2, positionY-2): *)
ifdef(`4-2+3-2',`(* 4-2, 3-2*)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring,x6:bitstring; MDH( (x1,x2,(x3,x4),(x5,x6)) ) = H(x6,H(x5,H(x4,H(x3,H(x2,H(x1,NIL))))))')dnl
ifdef(`4-2+2-2',`(* 4-2, 2-2*)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring,x6:bitstring; MDH( (x1,(x2,x3),x4,(x5,x6)) ) = H(x6,H(x5,H(x4,H(x3,H(x2,H(x1,NIL))))))')dnl
ifdef(`4-2+1-2',`(* 4-2, 1-2*)
otherwise forall x1:bitstring,x2:bitstring,x3:bitstring,x4:bitstring,x5:bitstring,x6:bitstring; MDH( ((x1,x2),x3,x4,(x5,x6)) ) = H(x6,H(x5,H(x4,H(x3,H(x2,H(x1,NIL))))))')dnl
