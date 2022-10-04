# SSH
-------------

## Protocol description

> Secure Shell (SSH) is a cryptographic network protocol for operating network services securely over an unsecured network.  - Wikipedia

Standardization:
* [RFC4250](https://datatracker.ietf.org/doc/html/rfc4250) – The Secure Shell (SSH) Protocol Assigned Numbers
* [RFC4251](https://datatracker.ietf.org/doc/html/rfc4251) – The Secure Shell (SSH) Protocol Architecture
* [RFC4252](https://datatracker.ietf.org/doc/html/rfc4252) – The Secure Shell (SSH) Authentication Protocol
* [RFC4253](https://datatracker.ietf.org/doc/html/rfc4253) – The Secure Shell (SSH) Transport Layer Protocol
* [RFC4254](https://datatracker.ietf.org/doc/html/rfc4254) – The Secure Shell (SSH) Connection Protocol
* [RFC4419](https://datatracker.ietf.org/doc/html/rfc4419) – Diffie-Hellman Group Exchange for the Secure Shell (SSH) Transport Layer Protocol (March 2006)
* [RFC4432](https://datatracker.ietf.org/doc/html/rfc4432) – RSA Key Exchange for the Secure Shell (SSH) Transport Layer Protocol (March 2006)


Protocol model build for the scenario described in the [ NDSS Transcript Collision Paper](https://hal.inria.fr/hal-01244855/document)

## Analysis details

Tamarin version description:

```
tamarin-prover 1.7.1, (C) David Basin, Cas Cremers, Jannik Dreier, Simon Meier, Ralf Sasse, Benedikt Schmidt, ETH Zurich 2010-2020
Git revision: 49b94968d36a1eee4f4759f761478a564b93b19d, branch: feature-assoc-concat
Compiled at: 2021-10-12 12:20:43.278613 UTC

commit bd591b866b6eacdf88bd6e958e7a5240fb0e3432 (origin/feature-assoc-concat)
Date:   Tue Oct 19 11:27:54 2021 +0200
```

### lemmas description

| name | description |
| ------ | ------ |
| sanity | checks reachability of the authentication |
| secrecy_key_{A,B} | checks for key leakage |
| trans_auth | both parties agree on all messages before they are hashed for the hash transcript |
| trans_hash_auth | agreement of both parties on the hash transcript |
| agree_keys | When B accepts a message transcript, B agrees on the pubkeys with A |
| agree_keys_all | When B accepts a message transcript, B agrees on the pubkeys and all the messages with A |
| agree_Bkey_2 | When A accepts a message transcript, A agrees on the B's pubkey with B |
| agree_Bkey_all_2 | When A accepts a message transcript, A agrees on the B's pubkey and all the exchanged messages with B |



## Results

We made three versions of the SSH model. The first version 'sshv2_HF_EC.spthy' models SSH in a standard way. The second and third version of the protocol are then modelled with the event based hash function [libray](../HashLibrary.splib). The '_V1' file is a simplified version of the model to ease termination.

### sshV2_HF_EC.spthy

The reference model [(here)](sshV2_HF_EC.spthy) terminates using

`tamarin-prover-concat --prove sshV2_HF_EC.spthy`

within 5.21s on a MacBook Pro 2019, 2,6 GHz 6-Core Intel Core i7, 16 GB DDR4 RAM

| lemma | result |
| ------ | ------ |
| sanity | verified |
| secrecy_key_{A,B} | verified |
| trans_auth | verified |
| trans_hash_auth | verified |
| agree_keys | verified |
| agree_keys_all | verified |
| agree_Bkey_2 | verified |
| agree_Bkey_all_2 | verified |



### sshV2_HEB_A.spthy

An chosen prefix collision attack on trans_auth can be found [here](CPcol_sshV2_HEB_A.png) using

`tamarin-prover-concat --prove sshV2_HEB_A.spthy -D=FreshDomain -D=CPcol`

within 1958.91s on a MacBook Pro 2019, 2,6 GHz 6-Core Intel Core i7, 16 GB DDR4 RAM

with the `-D=FixedLength` flag we get a speedup to 645.18s (~3x faster)



|  | FreshDomain | FreshDomain & CR | FreshDomain & CPcol | FreshDomain & CPcol & FixedLength |
| ------ | ------ | ------ | ------ | ------ |
| sanity | verified | verified | verified | verified |
| secrecy_key_{A,B} | falsified | verified | verified | verified |
| trans_auth | falsified | verified | falsified | falsified |
| trans_hash_auth | falsified | verified | verified | verified |
| agree_keys | falsified | verified | verified | verified |
| agree_keys_all | falsified | falsified | falsified | falsified |
| agree_Bkey_2 | verified | verified | verified | verified |
| agree_Bkey_all_2 | falsified | falsified | falsified | falsified |


The version with collision resistance suggests attacks on message agreement. It is a parameter confusion attack: **A** sends `I_A`, **B** sends `I_B`. In the hash transcript `I_A | I_B` is computed. The attacker can now replace the send messages by `I_A' = I_A | a` and `I_B' = a | I_B`. Hence **A** computes
`I_A | I_B'` and **B** computes `I_A' | I_B`

`I_A | I_B'` = `I_A | a | I_B` = `I_A' | I_B`

* [LH, Update 8.12] Update: I agree this is not as the purely parsing-related issue found on IKE (relying on concatenations but not on any hash weaknesses) since the attacker does manage to change the transcript (compared to the happy flow).
Yet, for this attack to be valid, it should be possible for the first element of `I_B` to be stuffed with `a` (for `I_B'` received by A) and for the last element of `I_A` to be stuffed with `a` (for `I_A'` received by B).
This seems possible for the first element (`a` at the start of `I_B`) as one can cheat with the overall length. For instance, consider just as an example `I_B = cookie | g^x | app_data` where cookie is length-varying and length-prefixed: `cookie = lengthCookie | c` with `lengthCookie` itself of fixed size 8 bytes and `c` of size `lengthCookie`. In that case, the attacker can stuff in `a = lengthCookie' | c'` where `lengthCookie'` is (in bytes) `|c'| + 8 + |c|`. B will receive `lengthCookie' | c' | lengthCookie | c | g^x | app_data` and will "parse" `c' | lengthCookie | c` as the cookie (of length `lengthCookie'`).
**However** I do not think this is doable for the last element of `I_B`. Indeed, the current, genuine last field of `I_B` should be unambiguously parsed by the recipient (here A). If my reasoning below is right, this field is thus length-prefixed or fixed-length. In both cases, it forbids the attacker to append some more content. I am not sure I understand where serialization is involved here. To me this rather looks like parsing, nope? At the end of the day, we want B receiving I_A' to accept/read this last field that is too long...
TODO: think of some restrictions that would preclude such "false attacks".

*[LH] Comment*: this is reminiscent of the attack on IKE without collision. As discussed together for Sigmna, I think those attacks are modeling artifact that are not practical. Here is my rationale: Message fields are (i) fixed-length or (ii) length-varying. In case (i), the field is parsed by extracting the appropriate number of bytes from the input buffer according to the spec (fixed length). In case (ii), there must be some length information for the recipient to be able to parse the message, for instance the field is length-prefixed. Therefore, there must be no confusion on how to parse the different fields of a given message.

* [CJ] the thing is that sometimes, what is hashed may not be the same as what was received on the network. E.g. there may be a serialization function for the communications and another one for building the hash payload. This is then bad practice, as soon as the second one is not injective.


As disussed, I think we can avoid such modeling artifacts this way: check that an agreement on transcriptC = m1 | m2 | m3 | m4 instead of transcript = <m1,m2,m3,m4>. So that all representatives of the associative-equivalence class of a given trannscriptC are considered to match each other. This makes sense as in practice, only one whille be considered valid throigh unambigious parsing (based on fixed-length or length-varying but with length information). Not always possible though as we may want to define agreement on specific fields. Maybe we need to limit the possible confusions somehow? I'll try to think about that.

* [CJ] This is actually the kind of things that is done with the lemma trans_auth and trans_hash_auth


**[LH]** Now I wonder if the other falsifications (e.g., agree_keys_all) are also of this type? Do we also find attacks that are not based on parsing ambiguity?

* [CJ] We can check either with the pictures, or with the alternative lemma that you discussed before, which kind of attack we get.

* [LH, Update 8.12] So with Cpcol there is no attack here then?


### sshV2_HEB_A_V1.spthy

|  | FreshDomain | FreshDomain & CR | FreshDomain & CPcol |
| ------ | ------ | ------ | ------ |
| sanity | verified | verified | verified |
| secrecy_key_{A,B} | falsified | verified | verified |
| trans_auth | falsified | verified | falsified |
| trans_hash_auth | falsified | verified | verified |
| agree_keys | falsified | verified | verified |
| agree_keys_all | falsified | falsified | falsified |
| agree_Bkey_2 | verified | verified | verified |
| agree_Bkey_all_2 | falsified | falsified | falsified |

This version is faster the previous as concatenation was only used where needed leading to a less general, but faster model.
