#!/usr/bin/env python
# coding=utf-8
"""
Language detection module
"""
from __future__ import unicode_literals
from __future__ import absolute_import

__author__ = "Manuel Ebert"
__copyright__ = "Copyright 2015, summer.ai"
__date__ = "2015-12-01"
__email__ = "manuel@summer.ai"

from nltk.tokenize import word_tokenize

# You can easily generate this stop word list with NLTK:
# stopwords = {lang: frozenset(stopwords.words(lang)) for lang in ("english", 'german', 'italian', 'french', 'spanish')}
STOPWORDS = {'german': frozenset([u'andere', u'anderm', u'andern', u'das', u'w\xfcrde', u'w\xe4hrend', u'sollte', u'selbst', u'anderr', u'anders', u'einer', u'wollte', u'als', u'alle', u'dessen', u'dazu', u'auf', u'dich', u'hab', u'sondern', u'demselben', u'aus', u'einige', u'derselbe', u'sonst', u'hatte', u'hat', u'bin', u'musste', u'waren', u'mein', u'deine', u'ihnen', u'deinem', u'deinen', u'deines', u'deiner', u'einmal', u'ich', u'dasselbe', u'du', u'bis', u'hin', u'wenn', u'viel', u'war', u'keiner', u'keines', u'die', u'warst', u'wird', u'w\xfcrden', u'haben', u'weil', u'nichts', u'ihn', u'keinen', u'dir', u'wir', u'kann', u'solcher', u'unse', u'nur', u'hinter', u'manche', u'solchen', u'es', u'er', u'will', u'ohne', u'f\xfcr', u'und', u'meinen', u'diesem', u'diesen', u'meinem', u'meiner', u'meines', u'dieser', u'dieses', u'indem', u'werde', u'dein', u'jede', u'denselben', u'wollen', u'dort', u'soll', u'jeden', u'jedem', u'diese', u'wo', u'seine', u'wirst', u'auch', u'jenen', u'keinem', u'jedes', u'jeder', u'habe', u'weiter', u'zur', u'uns', u'hatten', u'welcher', u'bist', u'werden', u'ob', u'ist', u'k\xf6nnte', u'ander', u'hier', u'einig', u'da\xdf', u'zum', u'solches', u'wie', u'aber', u'eines', u'ihr', u'nach', u'gewesen', u'desselben', u'damit', u'eine', u'ihm', u'einen', u'wieder', u'einem', u'jene', u'sind', u'jenem', u'welches', u'eurem', u'einiger', u'einiges', u'oder', u'weg', u'einigem', u'einigen', u'euer', u'dieselbe', u'was', u'von', u'jenes', u'jener', u'durch', u'mich', u'muss', u'unsen', u'ins', u'solchem', u'unsem', u'nun', u'bei', u'welchem', u'der', u'des', u'nicht', u'um', u'dann', u'dem', u'den', u'welchen', u'sein', u'ein', u'ihre', u'seinem', u'seinen', u'keine', u'alles', u'aller', u'noch', u'vom', u'unter', u'gegen', u'am', u'an', u'\xfcber', u'im', u'zwischen', u'vor', u'in', u'allen', u'allem', u'welche', u'seiner', u'seines', u'anderer', u'anderes', u'euch', u'manchem', u'derer', u'manchen', u'k\xf6nnen', u'also', u'manches', u'mancher', u'dieselben', u'sich', u'sie', u'zu', u'so', u'mir', u'anderen', u'mit', u'anderem', u'eurer', u'eures', u'zwar', u'dies', u'sehr', u'jetzt', u'etwas', u'derselben', u'eure', u'euren', u'da', u'solche', u'man', u'ihrem', u'kein', u'ihren', u'meine', u'doch', u'machen', u'denn', u'unser', u'unses', u'ihres', u'ihrer']), 'italian': frozenset([u'all', u'fanno', u'ebbi', u'stettero', u'stessi', u'sarei', u'faccia', u'nostra', u'facesse', u'avr\xe0', u'nostre', u'negl', u'farai', u'nostri', u'nostro', u'farei', u'hai', u'alle', u'le', u'alla', u'la', u'allo', u'lo', u'quelli', u'tu', u'quello', u'sia', u'li', u'starebbe', u'loro', u'faresti', u'ti', u'fareste', u'fossimo', u'stiate', u'cui', u'non', u'avesti', u'noi', u'di', u'dal', u'avr\xf2', u'nell', u'dell', u'avete', u'da', u'starai', u'fai', u'stando', u'facevo', u'stette', u'aveste', u'steste', u'avendo', u'pi\xf9', u'tra', u'sarete', u'l', u'ero', u'avremo', u'quella', u'facendo', u'stava', u'avrai', u'fece', u'starebbero', u'facessi', u'ed', u'feci', u'stemmo', u'stiamo', u'sarebbe', u'stesse', u'facevamo', u'facessimo', u'siano', u'sei', u'avrebbero', u'miei', u'nel', u'stiano', u'sua', u'dei', u'dagl', u'facciano', u'sul', u'suoi', u'per', u'stessero', u'avrete', u'lei', u'lui', u'facevi', u'starei', u'sugl', u'faceva', u'dalla', u'sareste', u'eravamo', u'nello', u'saresti', u'nella', u'faremo', u'eravate', u'anche', u'nelle', u'agli', u'avuti', u'foste', u'avuto', u'tuo', u'tua', u'negli', u'come', u'tue', u'avute', u'fummo', u'gli', u'c', u'avreste', u'quelle', u'stavate', u'\xe8', u'stavano', u'questo', u'questi', u'o', u'avresti', u'una', u'chi', u'coi', u'fui', u'staranno', u'col', u'dalle', u'con', u'star\xe0', u'ci', u'questa', u'stanno', u'avrebbe', u'furono', u'avevamo', u'perch\xe9', u'tuoi', u'stavamo', u'degl', u'avuta', u'staremo', u'tutto', u'degli', u'che', u'fossero', u'tutti', u'dove', u'sarai', u'avremmo', u'facciate', u'quante', u'facesti', u'starete', u'quanta', u'abbiate', u'quanto', u'quanti', u'contro', u'avessi', u'faranno', u'far\xe0', u'queste', u'ebbero', u'voi', u'siamo', u'agl', u'ho', u'farete', u'far\xf2', u'abbiamo', u'farebbe', u'ha', u'sarebbero', u'abbia', u'quale', u'avessimo', u'facessero', u'saranno', u'ma', u'sta', u'abbiano', u'dagli', u'avrei', u'sto', u'mi', u'ebbe', u'dello', u'facevate', u'un', u'del', u'era', u'avevano', u'stareste', u'delle', u'eri', u'della', u'facevano', u'faremmo', u'faceste', u'ad', u'stavi', u'ai', u'vi', u'stetti', u'in', u'al', u'avesse', u'sull', u'vostri', u'saremmo', u'il', u'io', u'vostro', u'vostra', u'avevate', u'vostre', u'staremmo', u'faccio', u'fosti', u'avemmo', u'mio', u'fossi', u'mia', u'sar\xe0', u'mie', u'ne', u'stia', u'dallo', u'star\xf2', u'sar\xf2', u'siete', u'avessero', u'staresti', u'avevo', u'avevi', u'fu', u'facciamo', u'dall', u'aveva', u'sue', u'erano', u'dai', u'essendo', u'stesti', u'sullo', u'sulla', u'sono', u'sulle', u'stai', u'a', u'sugli', u'e', u'avranno', u'i', u'hanno', u'farebbero', u'nei', u'saremo', u'su', u'sui', u'suo', u'si', u'facemmo', u'fecero', u'stavo', u'stessimo', u'uno', u'dov', u'fosse', u'se', u'siate']), 'spanish': frozenset([u'son', u'estar\xe1', u'estadas', u'tengamos', u'hubieras', u'sentidos', u'nuestra', u'teng\xe1is', u'\xe9l', u'tuvi\xe9semos', u'estos', u'tuvimos', u'tuviste', u'nuestro', u'otro', u'tuvieron', u'antes', u'le', u'han', u'la', u'estar\xedamos', u'lo', u'estar\xedas', u'tu', u'ten\xedamos', u'quienes', u'otra', u'hubi\xe9semos', u'hay', u'suyas', u'tendr\xe9', u'ti', u'estar', u'te', u'ten\xe9is', u'habr\xedas', u'tendr\xe1', u'porque', u'estuvimos', u'ser\xedais', u'estaba', u'esa', u'yo', u'\xe9ramos', u'ya', u'cuando', u'nada', u'de', u'est\xe1is', u'tuyos', u'hayan', u'tendr\xe9is', u'estuve', u'algunos', u'hayas', u'tanto', u'qu\xe9', u'seas', u'vosostros', u'm\xeda', u'tuvieras', u'nos', u'hubimos', u'est\xe9is', u'estoy', u'estaremos', u'hubieran', u'una', u'tuvieran', u'estar\xe9is', u'somos', u'fu\xe9semos', u'desde', u'sentida', u'habr\xe9', u'nosotras', u'estados', u'sentido', u'habr\xe1', u'el', u'fuera', u'en', u'habr\xeda', u'esos', u'tendr\xe1n', u'otras', u'habr\xe9is', u'ten\xedas', u'fuesen', u'fue', u'hubieseis', u'tenida', u'soy', u'fueseis', u'seamos', u'hube', u'sea', u'tendr\xedamos', u'estamos', u'todo', u'es', u'eres', u'estad', u'tuya', u't\xfa', u'tuvieseis', u'fueses', u'hab\xedas', u'm\xedas', u'tenido', u'muy', u'tuyo', u'algunas', u'poco', u'ese', u'haya', u'sus', u'estas', u'sobre', u'ser\xedamos', u'eso', u'hab\xedais', u'tened', u'estar\xe9', u'era', u'fuerais', u'habr\xedan', u'estuvieran', u'tienen', u'fuiste', u'tuvo', u'tus', u'fu\xe9ramos', u'estar\xedais', u'les', u'que', u'como', u'estuvieras', u'habido', u'tengan', u'tendr\xe1s', u'tenidas', u'ser\xedas', u'estar\xe1s', u'estuvierais', u'ten\xeda', u'hab\xeda', u'estuvo', u'eras', u'estuviera', u'estuvisteis', u'tuvierais', u'o', u'ser\xe1s', u'est\xe1bamos', u'tambi\xe9n', u'ser\xe1n', u'nosotros', u'algo', u'quien', u'fui', u'os', u'ser\xe9is', u'uno', u'hab\xedan', u'hubiera', u'habiendo', u'est\xe1', u'teniendo', u'fuisteis', u'por', u'est\xe9', u'durante', u'mucho', u'suya', u'donde', u'estuvieron', u'tendremos', u'erais', u'ante', u'tuvisteis', u'otros', u'estaban', u'suyo', u'tienes', u'fueron', u'tenemos', u'tuvieses', u'contra', u'esas', u'estado', u'pero', u'est\xe9s', u'estemos', u'est\xe9n', u'los', u'estabas', u'nuestros', u'se\xe1is', u'est\xe1s', u'ellos', u'tuvi\xe9ramos', u'estar\xe1n', u'fueran', u'suyos', u'habidos', u'hubiese', u'tendr\xedais', u'm\xe1s', u'vuestros', u'm\xedos', u'estabais', u'para', u'fuese', u'fuimos', u'estar\xedan', u'tendr\xedas', u'fueras', u'estuvieseis', u'tendr\xedan', u'vuestro', u'vuestra', u'ha', u'ten\xedais', u'he', u'me', u'has', u'hubo', u'seremos', u'hab\xe9is', u'hubi\xe9ramos', u'mi', u'tengo', u'est\xe1n', u'ten\xedan', u'sintiendo', u'un', u'del', u'hemos', u's\xed', u'tuviera', u'tengas', u'sean', u'habr\xedais', u'este', u'unos', u'esta', u'habr\xe1n', u'estando', u'eran', u'esto', u'al', u'hayamos', u'hab\xedamos', u'estuviese', u'hay\xe1is', u'hubieses', u'sois', u'tenidos', u'tuviese', u'habr\xe1s', u'tenga', u'ni', u'tuviesen', u'no', u'estuvieses', u'ellas', u'sentidas', u'tiene', u'habr\xedamos', u'estuviesen', u'cual', u'nuestras', u'mis', u'sin', u'todos', u'vosostras', u'hubisteis', u'tuyas', u'habremos', u'tuve', u'hubiste', u'ella', u'sentid', u'hubierais', u'hubieron', u'estada', u'siente', u'ser\xeda', u'estar\xeda', u'las', u'a', u'vuestras', u'estuvi\xe9ramos', u'e', u'entre', u'habida', u'm\xed', u'ser\xedan', u'muchos', u'm\xedo', u'su', u'hasta', u'estuvi\xe9semos', u'hubiesen', u'ser\xe1', u'y', u'habidas', u'tendr\xeda', u'con', u'estuviste', u'se', u'ser\xe9']), 'french': frozenset([u'e\xfbtes', u'\xeates', u'aient', u'auraient', u'aurions', u'auras', u'serait', u'le', u'serais', u'mais', u'la', u'eue', u'tu', u'ayante', u'eux', u'aux', u'te', u'eus', u'ta', u'aurais', u'aviez', u'de', u'ayantes', u'f\xfbtes', u'moi', u'sont', u'mon', u'ayant', u'serez', u'du', u'nos', u'aurez', u'eussiez', u'qu', u'd', u'furent', u'f\xfbt', u'\xe9t\xe9e', u'soient', u'leur', u't', u'\xe9t\xe9s', u'seriez', u'en', u'ses', u'avons', u'l', u'eu', u'et', u'sommes', u'tes', u'aurait', u'es', u'est', u'eurent', u'serions', u'sur', u'lui', u'soyons', u'ayants', u'\xe9tais', u'soyez', u'que', u'mes', u'qui', u'je', u'm\xeame', u'\xe0', u'c', u'ayons', u's', u'e\xfbmes', u'une', u'ou', u'\xe9tait', u'\xe9t\xe9', u'\xe9tants', u'\xe9t\xe9es', u'ce', u'son', u'auriez', u'des', u'\xe9tante', u'ont', u'avez', u'f\xfbmes', u'avait', u'avec', u'fussions', u'seraient', u'suis', u'eussions', u'toi', u'ton', u'eues', u'vous', u'aies', u'on', u'auront', u'aurons', u'avions', u'eut', u'me', u'fut', u'ma', u'fus', u'fussent', u'ait', u'j', u'dans', u'pour', u'n', u'seras', u'un', u'serai', u'sera', u'aie', u'ayez', u'avaient', u'aurai', u'votre', u'\xe9tiez', u'ai', u'eusse', u'\xe9taient', u'eussent', u'eusses', u'\xe9tantes', u'soit', u'as', u'au', u'il', u'sois', u'vos', u'\xe9tions', u'par', u'pas', u'fusses', u'fussiez', u'ne', u'\xe9tant', u'seront', u'serons', u'aura', u'avais', u'e\xfbt', u'notre', u'elle', u'nous', u'fusse', u'm', u'y', u'ces', u'sa', u'se']), 'english': frozenset([u'all', u'just', u'being', u'over', u'both', u'through', u'yourselves', u'its', u'before', u'herself', u'had', u'should', u'to', u'only', u'under', u'ours', u'has', u'do', u'them', u'his', u'very', u'they', u'not', u'during', u'now', u'him', u'nor', u'did', u'this', u'she', u'each', u'further', u'where', u'few', u'because', u'doing', u'some', u'are', u'our', u'ourselves', u'out', u'what', u'for', u'while', u'does', u'above', u'between', u't', u'be', u'we', u'who', u'were', u'here', u'hers', u'by', u'on', u'about', u'of', u'against', u's', u'or', u'own', u'into', u'yourself', u'down', u'your', u'from', u'her', u'their', u'there', u'been', u'whom', u'too', u'themselves', u'was', u'until', u'more', u'himself', u'that', u'but', u'don', u'with', u'than', u'those', u'he', u'me', u'myself', u'these', u'up', u'will', u'below', u'can', u'theirs', u'my', u'and', u'then', u'is', u'am', u'it', u'an', u'as', u'itself', u'at', u'have', u'in', u'any', u'if', u'again', u'no', u'when', u'same', u'how', u'other', u'which', u'you', u'after', u'most', u'such', u'why', u'a', u'off', u'i', u'yours', u'so', u'the', u'having', u'once'])}


def detect_language(sentence):
    """Detects the language of a sentence, out of English, German, Italian, French, and Spanish.
    Uses stop word frequency: intersects the tokens of a sentence with a list of stop-words for
    each language and picks the language with the highest intersection.
    Returns a string identifying the language."""
    tokens = [t.lower() for t in word_tokenize(sentence)]
    guesses = []
    for lang in STOPWORDS:
        guesses.append((float(sum(w in STOPWORDS[lang] for w in tokens)) / len(tokens), lang))
    return max(guesses)[1]


def is_english(sentence):
    """Determines whether a sentence is English.
    Will return True if at least 10% of the words are English stop words.
    This method is a lot faster than detect_language since we only have to run this
    procedure for one language."""
    tokens = [t.lower() for t in word_tokenize(sentence)]
    return float(sum(w in STOPWORDS['english'] for w in tokens)) / len(tokens) >= 0.1