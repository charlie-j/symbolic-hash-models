This folder contains all the needed material to reproduce the case studies of the paper "Hash Gone Bad: Automated discovery of protocol attacks that exploit hash function weaknesses" - V. Cheval, C. Cremers, A. Dax, L. Hirschi, C. Jacomme, S. Kremer, to appear at USENIX Security'23

To avoid installing manually our versions of Proverif and Tamarin, we recommand using the docker image provided at dockerhub.

# Docker installations
• Linux: follow instructions at https://docs.docker.com/get-docker/
• MacOS, there is a binary docker for Mac, which can be installed as a package (https://docs.docker.com/
docker-for-mac/), or, if you have homebrew, via ‘brew install --cask docker‘.

# Image pull

After the installation of docker, the ready to use image can be pulled in a few seconds with the following command:
`docker pull securityprotocolsresearch/tamarin-proverif-hashes:latest`


To launch the docker, execute the command `$ docker run securityprotocolsresearch/tamarin-proverif-hashes:latest`, which should display a README with instructions on how to use the tools.


# Case studies

The case-studies are split by tool, with corresponding READMEs detailing the case-studies (that can be read with `less`, or after installing inside the docker your favorite text editor), to be found in:
 * Proverif-Case-Studies
 * Tamarin-Case-Studies



# Rebuilding the image

Follow the instructions at `Docker/README.md`.


# Building you own tamarin and proverif

The two needed archives are contained in either `tamarin-prover-concat.zip` and `Docker/res/proverif-compfun.zip`. Both can be installed following the classical installation instructions of Proverif and Tamarin.

