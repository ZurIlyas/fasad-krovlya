# Сборка сайта «Фасад и кровля» (Екатеринбург) из шаблона krovlya-kit.
# python _build/build.py — собирает шаблон и кладёт готовый сайт в корень этой папки.
import re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
KIT = HERE.parent / 'krovlya-kit' / 'site-template'
subprocess.run([sys.executable, '-X', 'utf8', str(KIT / 'make_site.py'), str(KIT / 'companies' / 'fasad.json')], check=True)
SITE = KIT / 'sites' / 'fasad'
s = (SITE / 'index.html').read_text(encoding='utf-8')

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)

# отзывов у компании нет: пустую цитату и звёзды убираем, остаются ссылки на 2ГИС и ВКонтакте
s, k = re.subn(r'<div class="v3-testi"><div class="v3-testi-stars">★★★★★</div><div class="v3-testi-text"></div>.*?</div></div></div>', '', s, count=1, flags=re.S)
assert k == 1
rep('<div class="v3-testi-stars">★★★★★</div>', '', 2)
rep('.van-reviews { margin-top: 56px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));',
    '.van-reviews { margin-top: 56px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));')

# калькулятор считает не только кровлю
rep('Шаг 1 из 3 · Площадь кровли', 'Шаг 1 из 3 · Площадь')
rep('aria-label="Площадь кровли в квадратных метрах"', 'aria-label="Площадь в квадратных метрах"')
rep('Шаг 2 из 3 · Тип кровли', 'Шаг 2 из 3 · Вид работ')
rep("'Здравствуйте! Хочу рассчитать кровлю. Площадь: ' + data.area + ' м². Тип: ' + data.label + '.'",
    "'Здравствуйте! Хочу рассчитать работы. Площадь: ' + data.area + ' м². Что нужно: ' + data.label + '.'")
rep('/* «Ван»: правки', '/* правки')

# демо: плашка сверху и авторы фото в подвале
rep('<body>\n', '<body>\n<div style="background:#111B30;color:#fff;font:600 13px/1.4 Manrope,system-ui,sans-serif;text-align:center;padding:9px 16px;position:relative;z-index:50;white-space:normal;max-width:100vw;box-sizing:border-box">Демо-версия сайта. Фото и цены стоят для примера: заменим на ваши.</div>\n')
rep('</footer>', '''  <div style="flex-basis:100%;margin-top:14px;font-size:12px;opacity:.55;line-height:1.5">Фото для примера: Mmanokhin (<a href="https://commons.wikimedia.org/wiki/File:%D0%9C%D0%BE%D0%BD%D1%82%D0%B0%D0%B6_%D0%B2%D0%B5%D0%BD%D1%82%D0%B8%D0%BB%D0%B8%D1%80%D1%83%D0%B5%D0%BC%D1%8B%D1%85_%D1%84%D0%B0%D1%81%D0%B0%D0%B4%D0%BD%D1%8B%D1%85_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC_%D1%81_%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%D0%BC_%D1%83%D1%82%D0%B5%D0%BF%D0%BB%D0%B8%D1%82%D0%B5%D0%BB%D1%8F_%D0%B8_%D0%B3%D0%B8%D0%B4%D1%80%D0%BE%D0%B8%D0%B7%D0%BE%D0%BB%D1%8F%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85_%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%BE%D0%B2.JPG" target="_blank" rel="noopener">CC BY-SA 3.0</a>), Cjp24 (<a href="https://commons.wikimedia.org/wiki/File:PSE_Insulation_boards_and_plaster_applied_on_a_building_facade.jpg" target="_blank" rel="noopener">CC BY-SA 4.0</a>), Kamil Czaiński (<a href="https://commons.wikimedia.org/wiki/File:Ku%C5%BAnia_Raciborska,_Drzyma%C5%82y_4,_budynek_w_trakcie_termomodernizacji_(styropianizacja)_02.jpg" target="_blank" rel="noopener">CC BY-SA 4.0</a>), Unsplash; фото обрезаны.</div>
</footer>''')

assert 'Ван' not in s and 'Краснодар' not in s
for d in ('frames', 'frames-sm', 'assets'):
    shutil.copytree(SITE / d, HERE / d, dirs_exist_ok=True)
(HERE / 'index.html').write_text(s, encoding='utf-8')
(HERE / '.nojekyll').write_text('')
print('готово:', HERE / 'index.html')
