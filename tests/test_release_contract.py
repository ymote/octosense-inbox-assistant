import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'bundle'
def read(name): return json.loads((BUNDLE / name).read_text())

class ReleaseContract(unittest.TestCase):
    def test_notification_only_accepts_the_admitted_template(self):
        tool = next(t for t in read('tools.json')['tools'] if t['name'] == 'inboxassistant.notify')
        schema = tool['input_schema']
        self.assertEqual(tool['host_method'], 'glance.publish')
        self.assertFalse(schema['additionalProperties'])
        self.assertEqual(schema['properties']['template']['enum'], ['glance-workspace.splash'])
        self.assertEqual(set(schema['required']), {'card_id', 'title', 'summary', 'template', 'initial', 'notify'})
        self.assertTrue({'source', 'script', 'data'}.isdisjoint(schema['properties']))
        self.assertTrue((BUNDLE / 'glance-workspace.splash').is_file())

    def test_initial_payload_has_no_account_or_runtime_override(self):
        schema = next(t for t in read('tools.json')['tools'] if t['name'] == 'inboxassistant.notify')['input_schema']
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
        self.assertEqual(manifest['version'], '0.2.1')
        self.assertNotIn('signature', manifest['integrity'])
        self.assertEqual(manifest['agent']['triggers']['events'], ['inboxassistant.new_message'])
        self.assertTrue((BUNDLE / manifest['agent']['instructions']).is_file())

    def test_agent_tools_follow_fresh_identity_without_changing_host_methods(self):
        manifest = read('manifest.json')
        self.assertEqual(manifest['id'], 'io.github.ymote.inboxassistant')
        names = {t['name'] for t in read('tools.json')['tools']}
        self.assertTrue(all(n.startswith('inboxassistant.') for n in names))
        self.assertEqual(manifest['agent']['triggers']['events'], ['inboxassistant.new_message'])
        skill = read('skills/incoming-mail-triage/manifest.json')
        self.assertTrue(set(skill['uses']).issubset(names))
        source = (ROOT / 'src/workspace.splash').read_text()
        self.assertIn('inboxassistant.draft_edit', source)
        self.assertNotIn('with inbox.message', source)

    def test_app_and_glance_are_generated_from_the_same_current_source(self):
        # Generate in isolation: a stale template must fail without changing
        # the checked-in bundle, manifest authority or historical signature.
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / 'src').mkdir()
            (target / 'bundle').mkdir()
            for name in ('build_bundle.py', 'src/workspace.splash', 'bundle/manifest.json'):
                shutil.copyfile(ROOT / name, target / name)
            subprocess.run([sys.executable, str(target / 'build_bundle.py')], check=True)
            for name in ('main.splash', 'glance-workspace.splash'):
                self.assertEqual((target / 'bundle' / name).read_bytes(), (BUNDLE / name).read_bytes(), name)
            self.assertLessEqual((target / 'bundle/glance-workspace.splash').stat().st_size, 14 * 1024)

if __name__ == '__main__': unittest.main()
