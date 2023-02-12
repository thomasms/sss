import sss


@sss.keeps("one")
def one() -> int:
    return 123


@sss.uses("one", argname="first")
@sss.keeps("two")
def two(first=0) -> int:
    return first + 10


@sss.uses("one", argname="first")
@sss.uses("two", argname="second")
@sss.keeps("three")
def three(first=0, second=0) -> int:
    return first + second


last = sss.process((one, two, three))
print(last)

# also get from the store
print(sss.SSS_DEFAULT.get("three"))
