# hangman game

import random
def main():
    lost = True
    while lost == True:
        wordBank = ["apple", "banana", "grapefruit", "orange", "watermelon", "blueberry"]

        wordChoice = random.choice(wordBank)
        wordChoice = list(wordChoice)
        wordLen = len(wordChoice)
        print("\n")
        writing = "--- "*wordLen
        writing = writing.split(" ")
        del writing[wordLen]
        print(writing)

        going = True
        num_guess = 0
        used = []

        while going == True:
            print("Used Letters: ", used)
            print("\n")
            guess = input("Guess a letter: ")
            i = 0
            if guess in used:
                print("\n")
                print("You've already guessed that letter!")
            if guess not in used:
                
                for item in wordChoice:
                    if guess == wordChoice[i]:
                        del writing[i]
                        writing.insert(i,guess)
                    i +=1
                if guess not in wordChoice:
                    num_guess +=1
                    if num_guess == 1:
                        print("You have 1 try left")
                    else:
                        print("You have", 6 - num_guess, "tries left")
                    if num_guess >= 6:
                        print("\n")
                        print("You lost...")
                        print("Try again.")
                        lost = True
                        break
                print(writing)
                if writing == wordChoice:
                    print("\n")
                    print("You Won!")
                    lost = False
                    break
                if guess not in used:
                    used.append(guess)

if __name__ == "__main__":
    main()
    
