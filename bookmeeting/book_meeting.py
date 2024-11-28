from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from make_request import create_teams_meetings

llm = ChatOpenAI()
prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="""You are an assistant designed to help users book a meeting on Microsoft Teams.
    Give them the link to the meeting and rewrite the user for the meeting details such as:
    - Subject of the meeting
    - Start date and time
    - End date and time
    - Attendees' emails
Schedule the meeting by calling the `create_teams_meeting` function.

User query: {user_query}
""",
)

chain = LLMChain(prompt=prompt_template, llm=llm)


def book_meeting(user_input):
    response = chain.run(user_input)

    if "book a meeting" in user_input.lower():
        return create_teams_meetings(user_input)
    else:
        return response
