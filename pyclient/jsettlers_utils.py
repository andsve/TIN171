hex_grid = [0x17, 0x39, 0x5b, 0x7d
           ,0x15, 0x37, 0x59, 0x7b, 0x9d
           ,0x13, 0x35, 0x57, 0x79, 0x9b, 0xbd
           ,0x11, 0x33, 0x55, 0x77, 0x99, 0xbb, 0xdd
           ,0x31, 0x53, 0x75, 0x97, 0xb9, 0xdb
           ,0x51, 0x73, 0x95, 0xb7, 0xd9
           ,0x71, 0x93, 0xb5, 0xd7]

straight_edges = [0x06, 0x28, 0x4a, 0x6c, 0x8e
                 ,0x04, 0x26, 0x48, 0x6a, 0x8c, 0xae
                 ,0x02, 0x24, 0x46, 0x68, 0x8a, 0xac, 0xce
                 ,0x00, 0x22, 0x44, 0x66, 0x88, 0x11, 0xcc, 0xee
                 ,0x20, 0x42, 0x64, 0x86, 0xa8, 0xca, 0xec
                 ,0x40, 0x62, 0x84, 0xa6, 0xc8, 0xea
                 ,0x60, 0x82, 0xa4, 0xc6, 0xe8]

harbors = {
'3for1': [7, 8, 9, 10, 11, 12],
'clay': [17, 49, 65, 81, 97],
'ore' : [18, 50, 66, 82, 98],
'sheep': [19, 51, 67, 83, 99],
'grain': [20, 52, 68, 84, 100],
'lumber': [21, 53, 69, 85 ,101]
}


# This does not work, hmz
def road_to_nodes(r):
    cs = hex(r)[2:]
    if len(cs) == 1:
        cs = '0' + cs[0]
    c1, c2 = cs
    c1e = int(c1, 16) % 2 == 0
    c2e = int(c2, 16) % 2 == 0
    
    if c1e and c2e:
        n1 = r + 0x01
        n2 = r + 0x10 
    elif not c1e and c2e:
        n1 = r
        n2 = r + 0x11
    else:
        n1 = r - 0x11
        n2 = r

    return [n1, n2]

def nodes_around_hex(n):
    return [n + v for v in [0x01, 0x12, 0x21, 0x10, -0x01, -0x10]]
    
def roads_around_hex(n):
    # / \   n1 n2
    # | |  n0   n3
    # \ /   n5 n4
    return [  n - 0x11
            , n - 0x11 + 1
            , n + 0x01
            , n + 0x11 + 0x01
            , n + 0x11 + 0x10
            , n + 0x11 - 0x01
            ]

def adjacent_tiles(n):
    if n % 2 == 0:
        t1 = n - 0x21
        t2 = n + 0x01
        t3 = n - 0x01
    else:
        t1 = n - 0x10
        t2 = n - 0x12
        t3 = n + 0x10
    
    return [t1, t2, t3]

def node_to_roads(n):
    if n % 2 == 0:
        #   |    r1
        #  / \ r2  r3
        r1 = n - 0x10
        r2 = n - 0x11
        r3 = n + 0x10 + 1
    else:
        #  \ /    r1
        #   |   r2  r3
        r1 = n - 0x11
        r2 = n + 0x11
        r3 = n - 0x01
    return [ r1 if 0x0 < r1 < 0xff else None
           , r2 if 0x0 < r2 < 0xff else None
           , r3 if 0x0 < r3 < 0xff else None]



