harc
========

Harc is a toolkit for releasing code in the cloud. One part (the server) is installed on the host in the cloud. The other part (the client) is used to release your code to this server. Harc is build in Python.

# Installation
Harc currently supports Python 2.7

## Install from source using virtualenv

First, clone the repo on your machine and then install with `pip`:

```
$ git clone https://gitlab.oxyma.nl/oxyma/harc.git harc-master
$ mkdir harc
$ cd harc
$ virtualenv env
$ source env/bin/activate
$ cd ../harc-master
$ pip install -e .
```

## Check that the installation worked

Simply run `harc --help`.

# Usage

There is one main command line interface which you can use with the `harc` command. Whenever you are confused on how you are supposed to do something just type:

`harc --help` or `harc <subcommand> --help`

and a list of available options with descriptions will show up.

# License
Copyright © 2017, [Oxyma](https://www.oxyma.nl).
Released under the [Proprietary](LICENSE).
