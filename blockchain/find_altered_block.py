from naughty_nice import Block, Chain
from Crypto.Hash import MD5, SHA256
from Crypto.PublicKey import RSA

with open('official_public.pem', 'rb') as fh:
   official_public_key = RSA.importKey(fh.read())

chain = Chain(load=True, filename='blockchain.dat')
# chain.verify_chain(official_public_key)

# score identified by running print(chain.blocks[i]) with python3 find_altered_block.py | sort -u
for i in range(len(chain.blocks)):
    if chain.blocks[i].score == 4294967295:
        print(chain.blocks[i])
        print("dumping contents of the block")
        chain.blocks[i].dump_doc(0)
        chain.blocks[i].dump_doc(1)
        print("dumping just the binary block itself (block.dat)")
        chain.save_a_block(i)
