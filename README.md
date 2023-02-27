<p align="center">
  <img width="200" src="docs/_static/logo_with_text_below.svg">
  <div align="center" style="color: #2c5882; font-weight: bold; font-size: 14px; margin-top: -16px;">
    A state of the art NLP pipeline for Ancient Greek.
  </div>
</p>


<br>
<br>

This repository contains all code to reproduce our results.

## Features

 - [x] Part of speech tagging
 - [x] Lemmatization
 - [x] Dependency parsing
 - [x] Morphological analysis
 - [ ] Named entity recognition (work in progress)

## Installation

odyCy models can be directly installed from huggingface:

```bash
# TODO: We have to add a proper download link
```

## Usage

odyCy pipelines can be imported with spaCy.

```python
import spacy

nlp = spacy.load("grc_dep_treebanks_trf")  # TODO: Rename model here
```

Pipelines can then be used as any other spaCy pipeline.
([spaCy Documentation](https://spacy.io/usage))

For further information consult our Documentation (Add link).

## Performance

