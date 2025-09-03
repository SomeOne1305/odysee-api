from ..extensions import CacheStorage

def return_decoded_value(key:str)->str:
	value = CacheStorage.get(key)
	if value:
		value = value.decode('utf-8')
	return value