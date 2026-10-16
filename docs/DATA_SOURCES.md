# 데이터 출처 목록

2026-10-16 작성. 2부 개념 목록(`model/catalog.json`)과 한국 적용 사례에 쓸 국내 데이터·통계의 입구를 한곳에 모았다. "접근" 열은 원자료(마이크로데이터) 기준이고, 공표 집계는 대부분 로그인 없이 받을 수 있다. 상태 열은 서브에이전트 확인 결과(아래 §4)로 갱신한다.

## 1. 1순위 — 개인 단위 신뢰·참여·수급이 있는 조사

| 조사 | 기관 | 입구 | 접근 | 이 수업에서 쓰는 것 |
| --- | --- | --- | --- | --- |
| 한국복지패널 | 보건사회연구원·서울대 | **https://www.koweps.re.kr:442** (포트 없으면 421 오류) · 조사표 /data/survey/list.do | 이용등록 + 활용정보 입력, 승인 없이 SAS/SPSS/STATA 다운로드. 1~20차 등재 | 수급 유형이 가장 정밀(생계·의료·주거·교육급여, 장려금, 기초연금, 장애수당, 아동수당 14차~, 보육료). 대인신뢰는 3년 주기(1·4·7·10·13·16차) → **16차(2021)**. 18차 지침서 PDF: repository.kihasa.re.kr/bitstream/201002/45366/3/p20240418-03.pdf |
| 사회통합실태조사 | 한국행정연구원(KIPA) | https://www.kipa.re.kr (자동 접근 403, **브라우저로 직접**) · KOSSDA 2023 조사지침서 PDF: kossda.snu.ac.kr/bitstream/20.500.12236/28189/5/kor_interviewer_instruction_20230040.pdf · 2021년판 handle/20.500.12236/25722 | KIPA 또는 KOSSDA 회원 | 대인신뢰 q28, 기관신뢰, 공정성, 참여, 사회보장 영역. 2023 조사표·sav 위치는 Ji가 직접 확인 |
| 사회조사 | 국가데이터처(옛 통계청) | **MDIS https://mdis.mods.go.kr** (옛 mdis.kostat.go.kr은 301 이전) · 제공자료 /ofrData/selectOrgOfrData.do?curMenuNo=UI_POR_P9220 | ONE-ID(KOSIS 계정) 가입. 공공용은 다운로드, 인가용은 승인·유료·연구계획서 심사(2026-10-15 공지) | 2023년 복지·사회참여·여가·소득소비·노동 부문. 단체활동·자원봉사·기부·사회 신뢰. 시도. 공공용/인가용 구분은 확인 필요 |
| 한국종합사회조사(KGSS) | 성균관대 서베이리서치센터 | https://kgss.skku.edu · 데이터 /kgss/data.do · 코드북 /_res/kgss/etc/2003-2025_KGSS_Codebook_v5.pdf · 설문지 /_res/kgss/etc/부록1_한국종합사회조사_설문지.pdf | 2003~2025 누적 zip(SPSS·STATA). 로그인 조건 미확인 | GSS식 일반신뢰·단체 가입. 국제 비교(ISSP) 가능. **조사표·코드북이 바로 열리는 유일한 조사** |
| 지역사회건강조사 | 질병관리청 | https://chs.kdca.go.kr · 조사표 /chs/qt/qtMain.do · 지침서 /chs/mnl/mnlBoardMain.do · 절차 /chs/rdr/rdrInfoProcessMain.do | 서약서·활용계획서 제출(2025 지침서는 "승인 없이", 부록은 14일 심의. 누리집 확인) | **이웃 신뢰(ena_01a1)·단체 참여(enb_04~07)·기초수급(fma_04z1)·시군구 코드(signgu_code)가 한 사람에게**. 2011·13·15·17·19·23년. 복지패널에 이은 두 번째 개인 단위 후보. 조사표 2009~2025 전부 로그인 없이 받음 |

## 2. 2순위 — 통제·지역 집계·제도 변수

