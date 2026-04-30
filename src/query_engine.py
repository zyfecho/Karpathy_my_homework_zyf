from datetime import datetime
from openai import OpenAI

from src.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, WIKI_DIR, OUTPUT_DIR

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

SYSTEM_PROMPT = """你是一个基于个人知识库的AI助手。
你拥有以下知识库的全部内容（由用户提供的Markdown文件组成）。
请仅基于这些材料回答问题，如果知识库中没有相关信息，请明确说明。
回答时引用具体文件来源，格式为：(来源: 文件名.md)"""


class KarpathyKnowledgeBase:
    def __init__(self):
        self.context = self._load_wiki()
        self.chat_history: list[dict] = []

    def _load_wiki(self) -> str:
        parts = []
        for md in sorted(WIKI_DIR.glob("*.md")):
            content = md.read_text(encoding="utf-8")
            parts.append(f"\n---\nFILE: {md.name}\n---\n{content}")
        return "\n".join(parts)

    def _build_messages(self, question: str) -> list[dict]:
        system = SYSTEM_PROMPT + "\n\n知识库内容：\n" + self.context
        messages = [{"role": "system", "content": system}]
        messages.extend(self.chat_history)
        messages.append({"role": "user", "content": question})
        return messages

    def query(self, question: str) -> str:
        messages = self._build_messages(question)
        try:
            resp = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=4000,
                temperature=0.3,
            )
            if isinstance(resp, str):
                answer = resp
            else:
                answer = resp.choices[0].message.content
        except Exception as e:
            answer = f"[API调用失败] {e}"
        self.chat_history.append({"role": "user", "content": question})
        self.chat_history.append({"role": "assistant", "content": answer})
        return answer

    def save_session(self):
        if not self.chat_history:
            return None
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        path = OUTPUT_DIR / f"{ts}.md"
        lines = [f"# 问答记录 {ts}\n"]
        for msg in self.chat_history:
            role = "Q" if msg["role"] == "user" else "A"
            lines.append(f"\n## {role}\n\n{msg['content']}\n")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def reset(self):
        self.chat_history = []
