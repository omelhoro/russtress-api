#!/usr/bin/python
#coding=utf8
"""
Igor:
Fr 19. Sep 14:14:33 CEST 2014
"""
import pandas as pd
import re
from setstress import setup_stress,RUS_VOWELS_re
import os
#os.path.expanduser("~/Data/rus_corps")

def find_stss_syl(x):
    vows="".join(RUS_VOWELS_re.findall(x.lower()))
    if len(vows)==1:
        return 1
    if u"ё" in vows:
        return vows.index(u"ё")+1
    if not vows.count("`"):
        return 997
    if vows.count("`")>1:
        stressed=vows[vows.find("`")+1:].find("`")
    else:
        stressed=vows.find("`")
    if stressed!=-1:
        return stressed+1
    else:
        return 998

def run_ruscorpora(fact=0.5):
    #setup morpher
    set_stress,pm=setup_stress(exclude=(4,))
    cut_data=lambda df: df[:int(len(df)*fact)]
    corp_path=os.path.expanduser("~/Data/rus_corps/mrgd_df.csv")
    mk1_df=cut_data(pd.read_csv(corp_path,index_col=0,encoding="utf8"))
    del mk1_df['gramm']
    map_stress={k:zip(*set_stress(pm,k.replace("`",""))) for k in mk1_df['token'].unique()}
    # print map_stress
    mk1_df['tok_stress']= mk1_df['token'].apply(find_stss_syl)
    mk1_df=mk1_df[mk1_df.tok_stress!=997] # drop tokens where stress is unset 
    mk1_df['guessed_stress']=mk1_df['token'].map(lambda x: set(map_stress[x][0])) 
    mk1_df['type_guess']=mk1_df['token'].map(lambda x: map_stress[x][1]) 
    mk1_df['iseq']=mk1_df.apply(
            lambda x: x['tok_stress'] in list(x['guessed_stress'])[:1],axis=1)
    # mk1_df['iseq']=mk1_df.apply(
    #         lambda x: x['tok_stress'] in x['guessed_stress'] if x['tok_stress']!=997 else True,axis=1)
    print("Tokens ratio:")
    print mk1_df['iseq'].value_counts().div(len(mk1_df))
    print("Types ratio:")
    types_df=mk1_df.drop_duplicates('token')
    print types_df['iseq'].value_counts().div(len(types_df))
    types_df[types_df['iseq']==False].to_csv("corp_data/falses.csv",encoding="utf8")
    return mk1_df
def type_stress(df):
    # v=pd.DataFrame(df['type_guess'].value_counts())
    # v["ratio"]=v[0]/len(df)
    gr=df.groupby(["type_guess",'iseq'])["tok_stress"].count().unstack()
    gr_ratio=gr.div(gr.sum(axis=1),axis=0)
    ratio_total=gr.join(gr_ratio,lsuffix="_total",rsuffix="_ratio").fillna(0).sort("True_total",ascending=False)
    print gr,ratio_total
    return ratio_total
df=run_ruscorpora(0.5)
type_stats=type_stress(df)


if __name__=="__main__":
    import sys
    try:
        if len(sys.argv)>1:
            fact=float(sys.argv[-1])
            if fact> 1:
                raise ValueError
        else:
            fact=0.5
        df=run_ruscorpora(fact)
        gr=type_stress(df)
    except ValueError:
        print("Factor value is not valid: Choose something between 0.0 and 1.0")
