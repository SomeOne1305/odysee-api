from dataclasses import dataclass

@dataclass
class FileType():
	fileId:str
	url:str
	is_default: bool