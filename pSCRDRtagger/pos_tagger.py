# -*- coding: utf-8 -*-

import os
import sys
os.chdir("/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/")
sys.setrecursionlimit(100000)
sys.path.append(os.path.abspath(""))
os.chdir("/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/pSCRDRtagger")

from multiprocessing import Pool
from InitialTagger.InitialTagger import initializeCorpus, initializeSentence
from SCRDRlearner.Object import FWObject
from SCRDRlearner.SCRDRTree import SCRDRTree
from SCRDRlearner.SCRDRTreeLearner import SCRDRTreeLearner
from Utility.Config import NUMBER_OF_PROCESSES, THRESHOLD
from Utility.Utils import getWordTag, getRawText, readDictionary
from Utility.LexiconCreator import createLexicon



class RDRPOSTagger(SCRDRTree):
    def __init__(self):
        self.root = None

    def tagRawSentence(self, DICT, rawLine):
        line = initializeSentence(DICT, rawLine)
        sen = []
        wordTags = line.split()
        for i in range(len(wordTags)):
            fwObject = FWObject.getFWObject(wordTags, i)
            word, tag = getWordTag(wordTags[i])
            node = self.findFiredNode(fwObject)
            if node.depth > 0:
                sen.append(word + "/" + node.conclusion)
            else:
                sen.append(word + "/" + tag)
        return " ".join(sen)

def pos_tag(raw_text):
    modelPath = "../data/vn/data_train/train_3.txt.RDR"
    lexiconPath = "../data/vn/data_train/train_3.txt.DICT"

    # Initialize the POS tagger and load the model and dictionary
    tagger = RDRPOSTagger()
    tagger.constructSCRDRtreeFromRDRfile(modelPath)
    DICT = readDictionary(lexiconPath)

    # Process the raw text
    return tagger.tagRawSentence(DICT, raw_text)

# input_text = "Mua bánh_mì 500000 ."
# output = pos_tag(input_text)
# print("Tagged text:", output)  # In kết quả đã gắn thẻ từ loại của câu input