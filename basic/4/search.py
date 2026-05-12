import os
from serpapi import SerpApiClient
from dotenv import load_dotenv

class Search:
  """
  一个基于SerpApi的实战网页搜索引擎工具。
  它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
  """
  def __init__(self, apiKey:str = None):
    self.apikey = apiKey or os.get_env("SERPAPI_API_KEY")

    if not self.apikey:
      raise ValueError(f"serpapi apikey缺失")
    
    self. params = {
      "engine": "google",
      "api_key": self.apikey,
      "gl": "cn",  # 国家代码
      "hl": "zh-cn", # 语言代码
    }
  

  def search(self, query: str, params = None):
    try:
      _params = {}
      if params:
        _params = params
        _params.q = query
      else:
        _params = self.params
        _params.q = query

      client = SerpApiClient(_params)
      results = client.get_dict()

      # 智能解析:优先寻找最直接的答案
      if "answer_box_list" in results:
          return "\n".join(results["answer_box_list"])
      if "answer_box" in results and "answer" in results["answer_box"]:
          return results["answer_box"]["answer"]
      if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
          return results["knowledge_graph"]["description"]
      if "organic_results" in results and results["organic_results"]:
          # 如果没有直接答案，则返回前三个有机结果的摘要
          snippets = [
              f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
              for i, res in enumerate(results["organic_results"][:3])
          ]
          return "\n\n".join(snippets)
      
      return f"对不起，没有找到关于 '{query}' 的信息。"
    except Exception as e:
       return f"搜索时发生错误: {e}"