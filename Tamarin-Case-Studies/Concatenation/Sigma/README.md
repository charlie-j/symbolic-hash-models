
We developped three ways to model the hash function.

Remark that we use an associative builtin symbol `cons`, cf. [git](https://projects.cispa.saarland/cc/tamarin-prover/-/tree/feature-assoc-concat).

# Hash Function, Excpliti Capabilities - HF_EC

The hash funciton is simply a unary function symbol `hash`. Then, we add new explicit capabilites to the attacker by giving new equations. For instance, I used :
```
equations:  hash(cons(x,cons(CP1(x,y),l))) = coll(x,y,l),  hash(cons(x,cons(CP2(x,y),l)))=coll(x,y,l)
```
This equations captures at the same time Chosen-Prefix Collision resistance and length extensions. It however tends to greatly reduce automation. Some benchs/optimizations are needed to see if it can be of any use.

I also used the incomplete following set of equations that follows to model CP + LE:
```
equations: IH(cons(x,CP1(x,y))) = IH(cons(y,CP2(x,y))), hash(cons(x,y)) = IH(cons(IH(x),y))
```
This one allowed me to get the attack `sigma_HF_EC-CPcoll-pref-A-to-B.png`.
Yet, as I said, it is incomplete. Indeed, the formula `hash(cons(x,y)) = IH(cons(IH(x),y))` does not specify that for instance `hash(cons(x,cons(y,z))) = IH(cons(IH(x),cons(IH(y),z)))`.

# Hash Event Based, Explicit Capabilities - HEB_EC


The Hash Value is accessed in a rule by adding the event `HashC(valuetohash,~hash)`.

`HashC` event are linked to the definition of the hash value with the following restriction:

```
restriction isHash: // and inside the process, HashC allows to bind ~n to the hash value
"
All x n #i. HashC( x , n)@i ==> Ex #j. HashE(x,n)@j
"
```
Then, a rule allows to instantiate valid hashes:
```
rule newHash: // We may at any point create the value of a hash (with x unbound)
 [ Fr(~n)]--[HashE(x,~n)]->[]
```

As is, this emulates a ROM (remark that we also in theory need to add the fact that the hash is a funciton, i.e. maps an input value to a single output value.


## Any collisions

This is done with the following rule:
```
rule FullColl: // We can make everything collides, which breaks the properties
 [ Fr(~n)]--[HashE(x,~n), HashE(y,~n)]->[]
 ```

## Chosen Prefix Collisions
For any prefix `p1` and `p2`, there exists suffixes `~m1` and `~m2` that form a collision.

(the LE fact is used to link with the length extension attack)

```
rule CPHash:
   [In(<p1,p2>),Fr(~m1),Fr(~m2),Fr(~n)]--[CP(),
   HashE(cons(p1,~m1),~n), HashE(cons(p2,~m2),~n)]->[
   Out(<~m1,~m2,~n>), LE(~n,cons(p1,~m1),cons(p2,~m2))]

restriction CP:
"
All #i #j. CP()@i & CP()@j ==> #i = #j
"
```

For simplicity of proof searching, we only allow a single CP computation by the attacker.

## Length extensions attacks

A collision produced via chosen prefix can be extended with a common suffix.

```
rule newHashLengthExtension:
 [ LE(~m,x,y), Fr(~n)]--[HL(), HashE(cons(x,z),~n), HashE(cons(y,z),~n)]->[]

restriction SingExt:
"
All #i #j. HL()@i & HL()@j ==> #i = #j
"
```


# Hash Event Based, Axioms - HEB_A

The Hash Value is accessed in a rule by adding the event `HashC(valuetohash,hash)`. We put not other restriction by default, leaving all liberty to the attacker.

--> Remark that in general, we should use  `HashC(valuetohash,$hash)`, otherwise the attacker can compute anything. But in Sigma, the `hash` is only under a sign, and is thus hidden, and we don't give any attacker hash computation capabilities.

## No collisions

We can forbid any collisions with:

```
restriction noColl:
"
All x1 x2 n1 n2 #i #j. HashC(x1 ,n1)@i & HashC(x2, n2)@j  & n1 = n2 ==> x1=x2
"
```

## Chosen Prefix+ length extension

If two hashes are equal, either they correspond to the same input, or they correspond to a chosen prefix collision, with some continuation. The unchosen part in the CP collision is modelled with two functions symbols `col1` and `col2`.  Then, given two prefixes `p1` and `p2`, and a common suffix `l`, there exists collisions between messages of the form `cons(cons(p1,col1(p1,p2)),l)` and `cons(cons(p1,col2(p1,p2)),l)`.

It corresponds to the restriciton:
```
// x1 and x2 have the same hash value only if
//     0) they are equal
//     1) they are of both the form x = cons(p,l), with l some attacker unchosen value
//     2) they are a length extension
restriction noCollS:
"
All x1 x2 h1 h2 #i #j. HashC(x1 ,h1)@i & HashC(x2, h2)@j & h1 = h2 & i < j ==>
     (x1 = x2) |
//    (Ex p1 p2. x1 = cons(p1,col1(p1,p2)) &  x2 = cons(p2,col2(p1,p2)))      |
    (Ex p1 p2 l #k. x1 = cons(cons(p1,col1(p1,p2)),l) &  x2 = cons(cons(p2,col2(p1,p2)),l) & Token(p1,p2)[+]@k)
"
// The token is used to limit to one CPcol compution

rule Tok:
 [In(<p1,p2>)]--[Token(p1,p2)]->[]

restriction singToken:
"
All p1 p2 p3 p4 #i #j. Token(p1,p2)@i & Token(p3,p4)@j ==> #i =#j

"
```

We add the Token to only allow one CP collision computation.


# Comparison

 * HF_EC is very slow.
 * HEB_A and HEB_EC both seems to run in a reasonnable time (5 minutes to break secB in HEB_A, and 15 for HEB_EC). They are also both very useful to see in a single glance what is the CP collision computed.
