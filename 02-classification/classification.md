# 02. Классификация: ядра, линейки, сегменты, издания, каналы

## 2.1. Семейства ядер (главная ось классификации)

| Семейство | Годы | Ядро | Судьба |
|---|---|---|---|
| **DOS-оболочки / 9x** | 1985–2000 | 16-bit DOS + VMM32 (гибрид 16/32) | Мертво (98/Me — до 11.07.2006) |
| **NT** | 1993–н.в. | Гибридное ядро (команда Д. Катлера), Win32 | Живо; с 2015 нумерация заморожена на 10.0, builds 10240→29000+ |
| **CE** | 1996–2013 | RTOS-подобное компактное ядро | Мертво (Embedded Compact 7 — последняя) |
| **NT-мобильное** | 2012–2019 | NT 6.2/10.0 | Мертво (Windows 10 Mobile — до 14.01.2020) |
| **Производные** | 2001–н.в. | NT | Xbox OS, HoloLens, Windows IoT |

Эволюция NT-нумерации: 3.1 (1993) → 3.5/3.51 → 4.0 → 5.0 (2000) → 5.1/5.2 (XP/2003) → 6.0–6.3 (Vista…8.1) → 10.0 (Win10/11, Server 2016–2025). Разрыв Windows 95 ↔ NT преодолён только с XP (2001).

## 2.2. Сегменты

1. **Клиентский десктоп** — 1.0 … Windows 11 26H2.
2. **Серверный** — Advanced Server (1993) … Windows Server 2025; издания Standard/Datacenter/Essentials (и исторические Foundation, Small Business Server 2000–2011, Home Server 2007–2011).
3. **Мобильный** — CE/Pocket PC/Windows Mobile/Phone/Mobile (1996–2019).
4. **Встраиваемый/IoT** — NT Embedded (1999), XP Embedded (2001), Compact (до 2013), Standard 7/8, IoT Core/Enterprise (2015+), LTSC-ветки.
5. **Облачный** — Windows 365 Cloud PC (02.08.2021), Azure Virtual Desktop.
6. **Специальные** — Windows Team (Surface Hub), Holographic, S/SE (облегчённые), Starter, Media Center Edition, Tablet PC Edition, Ultimate, Multipoint.

## 2.3. Матрица изданий клиентской линейки

| Поколение | Издания |
|---|---|
| 1.x–3.x | (изданий нет, режимы: real / standard / 386 enhanced) |
| 95/98/Me | Retail, OEM, Upgrade; 95 OSR2/OSR2.5 |
| NT 3.1–4.0 | Workstation, Server, Advanced Server, Terminal Server (1999) |
| 2000 | Professional, Server, Advanced Server, Datacenter Server |
| XP | Home, Professional, MCE (2002/2004/2005), Tablet PC, Starter, x64, N/KN (антимонопольные), Embedded |
| Vista | Starter, Home Basic, Home Premium, Business, Enterprise, Ultimate (+N/KN) |
| 7 | Starter, Home Basic, Home Premium, Professional, Enterprise, Ultimate |
| 8/8.1 | Windows 8, Pro, Enterprise, RT (ARM) |
| 10 | Home, Pro, Pro for Workstations, Education, Enterprise, Enterprise LTSC, IoT Core/Enterprise, S, Team |
| 11 | Home, Pro, Pro Education, Pro for Workstations, Enterprise, Education, SE (свернуто после 24H2), IoT Enterprise LTSC 2024 |

Тренд: **упрощение линейки** (Vista/7 — 6–7 изданий; Win10/11 — фактически Home и Pro + корпоративные) и **удлинение LTSC-веток** (IoT Enterprise LTSC 2024 — поддержка до 10.10.2034).

## 2.4. Каналы обновлений (модель обслуживания)

| Механизм | Период | Суть |
|---|---|---|
| Ручные патчи + горячие фиксы | 1985–2003 | Отдельные KB по запросу |
| **Patch Tuesday** | с 10.2003 | Второй вторник месяца (введён после Blaster/Sasser) |
| Service Packs | 1995–2011 (Win7/2008R2 SP1) | Кумулятивные пакеты; Server 2025 возрождает идею через hotpatching (2025) |
| LTSB/LTSC | 2015–н.в. | 2015, 2016, 2019, 2021 (IoT — до 2032), 2024 (до 2034) |
| Semi-Annual Channel (H1/H2) | 2015–2021 | Два feature update в год (Win10) |
| Enablement-пакеты | 2019–н.в. | 1909, 20H2, 21H1/H2, 23H2, 25H2, 26H2 — «включатель» уже доставленных функций |
| **Continuous innovation** | с 2024–2026 | Ежемесячные новые функции + ежегодный enablement (официальная модель 26H2) |
| Insider-каналы | с 2014 | Canary, Dev, Beta, Release Preview |

## 2.5. Кодовые имена (систематизация)

**Подтверждены официально:** Neptune и Odyssey (отменённые предшественники XP), Whistler (XP), Longhorn (Vista), Threshold и Redstone (Win10), Germanium (24H2, фигурирует в документации Microsoft).

**По утечкам/индустриальным источникам:** Chicago (95), Memphis (98), Georgia (98 SE), Blackcomb → Vienna (поколение 7), Sun Valley (Win11 21H2), Sun Valley 2 (22H2), Nickel (23H2), Hudson Valley (упоминался для 25H2).

**Систематика имён выпуска:** годы (95/98/2000) → маркетинговые имена (Me, XP, Vista, 7) → «одно окно» (10) → возврат нумерации (11) → YYH2-формула (22H2…26H2).

## 2.6. Модель жизненного цикла

- Клиент: 10 лет (5 мейнстрим + 5 расширенной) — до Win10; далее feature updates 24 мес (Home/Pro) / 36 мес (Enterprise/Education).
- Сервер: 10 лет + ESU; Server 2025: мейнстрим до 09.10.2029, расширенная — до 10.10.2034.
- ESU (Extended Security Updates) — механика продолжения жизни: XP (2014–2017, с ограничениями), 7 (2020–2023), Win10 (корп. до 2028; потребители — до 12.10.2027: продлено 25.06.2026 со «стандартного» 13.10.2026).
- Рекорды долгожительства: XP — поддержка 12,5 лет; Windows 10 — 10 лет + 1 (ESU).
