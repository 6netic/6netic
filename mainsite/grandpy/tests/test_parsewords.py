from django.test import TestCase
from .. import parsewords


class ParsewordsTests(TestCase):

	def test_sentence_to_lower(self):
		""" 1- This function tests if a sentence can be converted to lower case """

		parse = parsewords.Parse()
		result = parse.transform_sentence_to_lower_without_apostrophes("Adresse Du Thyrse")
		self.assertEqual(result, "adresse du thyrse")


	def test_sentence_without_d(self):
		""" 2- This function tests if we can remove d' in a sentence """

		parse = parsewords.Parse()
		result = parse.transform_sentence_to_lower_without_apostrophes("feux d'artifice")
		self.assertEqual(result, "feux artifice")


	def test_sentence_without_l(self):
		""" 3- This function tests if we can remove l' in a sentence """

		parse = parsewords.Parse()
		result = parse.transform_sentence_to_lower_without_apostrophes("l'élevage de l'éléphant")
		self.assertEqual(result, "élevage de éléphant")


	def test_sentence_without_special_characters(self):
		""" 4- This function tests if we can remove special characters """

		parse = parsewords.Parse()
		result = parse.remove_special_characters_from_list("tout est prêt!: boisson, nourriture, etc... _ok pour vous?")
		self.assertEqual(result, "tout est prêt   boisson  nourriture  etc     ok pour vous ")


	def test_split_sentence(self):
		""" 5- This function tests if splitting sentence is done correctly """

		parse = parsewords.Parse()
		result = parse.transform_sentence_to_list("tout est prêt   boisson  nourriture  etc     ok pour vous ")
		self.assertEqual(result, ["tout", "est", "prêt", "boisson", "nourriture", "etc", "ok", "pour", "vous"])


	def test_clean_sentence(self):
		""" 6- This function tests if sentence can be cleaned up """

		parse = parsewords.Parse()
		result = parse.create_new_sentence(
			["salut", "grandpy", "est-ce", "que", "tu", "connais", "adresse", "tour eiffel"])
		self.assertEqual(result, "tour eiffel")
