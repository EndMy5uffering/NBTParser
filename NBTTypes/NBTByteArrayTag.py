from NBTTypes.NBTTag import NBTTag
from ctypes import c_byte
from typing import List
import struct

class NBTByteArrayTag(NBTTag):

    TAG_ID = 0x7
    def __init__(self, tag_name: str, payload: List[c_byte]):
        super().__init__(tag_name, payload)
    
    def get_bytes(self) -> List[c_byte]:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + struct.pack('>i', len(self.get_bytes())) + b''.join([e.value.to_bytes(1, 'big') for e in self.get_bytes()])
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, f'bytes({str(len(self.get_bytes()))})')