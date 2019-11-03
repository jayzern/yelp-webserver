# yelp-webserver

## Installation

Create a virtual environment
```bash
virtualenv venv
source venv/bin/activate
```

Install requirements via pip
```bash
pip install -r requirements.txt
```

## Usage

Change postgresql server in server.py:
```
DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
```

To run server
```python
python server.py
```
