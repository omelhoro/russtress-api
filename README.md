Rustress is an app to set stress marks in russian words.

It depends on pymorphy2 since it takes a different approach to the stress-problem:
Some apps use a complete dictionary of word forms to merge them with the occurences in the text.
This leads for the most frequent 20.000 words to 1.7 mio forms.

It can be easier and more effective: If you take some avaible corpus such as www.ruscorpora.ru, you can calculate that about 92% of tokens have the same stress position as their lemma ("normal form"). A big part of the rest 8% one can predict by a list of forms that have different stress than their lemma. Such list has tokens like "хочет,хочешь".

So a given token is first lookep up in the Tokens-Dict, or, if not there, is lemmatized by pymorphy and the lemma is then looked up in List-Dict.

The results are pretty awesome: The evaluation on a free avaible subset of ruscorpora shows 96% correctness.
In the following table you can see the strenghts and weaknesses of this approach:
If you exclude easy tasks as Jo-words, tokens with no vowels (numerals) and tokens with only one vowel, you can see
that the correctness for words with only one possible lemma-stress is nice, such as for the one possible tokens-stress.
The weaknesses are visible when there are two possibilities of setting the stress - here for the results, the first possibility was taken.This succeeds for lemmas with 72% correctness, for tokens it's only 50%.

<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th>iseq</th>\n      <th>False</th>\n      <th>True</th>\n    </tr>\n    <tr>\n      <th>type_guess</th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>(jo-stress,)</th>\n      <td> NaN</td>\n      <td>   443</td>\n    </tr>\n    <tr>\n      <th>(lem-stress,)</th>\n      <td>  77</td>\n      <td> 10112</td>\n    </tr>\n    <tr>\n      <th>(lem-stress, lem-stress)</th>\n      <td> 174</td>\n      <td>   454</td>\n    </tr>\n    <tr>\n      <th>(lem-stress, lem-stress, lem-stress)</th>\n      <td> NaN</td>\n      <td>     4</td>\n    </tr>\n    <tr>\n      <th>(no-vows,)</th>\n      <td> NaN</td>\n      <td>  1934</td>\n    </tr>\n    <tr>\n      <th>(not-found,)</th>\n      <td> 228</td>\n      <td>   379</td>\n    </tr>\n    <tr>\n      <th>(one-vow,)</th>\n      <td> NaN</td>\n      <td>  5453</td>\n    </tr>\n    <tr>\n      <th>(tok-stress,)</th>\n      <td>  43</td>\n      <td>  2613</td>\n    </tr>\n    <tr>\n      <th>(tok-stress, tok-stress)</th>\n      <td> 269</td>\n      <td>   269</td>\n    </tr>\n  </tbody>\n</table>

###TODO
- implement an statistical tagger as a backup if the token and lemma are not found
- disambiguate between different words ("тень" - "т'ени", "тенуть" - "тен'и")
- gr.div(gr.sum(axis=1),axis=0) port current Python-Dicts and to something more efficient like DAWG (since pymorphy already uses it)
