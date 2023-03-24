from typing import Optional

from .state import MessageBodyParseState, MessageIdParseState, FromParseState, ReplyToParseState, \
    ParseState
from .tokens import Token, MessageIdToken, FromToken, ReplyToToken, MessageBodyToken


def data_to_tokenized_text(
        message_id: str,
        author: str,
        text: Optional[str] = None,
        reply_to_message: Optional[str] = None
) -> str:
    tokens: list[Token] = [MessageIdToken(message_id), FromToken(author)]

    if reply_to_message is not None:
        tokens.append(ReplyToToken(reply_to_message))

    if text is not None:
        tokens.append(MessageBodyToken(text))

    return '\n'.join(
        (*map(lambda x: x.serialize(), tokens),)
    )


class TextToTokenSeqParser:
    def __init__(self):
        self._last_resort_state = MessageBodyParseState()
        self._states = [MessageIdParseState(), FromParseState(), ReplyToParseState()]

    # Returns true if any of self.states returned True
    # Raises an Error if there are more than one state that returned True(Should not happen)
    def _has_any_wanted_states(self, line: str) -> bool:
        matched_count = 0
        for state_candidate in self._states:
            if state_candidate.is_my_state(line):
                matched_count += 1

        if matched_count > 1:
            raise RuntimeError(f'Too many states indicated that this line is theirs line: {line}')

        return matched_count == 1

    # Raises an Error if there are more than one state that returned True(Should not happen)
    def _check_state_ambiguity(self, line: str):
        matched_count = 0
        for state_candidate in self._states:
            if state_candidate.is_my_state(line):
                matched_count += 1

        if matched_count > 1:
            raise RuntimeError(f'Too many states indicated that this line is theirs line: {line}')

    def _get_wanted_state(self, line: str) -> ParseState:
        for state_candidate in self._states:
            if state_candidate.is_my_state(line):
                return state_candidate

        raise RuntimeError('None of parse states matched')

    def _get_wanted_state_or_last_resort(self, line: str) -> ParseState:
        for state_candidate in self._states:
            if state_candidate.is_my_state(line):
                return state_candidate

        raise self._last_resort_state

    def parse(self, text: str) -> list[Token]:
        current_state = None
        tokens: list[Token] = []
        for line in text.splitlines():
            self._check_state_ambiguity(line)
            line = line.strip()
            # Choice state if it does not exist
            # if current_state is None:
            #     current_state = self._get_wanted_state_or_last_resort(line)
            if self._has_any_wanted_states(line):
                if current_state is not None:
                    tokens.append(current_state.dump())
                current_state = self._get_wanted_state_or_last_resort(line)
            elif current_state is not self._last_resort_state:
                if current_state is not None:
                    tokens.append(current_state.dump())
                current_state = self._last_resort_state

            current_state.consume_line(line)
        if current_state is not None:
            tokens.append(current_state.dump())
        return tokens
