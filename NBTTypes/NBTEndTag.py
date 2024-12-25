from . import NBTTag

class NBTEndTag(NBTTag):

    TAG_ID = 0x0
    def __init__(self, tag_name: str):
        super().__init__(tag_name, None)

    def to_bytes(self) -> bytes:
        return self.TAG_ID.to_bytes(1, 'big')

    def to_str(self, offset: int = 0, offsetChr: str = '\t') -> str:
        return self._strH(offset, offsetChr, '-')