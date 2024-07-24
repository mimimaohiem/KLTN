# -*- coding: utf-8 -*-

import os
import sys
os.chdir("../")
sys.setrecursionlimit(100000)
sys.path.append(os.path.abspath(""))
os.chdir("./pSCRDRtagger")

from multiprocessing import Pool
from InitialTagger.InitialTagger import initializeCorpus, initializeSentence
from SCRDRlearner.Object import FWObject
from SCRDRlearner.SCRDRTree import SCRDRTree
from SCRDRlearner.SCRDRTreeLearner import SCRDRTreeLearner
from Utility.Config import NUMBER_OF_PROCESSES, THRESHOLD
from Utility.Utils import getWordTag, getRawText, readDictionary
from Utility.LexiconCreator import createLexicon

# phân đoạn câu, phân đoạn từ và fix các từ phân đoạn sai.
############################################
from underthesea import word_tokenize, sent_tokenize


from underthesea import text_normalize

# Đường dẫn tới file chứa danh sách các từ cố định
fixed_words_path = '../data/vn/fixed_words_2.txt'
fixed_words = []

# Đọc các từ cố định từ file
with open(fixed_words_path, 'r', encoding='utf-8') as f:
    fixed_words = [text_normalize(line.strip().lower()) for line in f.readlines()]

# Đọc nội dung từ file input
file_path = '../data/vn/input.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Phân tách đoạn văn thành các câu
normallize=text_normalize(text.lower())
sentences = sent_tokenize(normallize)
print("Các câu:", sentences)

output_path = '../data/vn/output.txt'  # Đường dẫn tới file output

# Mở file để ghi kết quả
with open(output_path, 'w', encoding='utf-8') as output_file:
    # output_file.write("Các câu:\n")
    # output_file.write("\n".join(sentences) + "\n\n")
    
    # Phân tích từ cho mỗi câu và ghi vào filea
    for sentence in sentences:
        words = word_tokenize(sentence, format="text", fixed_words=fixed_words)
        output_file.write(words + "\n")

print("Đã lưu kết quả vào:", output_path)

#########################################

def unwrap_self_RDRPOSTagger(arg, **kwarg):
    return RDRPOSTagger.tagRawSentence(*arg, **kwarg)

class RDRPOSTagger(SCRDRTree):
    """
    RDRPOSTagger for a particular language
    """
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
            else:# Fired at root, return initialized tag
                sen.append(word + "/" + tag)
        return " ".join(sen)

    def tagRawCorpus(self, DICT, rawCorpusPath):
        lines = open(rawCorpusPath, "r").readlines()
        #Change the value of NUMBER_OF_PROCESSES to obtain faster tagging process!
        pool = Pool(processes = NUMBER_OF_PROCESSES)
        taggedLines = pool.map(unwrap_self_RDRPOSTagger, zip([self] * len(lines), [DICT] * len(lines), lines))
        outW = open(rawCorpusPath + ".TAGGED", "w")
        for line in taggedLines:
            outW.write(line + "\n")  
        outW.close()
        print("\nOutput file: " + rawCorpusPath + ".TAGGED")

def printHelp():
    print("\n===== Usage =====")  
    print('\n#1: To train RDRPOSTagger on a gold standard training corpus:')
    print('\npython RDRPOSTagger.py train PATH-TO-GOLD-STANDARD-TRAINING-CORPUS')
    print('\nExample: python RDRPOSTagger.py train ../data/goldTrain')
    print('\n#2: To use the trained model for POS tagging on a raw text corpus:')
    print('\npython RDRPOSTagger.py tag PATH-TO-TRAINED-MODEL PATH-TO-LEXICON PATH-TO-RAW-TEXT-CORPUS')
    print('\nExample: python RDRPOSTagger.py tag ../data/goldTrain.RDR ../data/goldTrain.DICT ../data/rawTest')
    print('\n#3: Find the full usage at http://rdrpostagger.sourceforge.net !')
    
def run():
    import sys
    args = sys.argv[1:]  # Lấy các đối số từ dòng lệnh
    if len(args) == 0:
        printHelp()
    elif args[0].lower() == "train":
        try:
            print("\n====== Start ======")
            createLexicon(args[1], 'full')
            createLexicon(args[1], 'short')
            getRawText(args[1], args[1] + ".RAW")
            DICT = readDictionary(args[1] + ".sDict")
            initializeCorpus(DICT, args[1] + ".RAW", args[1] + ".INIT")
            rdrTree = SCRDRTreeLearner(THRESHOLD[0], THRESHOLD[1])
            rdrTree.learnRDRTree(args[1] + ".INIT", args[1])
            rdrTree.writeToFile(args[1] + ".RDR")
            print('\nDone!')
            os.remove(args[1] + ".INIT")
            os.remove(args[1] + ".RAW")
            os.remove(args[1] + ".sDict")
        except Exception as e:
            print("\nERROR ==> ", e)
            printHelp()
    elif args[0].lower() == "tag":
        try:
            # Đặt các đường dẫn cố định vào biến
            modelPath = "../data/vn/data_train/train_3.txt.RDR"
            lexiconPath = "../data/vn/data_train/train_3.txt.DICT"
            outputPath = "../data/vn/output.txt"

            r = RDRPOSTagger()
            print("\n=> Read a POS tagging model from " + modelPath)
            r.constructSCRDRtreeFromRDRfile(modelPath)
            print("\n=> Read a lexicon from " + lexiconPath)
            DICT = readDictionary(lexiconPath)
            print("\n=> Perform POS tagging on " + outputPath)
            r.tagRawCorpus(DICT, outputPath)
        except Exception as e:
            print("\nERROR ==> ", e)
            printHelp()
    else:
        printHelp()

if __name__ == "__main__":
    run()
