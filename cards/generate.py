#!/usr/bin/env python3
"""Generates cards.html from department data, matching the reference card design."""
import html

TITLE = "УПРАВЛЕНИЕ ОБЕСПЕЧЕНИЯ ПРОЦЕДУР БАНКРОТСТВА"

CARDS = [
    {
        "id": "card-1",
        "positions": ["Советник", "Консультант"],
        "department": "Отдел анализа рисков и работы со стратегическими организациями",
        "icons": [
            ("chip", "Системное мышление и стратегический анализ"),
            ("bar-chart", "Анализ финансово-хозяйственной деятельности"),
            ("scale", "Судебное представительство"),
            ("pen-document", "Разработка нормативно-правовых актов"),
            ("book", "Знание законодательства о банкротстве и госслужбе"),
            ("shield", "Работа со стратегическими предприятиями и ОПК"),
            ("people", "Межведомственное взаимодействие"),
        ],
    },
    {
        "id": "card-2",
        "positions": ["Начальник отдела", "Консультант"],
        "department": "Отдел по участию в судебных спорах",
        "icons": [
            ("bar-chart", "Анализ финансово-хозяйственной деятельности"),
            ("chain", "Установление аффилированности"),
            ("shield", "Субсидиарная ответственность"),
            ("coin", "Взыскание ущерба"),
            ("doc-x", "Оспаривание сделок"),
            ("book", "Знание НК, ГК, АПК, ГПК, УПК и Закона о банкротстве"),
            ("checklist", "Контроль ЦК ВПД и методическая работа"),
        ],
    },
    {
        "id": "card-3",
        "positions": ["Консультант"],
        "department": "Отдел по проектной работе с крупнейшими и проблемными должниками",
        "icons": [
            ("bank", "Работа с крупнейшими должниками"),
            ("alert-triangle", "Работа с проблемными должниками"),
            ("spreadsheet", "Уверенное владение Excel и Word"),
            ("book", "Знание Закона о банкротстве"),
            ("graduation", "Юр./эконом. образование, опыт от 2 лет"),
            ("database", "Работа с правовыми базами данных"),
            ("pen-document", "Подготовка заключений и поручений"),
        ],
    },
    {
        "id": "card-4",
        "positions": ["Консультант"],
        "department": "Отдел контроля процедур банкротства",
        "icons": [
            ("exchange", "Координация требований по платежам"),
            ("bank", "Взаимодействие с органами власти"),
            ("pin-check", "Контроль территориальных органов"),
            ("document", "Методология и отчётность"),
            ("envelope", "Обращения граждан и юрлиц"),
            ("gear", "Оптимизация структуры и КПЭ"),
            ("people", "Комиссии, аналитика, разъяснения"),
        ],
    },
    {
        "id": "card-5",
        "positions": ["Консультант"],
        "department": "Отдел методологии и автоматизации",
        "icons": [
            ("bar-chart", "Аналитика больших данных"),
            ("chip", "Работа с искусственным интеллектом"),
            ("spreadsheet", "Excel, Word, PowerPoint"),
            ("gear", "Внедрение программного обеспечения"),
            ("refresh", "Оптимизация процессов"),
            ("checklist", "Методология и устранение ошибок"),
        ],
    },
    {
        "id": "card-6",
        "positions": ["Консультант"],
        "department": "Отдел стратегических направлений обеспечения процедур банкротства",
        "icons": [
            ("book", "Знание НК РФ и Закона о банкротстве"),
            ("gear", "Организация запуска процедур банкротства"),
            ("document", "Анализ материалов и включение требований в реестр"),
            ("database", "Работа с большими данными"),
            ("spreadsheet", "Аналитика, справки, заключения, презентации"),
            ("people", "Анализ смены АУ и ведение реестра АУ"),
            ("bar-chart", "КПЭ, риски, методология, разъяснения"),
        ],
    },
]

