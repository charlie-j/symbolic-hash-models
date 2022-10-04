# Equational Theory based threat models
-------


## List of case studies

For the following list of case studies we investigated the impact of changing the symbolic models of cryptographic primitives which are usually modeled as random oracles, like hashes (but also primitives that could be instantiated as hashes is practices, like PRFs, kdfs or sometimes MACs.) For those we replaced the models by a variety of more fine-grained hash functions models described later on.

#### Case Studies:

1. Key exchange protocols extract from [CSF12](https://cispa.saarland/group/cremers/downloads/papers/ScMeCrBa2012-tamarin.pdf). They can be found in the `csf-12` directory.
	* Diffie-Hellman
	* Jeong, Katz, Lee (2 Variants)
	* NISTS's KAS2 Key Agreement Protocol
	* NISTS's KAS1 Key Agreement Protocol (?is this a variant)
	* KEA+ Authenticated Key Exchange Protocol (5 Variants)
	* STS-MAC (2 Variants)
	* The Unified Model (UM) Key-Exchange Protocol
2. Authenticated key exchange protocols extracted from [AKE](https://www.research-collection.ethz.ch/handle/20.500.11850/72713). They can be found in the `ake` directory. They seem to be from the work resulting in the CSF12 paper, but are slightly different variants.
	* NAXOS (3 variants)
	* The Unified Model (UM) Key-Exchange Protocol (3 Variants)
3. Distance bounding protocols extracted from [Mauw](https://github.com/jorgetp/dbverify). They can be found in the `distance-bounding` directory.
	* Meadows et al.'s protocol (3 variants)
	* MAD
	* Kim and Avoine's protocol
	* Munilla and Peinado's protocol
	* CRCS (2 variants)
4. TESLA protocol model from [TESLA](https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/66840/eth-7011-02.pdf?sequence=2&isAllowed=y). It can be found in the `Tesla` directory.
5. A set of orginal tamarin models. They can be found in the `original` directory.
	* IKEv2 (2 Variants)
	* SSHv2
	* Flickr
	* Sigma
	* Telegram KE
	


## Definitions: ET Models

When we construct hash functions in the symbolic model, we usually model them unary function symbol with no equational theory. This models hash functions like and ideal random oracle.

We want to explore impact of modeling hash functions closer to their actual security definitions/guarantees. Therefore, we took the definitions by [Rogaway and Shrimpton](https://www.cs.ucdavis.edu/~rogaway/papers/relates.pdf) for keyed hash functions and build minimal models to break these definitions in the symbolic model. We then tried these models on several case studies.

Note that we also replaced occurences of the standard symbolic hash model `h(m)` with a keyed variant `h(k(),m)` where `k()` is a function symbol of arity zero. This `k()` does NOT represent any cryptographic key, but the public choice of an arbitrary hash function from a family of hash function indexed with `k()`.

All models can be found in the repository [Keyed Definitions](HashDefinitions.spthy) and [Unkeyed Definitions](UnkeyedHashes.spthy)


## Analysis details

Tamarin version description:

```
tamarin-prover 1.7.1, (C) David Basin, Cas Cremers, Jannik Dreier, Simon Meier, Ralf Sasse, Benedikt Schmidt, ETH Zurich 2010-2020
Git revision: 49b94968d36a1eee4f4759f761478a564b93b19d, branch: feature-assoc-concat
Compiled at: 2021-10-12 12:20:43.278613 UTC

commit bd591b866b6eacdf88bd6e958e7a5240fb0e3432 (origin/feature-assoc-concat)
Date:   Tue Oct 19 11:27:54 2021 +0200
```

As we only performed changes on the function symbols and the equational theory, execution of the files still works the standard way:

`tamarin-prover --prove [FILENAME]`


### Excuting all major case studies

To run all major case studies, run

```
python3 eval.py
```

Depending on the hardware used, this may take a while. (on a standard MacBook Pro (2019) it took roughly 12 Minutes)

The results are saved as `results` in the main directory. `results-precomputed` contains all results already and can be use for comparison.

## Results

```
Note:
If a we execute a protocol model and prove it to be secure 
(prove that the lemmas hold) when using the 'pre' hash model,
it is not needed to try the other hash models, as the 'pre'
hash model gives the attacker the strongest capabilities of 
the ET hash models.
```

```
Note 2:
Attacks one breaking the one-wayness of hash as
in the 'new_pre' model are often considered impossible
because of the compression property of hash functions.
This necessarily leads to collisions. Hence, without
additional information, recovering THE preimage unambiguously
is considered impossible.
```

1. The results for the key exchange protocols extracted from [CSF12](https://cispa.saarland/group/cremers/downloads/papers/ScMeCrBa2012-tamarin.pdf) are not terminating for the model breaking one-wayness of hashes. For the `pre` model it, however, terminates and yields no attacks. **No false or correct attacks were found**
2. The results for the key exchange protocols extracted from [AKE](https://www.research-collection.ethz.ch/handle/20.500.11850/72713) are not terminating for the model breaking one-wayness of hashes. For the `pre` model it, however, terminates and yields no attacks. **No false or correct attacks were found**
3. The results for the distance boundings models from [mauw](https://github.com/jorgetp/dbverify) terminate and yield no attacks for the `pre` model but for inverting the hash. Attacks on secrecy are found with `new_pre`. **Attacks were found when breaking one-wayness**
4. TESLA results can be found [here](https://docs.google.com/spreadsheets/d/18nWVXqfx9Uc6NdLQAX8jEKaq_FYfvDPe5plQeQHlDnE/edit?usp=sharing). Attacks when `new_pre(f)`, `new_pre(M)`, `pre(f)` **Attacks were found when breaking one-wayness or preimage resistance**
5. The results of the orginal case studies yield no attacks on the majority of models, but there was a potential attack when breaking one-wayness (`new_pre`) in the Flickr case study. **Attacks were found when breaking one-wayness**
model 
