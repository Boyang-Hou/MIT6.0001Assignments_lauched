# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for i in secret_word:
        if i not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    list_word = []
    for i in secret_word:
        if i in letters_guessed:
            list_word.append(i)
        else:
            list_word.append('_ ')

    return "".join(list_word)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    list_available = []
    for i in string.ascii_lowercase:
        if not i in letters_guessed:
            list_available.append(i)
    return "".join(list_available)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    vowels = "aeiou"

    print("Welcome to the game, Hangman!")
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f"You have {warnings_remaining} warnings left.")

    # --- 主游戏循环 ---
    while guesses_remaining > 0:
        # 检查是否胜利
        if is_word_guessed(secret_word, letters_guessed):
            break  # 游戏结束

        # 打印本轮状态
        print("-------------")
        print(f"You have {guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")

        # 1. 获取用户输入

        # 2. 验证输入（是不是字母？是否猜过？）

        # 3. 处理无效输入（扣除警告或猜测次数）

        # 4. 处理有效输入（检查字母是否在 secret_word 中）

        # 5. 处理猜对的情况 (显示 get_guessed_word)

        # 6. 处理猜错的情况 (扣除猜测次数)
        guess = input("Please guess a letter: ")
        if not guess.isalpha():
            # 处理惩罚
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print(
                    f"Oops! That is not a valid letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
            else:
                guesses_remaining -= 1
                print(
                    f"Oops! That is not a valid letter. You have {guesses_remaining} guesses left: {get_guessed_word(secret_word, letters_guessed)}")
            continue
        else:
            guess = guess.lower()
            if guess in letters_guessed:
                # 处理惩罚
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print(
                        f"Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                else:
                    guesses_remaining -= 1
                    print(
                        f"Oops!You've already guessed that letter. You have {guesses_remaining} guesses left: {get_guessed_word(secret_word, letters_guessed)}")
                continue
            else:
                letters_guessed.append(guess)

        if guess not in secret_word:
            print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
            if guess in vowels:
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1

        else:
            print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
        # --- 在这里添加你的游戏结束逻辑 ---
    if is_word_guessed(secret_word, letters_guessed):
        # 玩家胜利
        print("Congratulations, you won!")
        unique_letters = set(secret_word)
        scores = len(unique_letters) * guesses_remaining
        print(f'Your total score for this game is: {scores}')
    else:
        # 玩家失败
        print("Sorry, you ran out of guesses.")
        print(f"The word was {secret_word}.")


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    my_word_stripped = my_word.replace(' ', '')

    # 检查长度
    if len(my_word_stripped) != len(other_word):
        return False
    # 找出已经猜出的字母
    revealed_letters = []
    for i in my_word_stripped:
        if i != '_':
            revealed_letters.append(i)

    # 遍历索引
    for i in range(len(other_word)):

        my_char = my_word_stripped[i]
        other_char = other_word[i]

        if my_char != "_":
            # my_char不是下划线, 而是字母
            if my_char != other_char:
                # my_char other_char不匹配
                return False
        else:
            # my_char是一个下划线
            if other_char in revealed_letters:
                # other_char处在revealed_letters里面，这不可能
                return False

    # 循环完整运行
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    matched_words = []
    # 需要一个空列表来储存匹配的单词
    for i in wordlist:
        if match_with_gaps(my_word, i):
            matched_words.append(i)

    # 检查列表matched_words是否为空
    if len(matched_words) == 0:
        # 列表为空
        print("No matches found.")
    else:
        # 列表不为空，有匹配单词
        result_string = ' '.join(matched_words)
        print(result_string)


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    vowels = "aeiou"

    print("Welcome to the game, Hangman!")
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f"You have {warnings_remaining} warnings left.")

    # --- 主游戏循环 ---
    while guesses_remaining > 0:
        # 检查是否胜利
        if is_word_guessed(secret_word, letters_guessed):
            break  # 游戏结束

        # 打印本轮状态
        print("-------------")
        print(f"You have {guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")

        # 1. 获取用户输入

        # 2. 验证输入（是不是字母？是否猜过？）

        # 3. 处理无效输入（扣除警告或猜测次数）

        # 4. 处理有效输入（检查字母是否在 secret_word 中）

        # 5. 处理猜对的情况 (显示 get_guessed_word)

        # 6. 处理猜错的情况 (扣除猜测次数)
        guess = input("Please guess a letter: ")

        if guess == '*':
            # 如果是星号，你该做什么？
            # 你刚刚写了一个函数来做这件事。
            # 调用它。
            current_guess_words = get_guessed_word(secret_word, letters_guessed)
            show_possible_matches(current_guess_words)

            # 别忘了 'continue'，因为这一轮不需要再做别的了
            continue
        # --- 新逻辑结束 ---

        if not guess.isalpha():
            # 处理惩罚
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print(
                    f"Oops! That is not a valid letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
            else:
                guesses_remaining -= 1
                print(
                    f"Oops! That is not a valid letter. You have {guesses_remaining} guesses left: {get_guessed_word(secret_word, letters_guessed)}")
            continue
        else:
            guess = guess.lower()
            if guess in letters_guessed:
                # 处理惩罚
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print(
                        f"Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                else:
                    guesses_remaining -= 1
                    print(
                        f"Oops!You've already guessed that letter. You have {guesses_remaining} guesses left: {get_guessed_word(secret_word, letters_guessed)}")
                continue
            else:
                letters_guessed.append(guess)

        if guess not in secret_word:
            print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
            if guess in vowels:
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1

        else:
            print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
        # --- 在这里添加你的游戏结束逻辑 ---
    if is_word_guessed(secret_word, letters_guessed):
        # 玩家胜利
        print("Congratulations, you won!")
        unique_letters = set(secret_word)
        scores = len(unique_letters) * guesses_remaining
        print(f'Your total score for this game is: {scores}')
    else:
        # 玩家失败
        print("Sorry, you ran out of guesses.")
        print(f"The word was {secret_word}.")


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
