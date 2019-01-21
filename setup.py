from distutils.core import setup

setup(
    name='DistilFuzzyJoin',
    version='0.1.0',
    description='Placeholder fuzzy join',
    packages=['fuzzyjoin'],
    keywords=['d3m_primitive'],
    install_requires=[
        'pandas >= 0.22.0',
        'frozendict>=1.2',
        'fuzzywuzzy>=0.17.0',
        'python-Levenshtein>=0.12.0',
        'd3m',
    ],
    dependency_links=[
        'git+https://gitlab.com/datadrivendiscovery/d3m.git@devel#egg=d3m'
    ],
    entry_points={
        'd3m.primitives': [
            'distil.FuzzyJoin = fuzzyjoin.fuzzy_join:FuzzyJoinPrimitive'
        ],
    }
)
