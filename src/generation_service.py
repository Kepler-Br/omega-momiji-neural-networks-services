import re
from typing import List

from config import NeuralNetworkConfig
from dto import GenerateTextRequest, GenerateTextResponse, GenerateMessageRequest, GenerateMessageResponse, \
    GeneratedMessages
from kobold import KoboldClient
from text_wrapper import TextPromptWrapper


message_prompt = """
Let's roleplay a bit

{}

We're chatting in a chat room with several other people. Only answer with what Mila would write. The message format as follows:
The ID is inside '[]', the ID the message is reply to is inside '{{}}', the username is inside '<>', the message body is after ':'
So, the message with ID of '444' that is a reply to a message with ID of '443', username 'SOMEUSER' and message body 'Hello world' would look like this:
[444] {{443}} <SOMEUSER>: Hello world
Here are the messages:

{}

Answer in the Russian language and without quotes. If you think that you should reply to a message, put the message's ID at the start of the message
""".strip()

character_description = """

""".strip()

class GenerationService:
    def __init__(
            self,
            kobold_client: KoboldClient,
            neural_network_config: NeuralNetworkConfig,
            text_prompt_wrapper: TextPromptWrapper
    ):
        self._kobold_client = kobold_client
        self._neural_network_config = neural_network_config
        self._text_prompt_wrapper = text_prompt_wrapper
        self._message_regex = re.compile(r'\[(\d+)] (\{(\d*)})? ?<(.*)>:(.*)')

    def _parse_llm_message(self, text: str) -> List[GeneratedMessages]:
        accumulated_text: str = ""
        reply_to: str = None
        username: str = None
        messages: List[GeneratedMessages] = []

        for line in text.splitlines():
            matched = self._message_regex.match(line)
            if matched is not None:
                if len(accumulated_text.strip()) != 0:
                    messages.append(
                        GeneratedMessages(
                            text=accumulated_text,
                            reply_to=reply_to
                        )
                    )
                reply_to = matched.group(3)
                username = matched.group(4)
                accumulated_text = matched.group(5)
                pass
            else:
                accumulated_text += '\n' + line
            pass
        if len(accumulated_text) != 0:
            messages.append(
                GeneratedMessages(
                    text=accumulated_text,
                    reply_to=reply_to
                )
            )

        return messages

    async def generate_text(self, request: GenerateTextRequest) -> GenerateTextResponse:
        generation_output = await self._kobold_client.generate(
            prompt=request.text,
            max_context_length=self._neural_network_config.context,
            max_length=request.max_length,
            stop_sequence=self._text_prompt_wrapper.get_stop_sequence(),
            temperature=self._neural_network_config.temperature
        )

        return GenerateTextResponse(
            text=generation_output.results[0].text,
            finish_reason=generation_output.results[0].finish_reason
        )

    async def generate_messages(self, request: GenerateMessageRequest) -> GenerateMessageResponse:
        mapped_messages = map(lambda x: f"[{x.id}] <{x.username}>: {x.text}", request.messages)

        prompt = message_prompt.format(character_description, '\n'.join(mapped_messages))

        text = self._text_prompt_wrapper.wrap(prompt)

        generation_output = await self._kobold_client.generate(
            prompt=text,
            max_context_length=self._neural_network_config.context,
            max_length=request.max_length,
            stop_sequence=self._text_prompt_wrapper.get_stop_sequence(),
            temperature=self._neural_network_config.temperature
        )

        print(generation_output.results[0].text)

        print("\n")

        return GenerateMessageResponse(
            messages=self._parse_llm_message(generation_output.results[0].text)
        )
