dnl ### This file defines several macros to produce MDH theories
include(`foreach.m4')dnl
include(`forloop.m4')dnl
include(`stack.m4')dnl
include(`stack_sep.m4')dnl
include(`foreach.m4')dnl
dnl showRP helping function
define(`showRP', `)')dnl
dnl
dnl ## withFlat function takes 3 integers as arguments: number of MDH arguments, position of the collapse, size of the tuple being collapsed
define(`withFlat',`dnl
define(`nAll',eval(`$1+$3-1'))dnl
undefine(`ALL')undefine(`Middle')undefine(`Left')undefine(`Right')dnl
define(`ALL',     forloop(`i', `1',            eval(nAll+1),    `pushdef(`ALL',`x'i)'))dnl
define(`Middle',  forloop(`i', $2,             eval($2+$3),     `pushdef(`Middle',`x'i)'))dnl
define(`Left',    forloop(`i', `1',            eval($2),        `pushdef(`Left',`x'i)'))dnl
define(`Right',   forloop(`i', eval($2+$3),    eval(nAll+1),    `pushdef(`Right',`x'i)'))dnl
popdef(`ALL')popdef(`Middle')popdef(`Left')popdef(`Right')dnl			 
ifelse($2,`1',`dnl
dnl need to collapse first argument!
otherwise forall stack_foreach_sep(`ALL', `', `:bitstring', `,');
  MDH( ((stack_foreach_sep(`Middle',`',`',`,')), stack_foreach_sep(`Right',`',`',`,')) ) =
  H(stack_foreach_sep_lifo(`ALL', `',  `', `,H('),NIL stack_foreach(`ALL',`showRP')
',`dnl
ifelse($2,$1,`dnl
dnl need to collapse last  argument!
otherwise forall stack_foreach_sep(`ALL', `', `:bitstring', `,');
  MDH( (stack_foreach_sep(`Left',`',`',`,'), (stack_foreach_sep(`Middle',`',`',`,')) )) =
  H(stack_foreach_sep_lifo(`ALL', `',  `', `,H('),NIL stack_foreach(`ALL',`showRP')
',`dnl
dnl need to collapse argument strictly in the middle
otherwise forall stack_foreach_sep(`ALL', `', `:bitstring', `,');
  MDH( (stack_foreach_sep(`Left',`',`',`,'), (stack_foreach_sep(`Middle',`',`',`,')), stack_foreach_sep(`Right',`',`',`,')) ) =
  H(stack_foreach_sep_lifo(`ALL', `',  `', `,H('),NIL stack_foreach(`ALL',`showRP')
')')')dnl
define(`flat2',`dnl
withFlat($1,$2,`2')dnl
')dnl
define(`flat3',`dnl
withFlat($1,$2,`3')dnl
')dnl
define(`flat4',`dnl
withFlat($1,$2,`4')dnl
')dnl
define(`flat5',`dnl
withFlat($1,$2,`5')dnl
')dnl
define(`flat6',`dnl
withFlat($1,$2,`6')dnl
')dnl
dnl
dnl ## flatAll takes the number of arguments as 1st argument and the min size of collapsed tuple as second argument and considers all possibilities of flattening with collapsed tuples of size $2 <= $3
define(`flatAll',`dnl
forloop(`loop_i', `1', $1,`dnl argument of the collapse position
(* Position of the argument: loop_i. *)
forloop(`loop_j', $3, $2,`dnl size of the tuple being collapsed
(* Tuple being flattened of size: loop_j. *) withFlat($1,loop_i,loop_j)')
')')dnl
dnl
dnl ## noFlat function: takes one integer as argument: the number of MDH arguments
define(`happyFlow',`dnl
undefine(`LA')dnl
define(`LA',forloop(`i', `1', eval($1+1), `pushdef(`LA',`x'i)'))dnl
popdef(`LA')dnl
otherwise forall stack_foreach_sep(`LA', `', `:bitstring', `,');
  MDH( (stack_foreach_sep(`LA',`',`',`,')) ) =
  H(stack_foreach_sep_lifo(`LA', `',  `', `,H('),NIL stack_foreach(`LA',`showRP')')dnl
