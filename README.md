# ar

Adapt Retreat

Agent Based Model where regions are agents

As flooding events happen over time, Agents decide whether to adapt or retreat


## Versions

There are three versions of the model:
* [Toy](./src/toy): Toy model
* [Numeric_a](./src/numeric_a): Model populated with numbers from CIAM
* [Numeric_b](./src/numeric_b): Model also populated with numbers from CIAM, with region specific plotting.

As of writing on June 27th 2024, it is unclear whether numeric_b supercedes numeric_a or whether there are different parts of each that are at different parts of the conceptual frontier.

## Running model

To run toy model: ``python3 src/toy/toy.py arg1 arg2 arg3``, where
* ``arg1``: number of regions
* ``arg2``: probability of flood in fraction terms
* ``arg3``: probability of action in fraction terms

To run numeric_a model: ``python3 src/numeric_a/mvp.py arg1``, where
* ``arg1``: beta

To run numeric_b model: ``python3 src/numeric_b/gev.py arg1``, where
* ``arg1``: region number (i.e. select region)


## Develop branch
The develop branch contains files in development not yet in mainstream workflow, or relevant supporting information