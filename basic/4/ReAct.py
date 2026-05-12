import re
from llm_client import LlmClient
from tools import ToolExecutor, search

REACT_PROMPT_TEMPLATE = """
请注意你是一个具有调用外部能力的智能助手。

可用工具如下：
{tools}

请严格按照以下格式回复：
Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`：调用一个可用的工具。
- Finish[最终答案]：当你认为已经获得最终答案时。
- 当你搜集到足够的信息，能够回答用户问题时，你必须在`Action:`字段后使用 `Finish[最终答案]` 来输出最终答案。

现在，请开始解决以下问题：
Question: {question}
History: {history}
"""


class ReActAgent:
    def __init__(
        self, llm_client: LlmClient, tool_executor: ToolExecutor, max_steps: int = 5
    ):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        self.history = []
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"当前执行次数 {current_step}")

            tools = self.tool_executor.getAvailableTools()
            history = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools, question=question, history=history
            )

            llm_message = [{"role": "user", "content": prompt}]
            llm_response = self.llm_client.think(llm_message)

            if not llm_response:
                print("llm 没有有效输出")

            thought, action = self._parse_output(llm_response)
            if thought:
                print(f"🤔 思考: {thought}")
            if not action:
                print("没有有效的action输出，流程结束")
                break

            if action.startswith("Finish"):
                final_answer = self._parse_action_input(action)
                print(f"🎉 最终答案: {final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                self.history.append("Observation: 无效的Action格式，请检查。")
                continue
            tool_function = tool_executor.getTool(tool_name)

            observation = (
                tool_function(tool_input)
                if tool_function
                else f"错误：未找到名为 '{tool_name}' 的工具。"
            )
            print(f"👀 观察: {observation}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        print("已经达到最大执行次数，流程退出。")
        return None

    def _parse_output(self, output_str: str):
        thought_match = re.search(
            r"Thought:\s*(.*?)(?=\nAction:|$)", string=output_str, flags=re.DOTALL
        )
        action_match = re.search(
            r"(?m)^Action:\s*(.*?)$", string=output_str, flags=re.DOTALL
        )

        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None

        return thought, action

    def _parse_action(self, action: str):
        match = re.match(r"(\w+)\[(.*?)\]", action, re.DOTALL)
        return (match.group(1), match.group(2)) if match else (None, None)

    def _parse_action_input(self, action: str):
        match = re.match(r"\w+\[(.*)\]", action, re.DOTALL)
        return match.group(1) if match else ""


search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
search_name = "Search"

if __name__ == "__main__":
    llm_client = LlmClient()
    tool_executor = ToolExecutor()

    tool_executor.registerTool(search_name, search_desc, func=search)
    agent = ReActAgent(llm_client=llm_client, tool_executor=tool_executor, max_steps=5)

    agent.run("华为最新的手机是哪一款？它的主要卖点是什么？")
