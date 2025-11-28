# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

     #delete this line and replace with your code here
    if len(sequence) == 1:
        return [sequence]

    else:
        #分别取第一个字符first_char和其余字符rest_char
        first_char = sequence[0:1]
        perms_of_rest = sequence[1:]

        #递归调用并且使用get_permutations(sequence)返回结果列表
        partial_permutations = get_permutations(perms_of_rest)

        # 1. 我们需要创建一个空列表来存最终结果，比如 result = []
        result = []
        # 2. 第一层循环：我们要处理 perms_of_rest 里的每一个单词
        for p in partial_permutations:  # p 会依次是 'ust', 'sut'...

            # 3. 第二层循环：对于当前的单词 p (比如 'ust')，
            # 我们要找到所有可以插入 'b' 的位置。
            # 'ust' 有 3 个字母，意味着有 4 个空隙可以插 (开头, u后, s后, t后)
            # 你的任务：写出这层循环的逻辑
            # (提示：使用 range() 和字符串切片 Slicing)
            for i in range(len(p) + 1):
                new_p = p[:i] + first_char + p[i:]
                result.append(new_p)

        return result




if __name__ == '__main__':
    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    #delete this line and replace with your code here

