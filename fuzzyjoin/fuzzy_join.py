"""
   Copyright © 2018 Uncharted Software Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import typing
import os
import csv
import collections

import frozendict  # type: ignore
import pandas as pd  # type: ignore
import numpy as np

from d3m import container, exceptions, utils as d3m_utils
from d3m.metadata import base as metadata_base, hyperparams
from d3m.primitive_interfaces import base, transformer
from common_primitives import utils
from fuzzywuzzy import fuzz, process

__all__ = ('FuzzyJoinPrimitive',)

Inputs = container.Dataset
Outputs = container.Dataset


class Hyperparams(hyperparams.Hyperparams):
    left_col = hyperparams.Hyperparameter[str](
        default="",
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description='Name of left join column.'
    )
    right_col = hyperparams.Hyperparameter[str](
        default="",
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description='Name of right join column.'
    )
    accuracy = hyperparams.Hyperparameter[float](
        default=0.0,
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description='Requierd accuracy of join ranging from 0.0 to 1.0, where 1.0 is an exact match.'
    )


class FuzzyJoinPrimitive(transformer.TransformerPrimitiveBase[Inputs,
                                                              Outputs,
                                                              Hyperparams]):
    """
    Place holder fuzzy join primitive
    """

    __author__ = 'Uncharted Software',
    metadata = metadata_base.PrimitiveMetadata(
        {
            'id': '6c3188bf-322d-4f9b-bb91-68151bf1f17f',
            'version': '0.1.0',
            'name': 'Fuzzy Join Placeholder',
            'python_path': 'd3m.primitives.distil.FuzzyJoin',
            'keywords': ['join', 'columns', 'dataframe'],
            'source': {
                'name': 'Uncharted Software',
                'contact': 'mailto:cbethune@uncharted.software'
            },
            'installation': [{
                'type': metadata_base.PrimitiveInstallationType.PIP,
                'package_uri': 'git+https://github.com/unchartedsoftware/distil-fuzzy-join.git@' +
                               '{git_commit}#egg=distil-fuzzy-join'
                               .format(git_commit=d3m_utils.current_git_commit(os.path.dirname(__file__)),),
            }],
            'algorithm_types': [
                metadata_base.PrimitiveAlgorithmType.ARRAY_CONCATENATION,
            ],
            'primitive_family': metadata_base.PrimitiveFamily.DATA_TRANSFORMATION,
        }
    )

    def produce(self, *,
                left: Inputs,  # type: ignore
                right: Inputs,  # type: ignore
                timeout: float = None,
                iterations: int = None) -> base.CallResult[Outputs]:

        # attempt to extract the main table
        try:
            left_resource_id, left_df = utils.get_tabular_resource(left, None)
        except ValueError as error:
            raise exceptions.InvalidArgumentValueError("Failure to find tabular resource in left dataset") from error

        try:
            right_resource_id, right_df = utils.get_tabular_resource(right, None)
        except ValueError as error:
            raise exceptions.InvalidArgumentValueError("Failure to find tabular resource in right dataset") from error

        accuracy = self.hyperparams['accuracy'] * 100
        if accuracy <= 0 or accuracy > 100:
            raise exceptions.InvalidArgumentValueError("accuracy of " + str(self.hyperparams['accuracy']) +
                                                       " is out of range") from error

        # use d3mIndex from left col if present
        right_df = right_df.drop(columns='d3mIndex')

        # fuzzy match each of the left join col against the right join col value and save the results as the left
        # dataframe index
        choices = right_df[self.hyperparams['right_col']].unique()
        left_df.index = left_df[self.hyperparams['left_col']]. \
            map(lambda x: self._string_fuzzy_match(x, choices, accuracy))

        # make the right col the right dataframe index
        right_df = right_df.set_index(self.hyperparams['right_col'])

        # inner join on the left / right indices
        joined = container.DataFrame(left_df.join(right_df, lsuffix='_1', rsuffix='_2', how='inner'))

        # sort on the d3m index if there, otherwise use the joined column
        if 'd3mIndex' in joined:
            joined = joined.sort_values(by=['d3mIndex'])
        else:
            joined = joined.sort_values(by=[self.hyperparams['left_col']])
        joined = joined.reset_index(drop=True)

        # create a new dataset to hold the joined data
        resource_map = {}
        for resource_id, resource in left.items():  # type: ignore
            if resource_id == left_resource_id:
                resource_map[resource_id] = joined
            else:
                resource_map[resource_id] = resource
        result_dataset = container.Dataset(resource_map)

        return base.CallResult(result_dataset)

    def multi_produce(self, *,
                      produce_methods: typing.Sequence[str],
                      left: Inputs, right: Inputs,  # type: ignore
                      timeout: float = None,
                      iterations: int = None) -> base.MultiCallResult:  # type: ignore
        return self._multi_produce(produce_methods=produce_methods,
                                   timeout=timeout,
                                   iterations=iterations,
                                   left=left,
                                   right=right)

    def fit_multi_produce(self, *,
                          produce_methods: typing.Sequence[str],
                          left: Inputs, right: Inputs,  # type: ignore
                          timeout: float = None,
                          iterations: int = None) -> base.MultiCallResult:  # type: ignore
        return self._fit_multi_produce(produce_methods=produce_methods,
                                       timeout=timeout,
                                       iterations=iterations,
                                       left=left,
                                       right=right)

    @classmethod
    def _string_fuzzy_match(cls,
                            match: typing.Any,
                            choices: typing.Sequence[typing.Any],
                            min_score: float) -> typing.Optional[str]:
        choice, score = process.extractOne(match, choices)
        val = None
        if score >= min_score:
            val = choice
        return val
