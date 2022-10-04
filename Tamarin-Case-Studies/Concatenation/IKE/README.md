# IKEv2
----

## Information about IKEv2

It seems that IKEv2 uses SHA-1, SHA-2 or MD5 [Source](https://docs.defenseorchestrator.com/Configuration_Guides/Virtual_Private_Network_Management/0010_Site-to-Site_Virtual_Private_Network/Configuring_Site-to-Site_VPN_for_an_FTD/0030_Encryption_and_Hash_Algorithms_Used_in_VPN)

[RFC-Cookie](https://datatracker.ietf.org/doc/html/rfc5996#page-30)
[RFC Standard](https://datatracker.ietf.org/doc/html/rfc7296)
[RFC Implementation and Update](https://datatracker.ietf.org/doc/html/rfc8247)

## Analysis details

Tamarin version description:

```
tamarin-prover 1.7.1, (C) David Basin, Cas Cremers, Jannik Dreier, Simon Meier, Ralf Sasse, Benedikt Schmidt, ETH Zurich 2010-2020
Git revision: 49b94968d36a1eee4f4759f761478a564b93b19d, branch: feature-assoc-concat
Compiled at: 2021-10-12 12:20:43.278613 UTC

commit bd591b866b6eacdf88bd6e958e7a5240fb0e3432 (origin/feature-assoc-concat)
Date:   Tue Oct 19 11:27:54 2021 +0200
```

## Original File: [ikeV2_HF_EC.spthy](ikeV2_HF_EC.spthy)

HF_EC --> Hash Function - ?

Tamarin version of [ikeV2_HF_EC.pv](../../../proverif/sigma_HF_EC/ikeV2_HF_EC.pv)
using the cookie mechanism.


Results:
| Lemma       | /          | Single Session  | Collapse Hash | Single & Collapse |
| ------------- |:-------------:| :-----:| :-----:| :-----:|
| AccB(B,A,n,m) --> InitA(A,B,n,m1)      | False | True | False | False |
| AccA(A,B,n,m) --> InitB(B,A,n,m1)      | True | True | False| / |
| AccB(B,A,n,m) --> InitA(A,B1,n,m1)      | True | True | / | False |
| AccB(B,A,n,m) --> InitA(A,B,n,m)      | False | False | False | False |
| AccA(A,B,n,m) --> InitB(B,A,n,m)      | True | True | False | False |
| AccB(B,A,n,m) --> InitA(A,B1,n,m)      | False | False | False | False |
| secrecy_key_A | True | True | False | False |
| secrecy_key_B | True | True | False | False |

By collapsing the hash function to a single point, the adversary is able to actively MITM and
get the session key [attack](key_secrecy_hash_collapse.png)

We made an additional version of the protocol model where no cookie is used
[ikeV2_HF_EC_nocookie.spthy](ikeV2_HF_EC_nocookie.spthy)


Results:
| Lemma       | /          | Single Session  | Collapse Hash | Single & Collapse |
| ------------- |:-------------:| :-----:| :-----:| :-----:|
| AccB(B,A,n,m) --> InitA(A,B,n,m1)      | False | True | False | False |
| AccA(A,B,n,m) --> InitB(B,A,n,m1)      | True | True | False | False |
| AccB(B,A,n,m) --> InitA(A,B1,n,m1)      | True | True | False | False |
| AccB(B,A,n,m) --> InitA(A,B,n,m)      | False | False | False | False |
| AccA(A,B,n,m) --> InitB(B,A,n,m)      | True | True | False | False |
| AccB(B,A,n,m) --> InitA(A,B1,n,m)      | False | False | False | False |
| secrecy_key_A | True | True | False | False |
| secrecy_key_B | True | True | False | False |




## Using the concatenation operator and event based hashes

As we established a groundtruth of the lemmas, we exclude the lemmas the are false by default from the analysis



## Cookie

### Cookie - Event Based Hash

As a first step we change the standard hash function symbol and replace it 
by and event based hash model [ikeV2_HEB_EC.spthy](Cookie/HEB_EC/ikeV2_HEB_EC.spthy)

Results:
| Lemma       | /          | Single | no Collison | Single & no Coll | deterministic | Single & det | det & no Coll | all
| ----------- |:----------:| :-----:| :-----:| :-----:| :-----:| :-----:|:-----:| :-----:|
| AccB(B,A,n,m) --> InitA(A,B,n,m1)      | False | False | False | True | False | False | False | True |
| AccA(A,B,n,m) --> InitB(B,A,n,m1)      | False | False | True | True | False | False | True | True |
| AccB(B,A,n,m) --> InitA(A,B1,n,m1)     | / | / | / | / | / | / | / | / |
| AccB(B,A,n,m) --> InitA(A,B,n,m)       | False | False | False | False | False | False | False | False |
| AccA(A,B,n,m) --> InitB(B,A,n,m)       | False | False | True | True | False | False | True | True |
| AccB(B,A,n,m) --> InitA(A,B1,n,m)      | False | False | False | False | False | False | False | False |


### IKE Cookie - Event Based Hash

As a control step, before adding associative Concatenation, we tried to prove the the same lemmas
as before, but now with an event based hash function.

Results:
| Lemma       | /          | Single Session  | NoColl Hash | Single & NoColl | neutral & NoColl Hash | neutral & Single & NoColl |
| ------------- |:-------------:| :-----:| :-----:| :-----:| :-----:| :-----:|
| secrecy_key_A      | / | False | True | True | True | True |
| secrecy_key_B      | / | False | True | True | True | True |

The results were as expected, however, without any restrictions, tamarin did not terminate.
Further we added a neutral DH group element to the ET. It had no influence on the proofs.

### IKE Cookie - No DH Group Check - Event Based Hash
Look at the previous section.

Results:
| Lemma       | /          | Single Session  | NoColl Hash | Single & NoColl | neutral & NoColl Hash | neutral & Single & NoColl |
| ------------- |:-------------:| :-----:| :-----:| :-----:| :-----:| :-----:|
| secrecy_key_A      | / | False | True | True | True | True |
| secrecy_key_B      | / | False | True | True | True | True |






### Cookie - Event Based Hash - Associative Concatenation

We now additionally added the associative concatenation model
to the no cookie event based hash model [ikeV2_HEB_A.spthy](Cookie/HEB_A/ikeV2_HEB_A.spthy)

Results:
| Lemma       | /          | Single | no Collison | Single & no Coll | CPcol | Single & CPcol | CPcoll & no Coll | all
| ----------- |:----------:| :-----:| :-----:| :-----:| :-----:| :-----:|:-----:| :-----:|
| AccB(B,A,n,m) --> InitA(A,B,n,m1)      | False | False | False | True | False | True | False | True |
| AccA(A,B,n,m) --> InitB(B,A,n,m1)      | False | False | True | True | True | True | True | True |
| AccB(B,A,n,m) --> InitA(A,B1,n,m1)     | / | / | / | / | / | / | / | / |
| AccB(B,A,n,m) --> InitA(A,B,n,m)       | False | False | False | False | False | False | False | False |
| AccA(A,B,n,m) --> InitB(B,A,n,m)       | False | False | False | False | False | False | False | False |
| AccB(B,A,n,m) --> InitA(A,B1,n,m)      | False | False | False | False | False | False | False | False |

In this scenario, we found a potential attack on lemma 5.


We found a generic attack pattern on transcript with concatenations, which does not need any hash weaknesses. The idea is that when we have an expected transcript of the form:
```expected transcript = (a,b,c,d)```
And where the view of A is  
```transcript-by-A = (A,b,c,d)``` 
and the view of B is 
```transcript-by-B = (a,b,C,d)```
, where A and C are attacker controlled values, then a generic attack pattern is:
```A=a,b and C=b,c```
, which produces the two transcripts 
```((a,b),b,c,d)```
and 
```(a,b,(b,c),d)```
, which when seen as concatenations are of course equal. But it is an attack on the authentication, as the two parties don't agree on the individual values.

### IKE Cookie - Event Based Hash - Associative Concatenation

We know added the associative concatenation operator, which also helped with verification time

Results:
| Lemma       | /          | CPCol  | NoColl | neutral | neutral & NoColl Hash | neutral & CPCol |
| ------------- |:-------------:| :-----:| :-----:| :-----:| :-----:| :-----:|
| secrecy_key_A      | False | True | True | False | True | True |
| secrecy_key_B      | False | True | True | False | True | True |

### IKE Cookie - No DH Group Check - Event Based Hash - Associative Concatenation

Results:
| Lemma       | /          | CPCol  | NoColl | neutral | neutral & NoColl Hash | neutral & CPCol |
| ------------- |:-------------:| :-----:| :-----:| :-----:| :-----:| :-----:|
| secrecy_key_A      | False | True | True | False | True | True |
| secrecy_key_B      | False | True | True | False | False | False |

With not checking for valid DH elements we now could find an attack. The attack is described below.

#### IKE NDSS16 Attack

hash transcript of the information of A 
```
hashA = h(c, SA, gX, nA, infoA, nB, macA)

c  //cookie
SA  //cryptographic algorithms the initiator supports
gX  //DH key share
nA  //random nonce chosen by A
infoA  // crypt info which is mentioned in the NDSS paper but not in rfc7296
nB  //random nonce chosen by B
macA  //mac of public key of A under shared key
NE //neutral element represting small DH subgroup
```

First message exchanges
```
A:  --> SA_1, g^x, nA, infoA_1

B:  <-- SA_2, NE, nA, infoA_2 = <SA_1, g^x, nA, infoA_1>

B:  --> c_1

A:  <-- c_2 =  <c_1, SA_2, NE, nA>

B:  <-- c_1, SA_2, NE, nA, infoA_2 = <SA_1, g^x, nA, infoA>

B:  --> SB_1, g^y, nB, infoB_1

A:  <-- SB_2, NE, nB, infoB_2
```

Computations of A:
```
k = kdf(NE^x=NE,nA,nB)
macA = mac(pkA,k)

hashA = h(c, SA, gX, nA, infoA, nB, macA)
= h(c_2, SA_1, gX, nA, infoA_1, nB, macA))
= h(c_1, SA_2, NE, nA, SA_1, gX, nA, infoA_1, nB, macA)
```

Computations of A:
```
k = kdf(NE^y=NE,nA,nB)
macA = mac(pkA,k)

hashA = h(c, SA, gX, nA, infoA, nB, macA)
= h(c_1, SA_2, NE, nA, infoA_2, nB, macA)
= h(c_1, SA_2, NE, nA, SA_1, gX, nA, infoA_1, nB, macA)
```

And as both are the same, the verification will work.
As the attacker knows NE, nA and nB, the attacker can also compute k.

The attack graph can be seen [here](SecrecyCookie/HEB_A/attack_NDSS_paper.png)











### NoCookie - Event Based Hash

As a first step we change the standard hash function symbol and replace it 
by and event based hash model [ikeV2_HEB_EC.spthy](NoCookie/HEB_EC/ikeV2_HEB_EC.spthy)

Results:
| Lemma       | /          | Single | no Collison | Single & no Coll | deterministic | Single & det | det & no Coll | all
| ----------- |:----------:| :-----:| :-----:| :-----:| :-----:| :-----:|:-----:| :-----:|
| AccB(B,A,n,m) --> InitA(A,B,n,m1)      | False | False | False | True | False | False | False | True |
| AccA(A,B,n,m) --> InitB(B,A,n,m1)      | False | False | True | True | False | False | True | True |
| AccB(B,A,n,m) --> InitA(A,B1,n,m1)     | False | False | True | True | False | False | True | True |
| AccB(B,A,n,m) --> InitA(A,B,n,m)       | False | False | False | False | False | False | False | False |
| AccA(A,B,n,m) --> InitB(B,A,n,m)       | False | False | True | True | False | False | True | True |
| AccB(B,A,n,m) --> InitA(A,B1,n,m)      | False | False | False | False | False | False | False | False |


### NoCookie - Event Based Hash - Associative Concatenation

We now additionally added the associative concatenation model
to the no cookie event based hash model [ikeV2_HEB_A.spthy](NoCookie/HEB_A/ikeV2_HEB_A.spthy)

Results:
| Lemma       | /          | Single | no Collison | Single & no Coll | CPcol | Single & CPcol | CPcoll & no Coll | all
| ----------- |:----------:| :-----:| :-----:| :-----:| :-----:| :-----:|:-----:| :-----:|
| AccB(B,A,n,m) --> InitA(A,B,n,m1)      | False | False | False | True | False | True | False | True |
| AccA(A,B,n,m) --> InitB(B,A,n,m1)      | False | False | True | True | True | True | True | True |
| AccB(B,A,n,m) --> InitA(A,B1,n,m1)     | False | False | True | True | True | True | True | True |
| AccB(B,A,n,m) --> InitA(A,B,n,m)       | False | False | False | False | False | False | False | False |
| AccA(A,B,n,m) --> InitB(B,A,n,m)       | False | False | True | True | True | True | True | True |
| AccB(B,A,n,m) --> InitA(A,B1,n,m)      | False | False | False | False | False | False | False | False |





