#!/usr/bin/env python3
"""금요일 갱신: 현재 index.html을 archive/<호>/index.html로 옮기고 새 index.html을 만든다.
사용: python3 -I publish_week.py <새 호 번호> <새 공유용 HTML 경로> [이전 호 이름]
- 주소(/)는 항상 최신 호, 지난 호는 /archive/<호>/ 로 이관, 상단에 지난 호 목록 띠를 넣는다.
- 썸네일은 thumbs/ 한 폴더를 공유한다(지난 호가 쓰는 파일은 지우지 않는다)."""
import sys, os, re, json, html
R = os.path.dirname(os.path.abspath(__file__))
num, src = sys.argv[1], sys.argv[2]
prev = sys.argv[3] if len(sys.argv) > 3 else None
idx_p = os.path.join(R, 'index.html'); meta_p = os.path.join(R, 'archive', 'issues.json')
issues = json.load(open(meta_p, encoding='utf-8')) if os.path.exists(meta_p) else []
old = open(idx_p, encoding='utf-8').read()
BAR = re.compile(r'<div id="issuebar".*?</div>', re.S)
if prev and 'id="vplay-js"' in old:
    d = os.path.join(R, 'archive', prev); os.makedirs(d, exist_ok=True)
    a = BAR.sub('', old).replace('src="thumbs/', 'src="../../thumbs/')
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(a)
    issues = [i for i in issues if i['name'] != prev] + [{'name': prev}]
def bar(base):
    ls = ''.join(f'<a href="{base}archive/{html.escape(i["name"])}/" style="color:#ffd84d;margin-left:10px">{html.escape(i["name"])}</a>' for i in reversed(issues))
    return ('<div id="issuebar" style="position:fixed;z-index:9;left:12px;right:12px;bottom:calc(10px + env(safe-area-inset-bottom,0px));max-width:560px;margin:0 auto;border-radius:12px;background:#111e;border:1px solid #fff3;backdrop-filter:blur(8px);color:#fff;font:600 12px/1.5 system-ui,sans-serif;padding:7px 14px;text-align:center">'
            f'현재 {html.escape(num)}호 · 지난 호:{ls or " 아직 없음"}</div>')
sh = open(src, encoding='utf-8').read().replace('../thumbs/', 'thumbs/')
i = old.index('<body>') + len('<body>'); j = old.rindex('</body>')
open(idx_p, 'w', encoding='utf-8').write(old[:i] + '\n' + bar('') + sh + old[j:])
for it in issues:  # 지난 호 페이지에도 목록을 갱신해 서로 이동 가능하게 함
    p = os.path.join(R, 'archive', it['name'], 'index.html')
    if os.path.exists(p):
        t = BAR.sub('', open(p, encoding='utf-8').read()); k = t.index('<body>') + 6
        open(p, 'w', encoding='utf-8').write(t[:k] + '\n' + bar('../../').replace('현재 ' + num + '호', '지난 호 보는 중 · 최신은 <a href="../../" style="color:#ffd84d">' + num + '호</a>') + t[k:])
json.dump(issues, open(meta_p, 'w', encoding='utf-8'), ensure_ascii=False)
print('ok', num, [i['name'] for i in issues])
