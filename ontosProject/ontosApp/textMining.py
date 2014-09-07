import nltk
import numpy 

from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.probability import FreqDist

COUNTRIES = ['launiupoko','maui', 'cyprus', 'france', 'cabo', 'turkey', 'morocco', 'america']
SPORTS = ['football', 'baseball', 'soccer', 'tennis', 'rugby', 'basketball', 'cricket', 'swimming']

def top5(myList):
	if (len(myList) > 5):
		return myList[0:5]
	else:
		return myList



def accumTokens(xhtml):
	soup = BeautifulSoup(xhtml)
	raw = soup.get_text()
	tokens = word_tokenize(raw)
	return tokens

def getCountryDist(tokens):
	text = nltk.Text(tokens)
	countries = [w for w in text if (w.lower() in COUNTRIES)]
	fDist = FreqDist(countries)
	dictionary = fDist.items()
	return top5(dictionary)

def getSportsDist(tokens):
	text = nltk.Text(tokens)
	sports = [w for w in text if (w.lower() in SPORTS)]
	fDist = FreqDist(sports)
	dictionary = fDist.items()
	return top5(dictionary)


if __name__ == "__main__":
	enml = "<div>Hickory, football, swimming, dock</div>  <div>The soccer soccer tennis soccer clock.</div>  <div>The cricket struck one,</div>  <div>The rugby rugby down,</div>  <div>Hickory, dickory, dock.</div>  <div><br /></div>  <div>-- Author unknown</div>"
	tokens = accumTokens(enml)
	a = getSportsDist(tokens)
	print(a)


