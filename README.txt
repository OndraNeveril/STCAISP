Šifrovací pomůcky
Cipher decoder

Tagy: Šifry; Python; Strojové učení; Překlad textu

Odkaz na repositář (pokud není, nech prázdné):
Odkaz na výsledek (pokud není, nech prázdné):

---

Anotace projektu: Tady popiš svůj projekt, co bylo jeho cílem a čeho jsi dosáhl. Může být klidně abstract z paperu. Popis nemusí být dlouhý, vše stačí v jednom odstavci.

---

Paper: vlož cestu (path) k paperu např. `paper.pdf` nebo `documents/paper.pdf`

Reflexe: vlož cestu (path) l reflexi např. `reflexe.pdf` nebo `documents/reflexe.pdf`

Soubory:
  - fonty - obsahují skautské fonty,  které se používají k zašifrování textů, jedná se o 10 vybraných fontů, tak, aby byl překlad jednoznačný. Vyvužívají se pouze v programu dataset.py (více v sekci o něm).
  - dataset - složka obsahuje dvojici zašifrované a originální zprávy (soubory zadání.png a řešení.txt), vygenerované pomocí programu dataset.py, určené k natrénování a testování modelu na řešení šifer.
  - dataset.py - program, určený k vytváření datasetů, generuje náhodné anglický text o rozsahu několika krátkých vět, které následně překládá do všech vybraných fontů. Vzhledem k tomu, že dataset lze vytvořit pomocí tohoto progarmu a jednotlivých fontů, není součástí repozitáře.