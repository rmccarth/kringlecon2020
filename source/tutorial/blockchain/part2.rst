.. _Part2:

Naughty/Nice List with Blockchain Investigation Part 2 (11b)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 

**Difficulty:** 5

**Type:**  Main Questline
    
**Tooltip:**  

    "The SHA256 of Jack's altered block is: 58a3b9335a6ceb0234c12d35a0564c4e f0e90152d0eb2ce2082383b38028a90f. If you're clever, you can recreate the original version of that block by changing the values of only 4 bytes. Once you've recreated the original block, what is the SHA256 of that block?"


.. topic:: Solution and Explanation

    We can identify which block Jack Frost altered by dumping the naughty/nice scores out of the entire blockchain.dat and then sorting by unique values (hoping to see a value pop up that is anomylous).
    
    .. code-block:: python  

        for i in range(len(chain.blocks)):
            # now print the score of each block! 
            print(chain.blocks[i].score)  

    Piping the output of our code into a bash sort (unique):

    .. code-block:: bash

        $ python3 find_altered_block.py | sort -u
        > we spot '4294967295' in the output

    This compels us to write a new script (or alter the first one) to retrieve that block and its attached document contents:

    .. literalinclude:: ../../../blockchain/find_altered_block.py
        :language: python
        :linenos:

.. topic:: Investigating the PDF

    The PDF file was immediately interesting to me so I opened it to find a letter affirming Jack Frosts ultimate niceness - how strange. A game is certainly afoot. So I popped the pdf into `PDF-parser <https://github.com/DidierStevens/DidierStevensSuite/>`_. and stored the output in 'parser-pdf-output

    .. code-block:: bash

        $ parse-pdf-output contains output of `python3 ~/Downloads/DidierStevensSuite/pdf-parser.py -f 129459.pdf > parse-pdf-output`

    I spotted that this PDF has a lot of internal content for a 1 page document. But I wasn't sure what to make of it. I started reading everything I could about hash collisions from the repositories linked to us by the challenge tooltips and I found the full workshop video associated with the slidedeck that we were given detailing the different forms of hash collisions and how they are implemented (`Lecture Video <https://www.youtube.com/watch?v=BcwrMnGVyBI/>`_.)
    In the collisions git repository that was also linked by an elf-tooltip, I was able to find a subsection of the README.md that detailed how PDF's can be combined into one large document with enough excess randomness to collide the two files `PDF Collisions <https://github.com/corkami/collisions#pdf/>`_. I realized that if Shinny Upatree was somehow compromised...

.. topic:: Unicoll MD5 Collisions

    The methodology outlined in the collisions README.md indicated that the trick to displaying either document is to flip the byte associated with the document root.

    An exercise that I found useful in understanding how the bytes get altered in the 2-PDF collision was using vbindiff on the provided examples from the collisions repository.

    .. code-block:: bash

        $ vbindiff collision1.pdf collision2.pdf

    .. image:: ../../_static/vbindiff-collision1-v-collision2.png    
        :width: 400    
    
.. role:: raw-html(raw)
    :format: html  

:raw-html:`<br />`

.. topic:: Hex Editing the block.bin

    I began to play with the bytes in the PDF file and sure enough when I incremented the root byte "/Pages 2" => "/Pages 3", I noticed the content of the PDF document completely change!!
    
    However,the MD5 was altered! That meant I was missing something because if we want to maintain the md5 collision that is likely necessary to alter a block in the blockchain, the MD5 needs to remain unchanged. 
    
    At exactly 54:50 I clued into how the prefix structuring and collision blocks end up working together during the Unicoll collision. Essentially what happens is that we can specify an arbitrarily large beginning of the document to hold as our "prefix" (as long as it is divisible by 4), and then the next segment becomes the "collision block" which essentially serves as our random space to guess hex values until the md5sum matches the original document. The nice thing about this Unicoll collision is that the nibble that gets incremented/decrimented exactly mirrors the byte 10 bytes from the end of the prefix.

    It took some thinking but I eventually realized that the PDF portion of the collisions README.md also mentioned that this attack was performed using the Unicoll collison.
    Drawing on what I had learned from the workshop lecture video, I was able to suppose that maybe we have to decriment a different byte to maintain the hash collision. After playing with my hexcurse hexeditor for a bit to get the length of a line to be exactly 16 bytes, I was able to find where I needed to alter a byte to maintain the collision.

    .. code-block:: bash

        $ hexcurse -r 16 block.dat

    Editing the hex to flip the byte for /Pages **2** to /Pages **3** (0x32 => 0x33) and saving as a new document allows us to view the other document thats included within the PDF! And its contents are quite revealing to as Jack Frost's methodology!
    
    Reading into the newly revealed PDF content, Jack Frost got Shinny Upatree to leave the submission candidate PDF unattended and went and created a collision at that point which would provide Jack a post-hoc means to flip two bytes within the PDF data field of the blockchain block. This would ultimately change the root pointed to within the PDF (and keep the same hash!), revealing the previously hidden, supporting evidence of his "niceness".**
    
    That leaves us with an understanding of how Jack Frost altered the PDF to get Shinny Upatree to sign-off. But how did he get his naughty/nice score so high as well?

.. topic:: Closing out the Challenge

    Jack used the same Unicoll technique on the byte that dictates the **sign** of the naughty/niceness score. Jack took the beginning section of the block, using his pre-computed nonce from :ref:`Part1`, and set the prefix to contain the naughty/nice sign byte to be exactly 10 bytes before the end of the prefix.
    Jack was then able to run the Unicoll collision on the block which altered a value within the "Binary Blob" field, mirroring the byte that was altered in the prefix, and maintaining yet again the MD5 of the block. As the Binary Blob data section served as the 'collision block', the rest of the Blockchain Block could be appended with the content
    that we see in the PDF section of the block. As the content in the PDF section is also a hash collision with its doppleganger sibling PDF, whichever bytes are altered will yet again maintain the MD5. Finally, the block could be appended with the signature and signing section, which would remain unchanged regardless of which bytes were being altered above in the block.

    In summary, Jack Frost increments the Naughty/Nice byte (49th), and then decriments the 89th byte to maintain the hash collision. So to reverse this we decriment the 59th bit 1 => 0 and then increment the 89th byte D6 => D7.
    For the PDF since we found out we can increment the byte at the 109th byte in block.dat to reveal the original PDF that Shinny thought he was signing off on, we can conversely decriment the byte at the 149th location to maintain the hash collision.
    
    .. code-block:: bash
        
        $ vbindiff block.dat final-block.dat
    
    .. image:: ../../_static/vbindiff-init-v-final.png
        :width: 400
    
    
    This ultimately gives us:  

    .. code-block:: bash
    
        $ sha256sum block.dat 
         > fff054f33c2134e0230efb29dad515064ac97aa8c68d33c58c01213a0d408afb 
    
    And that solves the grand challenge for Kringlecon 3 Turtle Doves 2020!!  

    
    