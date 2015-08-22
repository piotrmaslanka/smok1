# coding=UTF-8
from weakref import WeakValueDictionary

CONNECTIONS = WeakValueDictionary()
# Połączenia to referencje słabe, gdyż obiekty mają umierać gdy połączenie zostanie zerwane (czyli wątek połączenia rzuci exceptionem)