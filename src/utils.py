BYTES_IN_KB = 1024


def bytes_to_megabytes(bytes_size: int) -> float:
    return bytes_size / (BYTES_IN_KB ** 2)
