from dbInterface import *


class Tester:
    def __init__(self):
        print '######## MyDB Tester V1.0 ########'

    @staticmethod
    def evaluate_result(test_cass_name=None, expected_result=[], real_result=[]):
        print 'Test result of "' + test_cass_name + '":',
        if expected_result == real_result:
            print 'OK'
        else:
            print 'Error'
            print 'Expected result:', expected_result
            print 'Real result:', real_result

    @staticmethod
    def test_insert():
        #TEST CASE #1:
        #insert into record into table

        test_case_name = 'Insert test'

        expected_result = [len(table_tag.data) + 1, 'new_tag']
        table_tag.insert({'name': 'new_tag'})
        row = table_tag.find(table_tag.top_id - 1)
        real_result = [len(table_tag.data), row['name']]

        Tester.evaluate_result(test_case_name, expected_result, real_result)
        return

    @staticmethod
    def test_update():
        #TEST CASE #2:
        #insert update record

        test_case_name = 'Update test'

        expected_result = [table_tag.top_id + 1, 'new_tag']
        table_tag.insert({'name': 'new_tag'})
        row = table_tag.find(table_tag.top_id - 1)
        real_result = [table_tag.top_id, row['name']]

        Tester.evaluate_result(test_case_name, expected_result, real_result)
        return
db_tester = Tester()
db_tester.test_insert()