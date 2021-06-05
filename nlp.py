import random
import spacy
import en_core_web_sm
import numpy as np

random_seed = 1234
random.seed(random_seed)
np.random.seed(random_seed)
nlp = en_core_web_sm.load()


def nlp_model(user_input):
    doc = nlp(user_input)

    token_list = []
    lemma_list = []
    pos_list = []
    tag_list = []
    stopword_list = []
    entity_list = []

    for token in doc:
        token_list.append(token.text)
        lemma_list.append(token.lemma_)
        pos_list.append(token.pos_)
        tag_list.append(token.tag_)
        stopword_list.append(token.is_stop)
        entity_list.append(token.ent_type_)
    token_arr = np.array(token_list)
    entity_arr = np.array(entity_list)
    tag_arr = np.array(tag_list)

    # mask for excluding stopword
    non_stop_mask = ~np.array(stopword_list)

    # authors' names without stopword
    person_mask = entity_arr == 'PERSON'
    date_mask = entity_arr == 'DATE'
    person_stop_mask = np.logical_and(non_stop_mask, person_mask)

    # title_mask
    title_mask1 = entity_arr == 'PRODUCT'
    title_mask2 = entity_arr == 'FAC'
    # title_mask3 = entity_arr = 'TITLE' (아직 구현 안됨)
    title_mask = np.logical_or(title_mask1, title_mask2)

    # genre_mask
    genre_mask1 = entity_arr == 'GPE'
    genre_mask2 = entity_arr == 'LOC'
    genre_mask3 = entity_arr == 'GEO'
    genre_mask4 = entity_arr == 'NORP'
    genre_mask5 = entity_arr == 'ORG'
    genre_mask6 = entity_arr == 'EVENT'
    genre_mask7 = entity_arr == 'WORK_OF_ART'
    # genre_mask8 = entity_arr = 'GENRE' (아직 구현 안됨)
    genre_mask = np.logical_or.reduce(
        (genre_mask1, genre_mask2, genre_mask3, genre_mask4, genre_mask5, genre_mask6, genre_mask7))

    # save personal name as str
    person_arr = token_arr[person_stop_mask]
    person_list = person_arr.tolist()
    person_str = ' '.join(person_list)

    # save date as str
    date_arr = token_arr[date_mask]
    date_list = date_arr.tolist()
    date_str = ' '.join(date_list)

    # save title as str
    title_arr = token_arr[title_mask]
    title_list = title_arr.tolist()
    title_str = ' '.join(title_list)

    # save genre as str
    genre_arr = token_arr[genre_mask]
    genre_list = genre_arr.tolist()
    genre_str = ' '.join(genre_list)

    # deprecate verb
    weight_arr = np.where((tag_arr != 'VBD') & (tag_arr != 'VBP'), '', '^0.5')
    weight_token_arr = np.core.defchararray.add(token_arr, weight_arr)

    no_stopword_arr = weight_token_arr[non_stop_mask]
    no_stopword_list = no_stopword_arr.tolist()
    no_stopword_str = ' '.join(no_stopword_list)

    processed_input_list = [no_stopword_str, person_str, date_str, title_str, genre_str]
    return processed_input_list
