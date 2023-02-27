# from PIL import Image
# from clip_interrogator import Config, Interrogator
#
# image_path = '/home/br/Pictures/0b15872acadd6dc7f2234044ade92b9d.jpg'
#
# image = Image.open(image_path).convert('RGB')
# ci = Interrogator(Config(clip_model_name="RN50-quickgelu/openai", blip_model_type='base'))
# print(ci.interrogate(image))
import time

from cachetools import TTLCache

ccc = TTLCache(maxsize=10, ttl=1.0)

ccc['123'] = 321

print(ccc['123'])

for i in range(10):
    ccc[str(i)] = i
    print(ccc[str(i)])
print(ccc['123'])
