##############################################################
# solve script for kringlecon 2020 vending-machine challenge #
##############################################################

import subprocess
import signal
import time

cipher = "LVEdQPpBwr"
solution = ""

for index in cipher:
    # solution starts at "", the more letters we guess correctly, we do solution += char
    print(f"solution thus far: {solution}", end="\r", flush=True)
    # for all chars in strings.printable, the ones that break bash, escaped
    charlist = ['\x0c', '\x0b', '\r', '\n', '\t', ' ', '~', '}', '|', '{', '\\`', '_', '^', ']', '\\', '[', '@', '?', '>', '=', '<', ';', ':', '/', '.', '-', ',', '+', '*', ')', '(', "'", '&', '%%', '$', '#', '\\"', '!', 'Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A', 'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0']
    for char in charlist:
        print(f"trying: {solution}{char}", end="\r", flush=True)
        # delete vending-machines.json so we can construct a new password and check its "encryption"
        subprocess.call("rm vending-machines.json > /dev/null", shell=True)
        # name: a, password: solutionThusFar+testedCharacter
        # this executes the vending-machine binary and outputs our controlled input, encrypted, into vending-machine.json
        command = 'printf "a\n'+solution+char+'\n" | ./vending-machines > /dev/null'
        process = subprocess.Popen(command, shell=True)
        # wait for binary to process our data
        time.sleep(.25)
        process.send_signal(signal.SIGINT)
        # read the json file and retrieve the password line
        with open('vending-machines.json') as f:
            content = f.readlines()[2:3][0].replace('password', '')
            # if the cipher character we are hoping for exists in the password line, ensure that
            # its location is in the place that we expectit to be
            if index in content and (content.find(index) == cipher.find(index) + 7):
                print("found a character match")
                print(char + " => " + index, end="\r", flush=True)
                # display the password contents of vending-machine.json
                print(content, end="\r", flush=True)
                # mostly for debugging purposes,but its useful to see where the letters are triggering
                print(content.find(index), end="\r", flush=True)
                print(cipher.find(index), end="\r", flush=True)
                solution += char
                # if we get a match, break out of the for loop after appending the char to solution. 
                # this then starts the next index character back from the beginning
                break
print(f"solution: {solution}")