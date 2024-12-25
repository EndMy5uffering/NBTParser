from .NBTTag import NBTTag
from ctypes import c_byte

class NBTByteTag(NBTTag):

    TAG_ID = 0x1
    def __init__(self, tag_name: str, payload: c_byte):
        super().__init__(tag_name, payload)
    
    def get_byte(self) -> c_byte:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.get_byte().value.to_bytes(1, 'big', signed=True)
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, str(self.get_byte().value))
