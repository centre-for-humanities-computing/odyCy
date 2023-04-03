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
# TODO: We have to add a proper download link
```

## Usage :whale:

OdyCy pipelines can be imported with spaCy.

```python
import spacy

nlp = spacy.load("grc_dep_treebanks_trf")  # TODO: Rename model here
```

Pipelines can then be used as any other spaCy pipeline.
([spaCy Documentation](https://spacy.io/usage))

Check out our Documentation on [Basic Usage](https://centre-for-humanities-computing.github.io/odyCy/getting_started.html).

## Performance :boat:

odyCy achieves state of the art performance on multiple tasks on unseen test data from the Universal Dependencies Perseus treebank,
and performs second best on the PROIEL treebank’s test set on even more tasks.
In addition performance also seems relatively stable across the two evaluation datasets in comparison with other NLP pipelines.

For plots and tables on OdyCy's performance, check out the Documentation page on [Performance](https://centre-for-humanities-computing.github.io/odyCy/performance.html)

