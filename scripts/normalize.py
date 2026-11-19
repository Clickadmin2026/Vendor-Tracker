import json,re
R=json.load(open('rows.json'))
idx=next(i for i,r in enumerate(R) if r['Vendor']=='Under Consideration')
main,watch=R[:idx],R[idx+1:]
LINKS=['Partner Portal','Program Guide','Training','Incentives','Deal Reg','Sales Tools','Battle Cards','Marketing Campaigns','Misc. Link 1','Misc. Link 2','Misc. Link 3','Misc. Link 4','Support URL','Website']
def bl(s): return [re.sub(r'^[•\s]+','',x).strip() for x in re.split(r'\n',s or '') if re.sub(r'^[•\s]+','',x).strip()]
def disti(s):
    s=(s or '').lower(); o=[]
    for k,n in [('arrow','Arrow'),('ingram','Ingram Micro'),('synnex','TD SYNNEX'),('exclusive','Exclusive Networks'),('carahsoft','Carahsoft'),('climb','Climb'),('direct','Direct')]:
        if k in s and n not in o: o.append(n)
    return o
out=[]
for r in main:
    v=r.get('Last Accessed / Verified','')
    m=re.match(r'(\d{2})([A-Za-z]{3})(\d{4})\s*(.*)',v)
    date=f"{m.group(3)}-{m.group(2).title()}-{m.group(1)}" if m else None
    mon={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    iso=f"{m.group(3)}-{mon[m.group(2).title()]:02d}-{m.group(1)}" if m else None
    st=(m.group(4).strip() if m else v) or 'unchecked'
    links={}
    for k in LINKS:
        u=r.get(k+'|url') or (r.get(k) if str(r.get(k,'')).startswith('http') else None)
        if u and not u.startswith('mailto'): links[k]=u
    t=r.get('Tier'); t=int(t) if str(t) in('1','2') else None
    out.append(dict(name=r['Vendor'].strip(),status=r.get('Status') or '',tier=t,pid=str(r.get('Partner ID') or ''),
      vehicles=bl(r.get('Purchasing Vehicle')) if r.get('Purchasing Vehicle') not in('NA',) else [],
      links=links,competitors=bl(r.get('Competitors')) if not str(r.get('Competitors','')).startswith('Network') else bl(r.get('Competitors')),
      distis=disti((r.get('Distributor') or '')+' '+(r.get('Disti') or '')),
      contacts=r.get('Vendor Contacts','') or '',engineers=bl(r.get('Click Engineer')),vertical=r.get('Vertical') or '',
      distiContacts=r.get('Disti Contacts','') or '',growth=r.get('Growth Opportunity') or '',notes=r.get('Notes') or '',
      vdate=iso,vstate=st.lower()))
w=[dict(name=r['Vendor'],reason=r.get('Status',''),tech=r.get('Partner Portal','')) for r in watch]
json.dump(dict(v=out,w=w),open('data.json','w'),ensure_ascii=False)
import collections;print(collections.Counter(o['vstate'] for o in out),w)
