from natasha import (
    Segmenter,
    MorphVocab,
    PER,
    NamesExtractor,
    NewsNERTagger,
    NewsEmbedding,
    Doc
)
def get_fio(text):
    emb = NewsEmbedding()
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    ner_tagger = NewsNERTagger(emb)
    names_extractor = NamesExtractor(morph_vocab)
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)
    for span in doc.spans:
        span.normalize(morph_vocab)
    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)
    if doc.spans:
        return {doc.spans[0].normal.title(): {k: v.title() for k, v in doc.spans[0].fact.as_dict.items()}}
    return None

def a(text):
    emb = NewsEmbedding()
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    ner_tagger = NewsNERTagger(emb)
    names_extractor = NamesExtractor(morph_vocab) # текст добавляем сюда

    doc = Doc(text)

    doc.segment(segmenter)

    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)

    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)

    return {_.normal.title(): _.fact.as_dict for _ in doc.spans if _.fact}
b = a('КАТЕГОРИЯ: Споры, связанные с и имущественными правами Иски о взыскании сумм по договору займа, кредитному договоруИСТЕЦ(ЗАЯВИТЕЛЬ): Черванев ДМитрий СергеевичОТВЕТЧИК: Суворова Ольга Анатольевна')

print(b[list(b.keys())[0]])