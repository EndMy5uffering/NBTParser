from .NBTTag import NBTTag

class NBTIntTag(NBTTag):

    TAG_ID = 0x3
    def __init__(self, tag_name: str, payload: int):
        super().__init__(tag_name, payload)
    
    def get_int(self) -> int:
        return self.payload
    
    def to_bytes(self) -> bytes:
        return super().to_bytes() + self.get_int().to_bytes(4, 'big', signed=True)
    
    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, str(self.get_int()))
