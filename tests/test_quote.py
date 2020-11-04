import unittest
from app.models import Quote


class QuoteTest(unittest.TestCase):
    '''
    Test class to test the behaviour of the quote class
    '''
    def setUp(self):
        '''
        set up method that will run before every test
        '''
        self.new_quote = Quote(22,"Ovidiu Platon","I don’t care if it works on your machine! We are not shipping your machine!")
        
    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote,Quote))
        
if __name__ =='__main__':
    unittest.main()    