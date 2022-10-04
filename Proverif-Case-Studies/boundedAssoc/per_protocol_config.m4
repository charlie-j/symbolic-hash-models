dnl ### This file contains protocol-specific configuration for the MDH theory: size of the list under a hash and size of nested tuples that need to be flattened. It uses macros defined in MDH_lib.pvl.
dnl # Number of arguments under hash in the happy flow
define(`nbArgs',`dnl
ifdef(`M_IKE',7)dnl
ifdef(`M_IKE_S',6)dnl
ifdef(`M_SIGMA',4)dnl
')dnl
dnl # Maximum size of the nested tuple that needs to be flattened (should be >= number of items stuffed in +1)
define(`maxSizeTuples',`dnl
ifelse(allFlat,`',`dnl
ifdef(`M_IKE',4)dnl
ifdef(`M_IKE_S',3)dnl
ifdef(`M_SIGMA',3)dnl
', `allFlat')')dnl
dnl
dnl # Minimum size of the nested tuple that needs to be flattened (should be <= number of items stuffed in)
define(`minSizeTuples',`dnl
ifelse(allFlat,`',`2',`allFlat')')dnl
dnl
(******* The number of arguments that is suitable for analyzing a protocol depends on the number of arguments given to MDH by honest agents.
Here it is nbArgs. Collapse tuples of size minSizeTuples <= size <= maxSizeTuples *)
fun MDH(bitstring):bitstring
reduc forall x:bitstring; MDH( NIL ) = NIL
dnl
(***** LIST FLATTENING *)
ifdef(`noFlat',`(* No flattening! *)',`dnl
ifdef(`allFlat',`(* All flattening for nbArgs arguments and collapsed tuples of size <= maxSizeTuples: *)
ifdef(`M_IKE',`(* For IKE v2: 7 arguments: *)
flatAll(nbArgs,maxSizeTuples,minSizeTuples)
flatAll(eval(nbArgs-1),maxSizeTuples,minSizeTuples)
')dnl
ifdef(`M_IKE_S',`(* For simplified IKE v2: 5 arguments: *)
flatAll(nbArgs,maxSizeTuples,minSizeTuples)
flatAll(eval(nbArgs-1),maxSizeTuples,minSizeTuples)
dnl flatAll(nbArgs,maxSizeTuples,minSizeTuples)
dnl flatAll(eval(nbArgs-1),maxSizeTuples,minSizeTuples)
dnl (* TARGET FLAT *)
dnl withFlat(`6',1,2)
dnl withFlat(`5',1,3)
')dnl
ifdef(`M_SIGMA',`(* For SIGMA: 4 arguments. *)
flatAll(nbArgs,maxSizeTuples,minSizeTuples)')')dnl
include(`target_flat_sigma.m4')dnl
')dnl

(***** HAPPY FLOW *)
ifdef(`M_IKE',`(* For IKE v2: 7 arguments (transcriptA): *)
happyFlow(nbArgs)
(* and also 6 arguments (transcriptB): *)
happyFlow(eval(nbArgs-1))
')dnl
ifdef(`M_IKE_S',`(* For simplified IKE v2: 5 arguments (transcriptA): *)
happyFlow(nbArgs)
(* and also 4 arguments (transcriptB): *)
happyFlow(eval(nbArgs-1))
')dnl
ifdef(`M_SIGMA',`(* For SIGMA: 4 arguments. *)
happyFlow(nbArgs)
')dnl
dnl
