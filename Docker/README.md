We recommend using dockerpull to reconstruct the docker which provides everything ready to play with.

Otherwise, to build the full docker.

First unzip the file tamarin-prover-concat.zip, and built the correspond docker `tamarin-prover/tamarin` with the etc/docker instructions.


Then, run `./Docker/build-hashes.sh` to build the tamarin-proverif/hashes docker image (from parent repository of this README).

It can then be pushed to dockerhub with:
```
docker tag tamarin-proverif/hashes:latest securityprotocolsresearch/tamarin-proverif-hashes:latest;
docker push securityprotocolsresearch/tamarin-proverif-hashes:latest
```
