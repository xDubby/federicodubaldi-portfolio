---

title: Pipeline di cleaning

order: 5

---



La pipeline è progettata seguendo un principio chiave:

\*\*ogni trasformazione deve essere deterministica e spiegabile\*\*.



Step principali:

1\. parsing difensivo del file (encoding, separatori)

2\. normalizzazione dei nomi colonna

3\. parsing e standardizzazione delle date

4\. conversione esplicita dei tipi numerici

5\. deduplicazione basata su chiavi definite

6\. rimozione di righe non valide con motivazione



Nessuna trasformazione “magica” o implicita:

ogni step è tracciabile e riproducibile.



