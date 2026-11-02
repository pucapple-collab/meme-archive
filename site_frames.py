#!/usr/bin/env python3
"""공공기관·기업 공유본을 밈 탭과 같은 어두운 화면·상단 줄(호 이동 칩 · 정보 · 건수)로 바꿔 쓴다.
사용: python3 -I site_frames.py <in.html> <out.html> <현재 호> <이 페이지가 최신 호면 latest 아니면 archive>
"""
import re, sys
src, out, n, mode = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
BASE = 'https://pucapple-collab.github.io/meme-archive/'
def url(k): return BASE if (mode == 'latest' and k == n) else BASE + 'archive/%d호/' % k
s = open(src, encoding='utf-8').read()
cnt = len(re.findall(r'class="(?:cd|card|pv|vid)', s))
css = '''<style id="sitetop">
:root{--bg:#0b0b0d;--p:#17171c;--fg:#f2f2f5;--mu:#a6a9b6;--ln:#2c2c34;--ac:#9fb0ff;--no:#ff8a98;--nb:#3a1a20;--f-body:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif}
html,body{background:#0b0b0d;color:var(--fg)}
body{padding-top:58px}
#sbar2{position:fixed;z-index:6;left:0;right:0;top:0;padding:10px 12px 8px;display:flex;gap:8px;align-items:center;justify-content:center;background:linear-gradient(#0b0b0d,#0b0b0df0 70%,#0b0b0d00)}
#sbar2 a,#sbar2 button{flex:none;border:0;border-radius:99px;font:600 13px var(--f-body);padding:8px 13px;text-decoration:none;white-space:nowrap;cursor:pointer}
#sbar2 .on{background:#fff;color:#000}#sbar2 .off{background:#fff2;color:#fff8}#sbar2 .inf{background:#fff2;color:#fff}
#sbar2 .cnt{flex:none;color:#fff;font:600 12px ui-monospace,monospace;background:#0007;border-radius:99px;padding:6px 10px}
main,.sum,.sum p,h1,h2,h3,p{color:var(--fg)}.mu{color:var(--mu)!important}
a{color:var(--ac)}
.tabs button.on,.btns button:first-child{color:#0b0b0d!important}.bx.bo,.bx.bo .bl,.bx.bo *{color:#0b0b0d!important}
</style>'''
left = '<a class="on" target="_top" href="%s">← %d호</a>' % (url(n-1), n-1)
info = '<button class="inf" onclick="var s=document.querySelector(\'.sum\');if(s)s.scrollIntoView({behavior:\'smooth\',block:\'start\'})">ⓘ 정보</button>'
right = '<a class="off">다음 호 없음</a>' if mode == 'latest' else '<a class="on" target="_top" href="%s">%d호 →</a>' % (url(n+1), n+1)
m_ = re.search(r'영상 (\d+)건', s)
cn = '<span class="cnt">영상 %s건</span>' % m_.group(1) if m_ else ''
bar = '<div id="sbar2">' + left + info + right + cn + '</div>'
s = s.replace('</head>', css + '</head>', 1)
i = s.index('<body>') + 6
s = s[:i] + bar + s[i:]
open(out, 'w', encoding='utf-8').write(s)
print('ok', out)
