# upyls - A collection of Python utilities

## Limited List

A List which can have a lower limit nd an upper limit set and only be filled with the number of items set by those 
limits

Just import and instantiate it
```
from upyls import LimitedList
limited_list = LimitedList(lower=0, upper=1)
```

## Unit of Work
Implementation of the Unit of Work pattern out of Martin Fowler's book [Patterns of 
Enterprise Applicaton Architecture](https://martinfowler.com/eaaCatalog/unitOfWork.html)

### UnitOfWorkMixin
This class is an abstract class (derived from ABC). It is designed as mixin, so you just can derive your class from it 
and your class gets the functionality of this mixin
class. 

For example:
```
from upyls import UnitOfWorkMixin

class MyUnitOfWork(UnitOfWorkMixin):
    <your code here>
```
The added functionality is to keep track of the attributes of the classes instances. If an attribute gets changed, it is marked as 
dirty and its old value is kept aside the new value.

If you have saved your instance you can call its commit-method and is will not be marked as dirty anymore and its old. 
value will be discarded. As in database transactions you can as well rollback, which means that the old value is put 
back into place and the new Value discarded. As well as with committing, the rollback-method leads to the instance not 
being marked as dirty anymore.

### UnitOfWorkManager
