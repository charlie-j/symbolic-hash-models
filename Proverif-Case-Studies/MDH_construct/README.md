# General comments
To launch ProVerif:
```
make <name>=1 [assoc=1 | col=1]

```
where `<name>` can be `ike`, `ike_s` or `sigma`.

By default, the file is run without collision using the MD construction for hash function. When `col=1` then the protocol is verified while allowed Chosen Prefix Collision. When `assoc=1`, instead of using the MD construction, we use the library representing an associative symbol under the hash.

Run `benchmark.sh` to run all our experiments that are fully automated.

# How to model the capabilities of the lattice

We provide here a blueprint on how to model the different capabilities of the lattice.

### Output Type (OT)

#### AdvMsg

To encode the output type, we need consider a fresh private channel `hvalue` and
a public channel `c`. We need to transform the honest processes so that every time a hash is computed,
the hash value is output on the private channel `hvalue`. For example, in the file `sigma_HF_EC_declaration.pvl`,
the process `B` contains:
```
...
let transcript:bitstring = (gx,(infoA,(exp(g,y),infoB))) in
let ht:bitstring = buildH(transcript) in
if signCheck(s, pkA) && m = mac( pk2bs(pkA), k ) then
...
```
which would be modified into:
```
...
let transcript:bitstring = (gx,(infoA,(exp(g,y),infoB))) in
let ht:bitstring = buildH(transcript) in
out(hvalue,ht);
if signCheck(s, pkA) && m = mac( pk2bs(pkA), k ) then
...
```
Then in parallel to the process `System`, we can add the following process:
```
!
in(hvalue,h:bitstring);
in(c,x:bitstring);
event AdvType(h,x)
```
The event `AdvType` binds the output of the hash and a chosen value by the attacker.
An axiom is then
added to indicate that these two values are equal when testing the equalities of hashes:
```
axiom x,h:bitstring; event(AdvType(h,x)) ==> eq_hash(h,adv(x))
```
We also need to add some axioms to indicate that the attacker cannot bind multiple terms to
the same hash and vice-versa.
```
axiom x,x',h,h':bitstring;
  event(AdvType(h,x)) && event(AdvType(h',x')) && eq_hash(h,h') ==> x = x';
  event(AdvType(h,x)) && event(AdvType(h',x)) ==> eq_hash(h,h').
```

Note that some of the axioms in the libraries must be updated to make them compatible with
the occurrence of `adv(x)` in the predicate `eq_hash`. For example the axiom
```
axiom x1,x2,h1',h2,h2':bitstring; eq_hash(H(x1,h1'),h2) ==> h2 = H(x2,h2').
```
is updated into:
```
axiom x,x1,x2,h1',h2,h2':bitstring; eq_hash(H(x1,h1'),h2) ==> h2 = H(x2,h2') || h2 = adv(x).
```

#### AdvAtom

To encode that the attacker must chose an atomic value, it suffices to add the following axiom:
```
axiom x,h:bitstring; event(AdvType(h,x)) && not(is_var(x)) && not(is_name(x)) ==> false.
```

### Length Extension (LE)

The library using the MD construct already consider Length extension. To remove it, we can
encode eq_hash(H(x),H(y)) as the equality of x and y with an associative pair symbol. We provide
the library `assoc_no_collision.pvl` that shows how to encode equality modulo an associative symbol
through the predicate `eq_assoc`.
```
pred eq_assoc(bitstring,bitstring) [block].
pred eq_hash(bitstring,bitstring) [block,evalGround=ground_eq_hash].
```
For instance, we consider the axiom:
```
axiom l1,l2:bitstring;
  eq_hash(H(l1),H(l2)) ==> eq_assoc(l1,l2)
  [forcedRemove]
.
```
The option `[forcedRemove]` typically remove the predicates in the premisses of the axioms for the clauses (to avoid generating too large clauses).
The associativity is handle by using a flattening computation function similar to the one used in the MD construct:
```
compfun flatten(bitstring):bitstring =
  forall x:bitstring; flatten(x) if is_var(x) || x = Nil -> x
  otherwise forall l1,l2,l3:bitstring; flatten((CPcol1(l1,l2),l3)) -> (CPcol1(flatten(l1),flatten(l2)),flatten(l3))
  otherwise forall l1,l2,l3:bitstring; flatten((CPcol2(l1,l2),l3)) -> (CPcol2(flatten(l1),flatten(l2)),flatten(l3))
  otherwise forall x1,x2,l:bitstring; flatten(((x1,x2),l)) -> flatten((x1,(x2,l)))
  otherwise forall x,l:bitstring; flatten((x,l)) -> (x,flatten(l))
  [mayFail]
.
```
Notice the presence of `CPcol1` and `CPcol2` that are included so in the prospect to add a library with Chosen Prefix
collision but without length extension.

### Collisions

We already showed how to encode Chosen Prefix collision. For identical-prefix collisions, we can rely on two functions `SPcol1(l)` and `SPcol2(l)` in a similar fashion. As previously, axioms must be updated to correspond to the targeted property.
For example, in `hash_collision.pvl`, we consider the following axiom with the MD construct:
```
eq_hash_col(H(CPcol1(h1',h2'),h1),H(u2,h2)) && not(is_var(u2)) ==>
  (u2 = CPcol1(h1'',h2'') && eq_hash(h1',h1'') && eq_hash(h2',h2'') && eq_hash_col(h1,h2)) ||
  (u2 = CPcol2(h1'',h2'') && eq_hash(h1,h1') && eq_hash(h1',h1'') && eq_hash(h2,h2') && eq_hash(h2',h2''));
```
With identical-predix collisions, such axioms would be updated into:
```
eq_hash_col(H(SPcol1(h1),h1'),H(u2,h2)) && not(is_var(u2)) ==>
  (u2 = SPcol1(h1'') && eq_hash(h1,h1'') && eq_hash_col(h1',h2)) ||
  (u2 = SPcol2(h1'') && eq_hash(h1,h1'') && eq_hash(h1',h2) && eq_hash(h1,h1'));
```
