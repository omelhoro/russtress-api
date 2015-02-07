declare var $;
var RUS_VOWELS:RegExp = /[`иеаоуяюыёэ]/gi;

interface WordItem {
    stressed:string;
    htmltag:string;
}

function setStress(t:string, insertFn):void {
    var split_t:string[] = t.split(/([\u2000-\u206F\u2E00-\u2E7F\'!\"#\$%&\(\)\*\+,\-\.\/:;<=>\?@\[\]\^_`\{\|\}~ \n])/g)
        .filter(Boolean);
    var d = {};
    split_t.forEach((itm)=> {
        var vows = itm.match(RUS_VOWELS);
        if (vows !== null && vows.length > 1) {
            d[itm] = ""
        }
    });
    $.getJSON("/stress", d, (d)=> {
            function fReplace(nth:number, i = 0) {
                //wrapper for setting the right vowel-number for replacing; JS-replace iterates over findings and calls inner fn
                function f_r(m) {
                    i++;
                    var res;

                    if (i == nth) {
                        res = "'" + m;
                    }
                    else {
                        res = m
                    }
                    return res
                }

                return f_r
            }

            function stress(w:string):WordItem {
                var res:WordItem;
                try {
                    var entry = d[w];
                    //take the first item of the answer; sometimes there are two or more possibilities
                    var nth:number = entry[0][0];
                    var info:string = entry[0][1];
                    var count = entry.length == 1 ? "one" : "more";
                    var stressed:string = w.replace(RUS_VOWELS, fReplace(nth));
                    //make Html string with class set to count and info
                    var t:string = "<span class='" + info + " " + count + "'>" + stressed + "</span>";
                    res = {stressed: stressed, htmltag: t}
                }
                catch (e) {
                    res = {stressed: w, htmltag: w}
                }
                return res

            }

            var outp:WordItem[] = split_t.map(stress);
            insertFn(outp)
        }
    )
}


$("#go_stress").click(()=> {
    var t:string = $("#stress_text").val();

    function append_text(outp:WordItem[]):void {
        var tokens:string = outp.map((e)=>e.stressed).join("");
        var withInfo:string = outp.map((e)=>e.htmltag).join("");
        var infoHtml = "<div>" + withInfo + "</div>";
        $('#output_stress').val(tokens);
        $("#stress-info").html(infoHtml)
    }

    setStress(t, append_text)
});