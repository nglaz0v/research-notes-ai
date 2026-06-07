from providers.factory import get_provider
from prompts import get_prompt
from knowledge_base import get_formulations


async def summarize_article(
    article_text: str,
    article_type: str = "default",
    discipline: str | None = None,
) -> str:
    """Main orchestrator: send article to LLM and return the summary.

    Args:
        article_text: The full text of the article to summarize.
        article_type: One of 'review', 'experimental', 'theoretical', 'default'.
        discipline: Optional discipline for KB-aware prompting.

    Returns:
        Structured summary with introduction, methods, results, conclusions,
        and self-check questions.
    """
    system_prompt = get_prompt(article_type)

    kb_context = ""
    if discipline:
        formulations = get_formulations(domain=discipline)
        if formulations:
            kb_context = "\nДоступные формулировки для использования:\n"
            for fmt in formulations[:5]:
                kb_context += f"- {fmt['formulation']} ({fmt['use_case']})\n"

    user_message = f"Проанализируй следующую статью и составь конспект согласно инструкции:\n\n{article_text}"
    if kb_context:
        user_message = kb_context + "\n\n" + user_message

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    provider = get_provider()
    result = await provider.generate(messages)
    return result
