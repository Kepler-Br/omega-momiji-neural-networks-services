import logging

from network.language_neural_network_abstract import LanguageNeuralNetworkAbstract


class LanguageNeuralNetworkStub(LanguageNeuralNetworkAbstract):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

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
            f'(Stub) Generating text:\n'
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
        return ['According to all known laws of aviation, there is no way that a bee should be able to fly. '
                'Its wings are too small to get its fat little body off the ground. '
                'The bee, of course, flies anyways.']
