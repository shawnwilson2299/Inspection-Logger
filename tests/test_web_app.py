"""Exercise real HTTP requests against an isolated, temporary local server."""
import http.client
import threading
import unittest
from http.server import HTTPServer
from urllib.parse import urlencode

import web_app


class BrowserFlowTests(unittest.TestCase):
    def setUp(self):
        web_app.current_inspection = None
        self.server = HTTPServer(('127.0.0.1', 0), web_app.InspectionHandler)
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.worker.join()
        web_app.current_inspection = None

    def request(self, method='GET', path='/', **form):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        body = urlencode(form) if method == 'POST' else None
        connection.request(method, path, body, {'Content-Type': 'application/x-www-form-urlencoded'})
        response = connection.getresponse()
        result = response.status, response.getheader('Location'), response.read().decode()
        connection.close()
        return result

    def start(self):
        status, location, _ = self.request('POST', '/start', batch_id='BATCH-45', sample_size='45')
        self.assertEqual((status, location), (303, '/'))

    def test_major_boundary_and_refresh_preserve_record_count(self):
        self.start()
        self.assertIn('<strong>ACCEPT</strong>', self.request()[2])
        for count in range(1, 5):
            status, location, _ = self.request('POST', '/record', severity='major', description=f'Defect {count}')
            self.assertEqual((status, location), (303, '/'))
            expected = 'ACCEPT' if count <= 3 else 'REJECT'
            for _ in range(2):
                page = self.request()[2]
                self.assertIn(f'<strong>{expected}</strong>', page)
                self.assertEqual(page.count('<li>'), count)

    def test_repeat_start_does_not_erase_existing_inspection(self):
        self.start()
        self.request('POST', '/record', severity='critical', description='Unsafe item')
        status, _, page = self.request('POST', '/start', batch_id='REPLACEMENT', sample_size='160')
        self.assertEqual(status, 409)
        self.assertIn('BATCH-45', page)
        self.assertIn('Unsafe item', page)
        self.assertIn('<strong>REJECT</strong>', page)

    def test_invalid_start_inputs_do_not_create_an_inspection(self):
        for size in ['0', '-1', '1.5', 'abc', '']:
            with self.subTest(size=size):
                self.request('POST', '/start', batch_id='TEST', sample_size=size)
                self.assertIsNone(web_app.current_inspection)
        self.request('POST', '/start', batch_id=' ', sample_size='45')
        self.assertIsNone(web_app.current_inspection)

    def test_invalid_defects_do_not_change_verdict_or_records(self):
        self.start()
        for severity, description in [('low', 'Scratch'), ('major', ' ')]:
            self.request('POST', '/record', severity=severity, description=description)
            self.assertEqual(web_app.current_inspection.defects, [])
            self.assertIn('<strong>ACCEPT</strong>', self.request()[2])

    def test_record_before_start_and_html_escaping(self):
        page = self.request('POST', '/record', severity='major', description='Scratch')[2]
        self.assertIn('Start an inspection before recording defects.', page)
        self.assertIsNone(web_app.current_inspection)
        self.request('POST', '/start', batch_id='<script>batch</script>', sample_size='45')
        self.request('POST', '/record', severity='minor', description='<script>defect</script>')
        page = self.request()[2]
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;script&gt;batch&lt;/script&gt;', page)
        self.assertIn('&lt;script&gt;defect&lt;/script&gt;', page)


if __name__ == '__main__':
    unittest.main()
