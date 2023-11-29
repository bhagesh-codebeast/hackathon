# Download Stuff
from huggingface_hub import hf_hub_download
import os

class do_download_model:
	def __init__(self, repo_id, model_path, file_list):
		self.repo_id = repo_id
		self.model_path = model_path
		self.file_list = file_list
	def do_download(self):
		local_dir = os.path.join(os.sep, self.model_path, self.repo_id.split('/')[-1])
		for file in self.file_list:
			hf_hub_download(
				repo_id=self.repo_id,
				filename=file,
				local_dir=local_dir
			)
		return self.repo_id, local_dir

# noocr
# listf = [".gitattributes", "README.md", "added_tokens.json", "config.json", "preprocessor_config.json", "pytorch_model.bin", "sentencepiece.bpe.model", "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json"]
# for file in listf:
#   hf_hub_download(repo_id="jinhybr/OCR-Donut-CORD", filename=file,local_dir="/app/models/OCRDOCUNTCORD/")