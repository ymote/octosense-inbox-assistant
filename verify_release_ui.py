#!/usr/bin/env python3
"""Verify genuine release install/update/local-state retention in an owned hidden Mac shell.
Requires a private test mirror prepared by prepare_release_test.py. Uses only
synthetic local drafts: no provider login, model call, email send or calendar write.
The local catalog uses an ephemeral test authority, not production admission.
"""
import argparse,hashlib,json,os,re,shutil,subprocess,time,urllib.parse,urllib.request
from pathlib import Path
class BaseInstance:
    def __init__(self,binary,base,profile,out,launch='apphub'):
        self.out=out;out.mkdir();self.log=(out/'native.log').open('w+')
        env={k:v for k,v in os.environ.items() if k in ('PATH','HOME','LANG','LC_ALL','TMPDIR')}
        env.update(MAKEPAD_HIDE_WINDOWS='1',SANDBOX_MUTE='1',MAKEPAD_WM_TEST_APP=launch,
          OCTOSENSE_HOME=str(profile/'shell'),OCTOSENSE_APP_DATA=str(profile/'apps'),
          OCTOS_APP_CORE_DIR=str(profile/'core'),OCTOSENSE_HUB=str(base/'mirror'),
          OCTOSENSE_HUB_ANCHOR=(base/'anchor-public.txt').read_text().strip(),OCTOSENSE_HUB_CATALOG='legacy')
        self.child=subprocess.Popen([str(binary),'--remote'],env=env,stdout=self.log,stderr=self.log,start_new_session=True)
        self.endpoint=None
        try:
            until=time.monotonic()+45
            while time.monotonic()<until:
                self.alive();text=(out/'native.log').read_text(errors='replace')
                m=re.search(r'listening on (127\.0\.0\.1:\d+)',text)
                if m:self.endpoint='http://'+m[1];break
                time.sleep(.15)
            if not self.endpoint:raise RuntimeError('owned instrument did not start')
        except BaseException:self.stop();raise
    def alive(self):
        if self.child.poll() is not None:raise RuntimeError('owned shell exited unexpectedly')
    def call(self,path,**q):
        self.alive()
        suffix='?'+urllib.parse.urlencode(q) if q else ''
        try:
            with urllib.request.urlopen(self.endpoint+path+suffix,timeout=15) as r:data=json.load(r)
        except urllib.error.HTTPError as error:
            body=error.read().decode(errors='replace')
            if path=='/snap' and error.code==404:raise
            raise RuntimeError('native instrument HTTP '+str(error.code)+': '+body) from error
        if 'err' in data:raise RuntimeError('native instrument: '+data['err'])
        return data
    def rows(self):
        return [r for r in self.call('/snap')['s'] if r.get('ty')!='Splash' and len(r.get('r',[]))==4 and r['r'][2]>0 and r['r'][3]>0]
    def find(self,*,text=None,widget=None,kind=None,timeout=20):
        until=time.monotonic()+timeout
        while time.monotonic()<until:
            try:
                snapshot=self.rows()
            except urllib.error.HTTPError as error:
                if error.code!=404:raise
                self.alive();time.sleep(.12);continue
            rows=[r for r in snapshot if (text is None or r.get('t')==text) and (widget is None or r.get('i')==widget) and (kind is None or r.get('ty')==kind) and r.get('enabled',True)]
            if len(rows)==1:return rows[0]
            if len(rows)>1:raise AssertionError('ambiguous visible widget '+str((text,widget,kind)))
            time.sleep(.12)
        raise AssertionError('missing visible widget '+str((text,widget,kind)))
    def click(self,wait=0,**criteria):
        r=self.find(**criteria);x,y,w,h=r['r'];self.call('/click',x=x+w/2,y=y+min(h/2,18),w=r.get('w',0),wait=wait)
    def scroll_find(self,dy,**criteria):
        for _ in range(8):
            try:return self.find(timeout=.4,**criteria)
            except AssertionError as error:
                if 'missing visible widget' not in str(error):raise
            self.call('/m',k='scroll',x=700,y=550,dy=dy,precise=1,w=0,wait=0)
        return self.find(**criteria)
    def confirm_install(self):
        self.scroll_find(360,widget='confirm',kind='Button')
        self.click(widget='confirm',kind='Button',wait=0)
    def open_installed(self):
        self.scroll_find(-360,text='Open',kind='Button')
        self.click(text='Open',kind='Button')
    def type(self,widget,text):
        self.click(widget=widget,kind='TextInput');self.call('/t',t=text,wait=0)
    def label(self,text):return self.find(text=text,kind='Label')
    def capture(self,name):
        deadline=time.monotonic()+8
        while True:
            try:data=self.call('/g');break
            except RuntimeError as error:
                if 'grab frame could not be submitted at arming; retry' not in str(error) or time.monotonic()>=deadline:raise
                self.alive();time.sleep(.2)
        source=Path(data['png']);shutil.copyfile(source,self.out/(name+'.png'))
        (self.out/(name+'.snapshot.json')).write_text(json.dumps(self.rows(),indent=2)+'\n')
    def stop(self):
        if hasattr(self,'_stop_result'):return self._stop_result
        requested=self.child.poll() is None
        forced=False
        if requested:
            if self.endpoint:
                try:self.call('/quit')
                except Exception:pass
            try:self.child.wait(timeout=8)
            except subprocess.TimeoutExpired:
                forced=True;self.child.terminate()
                try:self.child.wait(timeout=5)
                except subprocess.TimeoutExpired:self.child.kill();self.child.wait(timeout=5)
        self.log.close()
        self._stop_result=requested and not forced and self.child.returncode==0
        return self._stop_result

