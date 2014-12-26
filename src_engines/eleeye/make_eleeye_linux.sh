#!/bin/sh
g++ -DNDEBUG -O4 -Wall -oeleeye_linux src/base/pipe.cpp src/eleeye/ucci.cpp src/eleeye/pregen.cpp src/eleeye/position.cpp \
    src/eleeye/genmoves.cpp src/eleeye/hash.cpp src/eleeye/book.cpp src/eleeye/movesort.cpp src/eleeye/preeval.cpp \
    src/eleeye/evaluate.cpp src/eleeye/search.cpp src/eleeye/eleeye.cpp

