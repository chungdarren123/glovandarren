from typing import Protocol, Tuple

class AlgorithmStrategy(Protocol):
    def execute(self, content: str) -> Tuple[float, str]:
        '''
        Executes the algorithm on the given content.
        Returns a tuple of (score, label).
        '''
        ...