class Instance(BaseInstance):
 def many(self,text):
  until=time.monotonic()+10
  while time.monotonic()<until:
   rows=[r for r in self.rows() if r.get('t')==text]
   if rows:return rows
   time.sleep(.1)
  raise AssertionError('missing '+text)
 def click_index(self,text,index):
  r=self.many(text)[index];x,y,w,h=r['r'];self.call('/click',x=x+w/2,y=y+min(h/2,18),wait=0)
 def message(self,subject):
  for _ in range(8):
   rows=self.rows();titles=[r for r in rows if r.get('t')==subject]
   if len(titles)==1:
    y=titles[0]['r'][1];buttons=[r for r in rows if r.get('t')=='Open message' and y<r['r'][1]<y+160]
    if buttons:
     r=min(buttons,key=lambda x:x['r'][1]);x,y,w,h=r['r'];self.call('/click',x=x+w/2,y=y+min(h/2,18),wait=0);return
   self.call('/m',k='scroll',x=700,y=550,dy=220,precise=1,w=0,wait=0)
   time.sleep(.1)
  raise AssertionError('message action not reachable')
 def contains(self,text):
  until=time.monotonic()+10
  while time.monotonic()<until:
   if any(text in r.get('t','') for r in self.rows()):return
   time.sleep(.1)
  raise AssertionError('missing text '+text)
 def visible(self,widget):
  for dy in (-320,320):
   for _ in range(8):
    try:
     r=self.find(widget=widget,kind='TextInput',timeout=.15)
     if r['r'][3]>=35:return r
    except AssertionError:pass
    self.call('/m',k='scroll',x=700,y=550,dy=dy,precise=1,w=0,wait=0)
  return self.find(widget=widget,kind='TextInput')
 def value(self,widget):
  r=self.find(widget=widget,kind='TextInput');return r.get('val',r.get('t'))
 def replace(self,widget,value):
  self.visible(widget);self.click(widget=widget,kind='TextInput')
  self.call('/k',k='press',c='KeyA',cmd=1,wait=0);self.call('/t',t=value,wait=0)
  until=time.monotonic()+5
  while time.monotonic()<until:
   if self.value(widget)==value:return
   time.sleep(.1)
  raise AssertionError('native input differs: '+widget)
 def decline(self,profile,app,y,name):
  path=profile/'shell/approvals/consent.json'
  choices=json.loads(path.read_text())['apps'] if path.exists() else {}
  if app in choices:
   assert choices[app]['allowed'] is False;return
  self.capture(name)
  window=self.call('/s')['w'];assert len(window)==1
  w,h=window[0]['sz'];assert abs(w/h-1400/900)<.01
  self.call('/click',x=w*.375,y=h*y,w=window[0]['i'],wait=0)
  until=time.monotonic()+5
  while time.monotonic()<until:
   if path.exists():
    choices=json.loads(path.read_text())['apps']
    if app in choices:
     assert choices[app]['allowed'] is False;return
   time.sleep(.1)
  raise AssertionError('native decline did not record intended app: '+app)
