#!/usr/bin/env python3
"""Create an isolated, explicitly legacy test catalog from genuine keyless packs.
No production catalog or application profile is touched. No developer key is used.
Ephemeral Hub-only keys are destroyed after signing both local snapshots.
"""
import argparse, hashlib, json, os, shutil, subprocess
from pathlib import Path

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    a=argparse.ArgumentParser();a.add_argument('--hub',type=Path,required=True);a.add_argument('--source',required=True)
    a.add_argument('--versions',nargs='+',default=['v0.2.0','v0.2.1']);a.add_argument('--packs',type=Path,required=True);a.add_argument('--out',type=Path,required=True);v=a.parse_args()
    root=v.out.resolve();root.mkdir(mode=0o700,parents=True,exist_ok=False)
    mirror=root/'mirror';mirror.mkdir();sources=root/'verified';sources.mkdir();keys=root/'ephemeral-hub-keys';keys.mkdir(mode=0o700)
    steps=[]
    def run(*args):
        p=subprocess.run([str(v.hub.resolve()),*map(str,args)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
        if p.returncode: raise RuntimeError('native hub '+str(args[0])+' refused: '+p.stderr.decode(errors='replace').replace(str(root),'<owned-test-root>'))
        steps.append(str(args[0]));return p.stdout.decode().strip()
    receipt={'schema':1,'scope':'isolated-macos-ui-test-mirror','catalog_authority':'ephemeral-local-legacy-not-production-github-v2',
      'developer_key_used':False,'production_publication':False,'fixture_submission_issue':False,'hub_source':v.source,'hub_binary_sha256':digest(v.hub),'releases':[]}
    try:
        anchor=run('keygen',keys/'anchor.key');working=run('keygen',keys/'working.key')
        cert=run('certify','--anchor',keys/'anchor.key','--working',keys/'working.key')
        (root/'anchor-public.txt').write_text(anchor+'\n')
        for version in v.versions:
            pack=v.packs/version/'app.bundle.pack.json';bundle=sources/version
            run('publisher-unpack',pack,'--out',bundle);run('publisher-verify',bundle)
            manifest=json.loads((bundle/'manifest.json').read_text());g=manifest['integrity']['github']
            run('publish',bundle,'--catalog',mirror/'catalog.json','--out',mirror,
                '--publisher','github:'+g['repository_id'],'--repo','https://github.com/'+g['repository'],
                '--commit',g['commit'],'--anchor',anchor,'--key',keys/'working.key','--anchor-cert',cert)
            snapshot=root/('catalog-'+version+'.json');shutil.copyfile(mirror/'catalog.json',snapshot)
            entry=json.loads(snapshot.read_text())['entries'][-1]
            assert entry['manifest']['integrity']['github']==g
            receipt['releases'].append({'version':manifest['version'],'app_id':manifest['id'],
                'pack_sha256':digest(pack),'catalog_sha256':digest(snapshot),'source_commit':g['commit'],
                'full_github_proof_preserved':True})
        shutil.copyfile(root/('catalog-'+v.versions[0]+'.json'),mirror/'catalog.json')
        receipt['initial_catalog_sequence']=json.loads((mirror/'catalog.json').read_text())['sequence']
        receipt['update_catalog_sequence']=json.loads((root/('catalog-'+v.versions[-1]+'.json')).read_text())['sequence']
        receipt['prepared']=True
    finally:
        shutil.rmtree(keys)
        receipt['ephemeral_hub_private_keys_deleted']=not keys.exists()
        receipt['native_steps']=steps
        (root/'prepare-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'prepared':True,'releases':len(receipt['releases']),'ephemeral_hub_private_keys_deleted':True}))
if __name__=='__main__':main()
