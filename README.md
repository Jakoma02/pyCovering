![Pylint badge](https://github.com/Jakoma02/covering/workflows/Pylint/badge.svg)
![Tests badge](https://github.com/Jakoma02/covering/workflows/Python%20tests/badge.svg)

# pyCovering
_(Tento program je zápočtovým programem z předmětu Programování II. na MFF UK.)_

**pyCovering** je open-source generátor a vizualizátor dílků pyramidových
a obdélníkových hlavolamů, jejichž zadáním je vygenerované dílky poskládat
tak, aby vytvořili původní tvar.

![Screenshot](images/gui_screenshot.png)

## Minimální požadavky
- Python verze **alespoň 3.6**

## Instalace

_(Příklady jsou uváděny pro OS Linux, ale obdobným způsobem je možné
program instalovat i na ostatních platformách)_

1) Naklonujte tento repozitář na svůj počítač.
```
$ git clone https://github.com/Jakoma02/pyCovering.git
```

2) Přejděte do složky s repozitářem.
```
$ cd pycovering
```

3) _(Volitelné)_ Aktivujte `virtualenv`
```
$ python -m venv venv
$ source ./venv/bin/activate
```

4) Nainstalujte program pomocí nástroje pip.
```
$ pip install .
```

## Použití
Program je možné využívat ve dvou režimech:
 1) V grafickém rozhraní `pycovering`
 2) V příkazové řádce pomocí `pycovering-cli`

### Příkazová řádka
```
pycovering-cli {2d,pyramid} <model-arguments>
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
