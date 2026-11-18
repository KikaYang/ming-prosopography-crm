import re, json, csv
REIGNS={'洪武':1368,'建文':1399,'永樂':1403,'洪熙':1425,'宣德':1426,'正統':1436,'景泰':1450,'天順':1457,'成化':1465,'弘治':1488,'正德':1506,'嘉靖':1522,'隆慶':1567,'萬曆':1573,'泰昌':1620,'天啓':1621,'天啟':1621,'崇禎':1628}
NUM={'元':1,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
def cn(s):
    if s in ('元',): return 1
    if '十' in s:
        a,b=s.split('十'); return (NUM[a] if a else 1)*10+(NUM[b] if b else 0)
    return NUM[s]
MON=r'閏?(?:正|十[一二]?|[一二三四五六七八九])月'
STOP=r'(?='+MON+r'|以|由|召|復|晉|加|致仕|卒|免|丁憂|起復|兼|為|改|罷|削|入|仍|是|吏部|戶部|禮部|兵部|刑部|工部|少|太子|太常|太傅|太保|太師|翰林|詹事|左|右|南京|東閣|武英|文淵|謹身|華蓋|建極|中極|$|,|。|、|\(|\s)'
def lines(f):
    out=[]
    for l in open(f):
        l=l.rstrip('\n').replace('沈?','沈□').replace('李國 七月','李國□七月')
        if l.startswith('http') or '维基文库' in l or not l.strip(): continue
        out.append(l)
    return out
rows=[]  # (reign, ynum, gyear, label, rawtext)
persons={}  # full name -> last seen index
seen={'n':0}
order=[]
ALIAS={'孚敬璁':'張璁','孚敬':'張璁'}
BADSTART=set('兼以由召復晉加仍是入致卒免起改罷削為太少吏戶禮兵刑工翰詹左右侍南北東子學尚')
def resolve(tok_text, prev_open):
    for a,full in ALIAS.items():
        if tok_text.startswith(a): return full, tok_text[len(a):].strip()
    # try known names (longest first): full names and given-name abbreviations
    cands=[]
    for full in persons:
        for key in (full, full[1:]):
            if tok_text.startswith(key): cands.append((len(key),persons[full],full,key))
    if cands:
        cands.sort(reverse=True); _,_,full,key=cands[0]
        if prev_open and len(key)==1:  # previous entry not ending in "。": a one-character short name is read as a continuation line (fixes the misreading of Xu Youzhen's continuation line in juan 109, 2026-11-18)
            return None, tok_text
        rest=tok_text[len(key):]
        if rest=='' or re.match(STOP, rest) and (re.match(MON,rest) or not re.match(r'[\u4e00-\u9fff]',rest) or re.match(r'(以|由|召|復|晉|加|致仕|卒|免|丁憂|起復|兼|為|改|罷|削|入|仍|是|吏部|戶部|禮部|兵部|刑部|工部|少|太子|太常|翰林|詹事|左|右|南京)',rest)):
            seen['n']+=1; persons[full]=seen['n']; return full, rest.strip()
        m2=re.match(r'^(\S{2,3}?)'+STOP, tok_text)
        if m2 and len(m2.group(1))>len(key) and m2.group(1) not in persons:
            nf=m2.group(1); seen['n']+=1; persons[nf]=seen['n']; order.append(nf); return nf, tok_text[len(nf):].strip()
        seen['n']+=1; persons[full]=seen['n']; return full, rest.strip()
    m=re.match(r'^(\S{2,3}?)'+STOP, tok_text)
    if m and re.match(MON, m.group(1)+'月') is None and not re.fullmatch(MON, m.group(1)) and m.group(1)[0] not in BADSTART and not re.search(r'[,。、?]',m.group(1)) and (not prev_open or '入' in tok_text[:40]):
        full=m.group(1); seen['n']+=1; persons[full]=seen['n']; order.append(full); return full, tok_text[len(full):].strip()
    return None, tok_text
LABELS=[]
def run(f, start_pat=None):
    started = start_pat is None
    reign=None; gyear=None; label=None; cur=None
    for li,l in enumerate(lines(f)):
        if not started:
            if start_pat in l: started=True; gyear=1402; reign='洪武'; label='建文四年'
            else: continue
        lead=len(l)-len(l.lstrip())
        if lead>=30: left=''; right=l.strip()
        else:
            parts=re.split(r'\s{4,}', l.strip(), maxsplit=1)
            left=parts[0]; right=parts[1].strip() if len(parts)>1 else ''
        if left:
            m=re.match(r'^(洪武|建文|永樂|洪熙|宣德|正統|景泰|天順|成化|弘治|正德|嘉靖|隆慶|萬曆|泰昌|天啓|天啟|崇禎)?([元一二三四五六七八九十]{1,4})年', left)
            if m and not left.startswith('紀年'):
                if m.group(1): reign=m.group(1)
                if left.startswith('建文四年'): reign='洪武'; y=35
                else: y=cn(m.group(2))
                gyear=REIGNS[reign]+y-1; label=(reign or '')+m.group(2)+'年'
                if left.startswith('建文四年'): label='建文四年(洪武三十五年)'
                LABELS.append({'vol':f[2:5],'line':li,'year':gyear,'label':label})
                tail=left[m.end():]
            else:
                tail=left
            for rn in re.findall(r'(洪熙|宣德|正統|景泰|天順|成化|弘治|正德|嘉靖|隆慶|萬曆|泰昌|天啓|天啟|崇禎)', tail):
                if gyear is not None and REIGNS[rn] > REIGNS.get(reign,0): reign=rn
        right=re.sub(r'(?<=[正一二三四五六七八九十])\s+(?=月)','',right)
        if right.startswith('?'): right='□'+right[1:]
        if not right or gyear is None: continue
        prev_open = cur is not None and cur['text'] and not cur['text'].endswith('。')
        full, rest = resolve(right, prev_open)
        if full is None:
            if cur is not None: cur['text']+=right
            continue
        cur={'person':full,'reign':reign,'label':label,'year':gyear,'text':rest,'vol':f[2:5],'line':li}
        rows.append(cur)
run('ms109n.txt', start_pat='黃淮')
run('ms110n.txt')

blocks=[];curb=[]
for r in rows:
    if curb and (r['person'] in {x['person'] for x in curb} or r['vol']!=curb[-1]['vol']):
        blocks.append(curb); curb=[]
    curb.append(r)
blocks.append(curb)
import collections
def dp_assign(ents, labs):
    n=len(ents); m=len(labs)
    lines=[e['line'] for e in ents]
    # anchor: entry index on the same line as label (or first entry at/after label line within 1)
    anchor=[]
    for L in labs:
        a=[i for i,x in enumerate(lines) if x==L['line']]
        anchor.append(a[0] if a else None)
    # dup-free precompute: maxend[i] = largest j such that ents[i:j] has no repeated person
    maxend=[0]*n
    for i in range(n):
        seen=set(); j=i
        while j<n and ents[j]['person'] not in seen:
            seen.add(ents[j]['person']); j+=1
        maxend[i]=j
    INF=float('inf')
    best=[[INF]*(n+1) for _ in range(m+1)]; back=[[None]*(n+1) for _ in range(m+1)]
    best[0][0]=0
    for j in range(1,m+1):
        L=labs[j-1]; a=anchor[j-1]
        for e in range(1,n+1):
            for st in range(max(0,e-25),e):
                if best[j-1][st]==INF: continue
                c=0 if maxend[st]>=e else 1000
                if a is not None and not (st<=a<e): c+=500
                c+=abs((lines[st]+lines[e-1])/2-L['line'])*0.01
                v=best[j-1][st]+c
                if v<best[j][e]: best[j][e]=v; back[j][e]=st
    segs=[]; e=n
    for j in range(m,0,-1):
        st=back[j][e]; segs.append((st,e,labs[j-1])); e=st
    for st,e,L in segs:
        for r in ents[st:e]: r['year']=L['year']; r['label']=L['label']
    return best[m][n]
for vol in ('109','110'):
    ents=[r for r in rows if r['vol']==vol]
    labs=[]; seenl=set()
    for L in LABELS:
        if L['vol']!=vol: continue
        k=L['year']
        if k in seenl: continue
        seenl.add(k); labs.append(L)
    print(vol,'cost',round(dp_assign(ents,labs),2),'labels',len(labs))
json.dump({'rows':rows,'order':order,'nblocks':len(blocks)},open('zaifu.json','w'),ensure_ascii=False)
print(len(rows),'rows',len(order),'persons')
print(order)
