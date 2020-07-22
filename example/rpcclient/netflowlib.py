"""
This file belongs to https://github.com/bitkeks/python-netflow-v9-softflowd.

The test packets (defined below as hex streams) were extracted from "real"
softflowd exports based on a sample PCAP capture file.

Copyright 2016-2020 Dominik Pataky <software+pynetflow@dpataky.eu>
Licensed under MIT License. See LICENSE.
"""

# The flowset with 2 templates (IPv4 and IPv6) and 8 flows with data
import queue
import random
import socket
import time

#from netflow.collector import ThreadedNetFlowListener

# Invalid export hex stream
PACKET_INVALID = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"

CONNECTION = ('127.0.0.1', 1337)
NUM_PACKETS = 1000


def gen_pkts(n, idx):
    for x in range(n):
        if x == idx:
            yield PACKET_V9_TEMPLATE
        else:
            yield random.choice(PACKETS_V9)



def emit_packets(packets, delay=0.0001):
    """Send the provided packets to the listener"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for p in packets:
        sock.sendto(bytes.fromhex(p), CONNECTION)
        time.sleep(delay)
    sock.close()


def send_packets(packets, delay=0.0001, store_packets=-1) -> (list, float, float):
    """Starts a listener, send packets, receives packets

    returns a tuple: ([(ts, export), ...], time_started_sending, time_stopped_sending)
    """
    #listener = ThreadedNetFlowListener(*CONNECTION)
    tstart = time.time()
    emit_packets(packets, delay=delay)
    time.sleep(0.5)  # Allow packets to be sent and recieved
    tend = time.time()
    #listener.start()


"""
def send_recv_packets(packets, delay=0.0001, store_packets=-1) -> (list, float, float):
    listener = ThreadedNetFlowListener(*CONNECTION)
    tstart = time.time()
    emit_packets(packets, delay=delay)
    time.sleep(0.5)  # Allow packets to be sent and recieved
    tend = time.time()
    listener.start()

    pkts = []
    to_pad = 0
    while True:
        try:
            packet = listener.get(timeout=0.5)
            if -1 == store_packets or store_packets > 0:
                # Case where a programm yields from the queue and stores all packets.
                pkts.append(packet)
                if store_packets != -1 and len(pkts) > store_packets:
                    to_pad += len(pkts)  # Hack for testing
                    pkts.clear()
            else:
                # Performance measurements for cases where yielded objects are processed
                # immediatelly instead of stored. Add empty tuple to retain counting possibility.
                pkts.append(())
        except queue.Empty:
            break
    listener.stop()
    listener.join()
    if to_pad > 0:
        pkts = [()] * to_pad + pkts
    return pkts, tstart, tend
