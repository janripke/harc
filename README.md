harc
=

harc is a commandline tool for releasing code (into cloud).

# Installation
harc currently supports Python 3

--upgrade, update the python package if it already exists. 

## install a release (latest)
```
$ pip3 install --upgrade git+https://github.com/janripke/harc.git@1.0.33#egg=harc
```

## install from the main branch
```
$ pip3 install --upgrade git+https://github.com/janripke/harc.git#egg=harc
```

## post installation tasks

create config.json in ~/.harc :
```
{
  "proxies": {
    "http": "your-proxy.com:8080",
    "https": "your-proxy.com:8080"
  }
}
```

create credentials.json ~/.harc:
The azure section reflects the default azure credentials.
The git section reflects the default git credentials
These settings can be overruled in a project specific setup.
```
{
 "tenant_id": "1a12904d-3fe9-5246-g641-cjf04cdf0c6d",
 "client_id": "19c37574-8jgb-432f-bbee-02f9e1bf7b46",
 "azure": {
   "username": "jan.ripke@acme.org",
   "password": "******"
   },
 "git": {
   "username": "jan.ripke@acme.org",
   "password": "******"
   }
}
```

## Check the status of your installation

Simply run `harc --help`.


# Usage

There is one main command line interface which you can get with the `harc` command. Whenever you are confused on how you are supposed to do something just type:

`harc --help` or `harc <subcommand> --help`

and a list of available options with descriptions will be shown.
