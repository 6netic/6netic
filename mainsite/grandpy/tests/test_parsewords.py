from grandpy import parsewords


def test_if_sentence_to_lower():
	""" this function tests if a sentence can be converted to lower case """
	parse = parsewords.Parse()
	result = parse.transform_sentence_to_lower_without_apostrophes("Adresse Du Thyrse")
	assert result == "adresse du thyrse"


def test_if_sentence_without_d():
	""" This function tests if we can remove d' in a sentence """
	parse = parsewords.Parse()
	result = parse.transform_sentence_to_lower_without_apostrophes("feux d'artifice")
	assert result == "feux artifice"


def test_if_sentence_without_l():
	""" This function tests if we can remove l' in a sentence """
	parse = parsewords.Parse()
	result = parse.transform_sentence_to_lower_without_apostrophes("l'élevage de l'éléphant")
	assert result == "élevage de éléphant"


def test_if_sentence_without_special_characters():
	""" This function tests if we can remove special characters """
	parse = parsewords.Parse()
	result = parse.remove_special_characters_from_list("tout est prêt!: boisson, nourriture, etc... _ok pour vous?")
	assert result == "tout est prêt   boisson  nourriture  etc     ok pour vous "


def test_if_sentence_is_split():
	""" This function tests if sentence can be split """
	parse = parsewords.Parse()
	result = parse.transform_sentence_to_list("tout est prêt   boisson  nourriture  etc     ok pour vous ")
	assert result == ["tout", "est", "prêt", "boisson", "nourriture", "etc", "ok", "pour", "vous"]


def test_if_sentence_in_cleaned_list():
	""" This function tests if sentence can be cleaned up """
	parse = parsewords.Parse()
	result = parse.create_new_sentence(["salut", "grandpy", "est-ce", "que", "tu", "connais", "adresse", "openclassrooms"])
	assert result == "openclassrooms"