"""


def generate_packets(amount, version, template_every_x=100):
    packets = [PACKET_IPFIX]
    template = PACKET_IPFIX_TEMPLATE

    if version == 1:
        packets = [PACKET_V1]
    elif version == 5:
        packets = [PACKET_V5]
    elif version == 9:
        packets = [*PACKETS_V9]
        template = PACKET_V9_TEMPLATE

    if amount < template_every_x:
        template_every_x = 10

    # If the list of test packets is only one item big (the same packet is used over and over),
    # do not use random.choice - it costs performance and results in the same packet every time.
    def single_packet(pkts):
        return pkts[0]

    packet_func = single_packet
    if len(packets) > 1:
        packet_func = random.choice

    for x in range(amount):
        if x % template_every_x == 0 and version in [9, 10]:
            # First packet always a template, then periodically
            # Note: this was once based on random.random, but it costs performance
            yield template
        else:
            yield packet_func(packets)


# Example export for v1 which contains two flows from one ICMP ping request/reply session
PACKET_V1 = "000100020001189b5e80c32c2fd41848ac110002ac11000100000000000000000000000a00000348" \
            "000027c700004af100000800000001000000000000000000ac110001ac1100020000000000000000" \
            "0000000a00000348000027c700004af100000000000001000000000000000000"

# Example export for v5 which contains three flows, two for ICMP ping and one multicast on interface (224.0.0.251)
PACKET_V5 = "00050003000379a35e80c58622a55ab00000000000000000ac110002ac1100010000000000000000" \
            "0000000a0000034800002f4c0000527600000800000001000000000000000000ac110001ac110002" \
            "00000000000000000000000a0000034800002f4c0000527600000000000001000000000000000000" \
            "ac110001e00000fb000000000000000000000001000000a90000e01c0000e01c14e914e900001100" \
            "0000000000000000"

PACKET_V9_TEMPLATE = "0009000a000000035c9f55980000000100000000000000400400000e00080004000c000400150004" \
                     "001600040001000400020004000a0004000e000400070002000b00020004000100060001003c0001" \
                     "00050001000000400800000e001b0010001c001000150004001600040001000400020004000a0004" \
                     "000e000400070002000b00020004000100060001003c000100050001040001447f0000017f000001" \
                     "fb3c1aaafb3c18fd000190100000004b00000000000000000050942c061b04007f0000017f000001" \
                     "fb3c1aaafb3c18fd00000f94000000360000000000000000942c0050061f04007f0000017f000001" \
                     "fb3c1cfcfb3c1a9b0000d3fc0000002a000000000000000000509434061b04007f0000017f000001" \
                     "fb3c1cfcfb3c1a9b00000a490000001e000000000000000094340050061f04007f0000017f000001" \
                     "fb3bb82cfb3ba48b000002960000000300000000000000000050942a061904007f0000017f000001" \
                     "fb3bb82cfb3ba48b00000068000000020000000000000000942a0050061104007f0000017f000001" \
                     "fb3c1900fb3c18fe0000004c0000000100000000000000000035b3c9110004007f0000017f000001" \
                     "fb3c1900fb3c18fe0000003c000000010000000000000000b3c9003511000400"

# This packet is special. We take PACKET_V9_TEMPLATE and re-order the templates and flows.
# The first line is the header, the smaller lines the templates and the long lines the flows (limited to 80 chars)
PACKET_V9_TEMPLATE_MIXED = ("0009000a000000035c9f55980000000100000000"  # header
                            "040001447f0000017f000001fb3c1aaafb3c18fd000190100000004b00000000000000000050942c"
                            "061b04007f0000017f000001fb3c1aaafb3c18fd00000f94000000360000000000000000942c0050"
                            "061f04007f0000017f000001fb3c1cfcfb3c1a9b0000d3fc0000002a000000000000000000509434"
                            "061b04007f0000017f000001fb3c1cfcfb3c1a9b00000a490000001e000000000000000094340050"
                            "061f04007f0000017f000001fb3bb82cfb3ba48b000002960000000300000000000000000050942a"
                            "061904007f0000017f000001fb3bb82cfb3ba48b00000068000000020000000000000000942a0050"
                            "061104007f0000017f000001fb3c1900fb3c18fe0000004c0000000100000000000000000035b3c9"
                            "110004007f0000017f000001fb3c1900fb3c18fe0000003c000000010000000000000000b3c90035"
                            "11000400"  # end of flow segments
                            "000000400400000e00080004000c000400150004001600040001000400020004"  # template 1024
                            "000a0004000e000400070002000b00020004000100060001003c000100050001"
                            "000000400800000e001b0010001c001000150004001600040001000400020004"  # template 2048
                            "000a0004000e000400070002000b00020004000100060001003c000100050001")

# Three packets without templates, each with 12 flows
PACKETS_V9 = [
    "0009000c000000035c9f55980000000200000000040001e47f0000017f000001fb3c1a17fb3c19fd"
    "000001480000000200000000000000000035ea82110004007f0000017f000001fb3c1a17fb3c19fd"
    "0000007a000000020000000000000000ea820035110004007f0000017f000001fb3c1a17fb3c19fd"
    "000000f80000000200000000000000000035c6e2110004007f0000017f000001fb3c1a17fb3c19fd"
    "0000007a000000020000000000000000c6e20035110004007f0000017f000001fb3c1a9efb3c1a9c"
    "0000004c0000000100000000000000000035adc1110004007f0000017f000001fb3c1a9efb3c1a9c"
    "0000003c000000010000000000000000adc10035110004007f0000017f000001fb3c1b74fb3c1b72"
    "0000004c0000000100000000000000000035d0b3110004007f0000017f000001fb3c1b74fb3c1b72"
    "0000003c000000010000000000000000d0b30035110004007f0000017f000001fb3c2f59fb3c1b71"
    "00001a350000000a000000000000000000509436061b04007f0000017f000001fb3c2f59fb3c1b71"
    "0000038a0000000a000000000000000094360050061b04007f0000017f000001fb3c913bfb3c9138"
    "0000004c0000000100000000000000000035e262110004007f0000017f000001fb3c913bfb3c9138"
    "0000003c000000010000000000000000e262003511000400",

    "0009000c000000035c9f55980000000300000000040001e47f0000017f000001fb3ca523fb3c913b"
    "0000030700000005000000000000000000509438061b04007f0000017f000001fb3ca523fb3c913b"
    "000002a200000005000000000000000094380050061b04007f0000017f000001fb3f7fe1fb3dbc97"
    "0002d52800000097000000000000000001bb8730061b04007f0000017f000001fb3f7fe1fb3dbc97"
    "0000146c000000520000000000000000873001bb061f04007f0000017f000001fb3d066ffb3d066c"
    "0000004c0000000100000000000000000035e5bd110004007f0000017f000001fb3d066ffb3d066c"
    "0000003c000000010000000000000000e5bd0035110004007f0000017f000001fb3d1a61fb3d066b"
    "000003060000000500000000000000000050943a061b04007f0000017f000001fb3d1a61fb3d066b"
    "000002a2000000050000000000000000943a0050061b04007f0000017f000001fb3fed00fb3f002c"
    "0000344000000016000000000000000001bbae50061f04007f0000017f000001fb3fed00fb3f002c"
    "00000a47000000120000000000000000ae5001bb061b04007f0000017f000001fb402f17fb402a75"
    "0003524c000000a5000000000000000001bbc48c061b04007f0000017f000001fb402f17fb402a75"
    "000020a60000007e0000000000000000c48c01bb061f0400",

    "0009000c000000035c9f55980000000400000000040001e47f0000017f000001fb3d7ba2fb3d7ba0"
    "0000004c0000000100000000000000000035a399110004007f0000017f000001fb3d7ba2fb3d7ba0"
    "0000003c000000010000000000000000a3990035110004007f0000017f000001fb3d8f85fb3d7b9f"
    "000003070000000500000000000000000050943c061b04007f0000017f000001fb3d8f85fb3d7b9f"
    "000002a2000000050000000000000000943c0050061b04007f0000017f000001fb3d9165fb3d7f6d"
    "0000c97b0000002a000000000000000001bbae48061b04007f0000017f000001fb3d9165fb3d7f6d"
    "000007f40000001a0000000000000000ae4801bb061b04007f0000017f000001fb3dbc96fb3dbc7e"
    "0000011e0000000200000000000000000035bd4f110004007f0000017f000001fb3dbc96fb3dbc7e"
    "0000008e000000020000000000000000bd4f0035110004007f0000017f000001fb3ddbb3fb3c1a18"
    "0000bfee0000002f00000000000000000050ae56061b04007f0000017f000001fb3ddbb3fb3c1a18"
    "00000982000000270000000000000000ae560050061b04007f0000017f000001fb3ddbb3fb3c1a18"
    "0000130e0000001200000000000000000050e820061b04007f0000017f000001fb3ddbb3fb3c1a18"
    "0000059c000000140000000000000000e8200050061b0400"
]

# Example export for IPFIX (v10) with 4 templates, 1 option template and 8 data flow sets
PACKET_IPFIX_TEMPLATE = "000a05202d45a4700000001300000000000200400400000e00080004000c00040016000400150004" \
                        "0001000400020004000a0004000e000400070002000b00020004000100060001003c000100050001" \
                        "000200340401000b00080004000c000400160004001500040001000400020004000a0004000e0004" \
                        "00200002003c000100050001000200400800000e001b0010001c0010001600040015000400010004" \
                        "00020004000a0004000e000400070002000b00020004000100060001003c00010005000100020034" \
                        "0801000b001b0010001c001000160004001500040001000400020004000a0004000e0004008b0002" \
                        "003c0001000500010003001e010000050001008f000400a000080131000401320004013000020100" \
                        "001a00000a5900000171352e672100000001000000000001040000547f000001ac110002ff7ed688" \
                        "ff7ed73a000015c70000000d000000000000000001bbe1a6061b0400ac1100027f000001ff7ed688" \
                        "ff7ed73a0000074f000000130000000000000000e1a601bb061f04000401004cac110002ac110001" \
                        "ff7db9e0ff7dc1d0000000fc00000003000000000000000008000400ac110001ac110002ff7db9e0" \
                        "ff7dc1d0000000fc0000000300000000000000000000040008010220fde66f14e0f1960900000242" \
                        "ac110002ff0200000000000000000001ff110001ff7dfad6ff7e0e95000001b00000000600000000" \
                        "0000000087000600fde66f14e0f196090000affeaffeaffefdabcdef123456789000000000000001" \
                        "ff7e567fff7e664a0000020800000005000000000000000080000600fde66f14e0f1960900000000" \
                        "00000001fde66f14e0f196090000affeaffeaffeff7e567fff7e664a000002080000000500000000" \
                        "0000000081000600fe800000000000000042aafffe73bbfafde66f14e0f196090000affeaffeaffe" \
                        "ff7e6aaaff7e6aaa0000004800000001000000000000000087000600fde66f14e0f1960900000242" \
                        "ac110002fe800000000000000042aafffe73bbfaff7e6aaaff7e6aaa000000400000000100000000" \
                        "0000000088000600fe800000000000000042acfffe110002fe800000000000000042aafffe73bbfa" \
                        "ff7e7eaaff7e7eaa0000004800000001000000000000000087000600fe800000000000000042aaff" \
                        "fe73bbfafe800000000000000042acfffe110002ff7e7eaaff7e7eaa000000400000000100000000" \
                        "0000000088000600fe800000000000000042aafffe73bbfafe800000000000000042acfffe110002" \
                        "ff7e92aaff7e92aa0000004800000001000000000000000087000600fe800000000000000042acff" \
                        "fe110002fe800000000000000042aafffe73bbfaff7e92aaff7e92aa000000400000000100000000" \
                        "000000008800060008000044fde66f14e0f196090000affeaffeaffefd41b7143f86000000000000" \
                        "00000001ff7ec2a0ff7ec2a00000004a000000010000000000000000d20100351100060004000054" \
                        "ac1100027f000001ff7ed62eff7ed68700000036000000010000000000000000c496003511000400" \
                        "7f000001ac110002ff7ed62eff7ed687000000760000000100000000000000000035c49611000400" \
                        "08000044fde66f14e0f196090000affeaffeaffefd41b7143f8600000000000000000001ff7ef359" \
                        "ff7ef3590000004a000000010000000000000000b1e700351100060004000054ac1100027f000001" \
                        "ff7f06e4ff7f06e800000036000000010000000000000000a8f90035110004007f000001ac110002" \
                        "ff7f06e4ff7f06e8000000a60000000100000000000000000035a8f911000400"

# Example export for IPFIX with two data sets
PACKET_IPFIX = "000a00d02d45a47000000016000000000801007cfe800000000000000042acfffe110002fde66f14" \
               "e0f196090000000000000001ff7f0755ff7f07550000004800000001000000000000000087000600" \
               "fdabcdef123456789000000000000001fe800000000000000042acfffe110002ff7f0755ff7f0755" \
               "000000400000000100000000000000008800060008000044fde66f14e0f196090000affeaffeaffe" \
               "2a044e42020000000000000000000223ff7f06e9ff7f22d500000140000000040000000000000000" \
               "e54c01bb06020600"

PACKET_IPFIX_TEMPLATE_ETHER = "000a05002d45a4700000000d00000000" \
                              "000200500400001200080004000c000400160004001500040001000400020004000a0004000e0004" \
                              "00070002000b00020004000100060001003c000100050001003a0002003b00020038000600390006" \
                              "000200440401000f00080004000c000400160004001500040001000400020004000a0004000e0004" \
                              "00200002003c000100050001003a0002003b000200380006003900060002005008000012001b0010" \
                              "001c001000160004001500040001000400020004000a0004000e000400070002000b000200040001" \
                              "00060001003c000100050001003a0002003b00020038000600390006000200440801000f001b0010" \
                              "001c001000160004001500040001000400020004000a0004000e0004008b0002003c000100050001" \
                              "003a0002003b000200380006003900060003001e010000050001008f000400a00008013100040132" \
                              "0004013000020100001a00000009000000b0d80a558000000001000000000001040000747f000001" \
                              "ac110002e58b988be58b993e000015c70000000d000000000000000001bbe1a6061b040000000000" \
                              "123456affefeaffeaffeaffeac1100027f000001e58b988be58b993e0000074f0000001300000000" \
                              "00000000e1a601bb061f040000000000affeaffeaffe123456affefe0401006cac110002ac110001" \
                              "e58a7be3e58a83d3000000fc0000000300000000000000000800040000000000affeaffeaffe0242" \
                              "aa73bbfaac110001ac110002e58a7be3e58a83d3000000fc00000003000000000000000000000400" \
                              "00000000123456affefeaffeaffeaffe080102b0fde66f14e0f196090000affeaffeaffeff020000" \
                              "0000000000000001ff110001e58abcd9e58ad098000001b000000006000000000000000087000600" \
                              "00000000affeaffeaffe3333ff110001fde66f14e0f196090000affeaffeaffefde66f14e0f19609" \
                              "0000000000000001e58b1883e58b284e000002080000000500000000000000008000060000000000" \
                              "affeaffeaffe123456affefefdabcdef123456789000000000000001fde66f14e0f1960900000242" \
                              "ac110002e58b1883e58b284e0000020800000005000000000000000081000600000000000242aa73" \
                              "bbfaaffeaffeaffefe800000000000000042aafffe73bbfafde66f14e0f196090000affeaffeaffe" \
                              "e58b2caee58b2cae000000480000000100000000000000008700060000000000123456affefe0242" \
                              "ac110002fde66f14e0f196090000affeaffeaffefe800000000000000042aafffe73bbfae58b2cae" \
                              "e58b2cae000000400000000100000000000000008800060000000000affeaffeaffe123456affefe" \
                              "fe800000000000000042acfffe110002fe800000000000000042aafffe73bbfae58b40aee58b40ae" \
                              "000000480000000100000000000000008700060000000000affeaffeaffe123456affefefe800000" \
                              "000000000042aafffe73bbfafe800000000000000042acfffe110002e58b40aee58b40ae00000040" \
                              "0000000100000000000000008800060000000000123456affefeaffeaffeaffefe80000000000000" \
                              "0042aafffe73bbfafe800000000000000042acfffe110002e58b54aee58b54ae0000004800000001" \
                              "00000000000000008700060000000000123456affefeaffeaffeaffefe800000000000000042acff" \
                              "fe110002fe800000000000000042aafffe73bbfae58b54aee58b54ae000000400000000100000000" \
                              "000000008800060000000000affeaffeaffe123456affefe"

PACKET_IPFIX_ETHER = "000a02905e8b0aa90000001600000000" \
                     "08000054fde66f14e0f196090000affeaffeaffefd40abcdabcd00000000000000011111e58b84a4" \
                     "e58b84a40000004a000000010000000000000000d20100351100060000000000affeaffeaffe0242" \
                     "aa73bbfa04000074ac1100027f000001e58b9831e58b988a00000036000000010000000000000000" \
                     "c49600351100040000000000affeaffeaffe123456affefe7f000001ac110002e58b9831e58b988a" \
                     "000000760000000100000000000000000035c4961100040000000000123456affefeaffeaffeaffe" \
                     "08000054fde66f14e0f196090000affeaffeaffefd40abcdabcd00000000000000011111e58bb55c" \
                     "e58bb55c0000004a000000010000000000000000b1e700351100060000000000affeaffeaffe0242" \
                     "aa73bbfa04000074ac1100027f000001e58bc8e8e58bc8ec00000036000000010000000000000000" \
                     "a8f900351100040000000000affeaffeaffe123456affefe7f000001ac110002e58bc8e8e58bc8ec" \
                     "000000a60000000100000000000000000035a8f91100040000000000123456affefeaffeaffeaffe" \
                     "0801009cfe800000000000000042acfffe110002fdabcdef123456789000000000000001e58bc958" \
                     "e58bc958000000480000000100000000000000008700060000000000affeaffeaffe123456affefe" \
                     "fdabcdef123456789000000000000001fe800000000000000042acfffe110002e58bc958e58bc958" \
                     "000000400000000100000000000000008800060000000000123456affefeaffeaffeaffe08000054" \
                     "fde66f14e0f196090000affeaffeaffe2a044e42020000000000000000000223e58bc8ede58be4d8" \
                     "00000140000000040000000000000000e54c01bb0602060000000000affeaffeaffe123456affefe"
