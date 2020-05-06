def testExceptE():
    try:
        10/0
    except ZeroDivisionError as e:
        print('e',e,'e.args',e.args)
    finally:
        print('right')

testExceptE()