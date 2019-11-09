import unittest

from src import api

class TestStylePredictor(unittest.TestCase):

    def setUp(self) -> None:
        self.client = api.app.test_client()
        self.base_request = {'Size(L)': 21.0,
                             'OG': 1.069,
                             'FG': 1.013,
                             'ABV': 7.37,
                             'IBU': 64.62,
                             'Color': 5.97,
                             'BoilSize': 25.0,
                             'BoilTime': 60.0,
                             'Efficiency': 35.0,
                             'SugarScale_Plato': 0.0,
                             'SugarScale_Specific Gravity': 1.0,
                             'BrewMethod_All Grain': 0.0,
                             'BrewMethod_BIAB': 0.0,
                             'BrewMethod_Partial Mash': 0.0,
                             'BrewMethod_extract': 1.0}

    def test_get(self):
        """
        Tests basic functionality:
        can it predict and respond without errors ?
        """
        req_body = {k: str(v) for k, v in self.base_request.items()}

        response = self.client.get('/style/predict', data=req_body)

        expected = {
            'prediction': 7
        }
        self.assertDictEqual(expected, response.json)

    def test_nonnumeric_OG(self):
        """
        Tests error raised on values
        that cannot be converted to float
        """
        req_body = {k: str(v) for k, v in self.base_request.items()}
        req_body['OG'] = 'cat'

        response = self.client.get('/style/predict', data=req_body)

        expected = {'message': 'Value for OG is non-numeric or Nan'}
        self.assertDictEqual(expected, response.json)

    def test_nan(self):
        """
        Test error raised on Nan values
        """
        req_body = {k: str(v) for k, v in self.base_request.items()}

        req_body['ABV'] = float('nan')

        response = self.client.get('/style/predict', data=req_body)

        expected = {'message': 'Value for ABV is non-numeric or Nan'}
        self.assertDictEqual(expected, response.json)

    def test_onehot_feats(self):
        """
        Tests non-0-or-1 values for onehot
        feats.
        """
        req_body = {k: str(v) for k, v in self.base_request.items()}

        req_body['SugarScale_Plato'] = 2

        response = self.client.get('/style/predict', data=req_body)

        expected = {'message': 'Value for SugarScale_Plato is not 0 or 1'}
        self.assertDictEqual(expected, response.json)

    def test_onehot_feats_not_integer(self):
        """
        Tests whether api returns error
        on fractional values for onehot feats.
        """
        req_body = {k: str(v) for k, v in self.base_request.items()}

        req_body['SugarScale_Plato'] = 0.5

        response = self.client.get('/style/predict', data=req_body)

        expected = {'message': 'Value for SugarScale_Plato is not 0 or 1'}
        self.assertDictEqual(expected, response.json)

    def test_missing_feat(self):
        """
        Tests whether api returns error
        on missing features.
        """
        req_body = {k: str(v) for k, v in self.base_request.items()}

        del req_body['SugarScale_Plato']

        response = self.client.get('/style/predict', data=req_body)

        expected = {'message': 'Value for SugarScale_Plato is not 0 or 1'}
        self.assertDictEqual(expected, response.json)



if __name__ == '__main__':
    unittest.main()