ICON_DEFS = """
<symbol id="icon-exchange" viewBox="0 0 24 24"><path d="M4 8h13M13 4l4 4-4 4"/><path d="M20 16H7M11 12l-4 4 4 4"/></symbol>
<symbol id="icon-bank" viewBox="0 0 24 24"><path d="M3 10l9-6 9 6"/><path d="M5 10v9M9 10v9M15 10v9M19 10v9"/><path d="M3 21h18"/></symbol>
<symbol id="icon-pin-check" viewBox="0 0 24 24"><path d="M12 21s7-7.2 7-12a7 7 0 10-14 0c0 4.8 7 12 7 12z"/><path d="M9.3 9.2l1.9 1.9L15.2 7"/></symbol>
<symbol id="icon-document" viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M8 8h8M8 12h8M8 16h5"/></symbol>
<symbol id="icon-envelope" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3 6.5l9 6.5 9-6.5"/></symbol>
<symbol id="icon-gear" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M21.5 12h-3M5.5 12h-3M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1M18.4 18.4l-2.1-2.1M7.7 7.7L5.6 5.6"/></symbol>
<symbol id="icon-people" viewBox="0 0 24 24"><circle cx="8.5" cy="8" r="3"/><circle cx="16.2" cy="9" r="2.6"/><path d="M3 20c0-3.3 2.5-6 5.5-6s5.5 2.7 5.5 6"/><path d="M13.6 14.3c2.6.4 4.4 2.7 4.4 5.7"/></symbol>
<symbol id="icon-bar-chart" viewBox="0 0 24 24"><path d="M4 20V11M9.3 20V4M14.6 20v-8M19.9 20v-5.5"/><circle cx="19.9" cy="6" r="1.3" fill="currentColor" stroke="none"/></symbol>
<symbol id="icon-scale" viewBox="0 0 24 24"><path d="M12 3v18M6 22h12"/><path d="M3 6.5h18"/><path d="M6 6.5l3 4.3H3l3-4.3z"/><path d="M18 6.5l3 4.3h-6l3-4.3z"/><path d="M3 10.8a3 3 0 006 0M15 10.8a3 3 0 006 0"/></symbol>
<symbol id="icon-book" viewBox="0 0 24 24"><path d="M4 5.6c0-.9.7-1.6 1.6-1.6H12v16H5.6A1.6 1.6 0 014 18.4V5.6z"/><path d="M20 5.6c0-.9-.7-1.6-1.6-1.6H12v16h6.4c.9 0 1.6-.7 1.6-1.6V5.6z"/><path d="M12 4v16"/></symbol>
<symbol id="icon-shield" viewBox="0 0 24 24"><path d="M12 3l7.5 3v5.6c0 5-3.2 8.3-7.5 9.4-4.3-1.1-7.5-4.4-7.5-9.4V6l7.5-3z"/><path d="M8.7 12.2l2.2 2.2 4.4-4.4"/></symbol>
<symbol id="icon-chain" viewBox="0 0 24 24"><path d="M8.5 15.5l7-7"/><path d="M8 12.7l-2.4 2.4a3.6 3.6 0 005 5l2.4-2.4"/><path d="M16 11.3l2.4-2.4a3.6 3.6 0 00-5-5l-2.4 2.4"/></symbol>
<symbol id="icon-coin" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 6.5v11"/><path d="M9.3 9c0-1.3 1.2-2.2 2.7-2.2s2.7.9 2.7 2c0 3-5.4 1.4-5.4 4.5 0 1.1 1.2 2.2 2.7 2.2s2.7-.9 2.7-2.2"/></symbol>
<symbol id="icon-doc-x" viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 10.2l6 5.6M15 10.2l-6 5.6"/></symbol>
<symbol id="icon-checklist" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M7.5 9.2l1.6 1.6L12.5 7.2M7.5 15h9"/></symbol>
<symbol id="icon-alert-triangle" viewBox="0 0 24 24"><path d="M12 3.2l10 17.8H2L12 3.2z"/><path d="M12 10.2v4"/><circle cx="12" cy="17" r="0.9" fill="currentColor" stroke="none"/></symbol>
<symbol id="icon-spreadsheet" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 9.3h16M9.3 4v16M14.6 9.3V20"/></symbol>
<symbol id="icon-graduation" viewBox="0 0 24 24"><path d="M2 9l10-5 10 5-10 5-10-5z"/><path d="M6.5 11.2v4.6c0 1.7 2.5 3 5.5 3s5.5-1.3 5.5-3v-4.6"/><path d="M22 9v6"/></symbol>
<symbol id="icon-database" viewBox="0 0 24 24"><ellipse cx="12" cy="5.5" rx="8" ry="2.7"/><path d="M4 5.5V18c0 1.5 3.6 2.7 8 2.7s8-1.2 8-2.7V5.5"/><path d="M4 11.8c0 1.5 3.6 2.7 8 2.7s8-1.2 8-2.7"/></symbol>
<symbol id="icon-pen-document" viewBox="0 0 24 24"><rect x="4.5" y="3" width="13" height="18" rx="1.5"/><path d="M7.5 8h7M7.5 12h6M7.5 16h4"/><path d="M15 15.6l3.3-3.3 1.6 1.6-3.3 3.3H15v-1.6z"/></symbol>
<symbol id="icon-chip" viewBox="0 0 24 24"><rect x="7" y="7" width="10" height="10" rx="1.4"/><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.3 2.3M18 6l-2.3 2.3M6 18l2.3-2.3M18 18l-2.3-2.3"/><circle cx="12" cy="12" r="1.6"/></symbol>
<symbol id="icon-refresh" viewBox="0 0 24 24"><path d="M4.2 12a7.8 7.8 0 0113.6-5.2M19.8 12a7.8 7.8 0 01-13.6 5.2"/><path d="M17.2 3.2v4.4h-4.4M6.8 20.8v-4.4h4.4"/></symbol>
"""


