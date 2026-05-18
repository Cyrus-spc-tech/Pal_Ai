

from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from agents.llm import get_llm
from database import (
    save_message,
    get_session_messages,
    clear_session as db_clear_session,
)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "dr_pal_system.txt"


def _load_system_prompt() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8").strip()
    
    return (
        "You are Dr. Pal, a professional health advisor. "
        "Talk like a Gen-z so person take intrese in talking "
        "Ask about the user's full day — sleep, food, exercise, "
        "study, and activities — then give detailed, evidence-based advice."
        "use the same language the prompt is give like if english then english"
    )


def _get_session_history(session_id: str) -> BaseChatMessageHistory:

    history = ChatMessageHistory()
    messages = get_session_messages(session_id)
    
    for msg in messages:
        if msg["role"] == "human":
            history.add_user_message(msg["content"])
        elif msg["role"] == "ai":
            history.add_ai_message(msg["content"])
    
    return history


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

    def chat(self, user_message: str) -> str:
        # Save user message to database
        save_message(self.session_id, "human", user_message)
        
        response = self.chain.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": self.session_id}},
        )
        
        # Save AI response to database
        save_message(self.session_id, "ai", response)
        
        return response

    def get_history(self) -> list[dict]:
        return get_session_messages(self.session_id)

    def clear_session(self) -> None:
        db_clear_session(self.session_id)

    @property
    def message_count(self) -> int:
        messages = get_session_messages(self.session_id)
        return len(messages)

    def __repr__(self) -> str:
        return f"DrPal(session_id={self.session_id!r}, messages={self.message_count})"