INBOX_BODY='Please deliver Thursday at 10:30 AM Pacific.\nRing the bell twice. 谢谢。'
CALENDAR={'e_title':'Synthetic planning session','e_date':'2026-10-15','e_time':'10:30','e_end_date':'2026-10-15','e_end_time':'11:00','e_zone':'America/Los_Angeles','e_place':'Fictional meeting room','e_notes':'Bring synthetic planning notes.\nNo real calendar write.'}
def exercise(i,app,existing,checks):
 if app=='inbox':
  i.contains('Fictional inbox');i.message('Choose your refrigerator delivery window');i.contains('Choose your refrigerator delivery window');i.click(text='Compose reply',kind='Button')
  if existing:assert i.value('reply_body')==INBOX_BODY;checks.append('exact_multiline_unicode_reply_retained')
  else:i.replace('reply_body',INBOX_BODY);checks.append('fictional_reply_edited')
  i.click(widget='chat_tab',kind='Button');i.contains("Chat with this account's Inbox agent")
  i.click(widget='reply_tab',kind='Button');assert i.value('reply_body')==INBOX_BODY
  i.click(text='Review & Send',kind='Button');i.contains('Fictional draft saved')
  checks.extend(['reply_chat_share_exact_saved_local_draft','fictional_send_refused_without_provider'])
  i.capture('app-reply')
 else:
  i.contains('Connect Google')
  i.click(text='Resume draft' if existing else '+ Event',kind='Button')
  if existing:
   for key,value in CALENDAR.items():i.visible(key);assert i.value(key)==value
   checks.append('exact_complete_event_draft_retained')
  else:
   for key,value in CALENDAR.items():i.replace(key,value)
   checks.append('complete_local_event_draft_edited')
  i.visible('e_title');i.capture('app-event')
  i.click(text='Review & Save',kind='Button');i.contains('Keep this draft, then connect Google and choose a calendar.')
  checks.append('provider_write_without_account_refused')
  i.click(text='Keep draft',kind='Button');i.contains('Draft retained.')
def main():
 p=argparse.ArgumentParser();p.add_argument('--app',choices=['inbox','calendar'],required=True);p.add_argument('--binary',type=Path,required=True);p.add_argument('--source',required=True);p.add_argument('--mirror',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--first-only',action='store_true');a=p.parse_args()
 names={'inbox':('io.github.ymote.inboxassistant','Inbox Assistant'),'calendar':('io.github.ymote.googlecalendar','Google Calendar')};app,name=names[a.app]
 a.out.mkdir(mode=0o700,parents=True,exist_ok=False);profile=a.out/'profile';profile.mkdir(mode=0o700)
 clients=profile/'apps/.host/oauth/clients.json';clients.parent.mkdir(parents=True);clients.write_text('{}\n')
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 receipt={'schema':1,'app_id':app,'platform':'macOS','shell_source':a.source,'shell_binary_sha256':sha(a.binary),'catalog_authority':'ephemeral-local-legacy-not-production-v2','publisher_proof':'genuine-GitHub-tag-push','live_authentication':False,'provider_writes':False,'model_calls':False,'personal_data_used':False,'checks':[],'versions':[],'visual_review':'pending','status':'running'}
 receipt['inputs']=json.loads((a.mirror/'prepare-receipt.json').read_text())['releases'];active=None
 try:
  for idx,version in enumerate(['0.2.0'] if a.first_only else ['0.2.0','0.2.1','0.2.1']):
   if idx<2:shutil.copyfile(a.mirror/('catalog-v'+version+'.json'),a.mirror/'mirror/catalog.json')
   active=Instance(a.binary,a.mirror,profile,a.out/['first','update','restart'][idx])
   active.label(name)
   if idx==0:active.decline(profile,'apphub',.690,'00-hub-agent-consent');receipt['checks'].append('optional_hub_agent_declined')
   if idx<2:
    active.click(widget='search_tab',kind='Button');active.type('search',name);active.label(name);active.capture('01-search')
    active.click(text='Get' if idx==0 else 'Update',kind='Button');active.confirm_install();active.open_installed()
   else:active.click(widget='library',kind='Button');active.click(text='Open',kind='Button')
   active.contains('Fictional inbox' if a.app=='inbox' else 'Connect Google')
   choices=json.loads((profile/'shell/approvals/consent.json').read_text())['apps']
   assert app not in choices or choices[app]['allowed'] is False
   installed=profile/'apps/.bundles'/app/'bundle/manifest.json';data=json.loads(installed.read_text());assert data['version']==version
   genuine=json.loads((a.mirror/'verified'/('v'+version)/'manifest.json').read_text())
   assert data['integrity']['github']==genuine['integrity']['github'];receipt['checks'].append(['search_install_open_genuine_first_release','search_install_open_genuine_update','reopen_updated_app_from_library'][idx]);receipt['versions'].append(version)
   stage=[];exercise(active,a.app,idx>0,stage);receipt['checks'].extend([['first','update','restart'][idx]+':'+x for x in stage])
   assert active.stop();active=None
  receipt['status']='passed'
 except BaseException as error:
  receipt['status']='failed';receipt['error']=str(error)
  if active:
   try:active.capture('failure')
   except Exception:pass
  raise
 finally:
  receipt['owned_processes_stopped']=active.stop() if active else True
  (a.out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'status':receipt['status'],'checks':len(receipt['checks']),'owned_processes_stopped':receipt['owned_processes_stopped']}))
if __name__=='__main__':main()
