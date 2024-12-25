from NBTTypes import *
from ctypes import c_byte, c_short, c_longlong, c_float, c_double, c_uint8, c_uint16, c_uint32, c_ulonglong
import struct
from typing import Dict, Callable, List
import gzip
from pathlib import Path

TO_INT8: Callable[[bytes], c_byte] = lambda bs : c_byte(int.from_bytes(struct.unpack('c', bs)[0]))
TO_INT16: Callable[[bytes], c_short] = lambda bs : c_short(struct.unpack('>h', bs)[0])
TO_INT32: Callable[[bytes], int] = lambda bs : struct.unpack('>i', bs)[0]
TO_INT64: Callable[[bytes], c_longlong] = lambda bs : c_longlong(struct.unpack('>q', bs)[0])
TO_U_INT8: Callable[[bytes], c_uint8] = lambda bs : c_uint8(struct.unpack('B', bs)[0])
TO_U_INT16: Callable[[bytes], c_uint16] = lambda bs : c_uint16(struct.unpack('>H', bs)[0])
TO_U_INT32: Callable[[bytes], c_uint32] = lambda bs : c_uint32(struct.unpack('>I', bs)[0])
TO_U_INT64: Callable[[bytes], c_ulonglong] = lambda bs : c_ulonglong(struct.unpack('>Q', bs)[0])
TO_FLOAT32: Callable[[bytes], c_float] = lambda bs : c_float(struct.unpack('>f', bs)[0])
TO_FLOAT64: Callable[[bytes], c_double] = lambda bs : c_double(struct.unpack('>d', bs)[0])


class NBTScanner:
    def __init__(self, data):
        self.data = data
        self.current = 0
        
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()    
    
    def next(self) -> bytes:
        if not self.has_next():
            raise StopIteration
        x = self.data[self.current]
        self.current += 1
        return bytes([x])
    
    def has_next(self) -> bool:
        return self.current < len(self.data)
    
    def peek(self) -> bytes:
        return bytes(self.data[self.current])

    def parse_next(self, n: int) -> bytes:
        buff = []
        while n and self.has_next():
            buff.append(self.data[self.current])
            self.current += 1
            n = n - 1 #what is this used for???
        if not self.has_next():
            raise StopIteration
        return bytearray(buff)

def parse_tag_name(iter: NBTScanner, has_name: bool = True, default_name: str = 'NBT_TAG') -> str:
    if not has_name:
        return default_name
    return ''.join([chr(n) for n in iter.parse_next(TO_INT16(iter.parse_next(2)).value)])

def fallback(iter: NBTScanner, has_name: bool) -> NBTTag:
    raise Exception('Incorrect tag id was provided: ' + str(int(iter.data[iter.current - 1])))

def parse_end_tag(iter: NBTScanner, has_name: bool = True) -> NBTEndTag:
    return NBTEndTag('TAG_End')

def parse_byte_tag(iter: NBTScanner, has_name: bool = True) -> NBTByteTag:
    return NBTByteTag(parse_tag_name(iter, has_name, 'NBT_BYTE_TAG'), c_byte(iter.next()[0]))

def parse_short_tag(iter: NBTScanner, has_name: bool = True) -> NBTShortTag:
    return NBTShortTag(parse_tag_name(iter, has_name, 'NBT_SHORT_TAG'), TO_INT16(iter.parse_next(2)))

def parse_int_tag(iter: NBTScanner, has_name: bool = True) -> NBTIntTag:
    return NBTIntTag(parse_tag_name(iter, has_name, 'NBT_INT_TAG'), TO_INT32(iter.parse_next(4)))

def parse_long_tag(iter: NBTScanner, has_name: bool = True) -> NBTLongTag:
    return NBTLongTag(parse_tag_name(iter, has_name, 'NBT_LONG_TAG'), TO_INT64(iter.parse_next(8)))

def parse_float_tag(iter: NBTScanner, has_name: bool = True) -> NBTFloatTag:
    return NBTFloatTag(parse_tag_name(iter, has_name, 'NBT_FLOAT_TAG'), TO_FLOAT32(iter.parse_next(4)))

