import sys, io, os, errno
import struct


def decode_header(file):
    f = open(file, 'rb')

    header = f.read(25)

    h_name, h_int1, h_int2, dsize, dstart = struct.unpack_from('<9siiii', header)
    
    ##TODO: test if name == 'AMARCHIVE'
    
    tell = f.tell()

    if dstart >= tell:
        seek = dstart - tell
        f.seek(seek, io.SEEK_CUR) 

        end = dstart + dsize
        files = []
        while f.tell() < end:

            fstart = struct.unpack('<i', f.read(4))
            fint1 = struct.unpack('<i', f.read(4))
            fsize = struct.unpack('<i', f.read(4))
            name = b''
            while True:
                char = f.read(1)
                if char == b'\x00':
                    break
                name = name + char

            files.append((name.decode(), fstart[0], fsize[0]))
    
    f.close()
    return files

def extract_bin(file, name, start, size):
    dirname = os.path.splitext(file)[0]
    print('Record in {}'.format(dirname))

    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    f = open(file, 'rb')
    e = open( dirname + '\\' + name, 'wb')

    print('--Extracting: {} ({} bytes)'.format(name, size))

    f.seek(start, io.SEEK_SET)
    buffer = f.read(size)

    e.write(buffer)

    f.close()
    e.close()
    pass

def main(argv):
    if len(argv) == 0:
        argv = [ os.getcwd() ]
    for arg in argv:
        if os.path.isfile(arg):
            print("File {}".format(arg))
            files = decode_header(arg)
            for name, start, size in files:
                extract_bin(arg, name, start, size)
        if os.path.isdir(arg):
            print("Directory {}".format(arg))
            with os.scandir(arg) as it:
                for entry in it:
                    if entry.name.endswith('.gp7bank') and entry.is_file():
                        print('File {}'.format(entry.path))
                        files = decode_header(entry.path)
                        for name, start, size in files:
                            extract_bin(entry.path, name, start, size)

        


if __name__ == '__main__' :
    main(sys.argv[1:])    