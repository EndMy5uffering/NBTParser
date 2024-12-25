from .NBTTag import NBTTag
from ctypes import c_short

class NBTShortTag(NBTTag):

    # ID(1) PAYLOAD(2)
    TAG_ID = 0x2
    def __init__(self, tag_name: str, payload: c_short):
        super().__init__(tag_name, payload)
    
    def get_short(self) -> c_short:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.get_short().value.to_bytes(2, 'big', signed=True)
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, str(self.get_short().value))