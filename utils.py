import numpy as np

def _delta_to_vectors_generator(delta):
    vector = [0, 0, 0]
    see_retain = False
    see_op = False
    for record in delta:
        for key in record:
            if key == 'retain':
                see_op = False
                if not see_retain:
                    see_retain = True
                    vector[0] = record[key]
                else:
                    see_retain = False
                    vector[2] = record[key]
                    yield vector
                    vector = [0, 0, 0]
            elif key == 'insert' or key == 'delete':
                if see_op:
                    yield vector
                    vector = [0, 0, 0]
                vector[1] = len(record[key]) if key == 'insert' else -int(record[key])
                see_op = True
    if vector != [0, 0, 0]:
        yield vector

def delta_to_matrix(delta):
    return np.array([*_delta_to_vectors_generator(delta)])

def _matrix_to_delta_generator(matrix):
    delta = {}
    for vector in matrix:
        for i in range(3):
            if i == 0 or i == 2:
                if 'retain' in delta:
                    yield delta
                    if vector[i] != 0:
                        delta = {'retain': vector[i]}
                else:
                    if vector[i] != 0:
                        delta['retain'] = vector[i]
            else:
                if vector[i] > 0:
                    if 'insert' or 'delete' in delta:
                        yield delta
                        delta = {'insert': vector[i]}
                    else:
                        delta['insert'] = vector[i]
                elif vector[i] < 0:
                    if 'insert' or 'delete' in delta:
                        yield delta
                        delta = {'delete': -vector[i]}
                    else:
                        delta['delete'] = -vector[i]
    yield delta

def matrix_to_delta(matrix):
    return [*_matrix_to_delta_generator(matrix)]

def _ot_mat(old, new):
    factor_old = np.eye(len(old))
    factor_old = np.tile(factor_old, [len(new), 1])
    factor_new = np.eye(len(new))
    factor_new = np.reshape(np.tile(np.expand_dims(factor_new, 1), [1, len(old), 1]), [len(old)*len(new),-1])
    old_ = np.matmul(old.T, factor_old.T).T
    new_ = np.matmul(new.T, factor_new.T).T
    sub = new_ - old_
    before = sub.T[0] > 0
    after = sub.T[2] > 0
    new_.T[0] += old_.T[1] * before
    new_.T[2] += old_.T[1] * after
    new_ = np.reshape(new_, [-1, len(old), 3])
    new = np.sum(new_, 1)
    return new

def ot(oldDelta, delta):
    old = delta_to_matrix(oldDelta)
    new = delta_to_matrix(delta)
    return _ot_mat(old, new)

if __name__ == "__main__":
    new = matrix_to_delta(ot([{'retain': 0, 'insert': '!!!!!'}, {'retain': 5}], [{'retain': 5, 'insert': '!'}, {'retain': 7}]))
    print(new)