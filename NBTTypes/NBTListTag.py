from .NBTTag import NBTTag
from typing import List

class NBTListTag(NBTTag):

    TAG_ID = 0x9
    def __init__(self, tag_name: str, payload_id: int, payload: List[NBTTag]):
        super().__init__(tag_name, payload)
        self.payload_id = payload_id
    
    def get_tag_list(self) -> List[NBTTag]:
        return self.payload

    def at(self, idx: int) -> NBTTag:
        return self.payload[idx]
    
    def get_length(self) -> int:
        return len(self.payload)
    
    def get_content_type(self) -> str:
        if not self.payload:
            return 'NBTTag'
        return self.payload[0].get_nbt_type()
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.payload_id.to_bytes(1, 'big') + len(self.payload).to_bytes(4, 'big') + b''.join([e.to_bytes() for e in self.get_tag_list()])
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, self.get_content_type() + f'({str(self.get_length())})') + '\n'.join([f'{e.to_str(offset+1, offsetChr)}' for e in self.get_tag_list()]) + '\n' + f'{(offsetChr*offset)}<{self.get_nbt_type()} END>'