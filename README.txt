Šifrovací pomůcky
Cipher decoder

Tagy: Šifry; Python; Strojové učení; Rozpoznávání obrazu; Překlad textu

Odkaz na repositář: https://github.com/OndraNeveril/STCAISP
Odkaz na výsledek: decoder.exe

---

Anotace projektu: Tady popiš svůj projekt, co bylo jeho cílem a čeho jsi dosáhl. Může být klidně abstract z paperu. Popis nemusí být dlouhý, vše stačí v jednom odstavci.

---

Paper: paper.pdf

Reflexe: reflexe.pdf

Soubory:

  - dataset.py - program, určený k vytváření datasetů, generuje náhodná anglická slova, které následně překládá do všech vybraných fontů a dále jednotlivých písmen přčeložených do všech fontů. Vzhledem k tomu, že datasety lze vytvořit pomocí tohoto progarmu a jednotlivých fontů, nejsou součástí repozitáře.

  - Dataset - složka obsahuje dataset jednotlivých typů šifer (obrázku se zašifrovaným slovem přiřazeným ke správné tříde - typu šifry), vygenerované pomocí programu dataset.py, určené k natrénování a testování modelu na řešení šifer.

  - Dataset_letters - složka obsahující datasety pro každý typ šifry, sloužící k natrénování rozpoznávání jednotlivých písmen, rovnež generováno programem dataset.py

  - decoder.py - Zdrojový kód aplikace, definuje GUI a používá funkce z reseni.py za účelem vytvoření nebo dekódování šifry

  - decoder.exe - Samotná aplikace, uživatel načte obrázek a nechá si vyřešit šifru nebo zadá text a nechá si šifru vytvořit

  - fonty - obsahují skautské fonty,  které se používají k zašifrování textů, jedná se o 10 vybraných fontů, tak, aby byl překlad jednoznačný. Vyvužívají se pouze v programu dataset.py (více v sekci o něm).

  - modely - složka obsahující jednotlivé nejlepší natrénované modely označené názvy šifer, best_model.pth slouží k rozpoznávání jednotlivých šifer

  - output - složka sloužící k ukládání uživatelem vygenerovaných zadání šifer

  - reseni.py - "knihovna" obsahující mnou definované funkce používané k rozpoznání a vyřešení šifry, a k natrénování modelů. Při přímém spuštění tohoto zdrojového kódu se začnou trénovat neuronky,, nejdříve na typy šifer a poté na jednotlivé znaky pro každý typ šofry. Při načtení této knihovny jiným souborem se rovnou použijí nejlepší natrénované modely ze složky "modely"

  - STC_specifikace.pdf - Původní specifikace zadání projektu

