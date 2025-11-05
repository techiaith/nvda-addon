# Uned Technolegau Iaith - Lleisiau Niwral Cymraeg ar gyfer NVDA

> **⚠️ MEDDALWEDD BETA** - Fersiwn 2025.11.0
> Mae hwn yn feddalwedd beta sydd ar hyn o bryd yn cael ei brofi. Adroddwch am unrhyw broblemau ar y [dudalen problemau GitHub](https://github.com/techiaith/nvda-addon/issues).

**Trosi testun-i-lafar niwral Cymraeg yn unig ar gyfer NVDA. Dim ond lleisiau Cymraeg sy'n cael eu cefnogi.**

Mae'r ychwanegyn hwn yn gweithredu gyrrwr syntheseiddydd lleferydd ar gyfer NVDA gan ddefnyddio modelau TTS niwral. Mae'n cefnogi lleisiau Cymraeg [Piper](https://github.com/rhasspy/piper).

Mae [Piper](https://github.com/rhasspy/piper) yn system trosi testun-i-lafar niwral lleol, cyflym sy'n swnio'n wych ac wedi'i optimeiddio ar gyfer dyfeisiau pen isel fel y Raspberry Pi.

Gallwch wrando ar samplau llais Piper yma: [samplau llais Piper](https://rhasspy.github.io/piper-samples/).

Mae'r ychwanegyn hwn yn defnyddio [Sonata: Peiriant Rust traws-blatfform ar gyfer modelau TTS niwral](https://github.com/mush42/sonata) sy'n cael ei ddatblygu gan Musharraf Omer.

## Gofynion System

- **System Weithredu:** Windows 10/11 (pensaernïaeth x86 neu x64)
  - ⚠️ **NID yw ARM64 Windows yn cael ei gefnogi** - Ni fydd yr ychwanegyn yn gweithio ar ddyfeisiau Windows ARM (e.e., Surface Pro X, gliniaduron ARM)
- **Fersiwn NVDA:** 2025.1 neu'n ddiweddarach
- **Cysylltiad Rhyngrwyd:** Yn ofynnol ar gyfer lawrlwytho llais cychwynnol (tua 77 MB)

## Beth Sy'n Gynwysedig

- **Fersiwn:** 2025.11.0 Beta
- **Llais Cymraeg:** Llais niwral aml-siaradwr (ansawdd canolig, 3 siaradwr)
- **Cefnogaeth Iaith:** Cymraeg yn unig
- **Lawrlwytho awtomatig:** Mae'r llais yn cael ei lawrlwytho'n awtomatig ar y tro cyntaf

# Gosod

## Lawrlwytho'r ychwanegyn

Gallwch ddod o hyd i'r pecyn ychwanegyn o dan yr adran asedau ar y [dudalen ryddhau](https://github.com/techiaith/nvda-addon/releases/latest)

## Gosod Llais Awtomatig

**Mae lleisiau Cymraeg yn cael eu lawrlwytho ar y tro cyntaf gyda'ch caniatâd.**

Pan fyddwch yn gosod yr ychwanegyn hwn am y tro cyntaf:

1. Gosodwch yr ychwanegyn ac ailgychwynnwch NVDA
2. Bydd deialog yn ymddangos yn gofyn a hoffech chi lawrlwytho lleisiau Cymraeg (tua 77 MB)
3. Os byddwch yn clicio "Iawn", bydd y lawrlwythiad yn dechrau a dangos diweddariadau cynnydd
4. Bydd NVDA yn cyhoeddi cynnydd ar 25%, 50%, a 75% cwblhau
5. Pan fydd yn gyflawn, bydd deialog cadarnhau yn ymddangos
6. Cliciwch "Iawn" i ailgychwyn NVDA ac actifadu'r lleisiau Cymraeg

Os byddwch yn clicio "Na" ar y ddeialog gychwynnol, gallwch lawrlwytho lleisiau yn ddiweddarach trwy osodiadau lleferydd NVDA.

## Newid Rhwng Lleisiau

I newid rhwng lleisiau Cymraeg gwahanol neu addasu gosodiadau llais:

1. Agorwch Osodiadau NVDA (NVDA+N, yna P am Ddewisiadau, yna S am Osodiadau)
2. Ewch i'r categori Lleferydd
3. Dewiswch "Uned Technolegau Iaith - Welsh Neural Voices" fel eich syntheseiddydd
4. Defnyddiwch y rhestr gwympo Llais i ddewis rhwng y lleisiau Cymraeg sydd wedi'u gosod
5. Addaswch gyfradd, traw a sain fel y dymunwch

Mae'r holl reoli lleisiau yn cael ei wneud trwy osodiadau syntheseiddydd safonol NVDA.

## Nodyn ar ansawdd llais

Mae'r lleisiau sydd ar gael ar hyn o bryd wedi'u hyfforddi gan ddefnyddio setiau data TTS sydd ar gael yn rhad ac am ddim, sydd yn gyffredinol o ansawdd isel (yn bennaf llyfrau sain parth cyhoeddus neu recordiadau ansawdd ymchwil).

Yn ogystal, nid yw'r setiau data hyn yn gynhwysfawr, felly gall rhai lleisiau arddangos ynganiad anghywir neu ryfedd. Gellid datrys y ddau broblem drwy ddefnyddio setiau data gwell ar gyfer hyfforddi.

Yn ffodus, mae datblygwr `Piper` a rhai datblygwyr o'r gymuned dall a nam ar eu golwg yn gweithio ar hyfforddi lleisiau gwell.

## Cyfyngiadau Hysbys (Beta)

- **Platfform:** Dim ond ar Windows x86/x64 y mae'n gweithio. Nid yw ARM64 Windows yn cael ei gefnogi.
- **Dewis Llais:** Ar hyn o bryd dim ond un llais Cymraeg gyda 3 amrywiad siaradwr (ansawdd canolig) sy'n cael ei gynnwys.
- **Statws Profi:** Mae hwn yn feddalwedd beta - profion cyfyngedig sydd wedi'u cynnal.
- **Cydweddoldeb NVDA:** Yn gofyn am NVDA 2025.1 neu'n ddiweddarach.
- **Tro Cyntaf:** Angen cysylltiad rhyngrwyd ar gyfer lawrlwytho llais awtomatig ar y defnydd cyntaf.

Os byddwch yn dod ar draws problemau, adroddwch amdanynt ar y [dudalen problemau GitHub](https://github.com/techiaith/nvda-addon/issues).

# Cydnabyddiaethau

Mae'r ychwanegyn hwn yn seiliedig ar [Sonata-NVDA](https://github.com/mush42/sonata-nvda) gan Musharraf Omer, sydd wedi'i addasu i weithio'n gyfan gwbl gyda lleisiau Cymraeg.

Rydym yn cydnabod yn ddiolchgar:
- **Musharraf Omer** am ddatblygu [Sonata](https://github.com/mush42/sonata) - y peiriant Rust traws-blatfform ar gyfer modelau TTS niwral sy'n pŵer yr ychwanegyn hwn
- **Musharraf Omer** am yr [ychwanegyn Sonata-NVDA](https://github.com/mush42/sonata-nvda) gwreiddiol y mae'r gwaith hwn yn seiliedig arno
- **Prosiect Piper TTS** a **chymuned Rhasspy** am ddatblygu lleisiau TTS niwral o ansawdd uchel

# Trwydded

Hawlfraint(c) 2024-2025, Stephen Russell, Uned Technolegau Iaith / Language Technologies Unit, Prifysgol Bangor.

Mae'r feddalwedd hon wedi'i thrwyddedu o dan Y DRWYDDED GYHOEDDUS GYFFREDINOL GNU Fersiwn 2 (GPL v2).

Yn seiliedig ar Sonata-NVDA gan Musharraf Omer, sydd hefyd wedi'i drwyddedu o dan GPL v2.