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
                left: Inputs,
                right: Inputs,
                timeout: float = None,
                iterations: int = None) -> base.CallResult[Outputs]:
        return base.CallResult(left)

    def multi_produce(self, *,
                      produce_methods: typing.Sequence[str],
                      left: Inputs, right: Inputs,
                      timeout: float = None,
                      iterations: int = None) -> base.MultiCallResult:  # type: ignore
        return self._multi_produce(produce_methods=produce_methods,
                                   timeout=timeout,
                                   iterations=iterations,
                                   left=left,
                                   right=right)
