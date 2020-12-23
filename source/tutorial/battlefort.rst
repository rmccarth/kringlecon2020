.. _Battlefort:

Battlefort
^^^^^^^^^^


**Difficulty:** ~1-4
    
**Type:**  Sidequest

.. topic:: Easy/Medium Solution and Explanation

    The value of your player name (e.g. 1, 2, 3) determines the randomness of your board. You can enter a super large/random number to have a more complex board meaning its harder for the enemy to hit your ships. Also on easy/medium difficulty the enemies ships are pretty consistently in the exact same place from round to round.

    The easy and medium levels here are solved by playing the game and learning where the enemy ships are when you enter "1" as your playername. The easy level will be essential for solving the hard and insane challenges however. 


.. topic:: Hard/Insane Solution and Explanation

    The trick here is to use a 'pre-computatin' attack against the game.

    You can actually play two games at once which is critical to solving the challeng. you can play the game normally from 2020.kringlecon.com and also simultaneously by opening a browswer window at https://snowball2.kringlecastle.com/game

    Impossible mode requires 100% accuracy which we will address in a moment.

.. topic:: Hard Mode

    Note: In this challenge and in the Insane Mode challenge its vital that the window that you solve the challenge in is the same window where your main player is engaged in the quest (the main 2020.kringlecon.com window) or else you won't get credit for the win and will have to re-do your work.

    1) Open up an instance of the hard mode game (where you can see your player number).
    2) Take that player number and start up an easy game with that number as your player name.
    3) Start up the easy game and discover all of the locations of the enemies forts by just spam-clicking around. Note the locations of the forts (it helps to leave 1 square uncompleted to use as reference).
    4) Duplicate your work on the hard game, with all of the determined fort locations being solved ahead of time, it should be a simple matter to select the same squares on the hard-mode game!

.. topic:: Insane Mode

    By right clicking and selecting "inspect" you can view the HTML of the page. In this mode there is a comment at the bottom of the page which displays all 624 values that are rejected before the 625 value is selected. Convenient that 624 values is related to the mersenne twister! Lets use the 624 values to calculate our player ID, and then use that value along with the attack method from Hard Mode to win the Insane Mode game!

    1) start an insane mode game
    2) inspect the page and copy the contents of the thrown-out values into a file

    .. code-block:: bash

        $ cat seeds | awk '{print $1}' > extracted-seeds # this selects only the first column from the thrown-out seeds
        $ git clone https://github.com/kmyk/mersenne-twister-predictor.git
        $ cd mersenne-twister-predictor/bin
        $ cat ../../extracted-seeds | ./mt19937predict | head -n 1 > predicted.txt # this runs the mt19937 prediction script and outputs the next value in the sequence (what should be our player ID).
        $ cat predicted.txt

    Now you can use the methodology outlined above in the Hard Mode section to pass this level. 

    The mersenne-twister-predictor is incredibly useful in this case to calculate the PlayerID that is generated for us, and hidden from us by the game. This library and binary will also be useful in the Naughty/Nice Challenge so keep this git repository handy!