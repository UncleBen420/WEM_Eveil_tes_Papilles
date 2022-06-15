## Import libs

import json
import os
import time
#import pandas as pd
import numpy as np
import difflib

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from gensim import models, corpora, similarities
from gensim.models import KeyedVectors, Word2Vec, LsiModel, LdaModel, LdaMulticore

import spacy
nlp = spacy.load('fr_core_news_sm')

class EveilleTesPapilles:

    def __init__(self, path, recipeFilesName) -> None:
        self.recipeFiles = recipeFilesName
        self.recipeDta = self.__importFiles(recipeFilesName)
        #self.corpus_lemma = self.__loadJsonData('recipe_data_tokenized.json')
        self.ingredientDictionnary = self.__createIngredientList(self.recipeDta)
        self.ingredientDictionnaryLemma = self.__lemmaIngredientDictionnary()
        self.wv = KeyedVectors.load(path, mmap='r')
        self.stop_words = ['a','se','et',':','de','du','le','la','1','2','3','4','5','les','l\'','me','te','.',',','\'','(',')','6-7','!']

    def info(self):
        print('***************************')
        print('Information about the model')
        print('***************************\n')

        print('There are',len(self.recipeFiles),'recipe files')
        for i, file in enumerate(self.recipeFiles):
            print('There are',len(self.recipeDta[i]),'recipes for',file)

        print('There are',len(self.ingredientDictionnary),'ingredients in the dico')
        print('There are',len(self.ingredientDictionnaryLemma),'ingredients in the lemmatizated dico')


# ***************************************************************************************************
# Model load and train
# ***************************************************************************************************
    def LoadModel(self,path):
        self.wv = KeyedVectors.load(path, mmap='r')

    ## Model Word2Vec creation
    def Train(self, nltk_token):
        model = self.__CreateModel(nltk_token)
        print('The vocabulary has',len(model.wv.key_to_index),'words')
        print('The vector space is',len(model.wv[0]))
        return model

# ***************************************************************************************************
# Data extraction and processing
# ***************************************************************************************************
    ## Function to import the data
    def __loadJsonData(self, path):
        dta=[]
        count=0
        with open(path) as json_data:
            for line in json_data:
                dta.append(json.loads(line))
        return dta

    ## Import data files
    def __importFiles(self, filesPath):
        dta =[]
        for file in filesPath:
            dta.append(self.__loadJsonData(file))
        return dta

    ## French lemmatization
    def lemmatization(self, corpus="",corpus_lemma=""):
        if corpus_lemma=="":
            corpus_lemma = []
            [corpus_lemma.append(nlp(recipe)) for recipe in corpus]
            ##with open('recipe_data_tokenized.json', 'w') as outfile:
            ##    for i in range(len(corpus_lemma)):
            ##        liste = [token.lemma_ for token in corpus_lemma[i]]
            ##        jsonString = json.dumps(liste)
            ##        outfile.write(jsonString)
            ##        outfile.write('\n')
        nltk_token = []
        nltk_token = [[w.lower() for w in t if not w.lower() in self.stop_words] for t in corpus_lemma]
        return nltk_token

    def lemmaList(self,list):
        lemma =  [nlp(word) for word in list]
        nltk_token = []
        nltk_token = [[w.lower() for w in t if not w.lower() in self.stop_words] for t in lemma]

    def __createModel(self, corpus):
        start_time = time.time()
        model = Word2Vec(sentences=corpus, vector_size=100, window=5, min_count=1, workers=4)
        end_time = time.time()
        print('It tooks',end_time-start_time,'s')
        return model

    ## Create a corpus with the new data -> recipe or wine
    def __createCorpus(self, data):
        corpus = []
        for category in data:
            for text in category:
                try:
                    corpus.append(text['steps'])
                except:
                    corpus.append(text['description'])
        return corpus

    ## Create list of all ingredients from the recipe
    #  Be carefull, the list could be different than the embeddings
    def __createIngredientList(self, dataRecipe):
        ingredientsList=[]
        for category in dataRecipe:
            for text in category:
                try:
                    for ingredients in text['ingredients']:
                        ingredientsList.append(ingredients['ingredient'])
                except:
                    pass
        ingredientsLower = [ingredient.lower() for ingredient in ingredientsList]
        return corpora.Dictionary([ingredientsLower])

    def __lemmaIngredientDictionnary(self):
        ingredientsList = [nlp(value) for value in self.ingredientDictionnary.token2id]
        ingredientsList_lemma = [token[0].lemma_ for token in ingredientsList]
        ingredientDico_lemma = corpora.Dictionary([ingredientsList_lemma])
        return ingredientDico_lemma

    def listInIngredientDictionnary(self, list_words):
        new_list=[word for word in list_words if word in self.ingredientDictionnary.token2id]
        return new_list
    
    def listInEmbeddings(self, list_words):
        new_list =[]
        for word in list_words:
            if word in self.wv.index_to_key:
                if not word in self.stop_words:
                    new_list.append(word)
            else:
                wordInEmbeddings = self.similar(word)
                if not self.similar(word) == None: 
                    if not wordInEmbeddings in self.stop_words:
                        new_list.append(wordInEmbeddings)
        return new_list
    
    def similar(self,seq1):
        for word in self.wv.index_to_key:
            if difflib.SequenceMatcher(a=seq1.lower(), b=word.lower()).ratio() > 0.9:
                return word


# ***************************************************************************************************
# Job methods
# ***************************************************************************************************

    ## Display scatterplot of PCA
    def displayScatterplot(self, model, words): # assumes all words are in the vocabulary
        #%matplotlib inline
        word_vectors = [model.wv[word] for word in words]
        print(len(word_vectors[0]))
        twodim = PCA().fit_transform(word_vectors)[:,:2]
        plt.figure(figsize=(6,6))
        plt.scatter(twodim[:,0], twodim[:,1], edgecolors='k', c='r')
        for word, (x,y) in zip(words, twodim):
            plt.text(x + 0.03, y + 0.03, word)
            
    # It allow the user to get a suggestion of ingredient that can replace an ingredient in a recipe      
    # recipeReplacement():
    def predictIngredient(self,recipe,ingredient):
        recipe_lemma = nlp(recipe)
        recipe_word = [word.lemma_ for word in recipe_lemma]
        recipe_token = [w.lower() for w in recipe_word if not w.lower() in self.stop_words]
        tokenInDico = self.listInIngredientDictionnary(recipe_token)
        return self.predictSuggestion(tokenInDico,ingredient)
        #return self.wv.similar_by_vector(ingredient)
        
    # Predict an ingredient based on a list of ingredients with positive and negative similarity
    def predictSuggestion(self,ingredients,less=""):
        ingredientList = self.listInEmbeddings(ingredients)
        print("ingredients for the suggestion : ",ingredientList)
        suggestion = self.wv.most_similar(positive=ingredientList,topn=20)
        sugg = [ingredient[0] for ingredient in suggestion]
        if less == "":
            return self.listInIngredientDictionnary(sugg[:5])
        else:
            replacement =[]
            index = np.argsort(self.wv.distances(less,sugg))
            for i in range(5):
                replacement.append(sugg[index[i]])
            return self.listInIngredientDictionnary(replacement)
            
        

    def predictWinePairingWine(recipe,ingredients):
        pass
    def predictWinePairingRecipe(pairWell):
        pass
