.. _small model:

Small Pipeline
==============

If you want to enjoy the convenience of odyCy, but you need a faster pipeline for real-time production use,
or you just want to play around with odyCy on a less performant computer, we recommend trying out our small model.

The small pipeline is functionally quivalent to the base one, therefore the code is equivalent
except for installation and importing.

Getting Started
---------------

Install the pipeline from Hugginface Hub.

.. code-block:: bash

    # To install the small pipeline
    pip install https://huggingface.co/chcaa/grc_odycy_joint_sm/resolve/main/grc_odycy_joint_sm-any-py3-none-any.whl

Then import it with spaCy.

.. code-block:: python

   import spacy

   nlp = spacy.load("grc_odycy_joint_sm")

The rest can be found under :ref:`Basic Usage <getting started>`.

Differences
-----------

Unlike the large pipeline, the small one is not based on a pretrained transformer but uses
a `Tok2Vec layer <https://spacy.io/api/tok2vec/>`_ as its base embedding model.
This layer constructs embeddings based on sub-word features and encodes context from a window around
the given token, but does not use `Attention <https://en.wikipedia.org/wiki/Attention_(machine_learning)>`_.

The rest of the :ref:`Pipeline Architecture <pipeline architecture>` is identical.

Performance
~~~~~~~~~~~
For differences in performance between the small and large pipelines see :ref:`Performance <performance>`

