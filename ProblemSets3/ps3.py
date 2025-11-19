# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
     # TO DO... Remove this line when you implement this function
    #组件1: Clean & Wash the Data
    word = str.lower(word)
    if not word:
        return 0

    #组件2: Compute component 1 " first_component"
    first_component= 0
    for char in word:
        #.get()得到字典型数据里面key对应的value
        score = SCRABBLE_LETTER_VALUES.get(char,0)
        #如果word里面包含通配符'*', 程序SCRABBLE_LETTER_VALUES会因搜索不到'*' 返回0值
        first_component += score

    #组件3: Compute component 2 "second_componet"
    word_length = len(word)
    formula = 7 * word_length - 3 * (n - word_length) #int
    second_componet = max(1, formula)

    final_score = first_component * second_componet
    return final_score

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3)) #int, 整数形式
    hand["*"] = 1

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

      # TO DO... Remove this line when you implement this function
    new_hand = hand.copy()
    word = str.lower(word)

    for letter in word:
        if letter in new_hand and new_hand[letter] > 0:
            new_hand[letter] -= 1

    return new_hand
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

     # TO DO... Remove this line when you implement this function
    lower_word = word.lower()
    # 检查1: 手牌是否足够
    word_freq = get_frequency_dict(lower_word)
    for letter, required_count in word_freq.items():
        if hand.get(letter, 0) < required_count:
            # 玩家手牌里面只要没有'*'或其他word需要的牌，就报错
            return False

    #判断单词内是否含通配符"*"
    #如果不含，则按照Problem3的逻辑
    #如果含，则按照Problem4逻辑，以单词内含有通配符的条件来写代码

    #lower_word doesn't contain '*':
    if "*" not in lower_word:
        #检查2: lower_word是否在字典word_list里面
        if lower_word not in word_list:
            return False

        #检查无误后return True
        return True
    #including *
    else:
        #检查2: 是否在字典中?
        #创建possible_words列表，初始化并且将5种可能性放在possible_words里
        possible_words = []
        for vowel in VOWELS: #VOWELS = 'aeiou'
            possible_words.append(lower_word.replace('*', vowel))

        #循环检查5个可能性，如果有一个通过就报对
        for p_word in possible_words:
            if p_word in word_list:
                #找到一个通过，就return True
                return True
        #如果程序运行完for loop遍历possible_words, p_word都没通过, 则报错
        return False







#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
      # TO DO... Remove this line when you implement this function
    sum_letters = sum(hand.values())
    return sum_letters

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    total_score = 0
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Display the hand
        print("Current Hand:", end='')
        display_hand(hand)
        # Ask user for input
        word= input("Enter word, or '!!' to indicate that you are finished:" )
        # If the input is two exclamation points:
        if word == '!!':
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                n = calculate_handlen(hand)
                points = get_word_score(word, n)
                print(word," earned ", points, "points")
                total_score += points
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("Invalid input. Please try again.")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)#update_hand(hand, word)返回new_hand, 而不是hand!

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print("Total score:", total_score)
    # Return the total score as result of function
    return total_score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
     # TO DO... Remove this line when you implement this function
    if letter not in hand:
        return hand.copy()

    all_letters = VOWELS + CONSONANTS
    available_letters = []

    #遍历all_letters中的每一个char,
    for char in all_letters:
        #if char 不在hand里面（合乎要求）
        if char not in hand:
            available_letters.append(char)

    #循环结束，输出一个不包含hand中原有字母的干净list
    #从列表available_letters里面随便选一个new_letter
    new_letter = random.choice(available_letters)

    new_hand = hand.copy()
    new_hand[new_letter] = hand[letter]

    del new_hand[letter]
    return new_hand

    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    # TO DO... Remove this line when you implement this function
    #1.询问用户玩几局, 并且存储为变量num_hands
    #如果用户输入其他无效值, 默认值num_hands为1
    try:
        num_hands = int(input('Enter total number of hands: '))
    except ValueError:
        print('Invalid input. Defaulting to 1 hand')
        num_hands = 1

    #2.初始化分数
    total_game_score = 0

    #3.初始化开关记录——重玩replay和换词substitue
    substitue_used = False
    replay_used = False

    #4.每轮游戏循环num_hands次
    for i in range(num_hands):

        #A.发牌
        hand = deal_hand(HAND_SIZE)
        #B. 显示手牌 (让用户看到他拿到了什么)
        print(f"\n{'='*10} Hand {i+1} of {num_hands} {'='*10}")
        #C.处理换牌 (Substitution)

        #如果还有换牌机会
        if not substitue_used:
            print('Current hand:' ,end=' ')
            display_hand(hand)
            #询问用户想不想换牌
            substitute_requirement = input("Would you like to substitute a letter?").lower()
            if substitute_requirement == 'yes':
                #询问用户换哪张牌
                letter = input("Which letter would you like to replace?").lower()
                #更新手牌
                hand = substitute_hand(hand, letter)
                #换牌机会用完，更换状态
                substitue_used = True

        #D.准备重玩的数据
          #这步很关键：play_hand 会消耗手牌。
          #为了能重玩，你必须在玩之前，把当前的 hand 备份一份！
        hand_backup = hand.copy()

        #E.第一轮游玩
        score1 = play_hand(hand, word_list)

        #F.处理重玩 (Replay)

        #如果还有重玩机会
        if not replay_used:
            print(f"\nHand score: {score1}")
            #询问用户是否重玩
            replay_requirement = input("Would you like to replay the hand?").lower()
            if replay_requirement == 'yes':
                #重玩特权已经使用, 进入第二轮游戏
                replay_used = True

                #再次游玩，注意要使用备份的初始手牌！
                #规则说重玩不能再换牌，所以直接玩
                score2 = play_hand(hand_backup, word_list)

                #取两轮游戏最高分
                score1 = max(score1, score2)

        #G.累加总分
        total_game_score += score1
    #5.游戏结束，打印并且返回total_game_score
    print("Total score over all hands: ", total_game_score)
    print('-'*20)
    return total_game_score
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    #hand = {'a': 1, 'j': 1, 'e': 1, 'f': 1, '*': 1, 'r': 1, 'x': 1}
    #play_hand(hand, word_list)
