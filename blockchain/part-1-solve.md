solution script: predict_nonce.py
modules: random, mt19937predictor (pip install mersenne-twister-predictor)

summary: the nonce that is attached to each block in the naughty-or-nice blockchain is cryptographically insecure as the randbits(64) that are generated result from random.randrange(0xFFFFFFFFFFFFFFFF) which seeds from a mersenne twister.

details: more details in the predict_nonce.py script
