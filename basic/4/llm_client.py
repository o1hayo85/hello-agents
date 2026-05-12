import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()


class LlmClient:
    """
    为当前项目定制的LLM客户端。
    它用于调用任何兼容OpenAI接口的服务，并默认使用流式响应。
    """

    def __init__(
        self,
        apiKey: str = None,
        mode: str = None,
        baseUrl: str = None,
        timeout: int = None,
    ):
        self.apiKey = apiKey or os.getenv("LLM_API_KEY")
        self.mode = mode or os.getenv("LLM_MODEL_ID")
        self.baseUrl = baseUrl or os.getenv("LLM_BASE_URL")

        if not all([self.apiKey, self.baseUrl, self.mode]):
            raise ValueError("参数缺失")

        self.client = OpenAI(
            api_key=self.apiKey, base_url=self.baseUrl, timeout=timeout or 120
        )

    def think(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        print(f"正在调用模型 {self.mode} 进行思考")

        try:
            response = self.client.chat.completions.create(
                model=self.mode, messages=messages, temperature=temperature, stream=True
            )

            # 处理流式响应
            collected_content = []
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content or ""
                # print(content, end="", flush=True)
                collected_content.append(content)

            print()
            return "".join(collected_content)

        except Exception as e:
            print(f"调用llm api时发生错误 - {e}")
            return None


if __name__ == "__main__":
    try:
        llmAgent = LlmClient()
        exampleMessages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that writes Python code.",
            },
            {"role": "user", "content": "写一个快速排序算法"},
        ]

        print("--调用llm--")
        responseText = llmAgent.think(exampleMessages)
        if responseText:
            print("--大模型输出--")
            print(responseText)

    except Exception as e:
        print(e)
