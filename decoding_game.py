# decoding mini game

def main():
    import webbrowser
    webbrowser.open('https://inventwithpython.com/cipherwheel/')
    print("Use this decoder to figure out what the message says")
    print("The inner ring represents the letters in the message and the outer ring represents the letters in the code")
    puzzles = {"kljvkl aopz tlzzhnl  (Hint: i = b)":"decode this message",
               "aopz pz h wbggsl (Hint: i = b)":"this is a puzzle",
               "kag zqqp fa ruzp kagd bmdfzqd (Hint: n = b)":"you need to find your partner"}

    for puzzle in puzzles:
        print(puzzle)
        puzzle_answer = ""
        while puzzle_answer.lower() != puzzles[puzzle]:
            puzzle_answer = input("What does this message say?:")
            if puzzle_answer.lower() == puzzles[puzzle]:
                print("You got it!")
                break
            else:
                print("Try again")
            
if __name__ == "__main__":
    main()

#https://inventwithpython.com/cipherwheel/ is the site for the decoder ring