# Node -> Road LUT
roadLUT = {
     0x22: (0x22,0x23,0x32)
    ,0x23: (0x23,0x23,0x34)
    ,0x24: (0x24,0x25,0x34)
    ,0x25: (0x25,0x25,0x36)
    ,0x26: (0x26,0x27,0x36)
    ,0x27: (0x27,0x27,0x38)
    ,0x32: (0x32,0x32,0x43)
    ,0x34: (0x34,0x34,0x45)
    ,0x36: (0x36,0x36,0x47)
    ,0x38: (0x38,0x38,0x49)
    ,0x42: (0x42,0x43,0x52)
    ,0x43: (0x43,0x43,0x54)
    ,0x44: (0x44,0x45,0x54)
    ,0x45: (0x45,0x45,0x56)
    ,0x46: (0x46,0x47,0x56)
    ,0x47: (0x47,0x47,0x58)
    ,0x48: (0x48,0x49,0x58)
    ,0x49: (0x49,0x49,0x5a)
    ,0x52: (0x52,0x52,0x63)
    ,0x54: (0x54,0x54,0x65)
    ,0x56: (0x56,0x56,0x67)
    ,0x58: (0x58,0x58,0x69)
    ,0x5a: (0x5a,0x5a,0x6b)
    ,0x62: (0x62,0x63,0x72)
    ,0x63: (0x63,0x63,0x74)
    ,0x64: (0x64,0x65,0x74)
    ,0x65: (0x65,0x65,0x76)
    ,0x66: (0x66,0x67,0x76)
    ,0x67: (0x67,0x67,0x78)
    ,0x68: (0x68,0x69,0x78)
    ,0x69: (0x69,0x69,0x7a)
    ,0x6a: (0x6a,0x6b,0x7a)
    ,0x6b: (0x6b,0x6b,0x7c)
    ,0x72: (0x72,0x72,0x83)
    ,0x74: (0x74,0x74,0x85)
    ,0x76: (0x76,0x76,0x87)
    ,0x78: (0x78,0x78,0x89)
    ,0x7a: (0x7a,0x7a,0x8b)
    ,0x7c: (0x7c,0x7c,0x8d)
    ,0x83: (0x83,0x83,0x94)
    ,0x84: (0x84,0x85,0x94)
    ,0x85: (0x85,0x85,0x96)
    ,0x86: (0x86,0x87,0x96)
    ,0x87: (0x87,0x87,0x98)
    ,0x88: (0x88,0x89,0x98)
    ,0x89: (0x89,0x89,0x9a)
    ,0x8a: (0x8a,0x8b,0x9a)
    ,0x8b: (0x8b,0x8b,0x9c)
    ,0x8c: (0x8c,0x8d,0x9c)
    ,0x94: (0x94,0x94,0xa5)
    ,0x96: (0x96,0x96,0xa7)
    ,0x98: (0x98,0x98,0xa9)
    ,0x9a: (0x9a,0x9a,0xab)
    ,0x9c: (0x9c,0x9c,0xad)
    ,0xa5: (0xa5,0xa5,0xb6)
    ,0xa6: (0xa6,0xa7,0xb6)
    ,0xa7: (0xa7,0xa7,0xb8)
    ,0xa8: (0xa8,0xa9,0xb8)
    ,0xa9: (0xa9,0xa9,0xba)
    ,0xaa: (0xaa,0xab,0xba)
    ,0xab: (0xab,0xab,0xbc)
    ,0xac: (0xac,0xad,0xbc)
    ,0xb6: (0xb6,0xb6,0xc7)
    ,0xb8: (0xb8,0xb8,0xc9)
    ,0xba: (0xba,0xba,0xcb)
    ,0xbc: (0xbc,0xbc,0xcd)
    ,0xc7: (0xc7,0xc7,0xd8)
    ,0xc8: (0xc8,0xc9,0xd8)
    ,0xc9: (0xc9,0xc9,0xda)
    ,0xca: (0xca,0xcb,0xda)
    ,0xcb: (0xcb,0xcb,0xdc)
    ,0xcc: (0xcc,0xcd,0xdc)}
    
    
