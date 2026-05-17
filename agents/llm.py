
from langchain_core.language_models import BaseChatModel
from config import settings


def get_llm(
    temperature: float | None = None,
    streaming: bool = False,
) -> BaseChatModel:
   
    temp = temperature if temperature is not None else settings.llm_temperature

    if settings.llm_provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=settings.llm_model,
            temperature=temp,
            streaming=streaming,
            api_key=settings.groq_api_key,
        )

    elif settings.llm_provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.llm_model,
            temperature=temp,
            streaming=streaming,
            api_key=settings.openai_api_key,
        )

    else:
        raise ValueError(
            f"Unknown LLM provider: '{settings.llm_provider}'. "
            "Set LLM_PROVIDER=groq or LLM_PROVIDER=openai in .env"
        )