def parse_double_tag(iter: NBTScanner, has_name: bool = True) -> NBTDoubleTag:
    return NBTDoubleTag(parse_tag_name(iter, has_name, 'NBT_DOUBLE_TAG'), TO_FLOAT64(iter.parse_next(8)))

def parse_byte_array_tag(iter: NBTScanner, has_name: bool = True) -> NBTByteArrayTag:
    tag_name = parse_tag_name(iter, has_name, 'NBT_BYTE_ARRAY_TAG')
    array_size = TO_INT32(iter.parse_next(4))
    data = [c_byte(e) for e in iter.parse_next(array_size)]
    return NBTByteArrayTag(tag_name, data)

def parse_string_tag(iter: NBTScanner, has_name: bool = True) -> NBTStringTag:
    tag_name = parse_tag_name(iter, has_name, 'NBT_STRING_TAG')
    string_size = TO_U_INT16(iter.parse_next(2))
    text = ''.join([chr(c) for c in iter.parse_next(string_size.value)])
    return NBTStringTag(tag_name, text)

def parse_list_tag(iter: NBTScanner, has_name: bool = True) -> NBTListTag:
    tag_name = parse_tag_name(iter, has_name, 'NBT_LIST_TAG')
    content_ID = int.from_bytes(iter.next())
    size = TO_INT32(iter.parse_next(4))
    buff = []
    for i in range(0, size):
        buff.append(PARSE_FUNCTIONS.get(content_ID, fallback)(iter, False))
    return NBTListTag(tag_name, content_ID, buff)

def parse_compound_tag(iter: NBTScanner, has_name: bool = True) -> NBTCompoundTag:
    tag_name = parse_tag_name(iter, has_name, 'NBT_COMPOUND_TAG')
    next_tag = int.from_bytes(iter.next())
    result: NBTTag = PARSE_FUNCTIONS.get(next_tag, fallback)(iter)
    buff: List[NBTTag] = []
    while not isinstance(result, NBTEndTag):
        buff.append(result)
        next_tag = int.from_bytes(iter.next())
        result: NBTTag = PARSE_FUNCTIONS.get(next_tag, fallback)(iter)
    buff.append(result)
    return NBTCompoundTag(tag_name, buff)

def parse_int_array_tag(iter: NBTScanner, has_name: bool = True) -> NBTIntArrayTag:
    tag_name = parse_tag_name(iter, has_name, 'NBT_INT_ARRAY_TAG')
    size = TO_INT32(iter.parse_next(4))
    buff = []
    for _ in range(0, size):
        buff.append(TO_INT32(iter.parse_next(4)))
    return NBTIntArrayTag(tag_name, buff)

def parse_long_array_tag(iter: NBTScanner, has_name: bool = True) -> NBTLongArrayTag:
    tag_name = parse_tag_name(iter, has_name, 'NBT_LONG_ARRAY_TAG')
    size = TO_INT32(iter.parse_next(4))
    buff = []
    for _ in range(0, size):
        buff.append(TO_INT64(iter.parse_next(8)))
    return NBTLongArrayTag(tag_name, buff)


PARSE_FUNCTIONS:Dict[int, Callable[[NBTScanner, bool], NBTTag]]  = {
    0x0: parse_end_tag,
    0x1: parse_byte_tag,
    0x2: parse_short_tag,
    0x3: parse_int_tag,
    0x4: parse_long_tag,
    0x5: parse_float_tag,
    0x6: parse_double_tag,
    0x7: parse_byte_array_tag,
    0x8: parse_string_tag,
    0x9: parse_list_tag,
    0xA: parse_compound_tag,
    0xB: parse_int_array_tag,
    0xC: parse_long_array_tag,
}

def parse(data: bytes) -> NBTTag:
    scanner = NBTScanner(data)
    return PARSE_FUNCTIONS.get(int.from_bytes(scanner.next()), fallback)(scanner, True)

def parse_compressed(data: bytes) -> NBTTag:
    return parse(gzip.decompress(data))

def open_parse(path: Path) -> NBTTag:
    if not isinstance(path, Path):
        raise 'Provided path was not of type pathlib.Path'
    buffer = []
    with open(path, 'rb') as fp:
        buffer = fp.read()
    return parse_compressed(buffer)