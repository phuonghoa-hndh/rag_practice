import os

from langchain.agents import initialize_agent
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_groq import ChatGroq

from finance_bot.tools import (company_financials, company_information,
                               get_growth_metrics,
                               last_dividend_and_earnings_date,
                               stock_grade_updrages_downgrades, stock_news,
                               stock_splits_history,
                               summary_of_institutional_holders,
                               summary_of_mutual_fund_holders)

groq_api_key = os.environ.get("GROQ_API_KEY")


def define_agent():
    """
    Define the finance agent using AzureChatOpenAI
    :return:
    """
    tools = [
        company_financials,
        company_information,
        get_growth_metrics,
        last_dividend_and_earnings_date,
        stock_grade_updrages_downgrades,
        stock_news,
        stock_splits_history,
        summary_of_institutional_holders,
        summary_of_mutual_fund_holders,
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                """You are a helpful financial specialist.
                Give them the precision, easy to understand answer.
                Try to answer user query using available tools.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.""",
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm = ChatGroq(api_key=groq_api_key, model="llama3-8b-8192", temperature=0)

    finance_agent = initialize_agent(
        tools=tools, llm=llm, agent_kwargs={"prompt": prompt}
    )

    return finance_agent
