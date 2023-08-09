from NBTTypes.NBTTag import NBTTag
from ctypes import c_float
import struct

class NBTFloatTag(NBTTag):

    TAG_ID = 0x5
    def __init__(self, tag_name: str, payload: c_float):
        super().__init__(tag_name, payload)
    
    def get_float(self) -> c_float:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + struct.pack('>f', self.get_float().value)
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, str(self.get_float().value))
