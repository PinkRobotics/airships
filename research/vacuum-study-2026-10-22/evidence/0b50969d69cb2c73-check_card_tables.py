import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from checklib import *
import decimal
audit=Audit();mats=materials()
result=json.loads((ROOT/"RESULTS.json").read_text())
own_gaps=json.loads((ROOT/"INDEPENDENT-GAPS.json").read_text())
gapindex={(o["material"],o["reserve"],o["section_policy"],o["load_case"]):x
          for o,x in zip(read("GAPS.json")["rows"],own_gaps)}
own_hail=json.loads((ROOT/"INDEPENDENT-HAIL.json").read_text())
hailindex={(o["material"],o["reserve"],o["section_policy"],o["diameter_m"]):x
           for o,x in zip(read("HAIL.json")["rows"],own_hail)}
def token(name,field,text,expected):
    if expected is None:
        audit.check(name,field+" unavailable",True,text in ["unknown","no finite m"])
        return
    v=float(text);unit=float(decimal.Decimal(text).as_tuple().exponent)
    atol=.500001*10**unit+1e-10*abs(expected)
    audit.check(name,field,v,expected,rtol=0,atol=atol)
tables=[];current=[]
for line in (OWNER/"CARD.md").read_text().splitlines()+[""]:
    if line.startswith("|"):current.append([x.strip() for x in line.strip("|").split("|")])
    elif current:tables.append(current);current=[]
for tindex,table in enumerate(tables):
    for row in table[2:]:
        name=f"CARD table{tindex+1}/{row[0]}"
        if tindex==0:
            m=int(row[0]);expected=[]
            for pf,res in [(.001,"5"),(.001,"019"),(1e-6,"5"),(1e-6,"019")]:
                base,arr,_=base_data(res);s=base["section"]
                ss,_=peak(arr,mats["041-reference"],s["r_o_m"],s["wall_m"],base["least_screened_SF"])
                expected.append(scale(ss,m,pf)/1e9)
            for j,v in enumerate(expected):token(name,str(j),row[j+1],v)
        elif tindex==1:
            mat=row[0];w=next(x for x in result["witnesses"] if x["material"]==mat and x["reserve"]=="5")
            for j,k in enumerate(["frame_kg","total_including_reserve_sag_kg","SF_or_ceiling"]):
                token(name,k,row[j+1],w[k])
            for res,text in zip(["5","019"],row[4].split(" / ")):
                x=json.loads((ROOT/"fe"/f"{mat}-{res}-same_tube_mass-m6-intact.json").read_text())
                token(name,"same-mass/"+res,text,x["conditional_SF_or_ceiling"])
        elif tindex==2:
            mat=row[0]
            for res,text in zip(["5","019"],row[1].split(" / ")):
                x=json.loads((ROOT/"fe"/f"{mat}-{res}-same_tube_mass-m6-intact.json").read_text())
                expected=x["q1_whole_member_scale_needed_m10_Pf1e3_Pa"]
                token(name,"scale/"+res,text,None if expected is None else expected/1e9)
            g=gapindex[mat,"5","same_tube_mass","operating"]
            ss=mats[mat]["screen_compression_Pa"]
            x=json.loads((ROOT/"fe"/f"{mat}-5-same_tube_mass-m6-intact.json").read_text())
            target=x["q1_whole_member_scale_needed_m10_Pf1e3_Pa"]
            token(name,"scale-ratio",row[2],None if ss is None or target is None else target/ss)
            token(name,"m",row[3],g.get("hypothetical_m_needed_for_Pf1e3"))
        elif tindex==3:
            x=hailindex[row[0],"5","same_tube_mass",.0508];ss=x["stress_Shi_Pa"]
            for j,v in enumerate([ss/1e6,probability([ss],4.6,299e6),probability([ss],5.5,192e6)]):
                token(name,str(j),row[j+1],v)
        elif tindex==4:
            mat=row[0]
            for res,textsf,textratio in zip(["5","019"],row[1].split(" / "),row[2].split(" / ")):
                intact=json.loads((ROOT/"fe"/f"{mat}-{res}-same_tube_mass-m6-intact.json").read_text())
                cases=[json.loads(p.read_text()) for p in (ROOT/"fe").glob(f"{mat}-{res}-same_tube_mass-m6-lost*.json")]
                token(name,"postloss-SF/"+res,textsf,min(x["conditional_SF_or_ceiling"] for x in cases))
                values=[x["q1_peak_compression_Pa"] for x in cases]
                ratio=None if any(v is None for v in values) or intact["q1_peak_compression_Pa"] is None else max(values)/intact["q1_peak_compression_Pa"]
                token(name,"compression-ratio/"+res,textratio,ratio)
rounding=[]
for mat,reported in [("K13D2U-50-20-20-10",4282),("M55J-50-20-20-10",5249),("Al6061T6",21179)]:
    w=next(x for x in result["witnesses"] if x["material"]==mat and x["reserve"]=="5")
    total=w["total_including_reserve_sag_kg"]
    audit.check(mat,"report_mass_is_upward_integer_rounding",reported,math.ceil(total))
    rounding.append(dict(material=mat,exact_total_kg=total,reported_kg=reported,ceiling_kg=math.ceil(total),nearest_kg=round(total)))
dump("HEADLINE-MASS-ROUNDING.json",rounding)
audit.save("CARD-TABLES-CHECK.json")
