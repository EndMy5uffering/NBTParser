from .NBTTag import NBTTag
from ctypes import c_double
import struct

class NBTDoubleTag(NBTTag):

    TAG_ID = 6
    def __init__(self, tag_name: str, payload: c_double):
        super().__init__(tag_name, payload)
    
    def get_double(self) -> c_double:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + struct.pack('>q', self.get_double().value)

    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, str(self.get_double().value))