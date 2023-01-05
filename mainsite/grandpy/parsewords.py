from .stopwords import stop_words_list


class Parse:
    """ This class gives the tools to parse the question """

    def transform_sentence_to_lower_without_apostrophes(self, sentence):
        """ This method transforms a sentence to
        lower and removes d' and l' characters """

        sentence = sentence.lower()
        sentence = sentence.replace("d'", "")
        sentence = sentence.replace("l'", "")
        return sentence

    def remove_special_characters_from_list(self, sentence):
        """ This method removes all special characters from sentence """

        intab = "?,:;._!<>%"
        outtab = "          "
        trantab = str.maketrans(intab, outtab)
        sentence = sentence.translate(trantab)
        return sentence

    def transform_sentence_to_list(self, sentence):
        """ This method puts all words from sentence into a list """

        sentence = sentence.split()
        return sentence

    def create_new_sentence(self, sentence):
        """ This method creates a new sentence after removing useless words """

        stop_word_list = stop_words_list()
        old_sentence = []
        for word in sentence:
            if word not in stop_word_list:
                old_sentence.append(word)
        cleaned_sentence = " ".join(old_sentence)
        return cleaned_sentence
