#!/usr/bin/env python3
"""발행(publish_week·site_pager) 뒤 매번 실행: 페이지·기업/공공기관 프레임의 재생(vplay) 코드를 vplay_canon.js 최신본으로 통일하고,
프레임 안 script 조기 종료를 바로잡는다. 사용: python3 -I vplay_patch.py index.html [archive/*/index.html]"""
import sys, os
R = os.path.dirname(os.path.abspath(__file__)); body = open(os.path.join(R, 'vplay_canon.js'), encoding='utf-8').read()
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read(); i = s.index('id="vplay-js"'); a = s.index('>', i) + 1; b = s.index('</script>', a)
    old = s[a:b]; n = s.count(old); s = s.replace(old, body)
    s = s.replace('<\\/script></script>\n</body></html></script><script>(function(){var bs=', '<\\/script>\n</body></html></script><script>(function(){var bs=')
    s = s.replace('fix()})()<style id="vplay-css">', 'fix()})()<\\/script><style id="vplay-css">')
    open(p, 'w', encoding='utf-8').write(s); print(p, 'vplay 교체', n)
