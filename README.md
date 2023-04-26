# Setup

Setting up a virtual environment:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Setting up the database:
```
(venv) $ createdb warbler
(venv) $ python seed.py
```

Starting the server:
```
(venv) $ flask run
```
