import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    X_lens = test_set.get_all_Xlengths()
    # TODO implement the recognizer
    for X, lens in X_lens.values():
        # Save best result when recognizer during the iteration
        best_res = None
        # Save the maximum score after comparisons
        max_word_score = float("-inf")
        # Save likelihood of a word
        log_l = {}
        for word, model in models.items():
            try:
                # Score word using model
                word_score = model.score(X, lens)
                log_l[word] = word_score
                if word_score > max_word_score:
                    max_word_score = word_score
                    best_res = word
            except:
                log_l[word] = float("-inf")

        guesses.append(best_res)
        probabilities.append(log_l)

    return probabilities, guesses
