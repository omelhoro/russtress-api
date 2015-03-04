var RUS_VOWELS = /[`иеаоуяюыёэ]/gi;
function setStress(t, insertFn) {
    var split_t = t.split(/([\u2000-\u206F\u2E00-\u2E7F\'!\"#\$%&\(\)\*\+,\-\.\/:;<=>\?@\[\]\^_`\{\|\}~ \n])/g).filter(Boolean);
    var d = {};
    split_t.forEach(function (itm) {
        var vows = itm.match(RUS_VOWELS);
        if (vows !== null && vows.length > 1) {
            d[itm] = "";
        }
    });
    $.getJSON("/stress", d, function (d) {
        function fReplace(nth, i) {
            if (i === void 0) { i = 0; }
            //wrapper for setting the right vowel-number for replacing; JS-replace iterates over findings and calls inner fn
            function f_r(m) {
                i++;
                var res;
                if (i == nth) {
                    res = "'" + m;
                }
                else {
                    res = m;
                }
                return res;
            }
            return f_r;
        }
        function stress(w) {
            var res;
            try {
                var entry = d[w];
                //take the first item of the answer; sometimes there are two or more possibilities
                var nth = entry[0][0];
                var info = entry[0][1];
                var count = entry.length == 1 ? "one" : "more";
                var stressed = w.replace(RUS_VOWELS, fReplace(nth));
                //make Html string with class set to count and info
                var t = "<span class='" + info + " " + count + "'>" + stressed + "</span>";
                res = { stressed: stressed, htmltag: t };
            }
            catch (e) {
                res = { stressed: w, htmltag: w };
            }
            return res;
        }
        var outp = split_t.map(stress);
        insertFn(outp);
    });
}
$("#go_stress").click(function () {
    var t = $("#stress_text").val();
    function append_text(outp) {
        var tokens = outp.map(function (e) { return e.stressed; }).join("");
        var withInfo = outp.map(function (e) { return e.htmltag; }).join("");
        var infoHtml = "<div>" + withInfo + "</div>";
        $('#output_stress').val(tokens);
        $("#stress-info").html(infoHtml);
    }
    setStress(t, append_text);
});
$("#show-more").click(function (evt) {
    $("#more-info").toggle("fast");
});
//# sourceMappingURL=stress.js.map