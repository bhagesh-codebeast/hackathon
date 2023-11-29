# Run Stuff
from typing import Dict, List, Any
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
import re

# check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class do_ocr:
	def __init__(self, path=""):
		self.processor = DonutProcessor.from_pretrained(path)
		self.model = VisionEncoderDecoderModel.from_pretrained(path)
		self.model.to(device)
		self.decoder_input_ids = self.processor.tokenizer("<s_cord-v2>", add_special_tokens=False, return_tensors="pt").input_ids
	def __call__(self, data: Any) -> List[List[Dict[str, float]]]:
		inputs = data.pop("inputs", data)
		pixel_values = self.processor(inputs, return_tensors="pt").pixel_values
		outputs = self.model.generate(
			pixel_values.to(device),
			decoder_input_ids=self.decoder_input_ids.to(device),
			max_length=self.model.decoder.config.max_position_embeddings,
			early_stopping=True,
			pad_token_id=self.processor.tokenizer.pad_token_id,
			eos_token_id=self.processor.tokenizer.eos_token_id,
			use_cache=True,
			num_beams=1,
			bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
			return_dict_in_generate=True,
		)
		sequence = self.processor.batch_decode(outputs.sequences)[0]
		sequence = sequence.replace(self.processor.tokenizer.eos_token, "").replace(self.processor.tokenizer.pad_token, "")
		sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()
		remove_tags = lambda s: re.sub(r'<[^>]*>', '', s)
		sequence = remove_tags(sequence)
		return inputs, sequence

if __name__ == "__main__":
	imagex = '/content/sample_data/test.png'
	image = Image.open(imagex).convert("RGB")
	handler = do_ocr(path="/content/sample_data/model")
	# Sample input data
	sample_input = {
		"inputs": image
	}
	# Call the instance with the input data
	result = handler(sample_input)
	# Display the result
	print(result)