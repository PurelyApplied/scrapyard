def answer(start, length):
    '''Performs the XOR-checksum with triangular gaps.

    The checksum is optimized in the following ways:

    First, the XOR of values 10000000000 .. 10000011111 need not
    compare the leading 100000 in each value.  The repeated XOR of the
    prefix will reduce to zero if there are an even number of terms,
    or itself if there are an odd number of terms.

    Second, we know that the XOR of consecutive values from zero to
    2^k-1 (00..00 to 11..11) is zero for k > 1, and is equal to one
    for k = 1.  As such, we can "jump" terms according to the number
    of leading zeros.

    '''

    ## Handle the edgecase
    if length == 1:
        return start
    ## Identify leading constant bits, build bitmask
    last = start + length**2 - length + 1
    b_last = bin(last)[2:]
    b_start = bin(start)[2:]
    # pad with zeros to the starting binary string so lengths match.
    b_start = "0"*(len(b_last) - len(b_start)) + b_start
    # identify number of bits that will change between start and last
    important_bits = 0
    for i in range(len(b_last)):
        if b_last[-i] != b_start[-i]:
            important_bits = i
    # create the bitmask and adjust the start to compensate
    mask = 1
    for i in range(important_bits):
        mask = mask<<1 | 1
    original_start = start
    start &= mask
    ## Begin XOR checksums.  Begin with either 0 or original start value...
    # The number of terms follows triangular numbers, odd for length=1
    # (2, 5, 6, 9, 10...)
    checksum = start ^ original_start if length % 4 in (1, 2) else 0
    # Begin working through each row
    for row in range(length):
        row_start = start + row * length
        pos = 0
        while pos < length - row:
            value = row_start + pos
            # Identify number of trailing zeros and maximum jump size
            n_zeros = len(bin(value)) - len(bin(value).rstrip('0')) if value else 64
            max_step = length - row - pos
            jump = n_zeros
            while jump and 1<<jump > max_step:
                jump -= 1
            # Three cases:
            # - No jump: make XOR and take step
            # - One jump: every bit exists twice, except the least
            #   bit, which hits zero and one.  Yields XOR against 1
            # - Higher jump: equivalent to XOR against zero, yielding
            #   no change.
            if jump == 0:
                checksum ^= value
                pos += 1
            elif jump == 1:
                checksum ^= 1
                pos += 2
            else:
                pos += 1<<jump
    return checksum
