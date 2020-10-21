
class TestAnswer:
    def test_answer(self, cmdopt):
        if cmdopt == 'type1':
            print('type1')
        elif cmdopt == 'type2':
            print('type2')
        assert 1 == 1
