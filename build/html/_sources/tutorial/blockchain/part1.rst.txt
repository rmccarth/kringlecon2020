.. _Part1:

Naughty/Nice List with Blockchain Investigation Part 1 (11a)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Difficulty:** 5

**Type:**  Main Questline
    
**Tooltip:**   

    "Even though the chunk of the blockchain that you have ends with block 129996, can you predict the nonce for block 130000? Talk to Tangle Coalbox in the Speaker UNpreparedness Room for tips on prediction and Tinsel Upatree for more tips and tools. (Enter just the 16-character hex value of the nonce)"

.. topic:: Solution Script and Explanation

    The nonce that is attached to each block in the naughty-or-nice blockchain is cryptographically insecure as the randbits(64) that are generated result from random.randrange(0xFFFFFFFFFFFFFFFF) which seeds from a mersenne twister.

    The sourecode attached is commented and will provide even more clarity.

    .. literalinclude:: ../../../blockchain/predict_nonce.py
        :language: python
        :linenos:

    .. code-block:: bash  

        $ python3 predict_nonce.py
        > ['0xb744baba65ed6fce', '0x1866abd00f13aed', '0x844f6b07bd9403e4', '0x57066318f32f729d']

    The fourth value returned from our script is 0x57066318f32f729d so we submit **57066318f32f729d** as the answer and predicted nonce!

