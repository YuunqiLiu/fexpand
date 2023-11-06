

from pcpp import preprocessor

fi = open('test.f','r')
fo = open('test.o','w')

p = preprocessor.Preprocessor()

p.parse(fi.read())
print(p.analyze())