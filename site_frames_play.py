#!/usr/bin/env python3
"""공공기관·기업 탭 프레임에 밈 탭과 같은 공식 퍼가기 재생(vplay)을 넣는다. 사용: python3 -I site_frames_play.py <page.html>...
밈 탭의 vplay-js와 #vplay CSS를 그대로 복사한다. 다시 돌려도 한 번만 들어간다."""
import re, sys
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    i = s.index('id="vplay-js"'); js = s[s.index('>', i) + 1: s.index('</script>', i)]
    css = ''.join(re.findall(r'#vplay[^{}]*\{[^}]*\}', s[:i]))
    blk = '<style id="vplay-css">' + css + '</style><script id="vplay-js">' + js + '<\\/script>'
    n = 0
    def fix(m):
        global n
        t = m.group(2)
        t = re.sub(r'<style id="vplay-css">.*?<\\/script>', '', t, flags=re.S)
        k = t.rfind('</body>'); t = t[:k] + blk + t[k:] if k >= 0 else t + blk
        n += 1
        return m.group(1) + t + '</script>'
    s = re.sub(r'(<script type="text/plain" id="tabsrc-[gc]">)(.*?)</script>', fix, s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s); print(p, n)
