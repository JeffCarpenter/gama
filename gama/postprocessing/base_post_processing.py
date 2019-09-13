from abc import ABC
from typing import List, Union, Dict, Any

import pandas as pd


from gama.genetic_programming.components import Individual


class BasePostProcessing(ABC):
    """ All post-processing methods should be derived from this class.
    This class should not be directly used to configure GAMA.
    """

    def __init__(self, time_fraction: float):
        """

        Parameters
        ----------
        time_fraction: float
            The fraction of total time that should be reserved for this post-processing step.
        """
        self.time_fraction: float = time_fraction
        self._hyperparameters = {}

    def __str__(self):
        # Not sure if I should report actual used hyperparameters (i.e. include default), or only those set by user.
        user_set_hps = {parameter: set_value
                        for parameter, (set_value, default) in self._hyperparameters.items()
                        if set_value is not None}
        hp_configuration = ','.join([f"{name}={value}" for (name, value) in user_set_hps.items()])
        return f"{self.__class__.__name__}({hp_configuration})"

    @property
    def hyperparameters(self) -> Dict[str, Any]:
        """ Hyperparameter (name, value) pairs value determined by user > dynamic default > static default.

         Dynamic default values only considered if `dynamic_defaults` has been called.
         """
        return {parameter: set_value if set_value is not None else default
                for parameter, (set_value, default) in self._hyperparameters.items()}

    def _overwrite_hyperparameter_default(self, hyperparameter: str, value: Any):
        set_value, default_value = self._hyperparameters[hyperparameter]
        self._hyperparameters[hyperparameter] = (set_value, value)

    def dynamic_defaults(self, gama: 'Gama'):
        pass

    def post_process(
            self,
            x: pd.DataFrame,
            y: Union[pd.DataFrame, pd.Series],
            timeout: float,
            selection: List[Individual]) -> 'model':
        """
        Parameters
        ----------
        x: pd.DataFrame
            all training features
        y: Union[pd.DataFrame, pd.Series]
            all training labels
        timeout: float
            allowed time in seconds for post-processing
        selection: List[Individual]
            individuals selected by the search space, ordered best first

        Returns
        -------
        Any
            A model with `predict` and optionally `predict_proba`.
        """
        raise NotImplementedError("Method must be implemented by child class.")
