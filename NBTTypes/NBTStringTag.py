from .NBTTag import NBTTag
import struct

class NBTStringTag(NBTTag):

    # ID(1) LEN(2) PAYLOAD(UTF-8)
    TAG_ID = 0x8
    def __init__(self, tag_name: str, payload: str):
        super().__init__(tag_name, payload)
    
    def get_string(self) -> str:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + struct.pack('>H',len(self.payload))  + bytes(self.payload, 'utf-8')

    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, self.get_string())
    