#!/bin/bash

docker run -it -v $PWD:/flask -p 5000:5000 flashcards
