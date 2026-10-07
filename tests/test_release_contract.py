import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'bundle'
def read(name): return json.loads((BUNDLE / name).read_text())

class ReleaseContract(unittest.TestCase):
    def test_notification_only_accepts_the_admitted_template(self):
        tool = next(t for t in read('tools.json')['tools'] if t['name'] == 'inbox.notify')
        schema = tool['input_schema']
        self.assertEqual(tool['host_method'], 'glance.publish')
        self.assertFalse(schema['additionalProperties'])
        self.assertEqual(schema['properties']['template']['enum'], ['glance-workspace.splash'])
        self.assertEqual(set(schema['required']), {'card_id', 'title', 'summary', 'template', 'initial', 'notify'})
        self.assertTrue({'source', 'script', 'data'}.isdisjoint(schema['properties']))
        self.assertTrue((BUNDLE / 'glance-workspace.splash').is_file())

    def test_initial_payload_has_no_account_or_runtime_override(self):
        schema = next(t for t in read('tools.json')['tools'] if t['name'] == 'inbox.notify')['input_schema']
        initial = schema['properties']['initial']
        self.assertFalse(initial['additionalProperties'])
        self.assertEqual(set(initial['properties']), {'message'})
        self.assertEqual(initial['required'], ['message'])
        message = initial['properties']['message']
        self.assertFalse(message['additionalProperties'])
        self.assertEqual(set(message['required']), {'id', 'from', 'subject', 'body'})

    def test_tools_keep_private_account_scope_without_a_send_alias(self):
        tools = read('tools.json')['tools']
        for tool in tools:
            self.assertTrue(tool['private_data'])
            self.assertFalse(tool['shareable'])
            self.assertNotIn(tool['host_method'], ('gmail.send', 'gmail.draft.review', 'gmail.sheet.close'))
        manifest = read('manifest.json')
        self.assertEqual(manifest['version'], '0.1.1')
        self.assertEqual(manifest['agent']['triggers']['events'], ['inbox.new_message'])
        self.assertTrue((BUNDLE / manifest['agent']['instructions']).is_file())

    def test_ui_and_original_pixels_are_unchanged(self):
        prior = json.loads((ROOT / 'review/releases/0.1.0/RELEASE.json').read_text())['release_files_sha256']
        for name in ('main.splash', 'glance-workspace.splash', 'screenshots/01-main.png', 'screenshots/02-chat.png'):
            self.assertEqual(hashlib.sha256((BUNDLE / name).read_bytes()).hexdigest(), prior[name], name)

if __name__ == '__main__': unittest.main()
