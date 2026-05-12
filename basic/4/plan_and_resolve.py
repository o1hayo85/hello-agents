from llm_client import LlmClient
import ast

PLAN_PROMPT_TEMPLATE = """
你是一名顶级AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的步骤都是一个独立的、可执行的子任务，并且步骤严格按照逻辑顺序排列。
你输出的内容必须是一个python的列表，其中每一个子元素都是描述子任务的字符串。

问题：{question}
请严格按照以下格式输出你的计划，```python与```作为前后缀是必要的：
```python
  ["子任务1", "子任务2", "子任务3",...]
```
"""


class PlanAgent:
    def __init__(self, llm_agent: LlmClient) -> None:
        self.llm_agent = llm_agent

    def run(self, question: str):
        prompt = PLAN_PROMPT_TEMPLATE.format(question=question)
        message = [{"role": "user", "content": prompt}]

        print("生成计划中...")
        response_text = self.llm_agent.think(message)
        print(f"✅ 计划已生成:\n{response_text}")

        try:
            if "```python" in response_text:
                plan_str = response_text.split("```python")[1].split("```")[0].strip()
            else:
                plan_str = response_text.strip()
            plan = ast.literal_eval(plan_str)

            return plan if isinstance(plan, list) else []
        except Exception as e:
            print(f"解析响应发生错误 {e}，原始响应：{response_text}")
            return []


RESOLVE_PROMPT_TEMPLATE = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决“当前步骤”，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对“当前步骤”的回答:
"""


class ResolveAgent:
    def __init__(self, llm_agent: LlmClient) -> None:
        self.llm_agent = llm_agent

    def run(self, question: str, plan: list[str]):
        history = []
        final_answer = ""
        for i, step in enumerate(plan, start=1):
            print(f"\n-> 正在执行步骤 {i}/{len(plan)}: {step}")
            prompt = RESOLVE_PROMPT_TEMPLATE.format(
                question=question,
                plan=plan,
                history="\n".join(history),
                current_step=step,
            )
            message = [{"role": "user", "content": prompt}]
            response_text = self.llm_agent.think(messages=message) or ""
            history.append(f"步骤 {i}: {step}\n结果: {response_text}")
            final_answer = response_text

        return final_answer


class PlanAndResolveAgent:
    def __init__(self, llm_client: LlmClient) -> None:
        self.llm_client = llm_client
        self.plan_agent = PlanAgent(self.llm_client)
        self.resolve_agent = ResolveAgent(self.llm_client)

    def run(self, question: str):
        plan = self.plan_agent.run(question)
        if not len(plan):
            print("未生成有效的任务计划")
            return
        print(f"已生成计划 {plan}")

        answer = self.resolve_agent.run(question=question, plan=plan)
        print(f"最终生成答案：{answer}")
        return answer


if __name__ == "__main__":
    llm_client = LlmClient()
    plan_and_resolve_agent = PlanAndResolveAgent(llm_client)
    question = "把一头大象塞进冰箱需要几步？"

    plan_and_resolve_agent.run(question)
