
# 10denní tréninkový deník — Letní příprava

Jednoduchá webová aplikace (jeden soubor `index.html`, React přes CDN, bez nutnosti instalace) pro evidenci 10denního tréninkového plánu před dovolenou.

## Funkce
- 10 dní s popisem zaměření, rozpisem tréninku a checklistem úkolů
- Zaškrtávání splněných částí tréninku (den se označí jako splněný, když jsou hotové všechny úkoly)
- Poznámky ke každému dni
- Hodnocení dne (1–10) a celkové skóre za 10 dní (/100)
- Export průběhu do JSON souboru a jeho zpětné načtení (funguje i offline, bez účtu a databáze)

## Jak nahrát na GitHub a spustit přes GitHub Pages

1. Vytvoř nový repozitář na GitHubu, např. `treninkovy-denik`.
2. Nahraj do něj soubor `index.html` (a klidně i toto `README.md`) — buď přes web rozhraní GitHubu (**Add file → Upload files**), nebo z příkazové řádky:
   ```bash
   git init
   git add index.html README.md
   git commit -m "10denní tréninkový deník"
   git branch -M main
   git remote add origin https://github.com/TVOJE-JMENO/treninkovy-denik.git
   git push -u origin main
   ```
3. V repozitáři jdi do **Settings → Pages**.
4. U „Build and deployment“ vyber **Deploy from a branch**, větev `main` a složku `/ (root)`.
5. Ulož. Po chvíli bude appka dostupná na:
   `https://TVOJE-JMENO.github.io/treninkovy-denik/`

Žádný build krok, žádné závislosti — funguje to jako statická stránka.

## Poznámka k ukládání dat
Appka neukládá data do prohlížeče automaticky (kvůli kompatibilitě funguje čistě v paměti relace). Použij tlačítko **„Uložit průběh (JSON)“** na konci každého dne/tréninku a **„Načíst uložený průběh“** při dalším otevření appky, aby ses nemusel spoléhat na to, že prohlížeč data nesmaže.
