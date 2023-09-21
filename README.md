# test-annotate
Test model annotations through the Juju API

Basic operations are:
```
./annotate get         # list all annotations on the model
./annotate get foo     # print just the value of foo
./annotate set foo bar # set the value of 'foo' to 'bar'
./annotate set foo ""  # delete the annotation of 'foo'
```
