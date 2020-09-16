# Programátorská dokumentace

API dokumentace, vygenerovaná programem [Epydoc](http://epydoc.sourceforge.net/),
je dostupná na [samostatné stránce](https://jakoma02.github.io/pyCovering/).

PyCover generuje náhodné dílky pyramidových i obdélníkových (2D) skládačkových
hlavolamů. Program **negeneruje** (a ani si to neklade za cíl) dílky ani celá
rozložení **uniformně náhodně**, některá rozložení tedy může generovat častěji
než jiná.

Maximální rozměry pyramidy/obdélníku, které program dokáže pokrýt, nejsou pevně stanoveny,
jen může pokrývání větších rozměrů trvat neúměrné množství času. Vzhledem k randomizované
povaze programu se mohou také časy pokrývání modelu stejného modelu se stejnou konfigurací
drasticky měnit.

## Závislosti a použité nástroje
 - [VPython](https://vpython.org/)
 - [PySide2](https://wiki.qt.io/Qt_for_Python) (Qt 5), Qt designer
 - [Parameterized](https://github.com/wolever/parameterized) pro parametrické unit-testy
 - [Pylint](https://pylint.org/)
 - vim, git, ...

## Návrh
Kostru programu tvoří "model", který obsahuje samotnou logiku pokrývání. Pro zobrazení výsledku
pokrývání uživateli je pak použit "view". Tento návrh umožňuje rozbrazovat výsledky pokrývání
modelu různými způsoby, aniž by bylo potřeba měnit logiku modelu.

![Diagram tříd](images/class_diagram.svg)

Velkou část pokrývací logiky se skrývá ve třídě `GeneralCoveringModel`, od které všechny modely dědí.
Jednotlivé modely pak jen reimplementují některé funkce (např. `neighbors(pos)`, která vrací všechny
sousedy zadané pozice, přesněji je to jejich generátor).

### Moduly
 - `pycovering.models` - jádro celého programu, obsahuje logiku pokrývání a jednotlivé pokrývací modely
 - `pycovering.views` - obsahuje logiku zobrazování jednotlivých modelů
 - `pycovering.constraints` - obsahuje "hlídače omezení" (více v sekci omezení)
 - `pycovering.main` - stará se o parsování argumentů
 - `pycovering.qt_gui` - grafické rozhraní programu


## Algoritmus pokrývání
Program bere postupně jednotlivé prázdné pozice (podle nějakého lineárního
uspořádání pozic určeného modelem) a snaží se na ně vkládat náhodné dílky.
To dělá pomocí **randomizovaného backtrackingu**.

Nejprve je určena velikost dílku (aby byly všechny velikosti dílků přibližně
stejně pravděpodobné). Pak program hledá volné sousedy dosud vygenerovaného
bloku do té doby, než má block požadovanou velikost. Pokud nalezený blok splňuje
všechna omezení, je přidán do modelu. Pokud se dostane slepé
uličky, backtrackuje.

Pokud je požadovaná velikost bloku jednoznačně určena (tedy minimální a maximální
povolená velikost bloku se rovanají), zkontroluje se před přidáním bloku,
jestli budou mít všechny souvislé oblasti prázdných pozic velikost **dělitelnou
velikostí bloku**. V opačném případě později nebude možné model doskládat a přidání
bloku je okamžitě zamítnuto.

Pokud velikost bloku jednoznačná není, takto silná podmínka platit nemusí.
Proto se pouze ověřuje, jestli velikost nějaké souvislé oblasti není menší
než nejmenší povolená velikost bloku nebo naopak větší než největší povolená
velikost bloku.

Protože určit počet všech bloků, které jdou na danou pozici umístit, je výpočetně
náročné, provede program pevný počet pokusů o nalezení náhodného bloku.
Pokud žádný z nich nevede k cíli, i na této úrovni pokračuje v backtrackingu -
odstraní poslední přidaný blok a hledá k němu alternativu.


## Omezení/Constraints
Omezení je nějaká vlastnost, kterou musí všechny bloky splňovat (například
rovinnost nebo tvar cesty). Tato vlastnost je kontrolována před přidáním
každé pozice do bloku, aby algoritmus netrávil zbytečně mnoho času
ve slepých uličkách.

Protože při kontrole omezení pro novou pozici bloku často chceme s výhodou
využít informací zjištěných při kontrole předchozích pozic (např. pokud
ověřujeme rovinnost bloku a už známe předpis roviny, ve které všechny dosud
přidané body leží, nemusíme jej znovu hledat), pro kontrolu omezení
se používají tzv. **constraint watchers**, které jsou **stavové**
a **persistentní**.

Persistentnost znamená, že si watcher pamatuje i **všechny jeho předchozí
stavy** a je schopen je (pomocí metody `rollback_state()`) obnovit. To se při
backtrackingu hodí při vracení se ze slepých uliček.

Persistentnost znamená, že si watcher pamatuje i **všechny jeho předchozí
stavy** a je schopen je (pomocí metody `rollback_state()`) obnovit. To se při
backtrackingu hodí při vracení se ze slepých uliček

Každý watcher má metodu `check_position(pos)`. Ta nejprve načte poslední stav
ze zásobníku stavů a pak vrátí, jestli bude po přidání pozice `pos` blok stále
splňovat omezení. Při tom zároveň upraví svůj vnitřní stav, který po zavolání
metody `commit()` uloží na svůj zásobník stavů. Pokud pozice přidána není
(např. není splněno jiné omezení) a metoda `commit()` není zavolána, ani stav
na zásobníku upraven není.
