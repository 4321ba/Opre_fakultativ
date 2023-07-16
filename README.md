# Opre_fakultativ
Operációs rendszerek c. tárgy fakultatív programozós házi feladatai

A feladatleírások a tárgy moodle oldalán (voltak) elérhetők. Mivel a forráskód mellett a dokumentáció is fontos, ezért ezeket ide is bemásoltam (`doc_for_hf123` néven), de ezek a tantárgy tulajdonát képezik. Az itt megadott programkák az összes teszten átmentek, így komoly hiba nem lehet bennük. Alább bemásolom az elvárt bemenet és kimenet formátumát feladatonként, egy-egy példaként.

## Ütemező (Fakultatív HF1)

Programka: `scheduler.py`

Bemenet:

```
A,0,0,6
B,0,1,5
C,1,5,2
D,1,10,1
```

Kimenet:

```
ACABDB
A:2,B:8,C:0,D:0
```

## Lapcsere (Fakultatív HF2)

Programka: `pageturner.py`

Bemenet:

```
1,2,3,-1,5,-1
```

Kimenet:

```
ABC-AB
5
```

## Holtpontelkerülés (Fakultatív HF3)

Programka: `holtpont.py`

Bemenet:

```
T1,+R1,0,0,+R2,-R1,-R2
T2,+R2,+R1,-R1,-R2
T3,0,0,0,+R3,+R3,-R3,-R3
```

Kimenet:

```
T1,4,R2
T3,5,R3
```

## MFQ ütemező (egyedi feladat)

Összes feladathoz tartozó fájl: `mfq_szorgalmi` mappa

Mivel ez egy általam választott feladat volt, így a feladatkiírást és a teszteket is én írtam. Ezek megtalálhatóak a [dokumentáció](mfq_szorgalmi/documentation.pdf)ban.
