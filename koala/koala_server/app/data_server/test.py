import numpy as np
import pandas as pd


# arrays = [np.array(['op1', 'op1', 'op1', 'op1', 'op2', 'op2', 'op2', 'op2']),
#           np.array(['g1', 'g2', 1, 2, 1, 2, 1, 2])]
#
# s = pd.Series(np.random.randn(8), index=arrays)
# df = pd.DataFrame(np.random.randn(8, 4), index=arrays)
# print(df)
# df = pd.DataFrame(np.random.randn(3, 8), index=['A', 'B', 'C'], columns=arrays)
# print(df)
# for d in (df.to_dict(orient='records')):
#     print(d)
# print(list(df.columns))
# df2 = pd.DataFrame(np.random.randn(3, 3), index=['A', 'B', 'C'], columns=['sub1', 'sub2', 'task1'])
#
# # df2.columns = pd.MultiIndex.from_product([['a'], df2.columns])
# print(df2)
#
# df3 = df2.merge(df, left_index=True, right_index=True)
# print(df3)
# for d in (df3.to_dict(orient="records")):
#     print(d)
# print(df.columns.nlevels)
# t = df2['sub1']
# print(t)
# pass

arrays = [np.array([1, 1, 2, 2, 3, 3, 3, 3]),
          np.array([1, 2, 1, 2, 1, 2, 1, 2])]

arrays = [np.array([1, 1, 2, 2, 3, 3, 3, 3]),
np.array([1, 2, 1, 2, 1, 2, 1, 2])]

arrays = [['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two'],]
a = np.random.randint(1, 10, (8, 4))
b = a.astype(np.int64)
print(b)
df = pd.DataFrame(b, index=arrays, columns=["a", "b", "c", "d"])
# print(df)
# print(df[[1]])
#
# print(slice([1, 2]),)
#
# print(df.loc[(('bar', 'baz'), ),])
#
# print(type(df.loc['bar', ]))


# a = pd.Series(['bar']).to_dict()
#
# print(df.swaplevel(i=0, j=1))
#
# print(df)


from collections import OrderedDict, defaultdict
s = df.iloc[0]
dd = defaultdict(list)
print(s)
a = s.to_dict()
r = s.to_dict(dd)
print(r)
