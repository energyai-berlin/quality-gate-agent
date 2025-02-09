from datetime import timedelta
from typing import List
from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log

from src.utils.utils import update_table
from src.utils.utils import parse_json_string

with import_functions():
    from src.functions.llm_chat import llm_chat, LlmChatInput, Message


class MessageEvent(BaseModel):
    content: str


class EndEvent(BaseModel):
    end: bool

class ConfirmEvent(BaseModel):
    confirm: bool


@agent.defn()
class QGAgent:
    def __init__(self) -> None:
        self.end = False
        self.messages = [Message(
                    role="system",
                    content=""" You are an AI assistant that fills missing data with the context of the rest of the data. 
                    You receive a table name and a json with data. Return the json data with the nulls filled in and the table name. 
                    output: {{table_name:line , data: {lenght:10}}}""",
                )]
        self.data = {}
        self.table_name = ""

    @agent.event
    async def message(self, message: MessageEvent):
        try:
            log.info(f"Received message: {message.content}")
        

            self.messages.append(Message(role="user", content=message.content or ""))

            completion = await agent.step(
                llm_chat,
                LlmChatInput(messages=self.messages),
                start_to_close_timeout=timedelta(seconds=120),
            )
            log.info(f"Completion: {completion.choices[0].message.content}")

            completion_dict = parse_json_string(completion.choices[0].message.content)
            print(completion_dict)
            log.info(f"Completion_dict: {completion_dict}")
            self.table_name = completion_dict["table_name"]
            self.data = completion_dict["data"]

            return completion.choices[0].message.content
        except Exception as e:
            log.error(f"Error during message event: {e}")
            raise e

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return {"end": True}
    

    @agent.event
    async def confirmation(self, confirm: ConfirmEvent) -> ConfirmEvent:
        log.info("Confirmation received")
        update_table(self.table_name, self.data)
        log.info("Data updated")
        self.table_name = ""
        self.data = {}
        return {"confirm": True}


    @agent.run
    async def run(self, input: dict):
        await agent.condition(lambda: self.end)
        return
