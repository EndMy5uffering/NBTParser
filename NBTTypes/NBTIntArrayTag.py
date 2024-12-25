from . import NBTTag
from typing import List
import struct

class NBTIntArrayTag(NBTTag):

    TAG_ID = 0xB
    def __init__(self, tag_name: str, payload: List[int]):
        super().__init__(tag_name, payload)
    
    def get_int_array(self) -> List[int]:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + len(self.payload).to_bytes(4, 'big') + b''.join([struct.pack('>i', e) for e in self.get_int_array()])

    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, f'len({str(len(self.get_int_array()))})') + '\n' + '\n'.join([f'{(offsetChr*(offset+1))}- {str(e)}' for e in self.get_int_array()]) + '\n' + f'{(offsetChr*offset)}<{self.get_nbt_type()} END>'