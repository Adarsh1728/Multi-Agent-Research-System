
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


def make_llm(api_key, model_name):
    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0.2
    )


def research_planner(llm, question):

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an expert Research Planning Agent.

            Break the user's research question into:
            1. Main research objectives
            2. Important sub-questions
            3. Information required
            4. Research steps

            Create a clear research plan.
            Do not write the final report.
            """
        ),
        ("human", "{question}")
    ])

    response = (prompt | llm).invoke({
        "question": question
    })

    return response.content


def evidence_analyst(llm, question, plan, evidence):

    evidence_text = "\n\n".join(
        [
            f"Source: {item['source']}\n{item['content']}"
            for item in evidence
        ]
    )

    if not evidence_text:
        evidence_text = "No uploaded documents were retrieved."

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an Evidence Analysis Agent.

            Analyse the retrieved research information.

            Your responsibilities:
            1. Identify important findings.
            2. Compare relevant information.
            3. Identify supporting evidence.
            4. Identify research gaps.
            5. Highlight limitations.

            Never invent evidence or citations.
            """
        ),
        (
            "human",
            """
            Research Question:
            {question}

            Research Plan:
            {plan}

            Retrieved Evidence:
            {evidence}

            Provide a structured evidence analysis.
            """
        )
    ])

    response = (prompt | llm).invoke({
        "question": question,
        "plan": plan,
        "evidence": evidence_text
    })

    return response.content


def report_writer(
    llm,
    question,
    plan,
    analysis,
    evidence
):

    sources = "\n".join([
        (
            f"- [Source {i}] {item['source']}"
            + (
                f", Page {item['page']}"
                if item.get("page")
                else ""
            )
        )
        for i, item in enumerate(evidence, start=1)
    ])

    if not sources:
        sources = "No uploaded sources retrieved."

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a Professional Research Report Writer.

            Generate a detailed research report using:

            1. Executive Summary
            2. Introduction
            3. Research Objectives
            4. Key Findings
            5. Detailed Analysis
            6. Limitations
            7. Conclusion
            8. References

            Use source citations such as [Source 1] only
            when supported by the retrieved evidence.

            Never fabricate references, statistics or URLs.
            Clearly distinguish general background from
            findings supported by uploaded documents.
            """
        ),
        (
            "human",
            """
            Research Question:
            {question}

            Research Plan:
            {plan}

            Evidence Analysis:
            {analysis}

            Available Sources:
            {sources}

            Generate the final report in Markdown.
            """
        )
    ])

    response = (prompt | llm).invoke({
        "question": question,
        "plan": plan,
        "analysis": analysis,
        "sources": sources
    })

    return response.content
