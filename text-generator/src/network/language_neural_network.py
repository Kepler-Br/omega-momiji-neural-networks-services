import logging
from typing import Optional

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

from network.language_neural_network_abstract import LanguageNeuralNetworkAbstract


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
            count: int = 1,
            max_new_tokens: int = 50,
            num_beams: int = 5,
            no_repeat_ngram_size: int = 5,
            repetition_penalty: float = None,
            early_stopping: bool = True,
            seed: int = 42,
            top_k: int = 50,
            top_p: float = 0.95,
            temperature: float = 1.0,
            bad_words: list[str] = None
    ) -> list[str]:
        self.log.debug(
            f'Generating text:\n'
            f'Prompt: {prompt}\n'
            f'Count: {count}\n'
            f'Max new tokens: {max_new_tokens}\n'
            f'Num beams: {num_beams}\n'
            f'No repeat ngram size: {no_repeat_ngram_size}\n'
            f'Repetition penalty: {repetition_penalty}\n'
            f'Early stopping: {early_stopping}\n'
            f'Seed: {seed}\n'
            f'Top k: {top_k}\n'
            f'Top p: {top_p}\n'
            f'Temperature: {temperature}\n'
            f'Bad words: {bad_words}\n'
        )

        self._seed(seed)

        encoded_bad_words: Optional[list[list[int]]] = None

        if bad_words is not None and len(bad_words) != 0:
            encoded_bad_words = []

            for word in bad_words:
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
            max_new_tokens=max_new_tokens,
            num_beams=num_beams,
            no_repeat_ngram_size=no_repeat_ngram_size,
            early_stopping=early_stopping,
            num_return_sequences=count,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
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
