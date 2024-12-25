from .NBTTag import NBTTag
from ctypes import c_longlong
from typing import List
import struct

class NBTLongArrayTag(NBTTag):

    # ID(1) LEN(4) 
    TAG_ID = 0xC
    def __init__(self, tag_name: str, payload: List[c_longlong]):
        super().__init__(tag_name, payload)
    
    def get_long_list(self) -> List[c_longlong]:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + struct.pack('>i', len(self.payload)) + b''.join([n.value.to_bytes(8, 'big', signed=True) for n in self.get_long_list()])

    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, f'len({str(len(self.get_long_list()))})') + '\n' + '\n'.join([f'{(offsetChr*(offset+1))}- {e.value}' for e in self.get_long_list()]) + '\n' + f'{(offsetChr*offset)}<{self.get_nbt_type} END>'