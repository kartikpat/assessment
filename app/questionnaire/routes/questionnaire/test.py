import unittest
import os
import json

from app import create_app
import datetime

class QuestionnaireTestCase(unittest.TestCase):
    """This class represents the questionnaire test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.questionnaire = {
                "name": "test driven title",
                "status": 1,
                "type": 1,
                "assessor": 1,
                "created": "",
                "lastUpdated": "",
                "durationInMin": 30,
                "security": 1,
                "invocation": 1,
                "expiry": "",
                "quesbankType": 1,
                "description": "test driven description",
                "instruction": "test driven instruction"
            } 

    def test_questionnaire_creation(self):
        """Test API can create a questionnaire (POST request)"""
        res = self.client().post('/questionnaire', data=self.questionnaire)
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(res.data))

    # def test_api_can_get_all_questionnaire(self):
    #     """Test API can get a bucketlist (GET request)."""
    #     res = self.client().post('/questionnaire', data=self.questionnaire)
    #     self.assertEqual(res.status_code, 201)
    #     res = self.client().get('/bucketlists/')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertIn('Go to Borabora', str(res.data))

    # def test_api_can_get_questionnaire_by_id(self):
    #     """Test API can get a single bucketlist by using it's id."""
    #     rv = self.client().post('/bucketlists/', data=self.bucketlist)
    #     self.assertEqual(rv.status_code, 201)
    #     result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
    #     result = self.client().get(
    #         '/bucketlists/{}'.format(result_in_json['id']))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('Go to Borabora', str(result.data))

    # def test_bucketlist_can_be_edited(self):
    #     """Test API can edit an existing bucketlist. (PUT request)"""
    #     rv = self.client().post(
    #         '/bucketlists/',
    #         data={'name': 'Eat, pray and love'})
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.client().put(
    #         '/bucketlists/1',
    #         data={
    #             "name": "Dont just eat, but also pray and love :-)"
    #         })
    #     self.assertEqual(rv.status_code, 200)
    #     results = self.client().get('/bucketlists/1')
    #     self.assertIn('Dont just eat', str(results.data))

    # def test_bucketlist_deletion(self):
    #     """Test API can delete an existing bucketlist. (DELETE request)."""
    #     rv = self.client().post(
    #         '/bucketlists/',
    #         data={'name': 'Eat, pray and love'})
    #     self.assertEqual(rv.status_code, 201)
    #     res = self.client().delete('/bucketlists/1')
    #     self.assertEqual(res.status_code, 200)
    #     # Test to see if it exists, should return a 404
    #     result = self.client().get('/bucketlists/1')
    #     self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
# A bit of testing explanation. Inside the test_bucketlist_creation(self)