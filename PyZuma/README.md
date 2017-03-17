# Creazione ambiente di sviluppo

```
git clone https://github.com/nonzod/zuma.git Zuma
cd Zuma
python3 -m venv PyZuma/
source bin/activate
pip install Bluepy
pip install pygame
python src/Zuma.py
```

In caso di:

```
...
... No such file or directory: 'Zuma/PyZuma/lib/python3.5/site-packages/bluepy/bluepy-helper'
```

dalla dir dell'ambient virtuale e dopo `source bin/activate`:

-pip install git+https://github.com/Betree/pyMagicBlue.git-

```
cd lib/python3.5/site-packages/bluepy
make
```

# Codici pacchetti inviati

10 SPEED_LEFT SPEED_RIGHT>
