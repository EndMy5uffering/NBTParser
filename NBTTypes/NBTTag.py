from pathlib import Path
import gzip

class NBTTag:

    TAG_ID = -1
    def __init__(self, tag_name: str, payload = None):
        self.tag_name = tag_name
        self.payload = payload

    def get_name(self) -> str:
        return self.tag_name
    
    def get_nbt_type(self) -> str:
        return self.__class__.__name__
    
    def to_bytes(self) -> bytes:
        return self.TAG_ID.to_bytes(1, 'big') + len(self.get_name()).to_bytes(2, 'big') + bytes(self.get_name(), 'utf-8')
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return '<NBT base class>'
    
    def _strH(self, of, oc, p) -> str:
        return (oc*of) + f'<{self.get_nbt_type()}[{self.get_name()}] [{p}]>'
    
    def write_to_file(self, path: Path):
        with open(path, 'wb') as file:
            file.write(gzip.compress(self.to_bytes()))

    def __str__(self) -> str:
        return self.to_str()
    
    def __repr__(self) -> str:
        return f"<{self.__class__.TAG_ID} {self.__class__.__name__}> name: {self.tag_name}"