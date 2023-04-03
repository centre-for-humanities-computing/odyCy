<p align="center">
  <img width="200" src="docs/_static/logo_with_text_below.svg">
  <div align="center" style="color: #2c5882; font-weight: bold; font-size: 14px; margin-top: -18px;">
    A general-purpose NLP pipeline for Ancient-Greek.
  </div>
</p>
<br>

## Features :mount_fuji:

 - [x] Part of speech tagging
 - [x] Lemmatization
 - [x] Dependency parsing
 - [x] Morphological analysis
 - [ ] Named entity recognition (work in progress :construction:)

## Installation :sunrise:

OdyCy models can be directly installed from huggingface:

```bash
# To install the transformer-based pipeline
pip install https://huggingface.co/chcaa/grc_odycy_joint_trf/resolve/main/grc_odycy_joint_trf-any-py3-none-any.whl
# To install the tok2vec-based small pipeline
pip install https://huggingface.co/chcaa/grc_odycy_joint_sm/resolve/main/grc_odycy_joint_sm-any-py3-none-any.whl
```

## Usage :whale:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/centre-for-humanities-computing/odyCy/blob/main/tutorials/01_odycy_getting_started.ipynb#&offline=true&sandboxMode=true)

OdyCy pipelines can be imported with spaCy.

```python
import spacy

# For the transformer-based pipeline
nlp = spacy.load("grc_odycy_joint_trf")

# For a faster and smaller (but less accurate) tok2vec-based pipeline
nlp = spacy.load("grc_odycy_joint_sm")
```

Pipelines can then be used as any other spaCy pipeline.
([spaCy Documentation](https://spacy.io/usage))

Check out our Documentation on [Basic Usage](https://centre-for-humanities-computing.github.io/odyCy/getting_started.html).

## Performance :boat:

odyCy achieves state of the art performance on multiple tasks on unseen test data from the Universal Dependencies Perseus treebank,
and performs second best on the PROIEL treebank’s test set on even more tasks.
In addition performance also seems relatively stable across the two evaluation datasets in comparison with other NLP pipelines.

For plots and tables on OdyCy's performance, check out the Documentation page on [Performance](https://centre-for-humanities-computing.github.io/odyCy/performance.html)

