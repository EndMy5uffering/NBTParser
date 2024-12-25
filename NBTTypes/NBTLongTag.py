from . import NBTTag
from ctypes import c_longlong

class NBTLongTag(NBTTag):

    # ID(1) PAYLOAD(8)
    TAG_ID = 0x4
    def __init__(self, tag_name: str, payload: c_longlong):
        super().__init__(tag_name, payload)
    
    def get_long(self) -> c_longlong:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.get_long().value.to_bytes(8, 'big')
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, str(self.get_long().value))
