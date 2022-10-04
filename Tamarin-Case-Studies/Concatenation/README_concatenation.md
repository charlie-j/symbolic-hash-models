# Concatenation

Concat (||) is an associative operator that has no neutral element and that is not commutative.  It allows to model concatenation of bitstrings of arbitrary length.

Because the length are abstracted, there is no projection operator allowing to deconstruct inside a protocol `x||y` and obtain `x`, as we do not know the length of `x`. However, if the attacker obtains `x||y`, it can of course obtain `x` and `y`.

It is not recommended to use this operator for pattern matching inside the inputs, as its semantics is unclear. However, it come sin handy under a hash function to build a hash transcript from concatenation.

See the file `Example_comcat.spthy` to see it in action.

# WARNING

Using this operator is not complete, as maude may return a subset of the unifiers (as there may be infinitely many). Currently, Tamarin dies when maude gives such warning. If this happens, you should either stop using the operator, or find ways to reduce the possible set of unifiers, for instance specifying that some of the concatenated elements cannot themselves be concatenations.

# Neutral element

A neutral element can be added to the equational theory in a classical fashion, with:
```
functions: nill/0

equations: nill ||x = x, x||nill  =x
```
However, this may imply a huge loss of performances, or many termination failures.


# DEPRECATED bellow
# Pair
If we make pair associative, we get a lot of maude warnings. But, for attack finding, we can disable them.

Further, false attacks seem to appaer, for instance on `examples/csf12/JKL_TS1_2008_KI.spthy`. Here, the events `SidI(k1,k2,k)` and `SidR(k1,k2,k)` are raised, where k1 and k2 are local keys, and k the derived key. If the attacker can know `k` of an `SidI(k1,k2,k)`, a session reveal must have happened on some `SidR(k1,k2,k)` that leaked the `k`.  But with `k1 = <t1,t2> ` and `k2=t3` and `k1=t1` and `k2=<t2,t3>`, this property becomes broken. But that is only because it is not two arguments `k1,k2` in the event that should be used to link sessions together in the event, but a single `<k1,k2>`
Trying


Similar issue with NAXOS_eCK_private, essentially, all complciated secrecy queries are broken. And fixing them does not raise new attacks
