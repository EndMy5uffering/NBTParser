import gzip
from pathlib import Path
import NBT_Parser

def read_schem(path: Path):
    buffer = []
    with open(path, 'rb') as fp:
        buffer = fp.read()
    return gzip.decompress(buffer)

if __name__ == '__main__':
    schem = Path('./TestTile1.schem')
    uncompressed = read_schem(schem)
    tags = NBT_Parser.open_parse(schem)
    asBytes = tags.to_bytes()
    print(len(uncompressed), len(asBytes))
    for i in range(0, len(uncompressed)):
        if not uncompressed[i] == asBytes[i]:
            raise Exception(f'Not same byte({str(uncompressed[i])} != {str(asBytes[i])}) at {str(i)}')
    print('Same :D')

    savePath = Path('./out.schem')
    tags.write_to_file(savePath)