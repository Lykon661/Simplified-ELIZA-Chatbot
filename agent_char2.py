import re
import random

# 定义规则库：正则表达式 -> 响应模板列表
rules = {
    r'My name is (.*)': [
        "Nice to meet you, {0}. How are you feeling today?",
        "Hello, {0}. What would you like to talk about today?"
    ],
    r'I am (\d+) years old': [
        "What has being {0} years old been like for you recently?",
        "How do you feel about this stage of life at {0}?"
    ],
    r'I work as (.*)': [
        "How do you feel about working as {0}?",
        "What is it like for you to work as {0}?"
    ],
    r'My job is (.*)': [
        "How satisfied are you with your job as {0}?",
        "What does being {0} mean to you?"
    ],
    r'I study (.*)': [
        "What is it like studying {0}?",
        "How do you feel about learning {0}?"
    ],
    r'I am studying (.*)': [
        "What has your experience studying {0} been like?",
        "What do you enjoy or find difficult about studying {0}?"
    ],
    r'I like (.*)': [
        "What do you enjoy most about {0}?",
        "How long have you liked {0}?"
    ],
    r'I enjoy (.*)': [
        "What does {0} bring to your life?",
        "What do you enjoy most about {0}?"
    ],
    r'I need (.*)': [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?"
    ],
    r'Why don\'t you (.*)\?': [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?"
    ],
    r'Why can\'t I (.*)\?': [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?"
    ],
    r'I am stressed(.*)': [
        "What do you think is causing that stress?",
        "When do you feel most stressed?"
    ],
    r'I am busy(.*)': [
        "What has been keeping you so busy?",
        "How does being busy affect you?"
    ],
    r'I am (.*)': [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?"
    ],
    r'.* mother .*': [
        "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?"
    ],
    r'.* father .*': [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?"
    ],
    r'.*': [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?"
    ]
}

# 定义代词转换规则
pronoun_swap = {
    "i": "you", "you": "i", "me": "you", "my": "your",
    "am": "are", "are": "am", "was": "were", "i'd": "you would",
    "i've": "you have", "i'll": "you will", "yours": "mine",
    "mine": "yours"
}


def swap_pronouns(phrase):
    """
    对输入短语中的代词进行第一/第二人称转换
    """
    words = phrase.lower().split()
    swapped_words = [pronoun_swap.get(word, word) for word in words]
    return " ".join(swapped_words)


def update_memory(user_input, memory):
    """
    从用户输入中提取关键信息并更新记忆
    """
    memory_patterns = {
        "name": [r'My name is (.*)'],
        "age": [r'I am (\d+) years old'],
        "job": [r'I work as (.*)', r'My job is (.*)', r'I am a[n]? (.*)'],
        "study": [r'I study (.*)', r'I am studying (.*)'],
        "hobby": [r'I like (.*)', r'I enjoy (.*)', r'My hobby is (.*)']
    }

    for key, patterns in memory_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                memory[key] = match.group(1).strip(" .!?")
                break


def memory_prefix(user_input, memory):
    """
    根据上下文记忆生成一个简短前缀
    """
    lowered = user_input.lower()

    if ("work" in lowered or "job" in lowered) and memory["job"]:
        if memory["name"]:
            return f"{memory['name']}, you mentioned that you work as {memory['job']}. "
        return f"You mentioned that your job is {memory['job']}. "

    if ("study" in lowered or "school" in lowered) and memory["study"]:
        if memory["name"]:
            return f"{memory['name']}, you said you study {memory['study']}. "
        return f"You said you study {memory['study']}. "

    if ("like" in lowered or "enjoy" in lowered or "hobby" in lowered) and memory["hobby"]:
        if memory["name"]:
            return f"{memory['name']}, you mentioned that you enjoy {memory['hobby']}. "
        return f"You mentioned that you enjoy {memory['hobby']}. "

    if memory["name"] and random.random() < 0.25:
        return f"{memory['name']}, "

    return ""


def respond(user_input, memory):
    """
    根据规则库和上下文记忆生成响应
    """
    prefix = memory_prefix(user_input, memory)

    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            captured_group = match.group(1) if match.groups() else ''
            swapped_group = swap_pronouns(captured_group)
            response = random.choice(responses).format(swapped_group)
            return prefix + response

    return prefix + random.choice(rules[r'.*'])


# 主聊天循环
if __name__ == '__main__':
    memory = {
        "name": None,
        "age": None,
        "job": None,
        "study": None,
        "hobby": None
    }

    print("Therapist: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Therapist: Goodbye. It was nice talking to you.")
            break

        update_memory(user_input, memory)
        response = respond(user_input, memory)
        print(f"Therapist: {response}")
