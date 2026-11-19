import openpyxl, json, re
wb=openpyxl.load_workbook('/mnt/user-data/uploads/c29c0533-Vendor_Tracker.xlsx')
print(wb.sheetnames)
ws=wb['Vendor List']
hdr=[(c.value or '').strip() if c.value else None for c in ws[1]]
rows=[]
for r in ws.iter_rows(min_row=2):
    if not r[0].value: continue
    d={}
    for i,c in enumerate(r[:30]):
        h=hdr[i]
        if not h: continue
        v=c.value
        if v is not None: d[h]=str(v).strip() if not isinstance(v,(int,float)) else v
        if c.hyperlink and c.hyperlink.target: d[h+'|url']=c.hyperlink.target
    rows.append(d)
json.dump(rows,open('rows.json','w'))
print(len(rows)); print(hdr[:30])
import collections
for k in ['Status','Tier','Distributor','Last Accessed / Verified','Vertical','Purchasing Vehicle']:
    print(k,collections.Counter(str(r.get(k)) [:40] for r in rows).most_common(25))
print(sum(1 for r in rows for k in r if k.endswith('|url')),'links')
print([r['Vendor'] for r in rows])
