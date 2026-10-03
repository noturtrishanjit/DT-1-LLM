const log=document.querySelector('#chatLog');
const form=document.querySelector('#chatForm');
const input=document.querySelector('#chatInput');
const trainForm=document.querySelector('#trainForm');
const trainSteps=document.querySelector('#trainSteps');
const trainStatus=document.querySelector('#trainStatus');
const trainLog=document.querySelector('#trainLog');
function add(text,kind){const node=document.createElement('div');node.className=`bubble ${kind}`;node.textContent=text;log.appendChild(node);log.scrollTop=log.scrollHeight}
async function send(text){if(!text.trim())return;add(text,'user');input.value='';const thinking=document.createElement('div');thinking.className='bubble bot';thinking.textContent='The local model is thinking…';log.appendChild(thinking);try{const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:text,max_new_tokens:320})});const data=await res.json();thinking.remove();add(data.answer||data.error||'The model returned no text.','bot')}catch(err){thinking.remove();add('Could not reach the local model server. Start the selected launcher first.','bot')}}
form?.addEventListener('submit',e=>{e.preventDefault();send(input.value)});
document.querySelectorAll('[data-prompt]').forEach(b=>b.addEventListener('click',()=>send(b.dataset.prompt)));
async function refreshStatus(){if(!trainStatus)return;try{const data=await (await fetch('/api/status')).json();if(data.backend==='llama.cpp'){trainStatus.textContent=`Local pretrained backend ready · ${data.model||'Qwen'}`;const head=document.querySelector('.chat-head span:last-child');if(head)head.textContent='LOCAL MODEL';const note=document.querySelector('.demo-note');if(note)note.textContent='● Local pretrained model · prompts stay on this computer'}else{trainStatus.textContent=data.running?`Training active · PID ${data.pid}`:`Ready · checkpoint step ${data.step??'unknown'} · loss ${data.loss?Number(data.loss).toFixed(4):'unknown'}`;trainLog.textContent=data.log||'No training log yet.'}}catch(e){trainStatus.textContent='Server offline — start a DT lll launcher'}}
trainForm?.addEventListener('submit',async e=>{e.preventDefault();const steps=Math.max(1,Number(trainSteps.value||300));const res=await fetch('/api/train',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({steps})});const data=await res.json();trainStatus.textContent=data.error||`Training started · PID ${data.pid}`;refreshStatus()});
document.querySelector('#stopTraining')?.addEventListener('click',async()=>{await fetch('/api/train/stop',{method:'POST'});refreshStatus()});
setInterval(refreshStatus,3000);refreshStatus();