# HexTile -> Node LUT
nodeLUT = {
     0x23: (0x23,0x22,0x23,None,None,None,None)
    ,0x25: (0x25,0x24,0x25,None,None,None,None)
    ,0x27: (0x27,0x26,0x27,None,None,None,None)
    ,0x32: (0x32,0x22,0x32,None,None,None,None)
    ,0x34: (0x34,0x23,0x24,0x34,None,None,None)
    ,0x36: (0x36,0x25,0x26,0x36,None,None,None)
    ,0x38: (0x38,0x27,0x38,None,None,None,None)
    ,0x43: (0x43,0x32,0x42,0x43,None,None,None)
    ,0x45: (0x45,0x34,0x44,0x45,None,None,None)
    ,0x47: (0x47,0x36,0x46,0x47,None,None,None)
    ,0x49: (0x49,0x38,0x48,0x49,None,None,None)
    ,0x52: (0x52,0x42,0x52,None,None,None,None)
    ,0x54: (0x54,0x43,0x44,0x54,None,None,None)
    ,0x56: (0x56,0x45,0x46,0x56,None,None,None)
    ,0x58: (0x58,0x47,0x48,0x58,None,None,None)
    ,0x5a: (0x5a,0x49,0x5a,None,None,None,None)
    ,0x63: (0x63,0x52,0x62,0x63,None,None,None)
    ,0x65: (0x65,0x54,0x64,0x65,None,None,None)
    ,0x67: (0x67,0x56,0x66,0x67,None,None,None)
    ,0x69: (0x69,0x58,0x68,0x69,None,None,None)
    ,0x6b: (0x6b,0x5a,0x6a,0x6b,None,None,None)
    ,0x72: (0x72,0x62,0x72,None,None,None,None)
    ,0x74: (0x74,0x63,0x64,0x74,None,None,None)
    ,0x76: (0x76,0x65,0x66,0x76,None,None,None)
    ,0x78: (0x78,0x67,0x68,0x78,None,None,None)
    ,0x7a: (0x7a,0x69,0x6a,0x7a,None,None,None)
    ,0x7c: (0x7c,0x6b,0x7c,None,None,None,None)
    ,0x83: (0x83,0x72,0x83,None,None,None,None)
    ,0x85: (0x85,0x74,0x84,0x85,None,None,None)
    ,0x87: (0x87,0x76,0x86,0x87,None,None,None)
    ,0x89: (0x89,0x78,0x88,0x89,None,None,None)
    ,0x8b: (0x8b,0x7a,0x8a,0x8b,None,None,None)
    ,0x8d: (0x8d,0x7c,0x8c,None,None,None,None)
    ,0x94: (0x94,0x83,0x84,0x94,None,None,None)
    ,0x96: (0x96,0x85,0x86,0x96,None,None,None)
    ,0x98: (0x98,0x87,0x88,0x98,None,None,None)
    ,0x9a: (0x9a,0x89,0x8a,0x9a,None,None,None)
    ,0x9c: (0x9c,0x8b,0x8c,0x9c,None,None,None)
    ,0xa5: (0xa5,0x94,0xa5,None,None,None,None)
    ,0xa7: (0xa7,0x96,0xa6,0xa7,None,None,None)
    ,0xa9: (0xa9,0x98,0xa8,0xa9,None,None,None)
    ,0xab: (0xab,0x9a,0xaa,0xab,None,None,None)
    ,0xad: (0xad,0x9c,0xac,None,None,None,None)
    ,0xb6: (0xb6,0xa5,0xa6,0xb6,None,None,None)
    ,0xb8: (0xb8,0xa7,0xa8,0xb8,None,None,None)
    ,0xba: (0xba,0xa9,0xaa,0xba,None,None,None)
    ,0xbc: (0xbc,0xab,0xac,0xbc,None,None,None)
    ,0xc7: (0xc7,0xb6,0xc7,None,None,None,None)
    ,0xc9: (0xc9,0xb8,0xc8,0xc9,None,None,None)
    ,0xcb: (0xcb,0xba,0xca,0xcb,None,None,None)
    ,0xcd: (0xcd,0xbc,0xcc,None,None,None,None)
    ,0xd8: (0xd8,0xc7,0xc8,None,None,None,None)
    ,0xda: (0xda,0xc9,0xca,None,None,None,None)
    ,0xdc: (0xdc,0xcb,0xcc,None,None,None,None)}