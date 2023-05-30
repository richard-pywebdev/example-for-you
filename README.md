# example-for-you

## 05 Contact Form

This is an example project for build FastAPI web applications. 

### Usage

Using Fedora 38 Linux. 

### Install

```commandline
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r non_ver_reqs.txt
```

### Environment Variables

Included is a file `dotenv` which you need to update with real credentials and source.

```
source dotenv
```



### Run

```commandline
python main.py
```

### Localhost

This version runs using SSL, and can be accessed at https://localhost/docs

The self-signed CA certificate is included for importing into your system or browser. 
