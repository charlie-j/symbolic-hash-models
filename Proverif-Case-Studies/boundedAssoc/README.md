# General comments
We use a Makefile to handle M4-based pre-processing and to select the right M4 options based on the chosen protocol and model. The M4 options we use are described in `pretty.m4`.
We used the development version of ProVerif hosted at `git@gitlab.inria.fr:bblanche/proverif.git`, branch `master`, commit hash `0115ba5d6e3f`.
We ran our analyses on a Intel(R) Core(TM) i7-8550U CPU @ 1.80GH, Ubuntu 20.04, 16GB of RAM.

# SIGMA protocol
The main file is sigma_CP_bound.pv. It uses some M4 pre-processing.

To launch ProVerif:
```
make sigma=1 m4="-D <options>" 

```
where options are labels listed in pretty.md. For instance, use `make m4="-D noFlat -D noCol"` to check all properties without any list flattening or collision. By list flattening we mean that nested tuples are "flattened" into a normal form modulo; e.g., `MDH( (x1,(x2,x3),x4,x5) )` reduces to `H(x5,H(x4,H(x3,H(x2,H(x1,NIL)))))`.

The most powerful attacker and the default choice for attack finding can be obtained with `make sigma=1 m4="-D allFlat"`.
To restrict the size of the tuples being collapsed to a given size `size`, use `make sigma=1 m4="-D allFlat=size"`.

The results are listed and discussed in the paper.
Properties:
 - Auth(A->B) authentication of B from A's POV + agreement on transcript,
 - Auth(B->A) authentication of A from B's POV + agreement on transcript,
 - SecKey(A) secrecy of A's session key,
 - SecKey(B) secrecy of B's session key.

## Reflection attack
Command: `make sigma=1 m4="-D noFlat -D noCol -D refl -D noRole"`. <1s.
Auth(A->B) is violated due to a reflection attack where the attack just reflects back A's messages to itself. This attack requires A to accept to launch a session with himself but this leads to a reflection attack and a confusion on the role (lack of agreement on the peer's role). It is hard to think of a use case where this attack could be exploited.
Fix: check that pkA <> pkB or add role under the signature. Either option works (try to remove one of the two last options).

## Simple CPC attack
Command: `make sigma=1 m4="-D noFlat -D noRole"`. <1s.
Auth(A->B) is violated due to a MiM attacking two initiators A_1 and A_2 and using a collision attack on infoA_1 and infoA_2 that enables the attacker to make A_1 and A_2 believe that they are communicating with responders B_1 and B_2 respectively while they are connected to another initiator of the wrong identity (respectively A_1 and A_2). This attack breaks the agreement on the role and unilateral authentication (both ways).
To the best of our knowledge, this attack is new and has not been documented elsewhere.
Fix: authenticate the role by including the role under the signature. Try without the last option.

## Hash transcript attack based on a CPC [1]
Command: `make sigma=1 m4="-D 4-3"`. 5s. Note the option `-D 4-3` that only allows to flatten a nested tuple of size 3 at position 4.
All four properties are violated due to a complete MIM attack performing a hash transcript attack using a CPC stuffed in info_A' and info_B'. This is exactly the attack described in [1].

## Variant of the CPC attack [1]
Command: `make sigma=1 m4="-D 3-2`. 1.4s
Auth(B->A) and SecKey(B) are violated due to a CPC attack. As opposed to the CPC attack from [1], this attack does not violate the 2 other properties. The CPC is used as a placeholder for the DH shares so this attack works only if those elements allow a large enough search space for finding the CPC.

## Proofs
No IPC attack was found (command `make sigma=1 m4="-D allFlat -D allCol -D IPC`)
No CPC attack was found when the flattening only allows to flatten nested tuple at position 1 or 2.

# IKEv2 protocol: `ikeV2_HF_EC.pv`
Same as for sigma, except that you should add `ike=1`. For instance: `make ike=1 m4="-D noFlat -D noCol"`.
The most powerful attacker and the default choice for attack finding can be obtained with `make m4 ike=1 m4="-D allFLat"`.
Fixed size of collapse can also be provided as for Sigma. We introduced a new symbol `H_` for flattening list of arguments without taking potential hash collisions into account for defining a query expressing agreement on a transcript (using some associative concat operator). This new operator can be removed with the option `-D withoutList`.

Since the number of arguments under a hash can be as large as 6 for this model, ProVerif needs more computation time to conclude. In particular, we had to bound the size of the prefixes for which CPC or IPC are possible for ProVerif to terminate in a reasonable time.
seems to take forever to conclude. When collisions are enabled, use the option `-D boundedCol` (bounded collisions only).

We also have added a M4 option in both files: `noCook` and `forceCook` that respectively forbids or forces the use of the cookie mechanism. Without any of those options, the adversary actually chooses the use of cookie per session (default option).

Properties:
 - Agree(SA): agreement on pkA and SA
 - Agree(t): agreement on the transcript (with associative list)
 - Agree(h(t)): agreement on the hashed transcript (with associative list)
 
Results:                     Agree(SA) Agree(t)  Agree(h(t))
 - noFlat + noCol:               True   True    True - 1.18s. Command `make ike=1 m4="-D noCol -D noFlat""`.
 - allFlat + noCol:              False  True    True - 63s   --> colliding input on the cookie. Command `make ike=1 m4="-D noCol -D allFlat"`.
 - allFlat (withCol)             False  False   True - 240s (with bounded CPC/IPC)   --> CPC/IPC attack combined with the above. Works both with CPC or IPC. Command: `make ike=1 m4="-D allFlat"`.

Interestingly, for finding this attack one needs to specify in the model the fact that initiator and responder are willing to use cookie or not. Both options must co-exist for the attack to work. Indeed, A needs to accept cookie request and B must send a cookie and accept sessions where cookies are not requested.


# Simplified IKEv2 protocol: `simplified_ikeV2_HF_EC.pv`
This is a simplified IKEv2. Same as for IKEv2, except that you should add `ike_s=1`. For instance: `make ike_s=1 m4="-D noFlat -D noCol"`.
We have fine-tuned the flattening for speeding up the computation time.

Properties:
 - Agree(SA): agreement on pkA and SA
 - Agree(t): agreement on the transcript (with associative list)
 - Agree(h(t)): agreement on the hashed transcript (with associative list)
 
Results:                         Agree(SA) Agree(t)  Agree(h(t))
 - noFlat + noCol:               True   True    True - 0.59s
 - noFlat + withoutList:         True   True    True - 14s 
 - allFlat + noCol:              False  True    True - 1.58s   --> colliding input on the cookie 
 - allFlat (withCol)             False  False   True - 2.4s (with bounded CPC/IPC)   --> CPC/IPC attack combined with the above. Works both with CPC or IPC. 

[1] Transcript Collision Attacks: Breaking Authentication in TLS, IKE, and SSH. Bhargavan and Leurent. NDSS'16.
