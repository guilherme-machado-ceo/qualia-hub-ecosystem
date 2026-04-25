"""
Gurudev-QC SDK

Um SDK para desenvolvimento de algoritmos quânticos usando os princípios de Gurudev.
"""

__version__ = "0.1.0"
__author__ = "QIQU Team - Hubstry DeepTech"

from .compiler import GurudevQCCompiler
from .simulator import GurudevQCSimulator
from .algorithms import *

__all__ = [
    "GurudevQCCompiler",
    "GurudevQCSimulator",
]

