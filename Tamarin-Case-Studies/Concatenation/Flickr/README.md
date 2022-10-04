# Flickr
-------------

## Protocol description

[Flickr](https://www.flickr.com) is a photo management and sharing website with millions of users.

In 2009, the Flickr API implemented an authentication schemes which was based on bad hash functions,

which led to a bunch of exploits based on hash length extension: 
[Flickr Attack](https://vnhacker.blogspot.com/2009/09/flickrs-api-signature-forgery.html)


## Analysis details

Tamarin version description:

```
tamarin-prover 1.7.1, (C) David Basin, Cas Cremers, Jannik Dreier, Simon Meier, Ralf Sasse, Benedikt Schmidt, ETH Zurich 2010-2020
Git revision: 49b94968d36a1eee4f4759f761478a564b93b19d, branch: feature-assoc-concat
Compiled at: 2021-10-12 12:20:43.278613 UTC

commit bd591b866b6eacdf88bd6e958e7a5240fb0e3432 (origin/feature-assoc-concat)
Date:   Tue Oct 19 11:27:54 2021 +0200
```

## Flickr.spthy
This model is a minimal version of the Flickr API authentication mechanism.

It features the event based hash model using the [Library File](../HashLibrary.splib)

### lemmas description

| name | description |
| ------ | ------ |
| sanity | checks reachability of the authentication |
| KeySecrecy | checks for key leakage |
| helping_client | checks whether all message by the client are send over a key that was initialised by that client |
| helping_server | checks whether all message arriving at the server are received over a key that was initialised by that server |
| authenticate | checks whether for all clients and servers communicating over a key k, that k was established between them before at some point |
| authenticatePermissions | checks whether the permission requests received by the server were send by a client before |


## Results

An attack on authenticatePermission can be found [here](Flickr_Length_Extension.png) using

`tamarin-prover-concat --prove Flickr.spthy -D=FreshDomain -D=CR -D=LengthExtension`

within 1.49s on a MacBook Pro 2019, 2,6 GHz 6-Core Intel Core i7, 16 GB DDR4 RAM



|  | FreshDomain | AttackerDomain | FreshDomain & CR | AttackerDomain & CR | FreshDomain & CR & LengthExtension | AttackerDomain & CR & LengthExtension |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| sanity |  verified | verified | verified | verified | verified | verified |
| KeySecrecy | verified | verified | verified | verified | verified | verified |
| helping_client | verified | verified | verified | verified | verified | verified |
| helping_server | verified | verified | verified | verified | verified | verified |
| authenticate | verified | verified | verified | verified | verified | verified |
| authenticatePermissions | falsified | falsified | verified | falsified | falsified | falsified |


