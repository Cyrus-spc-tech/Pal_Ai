

from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from agents.llm import get_llm

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "dr_pal_system.txt"


def _load_system_prompt() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8").strip()
    # Fallback inline prompt (should not happen in normal use)
    return (
        "You are Dr. Pal, a professional health advisor. "
        "Ask about the user's full day — sleep, food, exercise, mood, "
        "study, and activities — then give detailed, evidence-based advice."
    )


_session_store: dict[str, BaseChatMessageHistory] = {}


def _get_session_history(session_id: str) -> BaseChatMessageHistory:

    if session_id not in _session_store:
        _session_store[session_id] = ChatMessageHistory()
    return _session_store[session_id]


def build_dr_pal_chain():
   
    system_prompt = _load_system_prompt()
    llm = get_llm(streaming=False)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    base_chain = prompt | llm | StrOutputParser()

    chain_with_history = RunnableWithMessageHistory(
        base_chain,
        _get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    return chain_with_history

class DrPal:

    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.chain = build_dr_pal_chain()
        self._message_count = 0

    def chat(self, user_message: str) -> str:
        self._message_count += 1
        response = self.chain.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": self.session_id}},
        )
        return response

    def get_history(self) -> list[dict]:
      
        history = _get_session_history(self.session_id)
        return [
            {"role": msg.type, "content": msg.content}
            for msg in history.messages
        ]

    def clear_session(self) -> None:
     
        if self.session_id in _session_store:
            del _session_store[self.session_id]
        self._message_count = 0

    @property
    def message_count(self) -> int:
        return self._message_count

    def __repr__(self) -> str:
        return f"DrPal(session_id={self.session_id!r}, messages={self._message_count})"
