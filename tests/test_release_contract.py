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
        self.assertEqual(manifest['version'], '0.1.2-ux.1')
        self.assertNotIn('signature', manifest['integrity'])
        self.assertEqual(manifest['agent']['triggers']['events'], ['inbox.new_message'])
        self.assertTrue((BUNDLE / manifest['agent']['instructions']).is_file())

    def test_agent_contract_and_historical_screenshots_are_unchanged(self):
        prior = json.loads((ROOT / 'review/RELEASE.json').read_text())['release_files_sha256']
        for name in ('AGENT.md', 'tools.json', 'skills/incoming-mail-triage/SKILL.md',
                     'skills/incoming-mail-triage/manifest.json',
                     'screenshots/01-main.png', 'screenshots/02-chat.png'):
            self.assertEqual(hashlib.sha256((BUNDLE / name).read_bytes()).hexdigest(), prior[name], name)

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
