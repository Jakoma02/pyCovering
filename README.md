![Pylint badge](https://github.com/Jakoma02/covering/workflows/Pylint/badge.svg)
![Tests badge](https://github.com/Jakoma02/covering/workflows/Python%20tests/badge.svg)

# Covering (TODO: jméno)
Zápočtový program pro p2x

## Instalace

### Minimální požadavky
- Python verze **alespoň 3.6**

_(Příklady jsou uváděny pro OS Linux, ale obdobným způsobem je možné
program instalovat i na ostatních platformách)_

1) _(Volitelné)_ Aktivujte `virtualenv`
```
> python -m venv venv
> source ./venv/bin/activate
```

2) Nainstalujte program pomocí `setup.py`
```
> ./setup.py install
```

## Použití
Program je možné využívat ve dvou režimech:
 1) V grafickém rozhraní `covering`
 2) V příkazové řádce pomocí `covering-cli`

### Příkazová řádka
```
covering-cli {2d,pyramid} <model-arguments>
```

Argumenty modelu jsou

1) společné
   - `--help`
   - `--min-block-size/-mib`
   - `--max-block-size/-mab`
   - `--verbose/-v`
2) 2d
   - `--height`
   - `--width`
   - `--visual` 
3) pyramid
   - `--size/s`
   - `--visual`
