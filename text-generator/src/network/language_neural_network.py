import logging
import time
from typing import Optional

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

from controller.model.history_generation_request import GenerationParams
from controller.model.message import Message
from message_tokenizer.to_message import map_tokens_to_messages
from message_tokenizer.tokenizer import TextToTokenSeqParser, data_to_tokenized_text
from network.language_neural_network_abstract import LanguageNeuralNetworkAbstract
from network.messages_to_prompt import messages_to_prompt
from util.message_id_mapper import MessageIdMapper


class LanguageNeuralNetwork(LanguageNeuralNetworkAbstract):
    def __init__(self, path: str, use_cpu: bool = False):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

        self.use_cpu = use_cpu
        self.log.debug('Loading model')
        self.log.debug('Loading tokenizer')
        self.tokenizer = GPT2Tokenizer.from_pretrained(path)
        self.log.debug('Loading model')
        self.model = GPT2LMHeadModel.from_pretrained(path)
        self.log.debug('Done')

        if not self.use_cpu:
            self.model = self.model.to('cuda')

    def _seed(self, seed: int):
        self.log.debug(f'Setting seed to {seed}')

        torch.manual_seed(seed)

    def generate(
            self,
            prompt: str,
            generation_params: GenerationParams,
            count: int = 1,
    ) -> list[str]:
        self.log.debug(
            f'Generating text:\n'
            f'Prompt: {prompt}\n'
            f'Count: {count}\n'
            f'Max new tokens: {generation_params.max_new_tokens}\n'
            f'Num beams: {generation_params.num_beams}\n'
            f'No repeat ngram size: {generation_params.no_repeat_ngram_size}\n'
            f'Repetition penalty: {generation_params.repetition_penalty}\n'
            f'Early stopping: {generation_params.early_stopping}\n'
            f'Seed: {generation_params.seed}\n'
            f'Top k: {generation_params.top_k}\n'
            f'Top p: {generation_params.top_p}\n'
            f'Temperature: {generation_params.temperature}\n'
            f'Bad words: {generation_params.bad_words}\n'
        )

        self._seed(generation_params.seed)

        encoded_bad_words: Optional[list[list[int]]] = None

        if generation_params.bad_words is not None and len(generation_params.bad_words) != 0:
            encoded_bad_words = []

            for word in generation_params.bad_words:
                encoded_bad_words.append(self.tokenizer.encode(word.strip()))

        tokenized = self.tokenizer(prompt, return_tensors="pt")
        tokenized_input_ids = tokenized.input_ids
        attention_mask = tokenized.attention_mask
        if not self.use_cpu:
            tokenized_input_ids = tokenized_input_ids.to('cuda')
            attention_mask = attention_mask.to('cuda')

        start_generation = time.time()

        out = self.model.generate(
            tokenized_input_ids,
            do_sample=True,
            attention_mask=attention_mask,
            max_new_tokens=generation_params.max_new_tokens,
            num_beams=generation_params.num_beams,
            no_repeat_ngram_size=generation_params.no_repeat_ngram_size,
            early_stopping=generation_params.early_stopping,
            num_return_sequences=count,
            top_k=generation_params.top_k,
            top_p=generation_params.top_p,
            temperature=generation_params.temperature,
            repetition_penalty=generation_params.repetition_penalty,
            bad_words_ids=encoded_bad_words
        )

        end_generation = time.time()

        ret = list(map(self.tokenizer.decode, out))

        del out
        del tokenized_input_ids
        del attention_mask
        del tokenized

        if not self.use_cpu:
            torch.cuda.empty_cache()

        self.log.debug(
            f'Generated in {end_generation - start_generation:.3} seconds:\n'
            f'Result: {ret}'
        )

        return ret

    def generate_messages(
            self,
            messages: list[Message],
            generation_params: GenerationParams,
            prompt_author: str,
            reply_to_id: Optional[str] = None,
            prompt: Optional[str] = None,
    ) -> list[Message]:
        mapper = MessageIdMapper()
        mapped = mapper.map_and_save_ids(messages)

        converted_messages = messages_to_prompt(mapped)
        prompt = data_to_tokenized_text(
            message_id=messages[-1].message_id,
            text=prompt,
            author=prompt_author,
            reply_to_message=reply_to_id,
        )
        generation_prompt = f'{converted_messages}\n{prompt}\n'
        generated = self.generate(prompt=generation_prompt, generation_params=generation_params, count=1)[0]
        generated = generated.replace(converted_messages, '').strip()

        tokens = TextToTokenSeqParser().parse(generated)

        return mapper.map_to_original_ids(map_tokens_to_messages(tokens))
