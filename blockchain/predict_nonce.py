#!/usr/bin/env python3

# this is the start of a pre-computation attack on the naughty-or-nice blockchain from Kringlecon 2020. 
# the challenge is not an exact satoshi blockchain but a clever re-enactment for sake of CTF (and very fun).
# the nonce that is associated with each block is not user-discovered like in bitcoin,
# but instead auto-added by the program executing the creation of the blockchain. 
# This nonce is cryptograhically insecure as it uses a mersenne twister to generate the random numbers.
# we are given a 1528 block sample size which is more than enough (624) to calculate the entire state of the mersenne 
# twister and calculate the next x nonces in the chain. 
# $ pip install mersenne-twister-predictor


import random
from mt19937predictor import MT19937Predictor
from naughty_nice import Block, Chain

""" return a list of n length containing future nonces (str)
1) Assumes local blockchain.dat, official_public.pem,  naughty_nice.py files
2) The kringlecon grand challenge part 1 requires predicting a nonce *4* blocks in the future. 

Callee: Call this function with a n value representing the number of nonces in the future that you would like back.
"""
def predict_nonce(nonceList: list, num_nonces: int, nonce_length: int):
    # this will hold predicted nonces
    future_nonce_list = []

    predictor = MT19937Predictor()
    for i in nonceList:
        predictor.setrandbits(i, nonce_length)
        
    # calculate the next 4 64-bit random numbers
    for i in range(num_nonces):
        predicted_bits = predictor.getrandbits(nonce_length)
        # convert predicted to hex and store
        future_nonce_list.append(hex(predicted_bits))

    return future_nonce_list


nonceList = []
chain = Chain(load=True, filename='blockchain.dat')
# iterate over the blocks and extract their nonces into the nonceList
for i in range(len(chain.blocks)):
    nonceList.append(chain.blocks[i].nonce)
future = predict_nonce(nonceList, 4, 64)
# print out the list of future nonces
print([hex(int(nonce, 16)) for nonce in future])
