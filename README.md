## RDRPOSTagger ##

**RDRPOSTagger** is a robust, easy-to-use and language-independent toolkit for POS and morphological tagging. It employs an error-driven approach to automatically construct tagging rules in the form of a binary tree. The main properties of RDRPOSTagger are as follows:

- RDRPOSTagger obtains very fast performance in both learning and tagging process.

- RDRPOSTagger achieves a very competitive accuracy in comparison to the state-of-the-art results. See experimental results including performance speed and tagging accuracy for 13 languages in our *AI Communications* article.

- RDRPOSTagger supports pre-trained models for fine-grained POS and morphological tagging  for Bulgarian, Czech, Dutch, English, French, German, Hindi, Italian, Portuguese, Spanish, Swedish, Thai and Vietnamese.  

- RDRPOSTagger also supports pre-trained universal POS tagging models for 40+ languages. These models are learned using training data from the Universal Dependencies (UD) v2.0. Universal POS tagging accuracies on UD v2.0 test sets are [HERE](https://github.com/datquocnguyen/RDRPOSTagger/blob/master/Models/UniPOS/Readme.md).

The general architecture and experimental results of RDRPOSTagger can be found in our following papers:

- Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. [RDRPOSTagger: A Ripple Down Rules-based Part-Of-Speech Tagger](http://www.aclweb.org/anthology/E14-2005). In *Proceedings of the Demonstrations at the 14th Conference of the European Chapter of the Association for Computational Linguistics*, EACL 2014, pp. 17-20, 2014. [[.PDF]](http://www.aclweb.org/anthology/E14-2005) [[.bib]](http://www.aclweb.org/anthology/E14-2005.bib)

- Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. [A Robust Transformation-Based Learning Approach Using Ripple Down Rules for Part-Of-Speech Tagging](http://content.iospress.com/articles/ai-communications/aic698). *AI Communications* (AICom), vol. 29, no. 3, pp. 409-422, 2016. [[.PDF]](http://arxiv.org/pdf/1412.4021.pdf) [[.bib]](http://rdrpostagger.sourceforge.net/AICom.bib)

**Please cite** either the EACL or the AICom paper whenever RDRPOSTagger is used to produce published results or incorporated into other software.

**Find more information about RDRPOSTagger at its website:** [http://rdrpostagger.sourceforge.net/](http://rdrpostagger.sourceforge.net/)

In addition, you might find my new toolkit [jPTDP](https://github.com/datquocnguyen/jPTDP) interesting: [jPTDP - A Novel Neural Network Model for Joint POS Tagging and Dependency Parsing](https://github.com/datquocnguyen/jPTDP). jPTDP also supports pre-trained models for 40+ languages from UD v2.0. Universal POS tagging accuracies of jPTDP on UD v2.0 test sets  are [HERE](https://github.com/datquocnguyen/jPTDP/blob/master/UDv2.0_results.txt).
