.. _performance:

Performance
===========

odyCy achieves state of the art performance on multiple tasks on unseen test data from the Universal Dependencies Perseus treebank, and performs second best on the PROIEL treebank's test set on even more tasks.
In addition performance also seems relatively stable across the two evaluation datasets in comparison with other NLP pipelines.

.. admonition:: How did we evaluate performance?
  :class: note

  In order to reproduce our measurements check out our repository for evaluation of ancient greek pipelines, `greevaluation <https://github.com/centre-for-humanities-computing/greevaluation>`_.


Individual Tasks
----------------

Part-of-Speech Tagging
''''''''''''''''''''''

odyCy achieves state of the art performance on the UD Perseus Treebank and performs second best on PROIEL.
Our pipeline scores highest when taking the weighted average of the two test sets.

.. raw:: html
   :file: _static/plots/Part-of-Speech Tagging Accuracy.html

Morphological Analysis
''''''''''''''''''''''

odyCy achieves state of the art performance on the UD Perseus Treebank and performs second best on PROIEL.

.. raw:: html
   :file: _static/plots/Morphological Analysis Accuracy.html

Dependency Parsing
''''''''''''''''''''''
odyCy achieves state of the art performance on the UD Perseus Treebank and performs second best on PROIEL.

.. raw:: html
   :file: _static/plots/Dependency Parsing UAS.html

|

.. raw:: html
   :file: _static/plots/Dependency Parsing LAS.html

.. admonition:: What is LAS and UAS?
   :class: note

   Unlabelled attachment score (UAS) denotes the percentage of words that get assigned the correct head,
   while labelled attachment score (LAS) is the percentage of words that get assigned the correct head and label. 
   For more information, read the following `chapter <https://web.stanford.edu/~jurafsky/slp3/14.pdf>`__
   by Jurafsky and Martin.

Sentence Segmentation
'''''''''''''''''''''

odyCy performs second best on PROIEL and has highest weighted average score in sentence segmentation.

.. raw:: html
   :file: _static/plots/Sentencization F1-score.html

.. _performance lemmatization:

Lemmatization
'''''''''''''

odyCy achieves the highest weighted average over the two test sets.

.. raw:: html
   :file: _static/plots/Lemmatization Accuracy.html

Our experiments have shown that our lemmatization pipeline's performance is comparable to
that of its neural subcomponent. Therefore it's ambiguous which will result in better predictions.
See: :ref:`Lemmatization <architecture lemmatization>`

.. image:: _static/lemmatizer_comparison.png
   :width: 800
   :alt: Lemmatizer comparison

Corpora
-------

Perseus
''''''''''''''''''''''

odyCy achieves state of the art performance on POS-tagging, Morphological Analysis and Dependency Parsing and performs second best in Lemmatization.

.. image:: _static/perseus_table.png
    :width: 800
    :alt: Performance on the Perseus Treebank.

PROIEL
''''''''''''''''''''''

odyCy performs second best in POS-tagging, Morphological Analysis, Dependency Parsing, Sentence Segmentation and Lemmatization.

.. image:: _static/proiel_table.png
    :width: 800
    :alt: Performance on the PROIEL Treebank.