def render_card(card):
    positions_html = " &nbsp;•&nbsp; ".join(html.escape(p) for p in card["positions"])
    icons_html = "\n".join(
        f'''        <div class="icon-col">
          <div class="icon-circle"><svg class="icon" viewBox="0 0 24 24"><use href="#icon-{icon_id}"/></svg></div>
          <div class="icon-label">{html.escape(label)}</div>
        </div>'''
        for icon_id, label in card["icons"]
    )
    return f'''
  <div class="slide" id="{card['id']}">
    <div class="bg-glow"></div>
    <div class="pill">{TITLE}</div>
    <div class="top-icon"><svg class="icon" viewBox="0 0 24 24"><use href="#icon-bar-chart"/></svg></div>
    <div class="position-row">
      <span class="position-text">{positions_html}</span>
      <span class="bullet"></span>
    </div>
    <div class="department">{html.escape(card["department"])}</div>
    <div class="icons-row">
{icons_html}
    </div>
  </div>'''


def main():
    slides = "\n".join(render_card(c) for c in CARDS)
    html_out = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Карточки отделов</title>
<style>
@font-face {{
  font-family: 'Montserrat';
  font-weight: 700;
  src: url('fonts/Montserrat-Bold.ttf') format('truetype');
}}
@font-face {{
  font-family: 'Montserrat';
  font-weight: 800;
  src: url('fonts/Montserrat-ExtraBold.ttf') format('truetype');
}}
@font-face {{
  font-family: 'Montserrat';
  font-weight: 900;
  src: url('fonts/Montserrat-Black.ttf') format('truetype');
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#111; }}
.slide {{
  position: relative;
  width: 1920px;
  height: 1080px;
  overflow: hidden;
  font-family: 'Montserrat', sans-serif;
  background:
    radial-gradient(ellipse 900px 720px at 88% 0%, rgba(139,92,246,0.55), transparent 62%),
    linear-gradient(135deg, #080a1e 0%, #10132f 38%, #221a50 72%, #362a6c 100%);
  margin-bottom: 40px;
}}
.pill {{
  position: absolute;
  top: 56px;
  left: 64px;
  max-width: 780px;
  padding: 30px 56px;
  border-radius: 70px;
  background: linear-gradient(100deg, #4dd0fa 0%, #7c6cf0 55%, #a35cf6 100%);
  box-shadow: 0 10px 34px rgba(124,108,240,0.4);
  color: #171233;
  font-weight: 800;
  font-size: 40px;
  line-height: 1.28;
  text-align: center;
  text-transform: uppercase;
}}
.top-icon {{
  position: absolute;
  top: 62px;
  right: 74px;
  width: 108px;
  height: 108px;
  border-radius: 50%;
  border: 2px solid rgba(120,205,255,0.85);
  background: radial-gradient(circle, rgba(90,70,150,0.25), rgba(20,15,45,0.05));
  display: flex;
  align-items: center;
  justify-content: center;
}}
.top-icon .icon {{ width: 52px; height: 52px; }}
.position-row {{
  position: absolute;
  top: 268px;
  left: 68px;
  display: flex;
  align-items: center;
  gap: 20px;
}}
.position-text {{
  color: #ffffff;
  font-weight: 800;
  font-size: 46px;
  white-space: nowrap;
}}
.bullet {{
  width: 18px;
  height: 18px;
  border-radius: 50%;
  flex-shrink: 0;
  background: radial-gradient(circle at 35% 32%, #d9c9ff, #8b5cf6);
  box-shadow: 0 0 16px 5px rgba(139,92,246,0.55);
}}
.department {{
  position: absolute;
  top: 348px;
  left: 68px;
  max-width: 1780px;
  font-weight: 800;
  font-size: 40px;
  line-height: 1.32;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  background: linear-gradient(90deg, #4dd0fa, #a879f6);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}}
.icons-row {{
  position: absolute;
  bottom: 96px;
  left: 70px;
  right: 70px;
  display: flex;
  justify-content: space-between;
}}
.icons-row::before {{
  content: '';
  position: absolute;
  top: 95px;
  left: 165px;
  right: 165px;
  height: 2px;
  background: rgba(125,175,255,0.35);
  z-index: 0;
}}
.icon-col {{
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 224px;
}}
.icon-circle {{
  width: 190px;
  height: 190px;
  border-radius: 50%;
  border: 2px solid rgba(103,196,255,0.85);
  background: radial-gradient(circle at 50% 38%, #2c2260 0%, #1b1542 58%, #120e2e 100%);
  box-shadow: 0 0 26px rgba(90,150,255,0.16), inset 0 0 22px rgba(0,0,0,0.45);
  display: flex;
  align-items: center;
  justify-content: center;
}}
.icon-circle .icon {{ width: 74px; height: 74px; }}
.icon-label {{
  margin-top: 24px;
  color: #ffffff;
  font-weight: 700;
  font-size: 23px;
  line-height: 1.35;
  text-align: center;
  max-width: 220px;
}}
.icon {{
  stroke: #ffffff;
  stroke-width: 1.6;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}}
svg.defs {{ position:absolute; width:0; height:0; }}
</style>
</head>
<body>
<svg class="defs"><defs>{ICON_DEFS}</defs></svg>
{slides}
</body>
</html>
'''
    with open("cards.html", "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Wrote cards.html")


if __name__ == "__main__":
    main()
