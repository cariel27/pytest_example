import pytest


class TestClass(object):
    # <<<<<< Process Marks - Parametrized Tests >>>>>>>>>>
    test_data_working = [(3, 3, 6), (4, 4, 8), (5, 5, 10), (6, 6, 12), (7, 7, 14), (8, 8, 16), (9, 9, 18), (10, 10, 20),
                         (11, 11, 22), (12, 12, 24), (13, 13, 26), (14, 14, 28), (15, 15, 30), (16, 16, 329),
                         (17, 17, 349)]
    test_data_not_implemented_yet = [(18, 18, 0), (19, 19, 0), (20, 20, 0), (21, 21, 0),
                                     (22, 22, 0), (23, 23, 0), (24, 24, 0), (25, 25, 0)]
    test_data_broken = [(1, 1, 0), (2, 2, 0)]
    
    @pytest.mark.parametrize("a,b,expected", test_data_working)
    @pytest.mark.test_process_marks("Working")
    def test_mark_function_by_process_tag_working_parametrized_working(self, a, b, expected):
        assert a + b == expected

    @pytest.mark.parametrize("a,b,expected", test_data_not_implemented_yet)
    @pytest.mark.test_process_marks("NotImplementedYet")
    def test_mark_function_by_process_tag_working_parametrized_not_implemented(self, a, b, expected):
        assert a + b == expected

    @pytest.mark.parametrize("a,b,expected", test_data_broken)
    @pytest.mark.test_process_marks("Broken")
    def test_mark_function_by_process_tag_working_parametrized_broken(self, a, b, expected):
        assert a + b == expected

    # @pytest.mark.test_process_marks("Working")
    # def test_mark_function_by_process_tag_working_that_pass(self):
    #     assert True
    #
    # @pytest.mark.test_process_marks("Working")
    # def test_mark_function_by_process_tag_working_that_fails(self):
    #     assert False
    #
    # @pytest.mark.test_process_marks("Working")
    # def test_mark_function_by_process_tag_working_that_fixed(self):
    #     assert True
    #

    #
    # # <<<<<< Process Marks >>>>>>>>>>
    # @pytest.mark.test_process_marks("US20589")
    # def test_mark_function_by_process_tag_working(self):
    #     assert True
    #
    # @pytest.mark.test_process_marks("NotImplementedYet")
    # def test_mark_function_by_process_tag_not_implemented_yet(self):
    #     assert True
    #
    # @pytest.mark.test_process_marks("Broken")
    # def test_mark_function_by_process_tag_broken(self):
    #     assert True
    #
    # @pytest.mark.test_process_marks("NotImplementedYet")
    # @pytest.mark.test_process_marks("Broken")
    # def test_mark_function_by_double_process_tag(self):
    #     assert True
    #
    # @pytest.mark.test_process_marks("Frozen")
    # def test_mark_function_by_process_mark_frozen(self):
    #     assert True
    #
    # @pytest.mark.test_process_marks("Working")
    # @pytest.mark.Broken
    # def test_mark_function_by_process_mark_and_no_process_mark(self):
    #     assert True
    #
    #  # <<<<<< No Process Mark >>>>>>>>>>
    #
    # def test_mark_function_without_mark(self):
    #     assert True
    #
    # @pytest.mark.NotATest
    # def test_mark_function_by_not_a_test_mark(self):
    #     assert True
    #
    # @pytest.mark.Working
    # def test_working(self):
    #     x = "this"
    #     assert 'h' in x
    #
    # @pytest.mark.Working
    # @pytest.mark.Broken
    # def test_working_and_broken(self):
    #     x = "this"
    #     assert 'h' in x
    #
    # @pytest.mark.Working
    # @pytest.mark.Frozen
    # def test_working_and_frozen(self):
    #     x = "this"
    #     assert 'h' in x
    #
    # @pytest.mark.Working
    # def test_working_that_fails(self):
    #     x = "hello"
    #     assert hasattr(x, 'check')

    # @pytest.mark.Broken
    # def test_broken(self):
    #     x = "broken"
    #     assert hasattr(x, 'working')
    #
    # @pytest.mark.NotImplementedYet
    # def test_not_implemented_yet(self):
    #     x = "not_implemented_yet test"
    #     assert hasattr(x, 'working')
