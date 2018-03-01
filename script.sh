#!/bin/sh


python main.py -i a_example.in -o a_out
echo 'a'
python main.py -i b_should_be_easy.in -o b_out
echo 'b'
python main.py -i c_no_hurry.in -o c_out
echo 'c'
python main.py -i d_metropolis.in -o d_out
echo 'd'
python main.py -i e_high_bonus.in -o e_out
echo 'e'
