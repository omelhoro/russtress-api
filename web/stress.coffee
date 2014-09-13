$=jQuery

set_stress =  (t,cl) ->
    split_t=t.split(/([,.;!?() ])/g)
    RUS_VOWELS=/[`иеаоуяюыёэ]/gi
    d={}
    for itm in split_t
        vows=itm.match(RUS_VOWELS)
        if vows!=null and vows.length>1
            d[itm]=""
    $.getJSON("/stress",d,(d) ->
        f_replace= (nth,i=0) ->
            #i=0
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
        outp=(stress(w) for w in split_t)
        cl(outp))

($ '#go_stress').click( (e) ->
    t=($ '#stress_text').val()
    append_text = (outp) ->
        ($ '#output_stress').val(outp.join(""))
    set_stress(t,append_text)
)
