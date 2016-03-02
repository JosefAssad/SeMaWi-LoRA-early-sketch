#!/usr/bin/env python

from PyLoRA import Lora
from SeMaWi import Semawi
from IPython import embed


if __name__ == '__main__':
    referencearkitektur = Lora('http://referencearkitektur.dk')
    fkwiki = Semawi('wiki.referencearkitektur.dk',
                    'Josef',
                    '!Pta5>,z<b&gT vlt6p6')
    embed()

