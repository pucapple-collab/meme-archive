#!/usr/bin/env python3
"""publish_week.py 실행 뒤 매번 실행: 상단 칩을 사이트 안 지난 호/다음 호 링크로 바꾼다(claude.ai 주소 칩 제거).
사용: python3 -I site_pager.py <현재 호 번호>"""
import re, os, sys, glob
cur = int(sys.argv[1]); R = os.path.dirname(os.path.abspath(__file__))
pat = re.compile(r'<script>\(function\(\)\{var b=document\.getElementById\("sbar"\);if\(!b\)return;(?:var L=|var a=document\.createElement\("a"\);a\.href="https://claude\.ai).*?\}\)\(\)</script>', re.S)
def js(n, pref):
    P = {k: (pref + ('' if k == cur else 'archive/%d호/' % k)) for k in range(1, cur + 1)}
    import json
    return ('<script id="sitepager">(function(){var P=%s,N=%d,t=0;function chip(k,left){var u=P[k],a=document.createElement(u!==undefined?"a":"span");a.className="pgchip";a.textContent=left?"← "+k+"호":k+"호 →";'
     'if(u!==undefined){a.href=u||"./";}else{a.textContent=left?"← 이전 호 없음":"다음 호 없음"}'
     'a.style.cssText="flex:none;border-radius:99px;font:600 13px var(--f-body);padding:8px 13px;text-decoration:none;white-space:nowrap;"+(u!==undefined?"background:#fff;color:#000":"background:#fff2;color:#fff8");return a}'
     'function fix(){var b=document.getElementById("sbar");if(!b)return;if(b.querySelector(".pgchip"))return;var c=b.querySelector(".cnt");b.insertBefore(chip(N-1,1),b.firstChild);b.insertBefore(chip(N+1,0),c||null)}'
     'var iv=setInterval(function(){fix();if(++t>50)clearInterval(iv)},300);fix()})()</script>') % (json.dumps(P, ensure_ascii=False), n)
pages = [(os.path.join(R, 'index.html'), cur, '')] + [(p, int(re.search(r'archive/(\d+)호', p).group(1)), '../../') for p in glob.glob(os.path.join(R, 'archive', '*호', 'index.html'))]
for p, n, pref in pages:
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<script id="sitepager">.*?</script>', '', s, flags=re.S)
    s = pat.sub('', s)
    i = s.rindex('</body>'); s = s[:i] + js(n, pref) + s[i:]
    open(p, 'w', encoding='utf-8').write(s)
print('ok', cur)
# 방문 통계 코드 넣기(11/04 Jc 지시)
import subprocess; subprocess.run([sys.executable, '-I', os.path.join(R, 'site_stats.py')], check=True)
