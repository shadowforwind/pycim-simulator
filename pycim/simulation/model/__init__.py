# -*- coding: utf-8 -*-
"""
module: model

Function: Provide three models of CIM

"""
# author: Peixiang Li, peixiangli@quanta.org.cn

from .c_number import RK45c_number
from .discrete import RK45Discrete,RK4Discrete,eulerDiscrete
from .meanField import RK45meanField
__all__ = ["RK45c_number","RK45Discrete","RK4Discrete","eulerDiscrete","RK45meanField"]