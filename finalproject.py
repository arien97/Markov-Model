#
# finalproject.py - Final Project
#
# Building an initial text model
#

import math

class TextModel:
    """ serves as a blueprint for objects that model a body of text
    """
    
    def __init__(self, model_name):
        """ constructs a new TextModel object by accepting a string
            model_name as a parameter and initializing the name, words
            and word_lengths
        """
        
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.commas = {}
    
    
    def __repr__(self):
        """ returns a string that includes the name of the model as well
            as the sizes of the dictionaries for each feature of text
        """
        s = "text model name: " + self.name + '\n'
        s += "  number of words: " + str(len(self.words)) + '\n'
        s += "  number of word lengths: " + str(len(self.word_lengths)) + '\n'
        s += "  number of stems: " + str(len(self.stems)) + '\n'
        s += "  number of sentence lengths: " + str(len(self.sentence_lengths)) + '\n'
        s += "  number of commas: " + str(len(self.commas)) 
        
        return s
    
    
    def add_string(self, s):
        """ adds a string of text s to the model by augmenting the feature
            dictionaries defined in the constructor
        """
        
        sentence_count = 1
        word_count_comma = 1
        
        for w in s:
            if w == ' ':
                sentence_count += 1
                word_count_comma += 1
            if w in ',':
                if word_count_comma not in self.commas:
                    self.commas[word_count_comma] = 1
                else:
                    self.commas[word_count_comma] += 1
                word_count_comma = 0
            if w in '.?!':
                if sentence_count not in self.sentence_lengths:
                    self.sentence_lengths[sentence_count] = 1
                else:
                    self.sentence_lengths[sentence_count] += 1
                
                sentence_count = 0
                word_count_comma = 0
            
        word_list = clean_text(s)
       

        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
                
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
                
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
                
            
          
            
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the model
        """
        
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        self.add_string(text)
        
        
        
    def save_model(self):
        """ saves the TextModel object self by writing its various feature
            dictionaries to files. One file written for each feature dictionary
        """
        
       
        f = open(self.name + '_' + 'words', 'w') 
        f.write(str(self.words))
        
        f2 = open(self.name + '_' + 'word_lengths', 'w') 
        f2.write(str(self.word_lengths))
        
        f3 = open(self.name + '_' + 'stems', 'w')
        f3.write(str(self.stems))
        
        f4 = open(self.name + '_' + 'sentence_lengths', 'w')
        f4.write(str(self.sentence_lengths))
        
        f5 = open(self.name + '_' + 'words_before_comma', 'w')
        f5.write(str(self.commas))
        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from their
            files and assignes them to the attributes called TextModel
        """
        f = open(self.name + '_' + 'words', 'r')
        d_str = f.read() 
        self.words = dict(eval(d_str)) 
        
        f2 = open(self.name + '_' + 'word_lengths', 'r')
        d_str2 = f2.read()
        self.word_lengths = dict(eval(d_str2))
        
        f3 = open(self.name + '_' + 'stems', 'r')
        d_str3 = f3.read()
        self.stems = dict(eval(d_str3))
        
        f4 = open(self.name + '_' + 'sentence_lengths', 'r')
        d_str4 = f4.read()
        self.sentence_lengths = dict(eval(d_str4))
        
        f5 = open(self.name + '_' + 'words_before_comma', 'r')
        d_str5 = f5.read()
        self.commas = dict(eval(d_str5))
        
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring the similarity
            of self and other - one score for each type of feature
        """
                
        word_score = compare_dictionaries(other.words, self.words)
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sent_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        comma_score = compare_dictionaries(other.commas, self.commas)
        
        sim_scores = [word_score, word_length_score, stem_score, sent_score, comma_score]
        return sim_scores
    
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other "source" TextModel objects 
            (source1 and source2) and determines which of these other TextModels is the more
            likely source of the called TextModel
        """
        
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print("scores for ", source1.name, ": ", scores1)
        print("scores for ", source2.name, ": ", scores2)
        
        weighted_sum1 = 10*scores1[0] + 3*scores1[1] + 5*scores1[2] + 7*scores1[3] + 2*scores1[4]
        weighted_sum2 = 10*scores2[0] + 3*scores2[1] + 5*scores2[2] + 7*scores1[3] + 2*scores1[4]
       
        if weighted_sum1 > weighted_sum2:
            print(self.name, "is more likely to have come from", source1.name)
            
        else:
            print(self.name, "is more likely to have come from", source2.name)
       
def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list
        containing the words in txt after it has been "cleaned"
    """
    
    new_txt = txt
    for symbol in """.,?"'!;:""":
        new_txt = new_txt.replace(symbol, '')
    
    words = new_txt.split()
    
    for i in range(len(words)):
        words[i] = words[i].lower()
    
    return words    
        
      
def stem(s):
    """ accepts a string as a parameter and returns the stem of the string
    """
   
    stem = ''
    if s[-3: ] == 'ier':
        stem = s[ :-2]
    elif s[-4: ] == 'iers':
        stem = s[ :-3]
    elif s[-2: ] == 'er':
        stem = s[ :-2]
    elif s[-3: ] == 'ing':
        if len(s) < 5:
            stem = s
        elif len(s) < 6 and s[ : 2] not in 'aeiou':
            stem = s
        else:
            stem = s[ : -3]
    elif s[-3: ] == 'ies':
        stem = s[ :-2] 
    elif s[-2: ] == 'es':
        stem = s[ :-2]
    elif s[-1: ] == 's' and s != 'was' and s != 'is' and s[-2: ] != "'s":
        stem = s[ :-1]
    elif s[-2: ] == 'ed':
        stem = s[ :-2]
    elif s[-4: ] == 'less':
        stem = s[ :-4]
    elif s[-1] == 'e' and s != 'the' and s != 'are' and s != 'there' and s != 'here' \
        and s != 'we' and s != 'he' and s != 'me' and s != 'she':
        stem = s[ :-1]
    elif s[-1] == 'y' and s != 'they':
        stem = s[ :-1] + 'i'
    else:
        stem = s
        
    return stem
    
        
def compare_dictionaries(d1, d2):
    """ takes two feature dictionaries d1 and d2 as inputs, and it should compute and 
        return their log similarity score
    """
    if d1 == {}:
        return -50
    
    total = 0
    for key in d1:
        total += d1[key]
          
    sim_score = 0
    for key in d2:
        if key in d1:
            sim_score += (d2[key] * math.log((d1[key] / total )))
        else:
            sim_score += (d2[key] * math.log((0.5 / total)))
                      
        
    return sim_score    
        
        
def test():
    """ tests the classify function by comparing two sources """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)        
        
        
        
def run_tests():
    """ your docstring goes here """
    source1 = TextModel('The Incredibles')
    source1.add_file('Incredibles.txt')

    source2 = TextModel('Shrek')
    source2.add_file('Shrek.txt')
    source2.add_file('Shrek2.txt')

    new1 = TextModel('The Bee Movie')
    new1.add_file('BeeMovie.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('Megamind')
    new2.add_file('Megamind.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('Shrek 3')
    new3.add_file('Shrek3.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('The Incredibles 2')
    new4.add_file('Incredibles2.txt')
    new4.classify(source1, source2)
        
        
        
        
        