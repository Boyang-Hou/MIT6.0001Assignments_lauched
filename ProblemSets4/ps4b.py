# Problem Set 4B
# Name: Boyang Hou
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        #delete this line and replace with your code here
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        #delete this line and replace with your code here
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''

        self.copy_valid_words = self.valid_words.copy()
        return self.copy_valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        #delete this line and replace with your code here
        # 初始化一个空字典
        shift_dict = {}

        # 第一轮：处理小写字母
        # 我们需要从 "abc...z" 里一个一个拿字母
        for letter in string.ascii_lowercase:
            # 现在 letter 是 'a'
            # 1. 找到 'a' 在字母表里的位置（索引 index）
            #    'a' 是第 0 个，'b' 是第 1 个...
            current_index = string.ascii_lowercase.find(letter) #(Python 里怎么找一个字符在字符串中的位置？提示：.find 或.index)

            # 2. 计算新位置 (你已经答对了公式！)
            #    比如 shift 是 1，current_index 是 0
            #    new_index = (0 + 1) % 26 = 1
            new_index = (current_index + shift) % 26

            # 3. 根据新位置，找回新的字母
            #    第 1 个字母是谁？是 'b'
            #    我们去 string.ascii_lowercase 里把第 new_index 号取出来
            new_letter = string.ascii_lowercase[new_index]

            # 4. 存入字典
            #    键(Key)是原来的 letter ('a')
            #    值(Value)是新的 new_letter ('b')
            shift_dict[letter] = new_letter

        for letter in string.ascii_uppercase:
            current_index = string.ascii_uppercase.find(letter)

            #计算新位置
            new_index = (current_index + shift) % 26
            # 3. 根据新位置，找回新的字母
            new_letter = string.ascii_uppercase[new_index]
            # 4. 存入字典
            shift_dict[letter] = new_letter

        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        #创建空列表来储存加密的结果。
        encrypto_message = []
        for char in self.message_text:
            #如果字符char在里self.message_text(字母), 转为加密形式
            if char in shift_dict:
                encrypto_message.append(shift_dict[char])
            else:#不在(标点符号空格)，保留原形式
                encrypto_message.append(char)
        #最后要返回string的呀
        return "".join(encrypto_message)



class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        super().__init__(text)#继承父类, 这一行跑完，你的 self 上就已经有了 self.message_text 和 self.valid_words
        self.shift = shift#自己初始化第三个属性 (shift)
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)



class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        super().__init__(text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        #1. 初始化数据
        #当前最高分
        max_score = 0
        #当前的冠军shift
        best_shift = 0
        # 目前的冠军解密文本
        best_text = ""

        #开始循环擂台赛
        for s in range(26):
            #1. 解密
            # 但在这里，我们可以简单地把 s 从 0 循环到 26，直接看哪个 s 能解出明文。
            decrypted_text = self.apply_shift(s)

            #2. 切割
            plaintext_list = decrypted_text.split(' ')
            #3. 鉴定与统计
            valid_count = 0 #初试分数为0

            for word in plaintext_list: #遍历列表中每一个词
                if is_word(self.valid_words, word):
                    valid_count += 1

            if valid_count > max_score:
                max_score = valid_count
                best_text = decrypted_text
                best_shift = s

        return (best_shift, best_text)



if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
 #   print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE
#1. 获取数据源input
    story_text = get_story_string()
#   or
#    story_text = open('story.txt').read()
#2. 创建一个CiphertextMessage实例
    cipher_text_message = CiphertextMessage(story_text)
#3. 执行破解Execution
    result = cipher_text_message.decrypt_message()
#4. Output
    print("--------------------------------------------------")
    print("Story Decoded!")
    print("Best Shift Used:", result[0])
    print("Decrypted Story:\n", result[1])
    print("--------------------------------------------------")
    #TODO: best shift value and unencrypted story 

