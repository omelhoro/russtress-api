$=jQuery
($ '#go_stress').click( (e) ->
    t=($ '#stress_text').val()
    toks=(w.trim() for w in t.split(" ") when w)
    RUS_VOWELS=/[`иеаоуяюыёэ]/gi
    ress= ([s,s.match(RUS_VOWELS)] for s in toks when s)
    d={}
    for itm in ress
        if itm[1]==null or itm[1].length>1
            d[itm[0]]=""
    tok_set= (k  for k,_ of d)
    console.log(tok_set)
    $.getJSON("/stress",d,(d) ->
        f_replace= (nth) ->
            i=0
            f_r = (m,j,string) ->
                i++
                if i==nth
                    "'"+m
                else
                    m
            return f_r

        stress= (w) ->
            try
                nth=d[w][0]
                return w.replace(RUS_VOWELS,f_replace(nth))
            catch e
                return w
        outp=(stress(w) for w in toks)
        ($ '#output_stress').val(outp.join(" "))))
