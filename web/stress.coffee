$=jQuery

set_stress =  (t,cl) ->
    split_t=(w for w in t.split(/([\u2000-\u206F\u2E00-\u2E7F\'!\"#\$%&\(\)\*\+,\-\.\/:;<=>\?@\[\]\^_`\{\|\}~ \n])/g) when w)
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
        # console.log d
        stress= (w) ->
            try
                entry=d[w]
                nth=entry[0][0]
                info=entry[0][1]
                count=if entry.length==1  then "one" else "more"
                stressed= w.replace(RUS_VOWELS,f_replace(nth))
                t="<span class='#{info} #{count}'>#{stressed}</span>"
                r=[stressed,t]
            catch e
                r= [w,w]
            # console.log r
            return r
        outp=(stress(w) for w in split_t)
        cl(outp))

($ '#go_stress').click( (e) ->
    t=($ '#stress_text').val()
    append_text = (outp) ->
        concat=(w[0] for w in outp).join("")
        with_info=$("<div>"+(w[1] for w in outp).join("")+"</div>")
        ($ '#output_stress').val(concat)
        ($ "#stress-info").html(with_info)
    set_stress(t,append_text)
)
