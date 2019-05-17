from distutils.core import setup

setup(
    name='DistilFuzzyJoin',
    version='0.2.0',
    description='Placeholder fuzzy join',
    packages=['fuzzyjoin'],
    keywords=['d3m_primitive'],
    install_requires=[
        'pandas >= 0.22.0',
        'frozendict>=1.2',
        'fuzzywuzzy>=0.17.0',
        'python-Levenshtein>=0.12.0',
        'd3m==2019.4.4',
        ],
    entry_points={
        'd3m.primitives': [
            'data_transformation.fuzzy_join.DistilFuzzyJoin = fuzzyjoin.fuzzy_join:FuzzyJoinPrimitive'
        ],
    }
)
