1) we can identify which block jack frost altered by dumping the naughty/nice scores out of the entire blockchain.dat and then sorting by unique values (hoping to see a value pop up that is anomylous as he only altered a single block (supposedly).

```python
for i in range(len(chain.blocks)):
	print(chain.blocks[i].score)
```

```bash
python3 find_altered_block.py | sort -u
```

We can see that a certain block has a score of 4294967295. We can then view, extract, and dump the contents of that block with the following python:

```python
for i in range(len(chain.blocks)):
    if chain.blocks[i].score == 4294967295:
        print(chain.blocks[i])
        print("dumping contents of the block")
        chain.blocks[i].dump_doc(0)
        chain.blocks[i].dump_doc(1)
        print(i)
        chain.save_a_block(i)
```

parse-pdf-output contains output of `python3 ~/Downloads/DidierStevensSuite/pdf-parser.py -f 129459.pdf > parse-pdf-output`

the data length fields are NOWHERE close to what they actually are (both Data fields are MUCH longer than what they are indicated as being)

```bash
xxd block.dat |awk '{print $10}' | less
```

Finding out that targeting a particular MD5 for a file is not possible was quite daunting to me. So far my understanding of block chains indicated that in order to tamper with a block you would need to alter it such that its MD5is exactly the same as it was when it was entered into the blockchain. Alas Jack Frost had an interesting means to exploit his objective afterall.

After studying how hash collisions can work with PDF style documents here: https://github.com/corkami/collisions#pdf I realized that my initial interpretation fo the pdf-parser output was indeed correct. 

The document tree within the PDF has been altered so that the root points to document at index 2 however there is also another document at index 3 (used in creating a hash collision between the two documents). 

In this way Jack must have been able to get Shinny Upatree to upload a PDF which actually had a collided pairing already created ahead of time by Jack. Lets see if we can view the document that Jack Frost had Shinny *think* he was uploading.

```bash
bless 129459.pdf
```

> Editing the hex to flip the byte for /Pages *2* to /Pages *3* (0x32 => 0x33) and saving as a new document allows us to view the other document thats included within the PDF! And its contents are quite revealing to as Jack Frosts methodology.


Jack Frost got Shinny Upatree to leave the submission candidate PDF unattended and went and created a collision at that point which would provide Jack a post-hoc means to flip the singular bit in the data field of the block, changing the root pointed to within the PDF (and keeping the same hash!) and reveal the supporting evidence of his "niceness". 

Supporting PDF *check*
Supporting Binary Blob *unchecked*
Score *unchecked*
Overall Block *unchecked*

I ended up solving the 2nd part of this challenge first (although I immediately spotted the sign-flip capability in the naughty/nice byte), I just didn't know how to make the md5sums match `md5sum block.dat` until I watched the lecture that accompanies the slide deck linked to us as a hint within the game: https://www.youtube.com/watch?v=BcwrMnGVyBI

At exactly 54:50 I clued into how the prefix structuring and collision blocks end up working together during the Unicoll collision. Essentially what happens is that we can specify an arbitrarily large beginning of the document to hold as our "prefix" (as long as it is divisible by 4), and then the next segment becomes the "collision block" which essentially serves as our random space to guess hex values until the md5sum matches the original document. The nice thing about this Unicoll collision is that the nibble that gets incremented/decrimented exactly mirrors the byte 10 bytes from the end of the prefix.

We can then suppose that Jack Frost created a collision block which held a prefix of all of the data in the block up to and including the last byte of the Data Length field. At that point the Binary blob data started (which he tricked Shinny Upatree into thinking was an image file...uploaded as a blob...c'mon Shinny..). 10 bytes before the end of the prefix would put the byte that gets incremented/decrimented at exactly the Naughty/Nice sign byte. 

So Jack Frost increments the Naughty/Nice byte (49th), and then decriments the 89th byte to maintain the hash collision. So to reverse this we decriment the 59th bit 1 => 0 and then increment the 89th byte D6 => D7.

For the PDF since we found out we can increment the byte at the 109th byte in block.dat to reveal the original PDF that Shinny thought he was signing off on, we can conversely decriment the byte at the 149th location to maintain the hash collision.

This ultimately gives us a `sha256sum block.dat => fff054f33c2134e0230efb29dad515064ac97aa8c68d33c58c01213a0d408afb which solves the grand challenge for Kringlecon 3 Turtle Doves 2020!!

- slixperi 


