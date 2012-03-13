import unittest


def sort(l):
    if len(l) <= 1:
        return l
    half = len(l) / 2
    l1 = l[:half]
    l2 = l[half:]
    return merge(sort(l1), sort(l2))


def merge(l1, l2):
    n = len(l1) + len(l2)
    i, j = 0, 0
    out = []
    for k in range(0, n):
        if l1[i] < l2[j]:
            out.append(l1[i])
            i += 1
        else:
            out.append(l2[j])
            j += 1
        if len(l1) == i:
            out.extend(l2[j:])
            break
        if len(l2) == j:
            out.extend(l1[i:])
            break
    return out


class TestSort(unittest.TestCase):
    def test_sort_list(self):
        result = sort([9, 4, 2, 1, 7, 5, 7])
        expected = [1, 2, 4, 5, 7, 7, 9]
        self.assertEquals(expected, result)

    def test_list_with_negative_number(self):
        result = sort([-9, 4, 2, 1, 7, 5, 7])
        expected = [-9, 1, 2, 4, 5, 7, 7]
        self.assertEquals(expected, result)

    def test_single_element_list(self):
        self.assertEquals([2], [2])

    def test_empty_list(self):
        self.assertEquals([], [])

if __name__ == '__main__':
    unittest.main()
