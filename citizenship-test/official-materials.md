# Official materials

Everything the state publishes about the exam. The three sample tests are
copied into [official-samples/](official-samples/); each PDF is five pages and
ends with its answer key. The ministry publishes them without a licence or
terms of use.

## Sample tests (образци на тестове)

Published in 2013 by the then Център за контрол и оценка на качеството на
училищното образование (now ЦОПУО). All three use the same 20-question layout
described in the [guide](README.md#the-seven-question-types). Candidates in
2025 report that the real papers follow the same layout but are harder.

| Test | Reading text | Official link | Mirror (source of the local copy) |
|---|---|---|---|
| [Вариант 1](official-samples/variant_1.pdf) | Бургас, „най-добрият град за живеене в България" 2012, with a ranking table | [variant_1.pdf](https://io.mon.bg/sites/default/files/uploads/docs/2013-06/variant_1.pdf) | [Sample-Test-1.pdf](https://www.bulgarian-citizenship.com/wp-content/uploads/2023/11/Sample-Test-1.pdf) |
| [Вариант 2](official-samples/variant_2.pdf) | Васил Левски | [variant_2.pdf](https://io.mon.bg/sites/default/files/uploads/docs/2013-06/variant_2.pdf) | [Sample-Test-2.pdf](https://www.bulgarian-citizenship.com/wp-content/uploads/2023/11/Sample-Test-2.pdf) |
| [Вариант 3](official-samples/variant_3.pdf) | Тетевен as a tourist destination | [variant_3.pdf](https://io.mon.bg/sites/default/files/uploads/docs/2013-06/variant_3.pdf) | [Sample-Test-3.pdf](https://www.bulgarian-citizenship.com/wp-content/uploads/2023/11/Sample-Test-3.pdf) |

Scribd also has copies of variants 1 and 3
([1](https://www.scribd.com/document/773955714/),
[3](https://www.scribd.com/document/773955777/)). No real past papers are
published anywhere that this research found.

**Where the local copies come from:** all three PDFs were downloaded again on
2026-10-03 directly from the io.mon.bg links above. Their SHA-256 hashes match
the previously committed mirror copies. The temporary download script has
been removed after use. The mirror links remain as fallback sources.

Each PDF has a matching JSON file in `official-samples/`, containing the
reading passage, the 20 questions and the official answer key for the MCP
tutor. The original PDFs remain the source of truth. Extraction retained
the question wording and options. In variant 3, answer 4's printed Cyrillic
б was extracted as the digit 6; the JSON records Б after checking the rendered
answer page. Official samples have no authored teaching explanations; the
AI tutor explains them after marking against the key.

Instruction printed on every paper: „Изберете само един от предложените
отговори и заградете с кръгче буквата пред него."

**Suggested use:** sit variant 1 cold in week 1 to see where you stand, and keep
variants 2 and 3 for the final week as timed mocks.

## The exam page

ЦОПУО, „Изпити по български език за българско гражданство – Обща информация":
<https://www.copuo.bg/node/600> (same page:
<https://io.mon.bg/node/600>). This is where the monthly dates, the
application form and the results are published. It blocks automated access, so
open it in a normal browser.

ЦОПУО address for applications: бул. „Цариградско шосе" 125, бл. 5, ет. 2,
1113 София.

## Law and ordinance

- **Закон за българското гражданство** (ДВ бр. 136/1998, last amended ДВ бр.
  55 от 16.06.2026). Consolidated text in the government's service register:
  <https://iisda.government.bg/adm_services/service_regulatory_file/20082_213644>.
  The relevant articles: чл. 12, ал. 1, т. 5 (language requirement), чл. 13–14
  (spouses, stateless persons), чл. 15 and 16 (exemptions).
- **Наредба № 5 от 03.09.1999 г. за реда за установяване владеенето на
  български език при придобиване на българско гражданство по натурализация**
  (ДВ бр. 81/1999; amended 2000, 2001, 2011, 2015, and at least once later).
  MON's page:
  <https://www.mon.bg/regulation/naredba-%E2%84%96-5-ot-03-09-1999-g-za-reda-za-ustanovyavane-vladeeneto-na-balgarski-ezik-pri-pridobivane-na-balgarsko-grazhdanstvo-po-naturalizaczia/>;
  2015 consolidated text: <https://ekspertis.bg/document/view/law/103028>.
  Key points:
  - чл. 2: a diploma from a Bulgarian school replaces the exam.
  - чл. 3: apply to the Minister of Education with a copy of your ID.
  - чл. 5: a ministry commission assesses and the minister issues the
    certificate.
  - чл. 6: a written test monthly; oral interview instead for the blind,
    disability group I–II and people over 70; retake after a waiting period.
  - чл. 7: applicants abroad can apply and sit the test through Bulgarian
    embassies and consulates.
- **Ministry of Foreign Affairs leaflet** on general naturalisation (lists the
  language certificate or a Bulgarian diploma among the documents):
  <https://www.mfa.bg/upload/564/5_Grajdanstvo_po_obshta_naturalizaciq.pdf>.
- **The 2023–2024 bill** that would have required Bulgarian from people of
  Bulgarian origin: motives at
  <https://www.mfa.bg/upload/104502/UO_MVNR_MOTIVI_17.11.2023.pdf>; first
  reading 21.02.2024 (BTA:
  <https://www.bta.bg/bg/news/bulgaria/622229-vladeeneto-na-balgarski-ezik-stava-zadalzhitelno-za-pridobivane-na-balgarsko-gra>).
  It did not become law.

## Pass statistics (ЦОПУО annual reports)

| Year | Candidates | Certificates | Source |
|---|---|---|---|
| 2018 | 705 | 547 (78%) | [report](https://io.mon.bg/sites/default/files/uploads/docs/2022-01/COPUO_doklad_za_de__nost_2018.pdf) |
| 2019 | 767 | 569 (417 by exam, 152 from documents) | [report](https://io.mon.bg/sites/default/files/uploads/docs/2022-01/COPUO_doklad_za_de__nost_2019.pdf) |

Later reports (2023 onwards) are under
<https://io.mon.bg/sites/default/files/uploads/docs/> but were not read.
