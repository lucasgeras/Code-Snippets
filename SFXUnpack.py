import os
import sys
if len(sys.argv) == 2:
    filename = sys.argv[1]
    unpack_folder = "./{filename}_unpacked/".format(filename=filename)
    sfx = open(filename,mode="rb")
    data = sfx.read()
    archivetag = b'\x21\x40\x49\x6e\x73\x74\x61\x6c\x6c\x45\x6e\x64\x40\x21'
    scripttag = b'\x21\x40\x49\x6e\x73\x74\x61\x6c\x6c\x40\x21'
    formattag = b'\x37\x7a'
    startoffset = 0
    while True:
        offset = data[startoffset:].find(archivetag)
        if offset == -1:
            if startoffset == 0:print("The archive does not contain 7z archive")
            break
        elif offset != 0:
            print("InstallEndTag Found on {hex_offset}".format(hex_offset=hex(startoffset + offset)))  
            for byte_offset in range(14,80):
                if data[startoffset + offset + byte_offset:startoffset + offset + byte_offset+2] == formattag:
                    print('7z archive tag found at {arch_offset}'.format(arch_offset=hex(startoffset + offset + byte_offset)))
                    archivefoundoffset = startoffset + offset + byte_offset
                    break
            startoffset = startoffset + offset + 14
    os.mkdir(unpack_folder)
    with open(unpack_folder + filename + '.7z', "wb") as archive:
        archive.write(data[archivefoundoffset:])
    startoffset = 0
    scriptnum = 0
    while True:
        offset = data[startoffset:].find(scripttag)
        if offset == -1:
            if startoffset == 0:print("The archive does not contain any scripts")
            break
        elif offset != 0:
            print("Install Script Found on {hex_offset}".format(hex_offset=hex(startoffset + offset)))
            endoffset = data[startoffset+offset:].find(archivetag) + startoffset + offset
            print("Install Script end Found on {hex_offset}".format(hex_offset=hex(endoffset-1)))
            #print(data[startoffset + offset:endoffset+14])
            with open(unpack_folder + filename + '_script' + '_'+ str(scriptnum) +'.bin', "wb") as script:
                script.write(data[startoffset + offset:endoffset+14])
            startoffset = startoffset + endoffset + 14
            scriptnum = scriptnum + 1
