import broom
import numpy as np

sw = broom.Sweeper()


def get_sub_array(A, which):
    """extract subarray from A determined by information in the list which
    """

    if not A.ndim == len(which):
        raise ValueError('A.ndim == len(which) not true')

    A_shape = A.shape

    slice_list = []

    for n, dim in enumerate(which):
        if dim == 'all':
            slice_list.append(slice(0, A_shape[n]))
        elif isinstance(dim, int) and dim - 1 <= A_shape[n]:
            slice_list.append(dim)
        else:
            raise ValueError('invalid value in which list...')

    return A[slice_list]


A = np.random.random((5, 3, 4))
which_list = [0, 'all', 2]

B = get_sub_array(A, which_list)

print A
print B