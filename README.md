Rustress is an app to set stress marks in russian words.

It depends on pymorphy2 since it takes a different approach to the stress-problem:
Some apps use a complete dictionary of word forms to merge them with the occurences in the text.
This leads for the most frequent 20.000 words to 1.7 mio forms.

It can be easier and more effective: If you take some avaible corpus such as www.ruscorpora.ru, you can calculate that about 92% of tokens have the same stress position as their lemma ("normal form"). A big part of the rest 8% one can predict by a list of forms that have different stress than their lemma. Such list has tokens like "хочет,хочешь".

So a given token is first lookep up in the Tokens-Dict, or, if not there, is lemmatized by pymorphy and the lemma is then looked up in List-Dict.

The results are pretty awesome: The evaluation on the 1 mio subset of ruscorpora shows 99% correctness.

###TODO
- implement an statistical tagger as a backup if the token and lemma are not found
- disambiguate between different words ("тень" - "т'ени", "тенуть" - "тен'и")
- port current Python-Dicts and to something more efficient like DAWG (since pymorphy already uses it)
