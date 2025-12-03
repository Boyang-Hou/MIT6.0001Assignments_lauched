# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
from pytz import timezone


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.lindex = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.lindex
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS



# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):

    # 1. 调用父类 Trigger 的初始化方法 (继承的规矩)
        super().__init__()
    # 2. 清洗传入的 phrase
    #    调用你下面写的 clean_text 方法处理 phrase
    #    将处理后的结果存入 self.cleaned_phrase
        self.cleaned_phrase = self.clean_text(phrase)
    def clean_text(self, text):
        """
        工具方法：将文本标准化。
        输入：原始字符串 (如 "The-Microsoft's!")
        输出：无标点、单空格分隔的小写字符串 (如 "the microsoft s")
        """
        # 第一步：大小写标准化
        #    将 text 里的所有字符转为小写
        text = text.lower()
        # 第二步：消灭标点符号
        #    遍历 string.punctuation 中的每一个符号：
        #        将 text 中的 该符号 替换为 空格 (注意：是空格，不是删除)
        for char in string.punctuation:
            text = text.replace(char, " ")
        # 第三步：处理多余空格并重组
        #    (目标：把 "a   b" 变成 "a b")
        #    利用字符串分割方法，将 text 切分成 单词列表 (自动丢弃多余空白)
        #    将 单词列表 重新拼接成 字符串，使用 单个空格 作为连接符
        word_list = text.split()
        text = ' '.join(word_list)
        # 第四步：返回结果
        #    返回最终处理好的字符串
        return text

    def is_phrase_in(self, text):
        """
        核心逻辑：判断 text 是否包含 self.cleaned_phrase
        """
        # 1. 清洗输入
        #    调用 clean_text 方法处理传入的 text (新闻标题)
        #    得到 cleaned_title
        cleaned_title = self.clean_text(text)

        # 2. 边界增强 (防止部分匹配)
        #    (目标：防止 "soft" 匹配到 "microsoft")
        #    在 self.cleaned_phrase 的 头部 和 尾部 各添加一个空格
        #    在 cleaned_title 的 头部 和 尾部 各添加一个空格
        spaced_cleaned_phrase = ' ' + self.cleaned_phrase + ' '
        spaced_cleaned_title = ' ' + cleaned_title + ' '
        # 3. 精确匹配
        #    判断 变形后的短语 是否 包含在 变形后的标题 中
        #    返回 判断结果 (True/False)
        if spaced_cleaned_phrase in spaced_cleaned_title:
            return True
        else:
            return False

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    # 不需要写 __init__，直接继承 PhraseTrigger 的

    def evaluate(self, story):
        # 1. 获取标题
        #    title = story.get_title()
        title = story.get_title()
        # 2. 核心判断
        #    调用 self.is_phrase_in(title)
        #    返回结果
        return self.is_phrase_in(title)#返回值为True or False

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):

    def evaluate(self, story):
        description = story.get_description()
        return self.is_phrase_in(description)#返回值为True or False
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
# 确保文件头部导入了: from datetime import datetime
# 确保文件头部导入了: import pytz

class TimeTrigger(Trigger):
    def __init__(self, time_string):
        # 1. 父类初始化
        super().__init__()
        self.time_string = time_string

        # 2. 格式字符串 (必须在 __init__ 里面)
        format_string = "%d %b %Y %H:%M:%S"
        # 3. 转换 (必须在 __init__ 里面)
        naive_time_obj = datetime.strptime(self.time_string, format_string)

        # 4. 加时区 (必须在 __init__ 里面)
        self.trigger_time = naive_time_obj.replace(tzinfo=pytz.timezone("EST"))

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
# 1. 获取新闻时间
#    调用 story 的方法获取 pubdate
        story_pubdate = story.get_pubdate()
# 2. 时区对齐 (Sanitization)
        #    如果它是 Naive 的 (tzinfo 为空)，强行给它穿上 EST 的马甲
        if story_pubdate.tzinfo is None:
            # 注意：replace 不会修改原对象，它返回一个新的对象
            # 所以你必须把结果重新赋值给 story_pubdate
            story_pubdate = story_pubdate.replace(tzinfo=pytz.timezone("EST"))
# 3. 执行比较
#    BeforeTrigger: 判断 story_pubdate 是否 < self.trigger_time
#    (AfterTrigger 则是 > )
#    返回 True 或 False
# COMPOSITE TRIGGERS
        return story_pubdate < self.trigger_time


