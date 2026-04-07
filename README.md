# 简化版 ELIZA 聊天机器人

这是一个使用 Python 编写的简化版 ELIZA 聊天机器人项目。

## 项目功能

- 基于规则的 ELIZA 对话机制
- 新增工作、学习、爱好、年龄、压力、忙碌等对话规则
- 支持简单的上下文记忆
- 可以记住用户提到的姓名、年龄、职业、学习内容和爱好
- 提供命令行交互式聊天体验

## 运行环境

- Python 3

## 运行方法

```bash
python agent_char2.py
```

输入 `quit`、`exit` 或 `bye` 可以结束对话。

## 项目文件说明

- `agent_char2.py`：聊天机器人主程序
- `agent-char2.pyproj`：Visual Studio Python 项目文件
- `agent-char2.slnx`：解决方案文件

## 示例

```text
You: My name is Alice
Therapist: Nice to meet you, alice. How are you feeling today?

You: I work as a teacher
Therapist: How do you feel about working as teacher?
```
