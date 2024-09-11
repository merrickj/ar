# ar

Adapt Retreat

Agent Based Model where regions are agents

As flooding events happen over time, Agents decide whether to adapt or retreat


## Versions

There are two versions of the model:
* [Toy](./src/toy): Toy model
* [Numeric](./src/numeric): Model populated with numbers from CIAM for all 29 DIVA coastal regions of Ireland


## Running model

To run toy model: ``python3 src/toy/toy.py arg1 arg2 arg3``, where
* ``arg1``: number of regions
* ``arg2``: probability of flood in fraction terms
* ``arg3``: probability of action in fraction terms

To run numeric model: ``python3 src/numeric_a/ar.py arg1``, where
* ``arg1``: beta, perception factor

To run numeric model in a diagnositc mode that enables plotting for a selected region: ``python3 src/numeric_b/ar.py GEV arg1``, where
* ``arg1``: region number (i.e. select region)


## Develop branch
The develop branch contains files in development not yet in mainstream workflow, or relevant supporting information