class AfterTrigger(TimeTrigger):
    # 1.
    #    调用 story 的方法获取 pubdate
    def evaluate(self, story):
        story_pubdate = story.get_pubdate()
        # 2. 时区对齐 (Sanitization)
        #    如果它是 Naive 的 (tzinfo 为空)，强行给它穿上 EST 的马甲
        if story_pubdate.tzinfo is None:
            # 注意：replace 不会修改原对象，它返回一个新的对象
            # 所以你必须把结果重新赋值给 story_pubdate
            story_pubdate = story_pubdate.replace(tzinfo=pytz.timezone("EST"))
        # 3. 执行比较
        #    BeforeTrigger: 判断 story_pubdate 是否 > self.trigger_time
        #    (AfterTrigger 则是 > )
        #    返回 True 或 False
        # COMPOSITE TRIGGERS
        return story_pubdate > self.trigger_time

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        #super().__init__()
        self.t = trigger

    def evaluate(self, story):
        return not self.t.evaluate(story)
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        #super().__init__()
        self.t1 = trigger1
        self.t2 = trigger2
    #实现and逻辑:二者同时为真，结果为真
    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        #super().__init__()
        self.t1 = trigger1
        self.t2 = trigger2
    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    输入:
        stories (list of NewsStory): 原始新闻列表
        triggerlist (list of Trigger): 你的触发器军团
    输出:
        list of NewsStory: 只有那些被触发器选中的新闻
    """
    # 1. 准备一个空列表，用来存“被选中的新闻”
    #    filtered = []
    filtered_stories = []

    # 2. 外层循环：遍历每一篇新闻 (story in stories)
    for story in stories:
    # 3. 内层循环：遍历每一个触发器 (trigger in triggerlist)
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
    # 4. 核心判断：
    #    如果 这个触发器.evaluate(这篇新闻) 是 True:
    #        把这篇新闻加入 filtered 列表
    #        break (关键！只要有一个触发器选中了，就不用问别的触发器了，防止重复添加)

    # 5. 返回 filtered 列表
    return filtered_stories



#======================
# User-Specified Triggers
#======================
# TODO: Problem 11
# line is the list of lines that you need to parse and for which you need
# to build triggers
def read_trigger_config(filename):
    """
        filename: the name of a trigger configuration file

        Returns: a list of trigger objects specified by the trigger configuration
            file.
        """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    # 1. 打开文件并读取行 (Skeleton 代码已经帮你做好了，lines 列表里是干净的字符串)
    # ... (保留原有的读取代码) ...
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)


    # 2. 初始化一个仓库 (字典)
    trigger_map = {}
    # 3. 初始化一个最终列表 (用来存 ADD 指令指定的触发器)
    triggers = []

    # 4. 遍历每一行 (line in lines)
    # A. 切分
    #    用逗号 ',' 分割字符串 -> 得到 parts 列表
    #    例如: ['t1', 'TITLE', 'election'] 或 ['ADD', 't5', 't6']
    for line in lines:
        parts = line.strip().split(',')
        # B. 判断类型
        #这是指令行！
        if parts[0] == 'ADD':#如果 parts[0] 是 'ADD':
            for trigger_name in parts[1:]:
                trigger_name = trigger_name.strip()#清洗数据triggername
                if trigger_name in trigger_map:
                    triggers.append(trigger_map[trigger_name])

        else:#否则 (它是定义行):
            name = parts[0]#提取名字: name = parts[0]
            type = parts[1]#提取类型: type = parts[1]
            args = parts[2:]#提取参数: args = parts[2:] (剩下的都是参数)

            trigger = None  # 临时变量，用来存新造出来的对象

            if type == "TITLE":
                trigger = TitleTrigger(args[0])

            elif type == "DESCRIPTION":
                trigger = DescriptionTrigger(args[0])

            elif type == "AFTER":
                trigger = AfterTrigger(args[0])

            elif type == "BEFORE":
                trigger = BeforeTrigger(args[0])

            elif type == 'NOT':
                # 难点：NOT 需要一个现成的触发器对象作为原料
                # args[0] 是名字 't1'，我们要去仓库 trigger_map 里拿对象
                trigger = NotTrigger(trigger_map[args[0]])

            elif type == "AND":
                trigger = AndTrigger(trigger_map[args[0]], trigger_map[args[1]])

            elif type == "OR":
                trigger = OrTrigger(trigger_map[args[0]], trigger_map[args[1]])

            if trigger:
                trigger_map[name] = trigger

    return triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        '''
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
        '''
        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')



        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
    # --- 加上你的临时测试 ---

