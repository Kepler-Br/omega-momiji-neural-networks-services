import logging

from network.generated_image import GeneratedImage
from network.image_generator_abstract import ImageGeneratorAbstract


class ImageGeneratorStub(ImageGeneratorAbstract):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def generate_image(
            self,
            prompt: str,
            negative_prompt: str,
    ) -> GeneratedImage:
        self.log.debug(f'(Stub) Generate image:\n'
                       f'Prompt: {prompt}\n'
                       f'Negative prompt: {negative_prompt}\n'
                       )

        return GeneratedImage(
            # GMOD "Missing texture" checkerboard pattern in PNG format
            image='iVBORw0KGgoAAAANSUhEUgAAAfQAAAH0CAYAAADL1t+KAAAMP2lDQ1BJQ0MgcHJvZmlsZQAASImVVwdY' +
                  'U8kWnluSkEBogVCkhN4E6VVKCC2CgFTBRkgChBJjIIjYEVHBtYsFbOiqiKJrAWStiGJhEex9UURgZV0s' +
                  '2JU3KaDrvvK9833nzn/PnPnPmXNn7r0DgNoZjkiUjaoDkCPME8eEBjImJiUzSD0AAQSgDOjAiMPNFTGj' +
                  'oyMAlOH27/L2FvSGct1eyvXP/v8qGjx+LhcAJBriVF4uNwfiowDglVyROA8AotRuNjNPJMVQgZYYJgjx' +
                  'UilOl+NKKU6V40Myn7gYFsTNACipcDjidABU26Gdkc9NhxyqAxA7CnkCIQBqDIj9cnKm8yBOgdga+ogg' +
                  'lvJ7pn7Hk/43ztQRTg4nfQTL5yITpSBBriibM+v/LMf/lpxsyXAMS6gqGeKwGOmcYd3uZE0Pl2IViPuF' +
                  'qZFREGtC/F7Ak/lDjFIyJGHxcn/UgJvLgjWDTxmgjjxOUDjEBhCHCLMjIxT21DRBCBtiuELQAkEeOw5i' +
                  'XYiX8nODYxU+28XTYxSx0Lo0MYupsF/kiGVxpbEeSbLimQr+Vxl8toIfUy3MiEuEmAKxeb4gIRJiVYgd' +
                  'crNiwxU+YwszWJHDPmJJjDR/c4hj+MLQQDk/lp8mDolR+Jfm5A7PF9ueIWBHKvDhvIy4MHl9sGYuR5Y/' +
                  'nAvWzhcy44d5+LkTI4bnwuMHBcvnjvXyhfGxCp73orzAGPlYnCLKjlb446b87FCp3RRi19z8WMVYPCEP' +
                  'Lkg5P54myouOk+eJF2ZyxkXL88FXgQjAAkGAASRQU8F0kAkEbf31/fBO3hMCOEAM0gEf2CsswyMSZT1C' +
                  'eI0FheBPiPggd2RcoKyXD/Kh/cuIVX61B2my3nzZiCzwDOIcEA6y4b1ENko4Ei0BPIUWwT+ic6ByYb7Z' +
                  'UKX9/94+bP1mYUJLhMIiGY7IUBv2JAYTg4hhxBCiDa6P++E+eAS8BkB1xj1xr+F5fPMnPCN0EJ4QbhI6' +
                  'CXenCYrEP2Q5HnRC/hBFLVK/rwVuCTnd8EDcF7JDZpyO6wN73BXGYeL+MLIbtLIUeUurwviB+28z+O5p' +
                  'KPzIjmSUrEMOIFv/OFLVVtVthEVa6+/rI881daTerJGeH+Ozvqs+D7bhP3piS7EjWAt2FruEncDqAQM7' +
                  'jTVgrdhJKR5ZXU9lq2s4WowsnyzII/hHvOEnK61krmONY5/jZ3lfHr9A+o4GrOmiWWJBekYegwm/CHwG' +
                  'W8h1GM1wdnR2AUD6fZG/vl7TZd8NhH75m63oDQC+vKGhoRPfbBFwrx9dDLf/s282q1PwNaEDwMUyrkSc' +
                  'L7fh0gsBviXU4E7TA0bADFjD+TgDd+ADAkAwGAeiQBxIAlNh9hlwnYvBTDAHLAQloAysAuvBZrAN7AR7' +
                  'wQFwGNSDE+AsuACugHZwE9yHq6cbPAcD4C34hCAICaEiNEQPMUYsEDvEGfFE/JBgJAKJQZKQFCQdESIS' +
                  'ZA6yCClD1iCbkR1INfILchw5i1xCOpC7yGOkD3mFfEQxVAXVQg1RS3QM6oky0XA0Dp2CpqMz0EK0GF2B' +
                  'bkSr0P1oHXoWvYLeRDvR5+ggBjBljI6ZYPaYJ8bCorBkLA0TY/OwUqwcq8JqsUb4nK9jnVg/9gEn4jSc' +
                  'gdvDFRyGx+NcfAY+D1+Ob8b34nV4M34df4wP4F8JVIIBwY7gTWATJhLSCTMJJYRywm7CMcJ5uJe6CW+J' +
                  'RCKdaEX0gHsxiZhJnE1cTtxCPEg8Q+wgdhEHSSSSHsmO5EuKInFIeaQS0ibSftJp0jVSN+m9krKSsZKz' +
                  'UohSspJQqUipXGmf0imla0o9Sp/I6mQLsjc5iswjzyKvJO8iN5KvkrvJnygaFCuKLyWOkklZSNlIqaWc' +
                  'pzygvFZWVjZV9lKeoCxQXqC8UfmQ8kXlx8ofVDRVbFVYKpNVJCorVPaonFG5q/KaSqVaUgOoydQ86gpq' +
                  'NfUc9RH1vSpN1UGVrcpTna9aoVqnek31hRpZzUKNqTZVrVCtXO2I2lW1fnWyuqU6S52jPk+9Qv24+m31' +
                  'QQ2ahpNGlEaOxnKNfRqXNHo1SZqWmsGaPM1izZ2a5zS7aBjNjMaicWmLaLto52ndWkQtKy22VqZWmdYB' +
                  'rTatAW1NbVftBO0C7Qrtk9qddIxuSWfTs+kr6Yfpt+gfdQx1mDp8nWU6tTrXdN7pjtIN0OXrluoe1L2p' +
                  '+1GPoResl6W3Wq9e76E+rm+rP0F/pv5W/fP6/aO0RvmM4o4qHXV41D0D1MDWIMZgtsFOg1aDQUMjw1BD' +
                  'keEmw3OG/UZ0owCjTKN1RqeM+oxpxn7GAuN1xqeN/2BoM5iMbMZGRjNjwMTAJMxEYrLDpM3kk6mVabxp' +
                  'kelB04dmFDNPszSzdWZNZgPmxubjzeeY15jfsyBbeFpkWGywaLF4Z2llmWi5xLLestdK14ptVWhVY/XA' +
                  'mmrtbz3Dusr6hg3RxtMmy2aLTbstautmm2FbYXvVDrVztxPYbbHrGE0Y7TVaOLpq9G17FXumfb59jf1j' +
                  'B7pDhEORQ73DizHmY5LHrB7TMuaro5tjtuMux/tOmk7jnIqcGp1eOds6c50rnG+4UF1CXOa7NLi8dLVz' +
                  '5btudb3jRnMb77bErcnti7uHu9i91r3Pw9wjxaPS47anlme053LPi14Er0Cv+V4nvD54u3vneR/2/svH' +
                  '3ifLZ59P71irsfyxu8Z2+Zr6cnx3+Hb6MfxS/Lb7dfqb+HP8q/yfBJgF8AJ2B/QwbZiZzP3MF4GOgeLA' +
                  'Y4HvWN6suawzQVhQaFBpUFuwZnB88ObgRyGmIekhNSEDoW6hs0PPhBHCwsNWh91mG7K57Gr2wDiPcXPH' +
                  'NYerhMeGbw5/EmEbIY5oHI+OHzd+7fgHkRaRwsj6KBDFjlob9TDaKnpG9K8TiBOiJ1RMeBbjFDMnpiWW' +
                  'Fjstdl/s27jAuJVx9+Ot4yXxTQlqCZMTqhPeJQYlrknsnDhm4tyJV5L0kwRJDcmk5ITk3cmDk4InrZ/U' +
                  'PdltcsnkW1OsphRMuTRVf2r21JPT1KZxph1JIaQkpuxL+cyJ4lRxBlPZqZWpA1wWdwP3OS+At47Xx/fl' +
                  'r+H3pPmmrUnrTfdNX5vel+GfUZ7RL2AJNgteZoZlbst8lxWVtSdrKDsx+2COUk5KznGhpjBL2DzdaHrB' +
                  '9A6RnahE1DnDe8b6GQPicPHuXCR3Sm5Dnhb8kW+VWEsWSx7n++VX5L+fmTDzSIFGgbCgdZbtrGWzegpD' +
                  'Cn+ejc/mzm6aYzJn4ZzHc5lzd8xD5qXOa5pvNr94fveC0AV7F1IWZi38rcixaE3Rm0WJixqLDYsXFHct' +
                  'Dl1cU6JaIi65vcRnybal+FLB0rZlLss2Lftayiu9XOZYVl72eTl3+eWfnH7a+NPQirQVbSvdV25dRVwl' +
                  'XHVrtf/qvWs01hSu6Vo7fm3dOsa60nVv1k9bf6nctXzbBsoGyYbOjREbGzaZb1q16fPmjM03KwIrDlYa' +
                  'VC6rfLeFt+Xa1oCttdsMt5Vt+7hdsP3OjtAddVWWVeU7iTvzdz7blbCr5WfPn6t36+8u2/1lj3BP596Y' +
                  'vc3VHtXV+wz2raxBayQ1ffsn728/EHSgoda+dsdB+sGyQ+CQ5NAfv6T8cutw+OGmI55Hao9aHK08RjtW' +
                  'WofUzaobqM+o72xIaug4Pu54U6NP47FfHX7dc8LkRMVJ7ZMrT1FOFZ8aOl14evCM6Ez/2fSzXU3Tmu6f' +
                  'm3juRvOE5rbz4ecvXgi5cK6F2XL6ou/FE5e8Lx2/7Hm5/or7lbpWt9Zjv7n9dqzNva3uqsfVhnav9saO' +
                  'sR2nrvlfO3s96PqFG+wbV25G3uy4FX/rzu3Jtzvv8O703s2++/Je/r1P9xc8IDwofaj+sPyRwaOq321+' +
                  'P9jp3nnycdDj1iexT+53cbueP819+rm7+Bn1WXmPcU91r3Pvib6QvvY/Jv3R/Vz0/FN/yZ8af1a+sH5x' +
                  '9K+Av1oHJg50vxS/HHq1/LXe6z1vXN80DUYPPnqb8/bTu9L3eu/3fvD80PIx8WPPp5mfSZ83frH50vg1' +
                  '/OuDoZyhIRFHzJH9CmBQ0bQ0AF7tAYCaBAANns8ok+TnP5kg8jOrDIH/hOVnRJm4A1ALG+lvPOsMAIeg' +
                  'Wi6A3AEASH/h4wIA6uIyosNnNdm5UipEeA7YHiRFd9cmLAM/iPzM+V3eP7ZAyuoKfmz/Bcutex4eW9qH' +
                  'AAAABmJLR0QA7AD/AACq/6VMAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5wIcCA8rgq2O6gAA' +
                  'ABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAfASURBVHja7dfBDVwxDENBMvj9t6yU' +
                  'kJOMjT3TgMDTgzqZybKm2ycyWZ9hhx122GGHHT+7408AgP+eoAOAoAMAgg4ACDoAIOgAIOgAgKADAIIO' +
                  'AAg6AAg6ACDoAICgAwCCDgCCDgAIOgAg6ACAoAOAoAMAgg4ACDoAIOgAIOgAgKADAAc0yWwfmf0TaRo7' +
                  '7LDDDjvseHWHDx0ALiDoACDoAICgAwCCDgAIOgAIOgAg6ACAoAMAgg4Agg4ACDoAIOgAgKADgKADAIIO' +
                  'AAg6ACDoACDoAICgAwCCDgAIOgAIOgAg6ADAAd9k1o80Xb9hhx122GGHHS/v8KEDwAUEHQAEHQAQdABA' +
                  '0AEAQQcAQQcABB0AEHQAQNABQNABAEEHAAQdABB0ABB0AEDQAQBBBwAEHQAEHQAQdABA0AEAQQcAQQcA' +
                  'BB0AOKBJZvvI7J9I09hhhx122GHHqzt86ABwAUEHAEEHAAQdABB0AEDQAUDQAQBBBwAEHQAQdAAQdABA' +
                  '0AEAQQcABB0ABB0AEHQAQNABAEEHAEEHAAQdABB0AEDQAUDQAQBBBwAO+CazfqTp+g077LDDDjvseHmH' +
                  'Dx0ALiDoACDoAICgAwCCDgAIOgAIOgAg6ACAoAMAgg4Agg4ACDoAIOgAgKADgKADAIIOAAg6ACDoACDo' +
                  'AICgAwCCDgAIOgAIOgAg6ADAAU0y20dm/0Saxg477LDDDjte3eFDB4ALCDoACDoAIOgAgKADAIIOAIIO' +
                  'AAg6ACDoAICgA4CgAwCCDgAIOgAg6AAg6ACAoAMAgg4ACDoACDoAIOgAgKADAIIOAIIOAAg6AHDAN5n1' +
                  'I03Xb9hhhx122GHHyzt86ABwAUEHAEEHAAQdABB0AEDQAUDQAQBBBwAEHQAQdAAQdABA0AEAQQcABB0A' +
                  'BB0AEHQAQNABAEEHAEEHAAQdABB0AEDQAUDQAQBBBwAOaJLZPjL7J9I0dthhhx122PHqDh86AFxA0AFA' +
                  '0AEAQQcABB0AEHQAEHQAQNABAEEHAAQdAAQdABB0AEDQAQBBBwBBBwAEHQAQdABA0AFA0AEAQQcABB0A' +
                  'EHQAEHQAQNABgAO+yawfabp+ww477LDDDjte3uFDB4ALCDoACDoAIOgAgKADAIIOAIIOAAg6ACDoAICg' +
                  'A4CgAwCCDgAIOgAg6AAg6ACAoAMAgg4ACDoACDoAIOgAgKADAIIOAIIOAAg6AHBAk8z2kdk/kaaxww47' +
                  '7LDDjld3+NAB4AKCDgCCDgAIOgAg6ACAoAOAoAMAgg4ACDoAIOgAIOgAgKADAIIOAAg6AAg6ACDoAICg' +
                  'AwCCDgCCDgAIOgAg6ACAoAOAoAMAgg4AHPBNZv1I0/Ubdthhhx122PHyDh86AFxA0AFA0AEAQQcABB0A' +
                  'EHQAEHQAQNABAEEHAAQdAAQdABB0AEDQAQBBBwBBBwAEHQAQdABA0AFA0AEAQQcABB0AEHQAEHQAQNAB' +
                  'gAOaZLaPzP6JNI0ddthhhx12vLrDhw4AFxB0ABB0AEDQAQBBBwAEHQAEHQAQdABA0AEAQQcAQQcABB0A' +
                  'EHQAQNABQNABAEEHAAQdABB0ABB0AEDQAQBBBwAEHQAEHQAQdADggG8y60eart+www477LDDjpd3+NAB' +
                  '4AKCDgCCDgAIOgAg6ACAoAOAoAMAgg4ACDoAIOgAIOgAgKADAIIOAAg6AAg6ACDoAICgAwCCDgCCDgAI' +
                  'OgAg6ACAoAOAoAMAgg4AHNAks31k9k+kaeywww477LDj1R0+dAC4gKADgKADAIIOAAg6ACDoACDoAICg' +
                  'AwCCDgAIOgAIOgAg6ACAoAMAgg4Agg4ACDoAIOgAgKADgKADAIIOAAg6ACDoACDoAICgAwAHfJNZP9J0' +
                  '/YYddthhhx12vLzDhw4AFxB0ABB0AEDQAQBBBwAEHQAEHQAQdABA0AEAQQcAQQcABB0AEHQAQNABQNAB' +
                  'AEEHAAQdABB0ABB0AEDQAQBBBwAEHQAEHQAQdADggCaZ7SOzfyJNY4cddthhhx2v7vChA8AFBB0ABB0A' +
                  'EHQAQNABAEEHAEEHAAQdABB0AEDQAUDQAQBBBwAEHQAQdAAQdABA0AEAQQcABB0ABB0AEHQAQNABAEEH' +
                  'AEEHAAQdABB0AOCfJulkZvtO0wNb1mfYYYcddthhx8/u8KEDwAUEHQAEHQAQdABA0AEAQQcAQQcABB0A' +
                  'EHQAQNABQNABAEEHAAQdABB0ABB0AEDQAQBBBwAEHQAEHQAQdABA0AEAQQcAQQcABB0AOKBJZvvI7J9I' +
                  '09hhhx122GHHqzt86ABwAUEHAEEHAAQdABB0AEDQAUDQAQBBBwAEHQAQdAAQdABA0AEAQQcABB0ABB0A' +
                  'EHQAQNABAEEHAEEHAAQdABB0AEDQAUDQAQBBBwAO+CazfqTp+g077LDDDjvseHmHDx0ALiDoACDoAICg' +
                  'AwCCDgAIOgAIOgAg6ACAoAMAgg4Agg4ACDoAIOgAgKADgKADAIIOAAg6ACDoACDoAICgAwCCDgAIOgAI' +
                  'OgAg6ADAAU0y20dm/0Saxg477LDDDjte3eFDB4ALCDoACDoAIOgAgKADAIIOAIIOAAg6ACDoAICgA4Cg' +
                  'AwCCDgAIOgAg6AAg6ACAoAMAgg4ACDoACDoAIOgAgKADAIIOAIIOAPy+vwXqoNucgOQoAAAAAElFTkSu' +
                  'QmCC',
        )
