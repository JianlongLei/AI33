import requests

r = requests.post('https://clipdrop-api.co/text-inpainting/v1',
  # files = {
  #   'image_file': ('image.jpg', image_file_object, 'image/jpeg'),
  #   'mask_file': ('mask.png', mask_file_object, 'image/png')
  #   },
  data = { 'text_prompt': 'A woman with a red scarf' },
  headers = { 'x-api-key': 'sk-1zrwYEUEfeu8XKllrtLY2s3K3wHKsWlAm7i7qaZc9ocuwVOs'}
)
if (r.ok):
  print(r.json())
  # r.content contains the bytes of the returned image
else:
  r.raise_for_status()