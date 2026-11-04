#!/usr/bin/env python3
"""사이트 모든 index.html에 방문 통계(GoatCounter) 코드를 넣는다. 여러 번 실행해도 한 번만 들어감.
site_pager.py 끝에서 자동 실행된다. 통계는 GoatCounter 대시보드(Jc 로그인)에서만 보이고 페이지에는 숫자를 표시하지 않는다.
본인 기기 제외: 각 브라우저에서 사이트 주소 뒤에 #toggle-goatcounter 를 붙여 한 번 연다(다시 열면 해제).
사용: python3 -I site_stats.py"""
import re, os, glob
CODE = 'memesuwon'  # GoatCounter 가입 때 정한 코드. 바꾸면 이 줄만 고치고 다시 실행
R = os.path.dirname(os.path.abspath(__file__))
TAG = ('<script id="gcstats" data-goatcounter="https://%s.goatcounter.com/count" '
       'async src="https://gc.zgo.at/count.js"></script>') % CODE
n = 0
for p in [os.path.join(R, 'index.html')] + glob.glob(os.path.join(R, 'archive', '*', 'index.html')):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<script id="gcstats"[^>]*></script>', '', s)
    i = s.rindex('</body>'); s = s[:i] + TAG + s[i:]
    open(p, 'w', encoding='utf-8').write(s); n += 1
print('stats ok', n, CODE)
