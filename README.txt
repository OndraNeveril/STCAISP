Šifrovací pomůcky
Cipher decoder

Tagy: Šifry; Python; Strojové učení; Rozpoznávání obrazu; Překlad textu

Odkaz na repositář: https://github.com/OndraNeveril/STCAISP
Odkaz na výsledek:

---

Anotace projektu: Tady popiš svůj projekt, co bylo jeho cílem a čeho jsi dosáhl. Může být klidně abstract z paperu. Popis nemusí být dlouhý, vše stačí v jednom odstavci.

---

Paper: vlož cestu (path) k paperu např. `paper.pdf` nebo `documents/paper.pdf`

Reflexe: vlož cestu (path) l reflexi např. `reflexe.pdf` nebo `documents/reflexe.pdf`

Soubory:
  - fonty - obsahují skautské fonty,  které se používají k zašifrování textů, jedná se o 10 vybraných fontů, tak, aby byl překlad jednoznačný. Vyvužívají se pouze v programu dataset.py (více v sekci o něm).
  - Dataset - složka obsahuje dvojici zašifrované a originální zprávy (soubory zadání.png a řešení.txt), vygenerované pomocí programu dataset.py, určené k natrénování a testování modelu na řešení šifer.
  - dataset.py - program, určený k vytváření datasetů, generuje náhodné anglický text o rozsahu několika krátkých vět, které následně překládá do všech vybraných fontů. Vzhledem k tomu, že dataset lze vytvořit pomocí tohoto progarmu a jednotlivých fontů, není součástí repozitáře.
  - reseni.py - "knihovna" obsahující mnou definované funkce používané k rozpoznání a vyřešení šifry, a k natrénování modelu. Při přímém spuštění tohoto zdrojového kódu se začne trénovat neuronka, při načtení této knihovny se rovnou použije nejlepší natrénovaný model (best_model.pth)
  - decoder.py - Zdrojový kód aplikace, definuje GUI a používá funkce z reseni.py
  - decoder.exe - Samotná aplikace, uživatel načte obrázek a nechá si vyřešit šifru
  - best_model.pth - Natrénovaný model, výsledek trénování souborem reseni.py na Datasetu
