requirments.txt-ben találhatóak a futtatáshoz szükséges csomagok, telepítése:

conda create --name env --file requirements.txt

parancssori paraméterként megadhatóak a következőek, ebben a sorrendben:
        -generált gráfok száma: int
        -csúsok "alsó korlátja": int
        -csúcsok "felső korlátja": int
        -erdős-rényi gráf él-valószínűsége: float
        -threshold (algoritmus 1-hez): float
        -k: int
        -cpu_number: int
        -run_id: int // futás azonosító, reprot/[run_id] mappába kerülnek az eredmények