"""A "translation dictionary".  Internal counter increments upon any
key access that the dictionary does not contain, assigning that key to
the counter."""


# noinspection PyStatementEffect
class Translation(dict):
    def __init__(self, *args, read_args_as_key_value_pairs=False):
        super(Translation, self).__init__()
        self._current = 0
        self._locked = False
        if read_args_as_key_value_pairs:
            for k, v in args:
                self[k] = v
        else:
            for k in args:
                self[k]

    def __missing__(self, key):
        if self._locked:
            raise KeyError("'{}' missing in locked translation.".format(key))
        self[key] = self._current
        self._current += 1
        return self[key]

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def translate(self, iterable, drop_missing=False):
        if drop_missing:
            return (self[i] for i in iterable if i in self)
        else:
            return (self[i] for i in iterable)

    def write(self, filename, header="", width=0):
        if not self:
            return
        width = width or max(len(str(k)) for k in self)
        buff = ""
        if header:
            buff += header.rstrip() + "\n"
        buff += ("# Note that this translation is zero-indexed,"
                 " which may not match a 1-indexed metis file. \n")
        buff += "#\n# <Original name> <Translated name> \n"
        buff += ("\n".join(
            "{{:>{0}}} {{:>{0}}}".format(width).format(
                k, v)
            for k, v in sorted(self.items(), key=lambda x: x[1])))
        buff += "\n"
        if filename is None:
            print(buff)
        else:
            with open(filename, 'w') as o:
                o.write(buff)


def load_translation_file(filename, key_in_type=str, value_in_type=int):
    with open(filename) as f:
        as_dict = {key_in_type(line.split()[0])
                   : value_in_type(line.split()[1])
                   for line in f
                   if line.strip()
                   and not line.strip()[0] in ";%#"}
    as_pairs = list(as_dict.items())
    as_translation = Translation(*as_pairs, read_args_as_key_value_pairs=True)
    as_translation.lock()
    return as_translation


def reverse(d: dict):
    return {v: k for k, v in d.items()}