| 자료 | 기관 | 입구 | 쓰임 |
| --- | --- | --- | --- |
| KOSIS 국가통계포털 | 국가데이터처 | https://kosis.kr | 시도·시군구 집계(수급률, 인구, 재정), OpenAPI. 계정이 MDIS ONE-ID와 공용 |
| MDIS 마이크로데이터 | 국가데이터처 | **https://mdis.mods.go.kr** | 가계금융복지조사(공적이전 항목별), 인구주택총조사 표본, 사회조사. 공공용 다운로드 / 인가용 원격접근·센터(승인·유료) / 주문형 |
| KOSSDA 한국사회과학자료원 | 서울대 | https://kossda.snu.ac.kr (자동 접근 403, 브라우저로) · 이용가이드 2024: kudos.knu.ac.kr/download/db/Manuals/2024KOSSDA.pdf | 사회통합실태조사·KGSS·주민참여예산 실태조사(2015, handle/20.500.12236/25654) 보관. 회원가입 → 다운로드 → 결과보고, 활용 후 파기 |
| 한국노동패널(KLIPS) | 한국노동연구원 | https://www.kli.re.kr/klips · 설문지 /klips/menu.es?mid=a40301050000 · 코드북 /klips/menu.es?mid=a40302000000 | 회원가입·로그인. 공개용·무응답대체·CNEF·자료추출시스템. 신뢰 문항은 부가조사에 한정 |
| 노인실태조사·청년삶실태조사 | 보건사회연구원 데이터포털 | https://www.kihasa.re.kr/dataportal/kor/contents/ContentsList.html | 신청서(목적·연구계획서·보안서약) → 승인 후 2주 다운로드. 청년삶실태조사 제공 여부 미확인 |
| 공공데이터포털 | 행정안전부 | https://www.data.go.kr | 아동수당·기초연금 수급 현황 파일, 지자체 주민참여예산 자료. 회원가입, API는 활용신청 |
| 지방재정365 | 행정안전부 | https://www.lofin365.go.kr | 시군구 복지 지출·주민참여예산 규모 (Freitag 한국 적용: 지방자치 수준). 공시·통계·데이터셋 |
| 주민투표·주민발의·주민참여예산 통계 | 행정안전부·선관위 | **공식 통계표 미확인** | Freitag 한국 적용: 직접민주주의 건수. 행안부 자치분권 자료실·선관위 선거통계시스템에서 Ji가 직접 찾아야 함 |
| 서울서베이 | 서울시 | https://data.seoul.go.kr (2026 서울서베이 공지 있음, 원자료 페이지 미확인) | 자치구 단위 신뢰·참여 (수도권 사례) |
| SGIS 통계지리정보 | 국가데이터처 | **https://sgis.mods.go.kr** (옛 sgis.kostat.go.kr은 302 이전) | 시군구 경계·격자. 회원가입·이용신청, API 키 |
| 복지로 | 보건복지부 | https://www.bokjiro.go.kr | 아동수당 연혁: 2018.9 소득 하위 90% 선별 도입 → **2019.1 소득 기준 폐지(보편)** → 2019.9 만 7세 미만으로 연령 확대 |
| e-나라지표 | 정부 | https://www.index.go.kr | 아동수당·기초연금 수급 추이. 2018·2019 수급자 표는 검색에서 못 찾음 → 보건복지부 통계연보·국회 자료로 |

## 3. 국제 조사 — 외국인 연구자가 받을 수 있는 것 (2026-10-16 확인)

GESIS·ANES·PSID는 자동 접속이 403이라 접근 조건은 검색 요약 기준. ESS 질문지와 SHP 이용 안내는 원문을 읽었다.

