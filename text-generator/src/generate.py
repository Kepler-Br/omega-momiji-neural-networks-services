from typing import Optional

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class LanguageNeuralNetwork:
    def __init__(self, path: str, use_cpu: bool = False):
        self.use_cpu = use_cpu
        self.tokenizer = GPT2Tokenizer.from_pretrained(path)
        self.model = GPT2LMHeadModel.from_pretrained(path)
        if not self.use_cpu:
            self.model = self.model.to('cuda')

    def seed(self, seed: int):
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
            bad_words: list[str] = None) -> list[str]:
        torch.manual_seed(seed)

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
            bad_words_ids=encoded_bad_words)

        ret = list(map(self.tokenizer.decode, out))

        del out
        del tokenized_input_ids
        del attention_mask
        del tokenized

        if not self.use_cpu:
            torch.cuda.empty_cache()

        return ret
