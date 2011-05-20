import numpy as np

# {{{ vector types

class vec:
    pass

def _create_vector_types():
    field_names = ["x", "y", "z", "w"]

    name_to_dtype = {}
    dtype_to_name = {}

    counts = [2, 3, 4, 8, 16]
    for base_name, base_type in [
        ('char', np.int8),
        ('uchar', np.uint8),
        ('short', np.int16),
        ('ushort', np.uint16),
        ('int', np.uint32),
        ('uint', np.uint32),
        ('long', np.int64),
        ('ulong', np.uint64),
        ('float', np.float32),
        ('double', np.float64),
        ]:
        for count in counts:
            name = "%s%d" % (base_name, count)

            titles = field_names[:count]
            if len(titles) < count:
                titles.extend((count-len(titles))*[None])

            dtype = np.dtype(dict(
                names=["s%d" % i for i in range(count)],
                formats=[base_type]*count,
                titles=titles))

            name_to_dtype[name] = dtype
            dtype_to_name[dtype] = name

            setattr(vec, name, dtype)

            my_field_names = ",".join(field_names[:count])
            my_field_names_defaulted = ",".join(
                    "%s=0" % fn for fn in field_names[:count])
            setattr(vec, "make_"+name, 
                    staticmethod(eval(
                        "lambda %s: array((%s), dtype=my_dtype)"
                        % (my_field_names_defaulted, my_field_names),
                        dict(array=np.array, my_dtype=dtype))))

    vec._dtype_to_c_name = dtype_to_name
    vec._c_name_to_dtype = name_to_dtype

_create_vector_types()

# }}}
