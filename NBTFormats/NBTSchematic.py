from NBTTypes import NBTTag, NBTListTag, NBTCompoundTag, NBTEndTag, NBTShortTag, NBTIntArrayTag, NBTIntTag, NBTByteArrayTag
from ctypes import c_short, c_byte
from dataclasses import dataclass, field
import numpy as np
from scipy.ndimage import label, find_objects

# Entity data is missing in Schematic

@dataclass
class Schematic:
    width:int  # X-Axis
    height:int # Y-Axis
    length:int # Z-Axis
    palette:dict[str, int] = field(default_factory=dict)
    data:list[int] = field(default_factory=dict) # YZX
    block_entities: NBTTag = None

    def __post_init__(self):
        data_set = set(self.data)
        self.palette = {k:v for k,v in self.palette.items() if v in data_set}


    @classmethod
    def from_nbt(cls, nbt_data:NBTCompoundTag) -> "Schematic":
        if nbt_data.get_tag_by_name("Schematic"):
            nbt_data = nbt_data["Schematic"]
        return cls(
            width=nbt_data["Width"].payload.value,
            height=nbt_data["Height"].payload.value,
            length=nbt_data["Length"].payload.value,
            palette={x.get_name():x.payload for x in nbt_data["Blocks"]["Palette"].payload if not type(x) is NBTEndTag},
            data=[x.value for x in nbt_data["Blocks"]["Data"].payload]
        )
    
    def sliced_clone(self, region: tuple[slice, slice, slice]) -> "Schematic":
        """Region in YZX order"""
        clone = Schematic(
            width  = region[2].stop - region[2].start,   # X-Axis
            height = region[0].stop - region[0].start,   # Y-Axis
            length = region[1].stop - region[1].start ,  # Z-Axis
            data = np.array(self.data).reshape((self.height, self.length, self.width))[region].flatten().tolist(),
            palette = self.palette
        )
        return clone

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
                    NBTListTag("BlockEntities", NBTCompoundTag.TAG_ID, payload=[]),
                    NBTByteArrayTag('Data', payload=[c_byte(x) for x in self.data]),
                    NBTEndTag()]),
                NBTEndTag()]),
            NBTEndTag()])

    def _get_height_map(self, axis=0) -> np.array:
        """
        Projects the schematic down onto the xz plane or along a given axis
        Arguments:
        axis -- the axis along wich the schematic is projected onto a plane
        Retruns:
        -> A numpy array of the projected features
        """
        x = np.array(self.data)
        y = x.reshape((self.height, self.length, self.width))
        y = np.add.reduce(y, axis=axis)
        y[y>0] = 1
        return y
    
    def data_as_3D(self) -> np.array:
        return np.array(self.data).reshape((self.height, self.length, self.width))

    def _find_collections(self, feature_map: np.array):
        labeled_array, num_features = label(feature_map)
        return find_objects(labeled_array)
    
    def separate(self) -> list["Schematic"]:
        height_map = self._get_height_map()
        bounding_boxes = self._find_collections(height_map)

        for box in bounding_boxes:
            sliced = self.sliced_clone((slice(0,self.height), *box)) 

            feature2 = sliced._get_height_map(1)
            bounding2 = sliced._find_collections(feature2)
            s0, s1 = bounding2[0]
            yield self.sliced_clone((s0, *box))
