# pip install rembg onnxruntime

from PIL import Image
from rembg import remove

input_patch = "./img/foto_original.jpeg"
output_patch = "./img/foto_fundo_removido.png"

_input = Image.open(input_patch)
_output = remove(_input)
_output.save(output_patch)
