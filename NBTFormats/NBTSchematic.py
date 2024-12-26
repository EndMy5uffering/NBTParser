from NBTTypes import NBTCompoundTag, NBTEndTag, NBTShortTag, NBTIntArrayTag, NBTIntTag, NBTByteArrayTag
from ctypes import c_short, c_byte
from dataclasses import dataclass, field


# Entity data is missing in Schematic

@dataclass
class Schematic:
    width:int
    height:int
    length:int
    palette:dict[str, int] = field(default_factory=dict)
    data:list[int] = field(default_factory=dict)
    
    def __init__(self, nbt_data:NBTCompoundTag):
        if nbt_data.get_tag_by_name("Schematic"):
            nbt_data = nbt_data["Schematic"]
        self.width=nbt_data["Width"].payload.value
        self.height=nbt_data["Height"].payload.value
        self.length=nbt_data["Length"].payload.value
        self.palette={x.get_name():x.payload for x in nbt_data["Blocks"]["Palette"].payload if not type(x) is NBTEndTag}
        self.data=[x.value for x in nbt_data["Blocks"]["Data"].payload]
    
    def export_as_nbt(self):
        return NBTCompoundTag('', payload=[
            NBTCompoundTag('Schematic', payload=[
                NBTShortTag('Width', c_short(self.width)),
                NBTShortTag('Height', c_short(self.height)),
                NBTShortTag('Length', c_short(self.length)),
                NBTIntArrayTag('Offset', [0,0,0]),
                NBTIntTag('Version', 3),
                NBTIntTag('DataVersion', 3955),
                
                NBTCompoundTag('Blocks', payload=[
                    NBTCompoundTag('Palette', payload=[
                        *[NBTIntTag(k, v) for k,v in self.palette.items()],
                        NBTEndTag()]),
                    NBTByteArrayTag('Data', payload=[c_byte(x) for x in self.data]),
                    NBTEndTag()]),
                NBTEndTag()]),
            NBTEndTag()])