| 조사 | 입구 | 외국인 접근 | 신뢰 | 참여 | 복지·제도 | 한국 포함 |
| --- | --- | --- | --- | --- | --- | --- |
| **ESS** 유럽사회조사 | https://ess.sikt.no | 등록만(무료) R11까지 | ppltrst 0~10(K&R과 같은 척도), pplfair, 기관신뢰 trstprl·trstlgl·trstplc(B6~12) | 단체·정당 활동 B15~17 | **R4(2008)·R8(2016) 복지국가 모듈** E1~42: 부정수급 인식·실업급여 조건 태도. 본인 수급은 주소득원만 | 미포함 |
| **SHP** 스위스 가구패널 | https://forscenter.ch/projects/swiss-household-panel/data/ | SWISSUbase 계약 서명(무료·비상업) | 일반신뢰 | 결사체 가입·자원봉사(Freitag 2006 원자료) | 사회·민간 이전소득 | 없음 |
| ISSP | https://issp.org (GESIS 배포) | GESIS 등록(무료) | 2014 Citizenship II 정치인 신뢰 | 2014 단체 가입 | 2016 Role of Government V | **2014 한·일, 2016 한국** |
| WVS / EVS | https://www.worldvaluessurvey.org · https://europeanvaluesstudy.eu | 등록만(무료, 재배포 금지) | 일반신뢰·기관신뢰 | 단체 가입 | 태도 문항 | WVS W7 한국·미국. 일본은 SSJDA 신청 |
| GSS 미국 | https://gss.norc.org | 공개 다운로드 | TRUST, FAIR, 기관신뢰 CON* | MEMNUM 등 | HELPPOOR·NATFARE 태도. 수급 변수 미확인 | 없음. 2006~14 패널 있음 |
| EASS 동아시아 | ICPSR 36277 | JGSS와 동일 | 2012 Network Social Capital 모듈 | 단체 가입 | 미확인 | 한·일·중·대만 |
| JGSS / SSJDA 일본 | https://jgss.daishodai.ac.jp · https://csrda.iss.u-tokyo.ac.jp | 계정 + 연구계획 심사, 대학원생은 지도교수 동의. 해외는 직접 문의 | 미확인 | 미확인 | 미확인 | 없음(EASS로 연결) |
| SHARE 유럽 50+ | https://share-eric.eu | User Statement 이메일, 약 10영업일 | 미확인 | 미확인 | 연금·수급 미확인 | 없음 |
| Eurobarometer | GESIS | 등록 | 기관신뢰 | — | — | 없음 |
| CPS 시민참여 보충 | 미국 센서스·AmeriCorps | 공개 | — | 자원봉사·참여 | — | 없음 |
| ANES | https://electionstudies.org | 등록 | VCF0619 일반신뢰 | — | — | 없음 |
| PSID | https://psidonline.isr.umich.edu | 등록 | 미확인 | 미확인 | 수급 변수 | 없음 |
| ICPSR | https://www.icpsr.umich.edu | 무료 MyData 계정, 일부는 기관회원 한정(성균관대 회원 여부 미확인) | — | — | — | EASS 경유 |

**판단** Freitag 재현(제도 → 결사체)은 SHP가 1순위. K&R 재현(선별 수급 → 신뢰)은 국제 공개 자료 중 개인 수급 변수가 확인된 곳이 없다. 가장 가까운 것은 ESS R8 복지 모듈이나 인식 문항이고 횡단면이다. 한국을 함께 보려면 ISSP 2014. GSS 패널은 코드북에서 패널 파일 내 문항을 먼저 확인.

## 3-1. 선행연구 검색

| 자료 | 입구 | 쓰임 |
| --- | --- | --- |
| OpenAlex API | https://api.openalex.org | 선행연구 후보 수집(corpus/fetch_openalex.py). cursor 2페이지째 401 → page 방식 |
| Semantic Scholar API | https://api.semanticscholar.org | 인용 보완 |
| KCI | https://www.kci.go.kr | 국내 논문 검색("사회자본 결정요인", "복지 수급 신뢰", "제도신뢰 대인신뢰") |
| RISS | https://www.riss.kr | 국내 학위논문 |
| DBpia | https://www.dbpia.co.kr | 국내 논문 전문(학교 계정) |

## 4. 확인 결과 (2026-10-16, 서브에이전트 WebFetch·curl)

- 주소 이전: MDIS → mdis.mods.go.kr, SGIS → sgis.mods.go.kr (주관이 국가데이터처로 바뀜). 복지패널은 :442 포트 필수.
- 자동 접근 차단(403): kipa.re.kr, kossda.snu.ac.kr → 브라우저로 직접 열면 됨. sky.kipa.re.kr은 도서관 사이트라 조사 자료 없음.
- 조사표가 바로 열리는 곳: KGSS(코드북·설문지 PDF), 지역사회건강조사(조사표 페이지), 복지패널(조사표 목록, 파일은 로그인 후), 사회통합실태조사 2023 조사지침서(KOSSDA PDF).
- 미확인: 아동수당 2018·2019 수급자 수 공식 표, 주민투표·주민참여예산 공식 통계표, 청년삶실태조사 제공 경로, 서울서베이 원자료 페이지, MDIS 사회조사의 공공용/인가용 구분과 수수료.
- 로그인 뒤 화면과 실제 파일 다운로드는 확인하지 못함.

## 5. 다음 할 일

1. Ji: 복지패널 16차·사회통합실태조사 2023·사회조사 2023의 **조사표**를 받아 Google Drive 폴더에 올린다 → `model/catalog.json`.
2. 아동수당 2018·2019 수급자 수와 행정 비용 논란 수치(KOSIS·e-나라지표·국회 자료)를 5장 대사용으로 확인한다.
3. 시군구 결합이 필요하면 지역사회건강조사 원시자료 신청(승인에 시간이 걸리므로 일찍).
