#!/usr/bin/python
#coding=utf8
'''
Created on 08.09.14
@author: igor'''
import re
import pymorphy2
import csv
import os

print(os.getcwd())

def csv_dct(fl):
    with open(fl) as f:
        return {l[0].decode("utf8"):l[1] for l in csv.reader(f)}
#%timeit d=csv_dct("dict_data/lem_df.csv")
#%timeit d1=pd.read_csv("dict_data/lem_df.csv",encoding="utf8",index_col=0,squeeze=True).to_dict()

def pm_setup(): 
    #must be a bug in morph:
    #эту - етот
    conv={u"етот":u"этот"}
    morph=pymorphy2.MorphAnalyzer()
    def pymorphy_lemmas(w):
        return {conv.get(x.normal_form,x.normal_form) for x in morph.parse(w)}
    return pymorphy_lemmas


# comp_df=pd.read_csv("dict_data/lem_df.csv",encoding="utf8",index_col=0,squeeze=True).to_dict()
# stss_df=pd.read_csv("dict_data/tok_df.csv",index_col=0, encoding="utf8",squeeze=True).to_dict()
# # jo_sr=pd.read_csv("dict_data/jo_sr.csv",encoding="utf8",index_col=0,squeeze=True).to_dict()
# bl_dct=pd.read_csv("dict_data/biglit_sr.csv",encoding="utf8",index_col=0,squeeze=True).to_dict()

RUS_VOWELS=u"[`иеаоуяюыёэ]"
RUS_VOWELS_re=re.compile(RUS_VOWELS)
def setup_stress(data_path="./dict_data"):
    comp_df=csv_dct("%s/lem_df.csv" %data_path )
    stss_df=csv_dct("%s/tok_df.csv" %data_path)
    #jo_dct=csv_dct("%s/jo_sr.csv" %data_path)
    bl_dct=csv_dct("%s/biglit_sr.csv" %data_path)
    def set_stress(fn,w):
        w=w.lower()
        vows= RUS_VOWELS_re.findall(w)
        if not vows:
            return {998}
        if u"ё" in vows:
            return {vows.index(u"ё")+1}
        if len(vows)==1:
            return {1}
        try:
            res={int(x) for x in stss_df[w].split("|") if x}
        except KeyError:
            #conv.get account for bug
            lemmas=fn(w)
            res=set()
            for l in lemmas:
                # print w,l
                lres={int(x) for x in comp_df.get(l,bl_dct.get(l,"999")).split("|") if x and x!='None'}
                res=res.union(lres)
        return res
    return set_stress,pm_setup()
