# General

[Glossary](https://github.com/explosion/spaCy/blob/master/spacy/glossary.py)

# Specific points

## Location

* It might help to make an [Entity ruler](https://spacy.io/usage/rule-based-matching#entityruler) for the admin. divisions
* I'm still unsure aboutthe implication chains for admin. divisions
* For exact: Geographic tags may do the job, but since they aren't necessairly english, it sometimes catches them as ORGs
* area of accident - just most specific GEO?

## Vechicles

* It might make sense to make a custom ruler for those?
* Just list all involved and decide primacy in order

## numbers of people

* Should be fairly straight forward? named entities (PROPN) + numbers (NUM)
* VERB/ADJ (injured/killed/wounded/dead/etc.) [-- nummod --> NUM]/[-- nsubjpass --> NOUN (others/etc.) -- nummod--> NUM] ?

## Dates

* Stated in text takes precedence over metadata
* There is something in the NER module for dates and times

## Ages

* numbers that arent counts?
* PROPN -- appos --> NUM ?

## Type