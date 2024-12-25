from . import NBTTag
from typing import Any, List

class NBTCompoundTag(NBTTag):

    TAG_ID = 0xA
    def __init__(self, tag_name: str, payload: List[NBTTag]):
        super().__init__(tag_name, payload)
    
    def get_tags(self) -> List[NBTTag]:
        return self.payload
    
    def at(self, idx: int) -> NBTTag:
        return self.payload[idx]

    def get_tag_by_name(self, tag_name: str, default: Any = None) -> NBTTag | None:
        for tag in self.payload:
            if tag.get_name() == tag_name:
                return tag
        return default
    
    def has_tag(self, tag_name: str) -> bool:
        for tag in self.payload:
            if tag.get_name() == tag_name:
                return True
        return False

    def to_bytes(self) -> bytes:
        return super().to_bytes() + b''.join([e.to_bytes() for e in self.get_tags()])
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, f'len({str(len(self.get_tags()))})') + '\n' + '\n'.join([f'{e.to_str(offset+1, offsetChr)}' for e in self.get_tags()]) + '\n' + f'{(offsetChr*offset)}<{self.get_nbt_type()} END>'
    
    def __getitem__(self, key:str) -> NBTTag:
        ret = self.get_tag_by_name(tag_name=key)
        if ret is None:
            raise KeyError()
        return ret