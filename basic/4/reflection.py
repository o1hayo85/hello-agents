from typing import Any, Dict, List


class Memory:
    """
    一个简单的短期记忆模块，用于存储智能体的行为和反思轨迹。
    """

    def __init__(self) -> None:
        self.memory_list: List[Dict[str, Any]] = []

    def append(self, type: str, content: str):
        """
        向记忆中添加一条新纪录。

        参数：
        - type: 记录的类型，execution或relfection
        - content: 记录的具体内容
        """
        record = {"type": type, "content": content}
        self.memory_list.append(record)
        print(f"📝记忆已更新，新增一条{type}记录")

    def get_trajectory(self):
        """
        将所有记忆记录格式化为一个连贯的字符串文本，用于构建提示词。
        """
        trajectory_parts = []

        for memory in self.memory_list:
            if memory["type"] == "execution":
                trajectory_parts.append(
                    f"--- 上一轮尝试 (代码) ---\n{memory['content']}"
                )
            elif memory["type"] == "reflection":
                trajectory_parts.append(f"--- 评审员反馈 ---\n{memory['content']}")
        return "\n\n".join(trajectory_parts)

    def get_last_executiont(self):
        """
        获取最近一次的执行结果 (例如，最新生成的代码)。
        如果不存在，则返回 None。
        """

        for memory in reversed(self.memory_list):
            if memory["type"] == "execution":
                return memory["content"]

        return None


INITIAL_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。请根据以下要求，编写一个Python函数。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。

要求: {task}

请直接输出代码，不要包含任何额外的解释。
"""

REFLECT_PROMPT_TEMPLATE = """
你是一位极其严格的代码评审专家和资深算法工程师，对代码的性能有极致的要求。
你的任务是审查以下Python代码，并专注于找出其在<strong>算法效率</strong>上的主要瓶颈。

# 原始任务:
{task}

# 待审查的代码:
```python
{code}
```

请分析该代码的时间复杂度，并思考是否存在一种<strong>算法上更优</strong>的解决方案来显著提升性能。
如果存在，请清晰地指出当前算法的不足，并提出具体的、可行的改进算法建议（例如，使用筛法替代试除法）。
如果代码在算法层面已经达到最优，才能回答“无需改进”。

请直接输出你的反馈，不要包含任何额外的解释。
"""

REFINE_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。你正在根据一位代码评审专家的反馈来优化你的代码。

# 原始任务:
{task}

# 你上一轮尝试的代码:
{last_code_attempt}
评审员的反馈：
{feedback}

请根据评审员的反馈，生成一个优化后的新版本代码。
你的代码必须包含完整的函数签名、文档字符串，并遵循PEP 8编码规范。
请直接输出优化后的代码，不要包含任何额外的解释。
"""


class ReflectionAgent:
    def __init__(self) -> None:
        pass

    def run(self):
        pass
