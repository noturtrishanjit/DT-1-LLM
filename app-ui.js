const list=document.querySelector('#messageList');
const form=document.querySelector('#chatForm');
const input=document.querySelector('#chatInput');
const count=document.querySelector('#messageCount');
const sideDot=document.querySelector('#sideDot');
const sideStatus=document.querySelector('#sideStatus');
const sideModel=document.querySelector('#sideModel');
const pill=document.querySelector('#backendPill');
const modelName=document.querySelector('#modelName');
const inspectorModel=document.querySelector('#inspectorModel');
const healthText=document.querySelector('#healthText');
const healthMeter=document.querySelector('#healthMeter');
const storeKey='dt-lll-workspace-history-v1';
let messages=JSON.parse(localStorage.getItem(storeKey)||'[]');
function save(){localStorage.setItem(storeKey,JSON.stringify(messages))}
function updateCount(){count.textContent=`${messages.length} message${messages.length===1?'':'s'}`}
function render(){list.innerHTML='';if(!messages.length){list.innerHTML='<div class="empty-state"><strong>Your local AI workspace.</strong>Ask DT lll for a clear explanation, a math solution, a beginner Java example, or a friendly conversation.</div>'}else{for(const m of messages){const el=document.createElement('div');el.className=`message ${m.role==='user'?'user':'bot'}`;el.textContent=m.content;list.appendChild(el)}}updateCount();list.scrollTop=list.scrollHeight}
function add(role,content){messages.push({role,content,at:new Date().toISOString()});save();render()}
async function send(text){text=text.trim();if(!text)return;add('user',text);input.value='';input.style.height='auto';const thinking=document.createElement('div');thinking.className='message bot thinking';thinking.textContent='DT lll is thinking locally…';list.appendChild(thinking);list.scrollTop=list.scrollHeight;try{const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:text,max_new_tokens:Number(document.querySelector('#lengthSelect').value),temperature:Number(document.querySelector('#tempSelect').value)})});const data=await res.json();thinking.remove();if(!res.ok)throw new Error(data.error||'The local DT lll server returned an error.');add('assistant',data.answer||'DT lll returned no text.')}catch(err){thinking.remove();add('assistant',`I could not reach DT lll. Start the local server first.\n\nDetails: ${err.message}`)}}
form.addEventListener('submit',e=>{e.preventDefault();send(input.value)});
input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();form.requestSubmit()}});
input.addEventListener('input',()=>{input.style.height='auto';input.style.height=Math.min(input.scrollHeight,140)+'px'});
document.querySelectorAll('[data-prompt]').forEach(b=>b.addEventListener('click',()=>send(b.dataset.prompt)));
document.querySelector('#newChat').addEventListener('click',()=>{if(messages.length&&!confirm('Start a new conversation and clear this local transcript?'))return;messages=[];save();render();input.focus()});
document.querySelector('#clearChat').addEventListener('click',()=>{if(!messages.length)return;if(confirm('Clear this local conversation?')){messages=[];save();render()}});
document.querySelector('#exportChat').addEventListener('click',()=>{const text=messages.map(m=>`${m.role==='user'?'You':'DT lll'}:\n${m.content}`).join('\n\n');const blob=new Blob([text||'No messages yet.'],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='dt-lll-conversation.txt';a.click();URL.revokeObjectURL(a.href)});
async function health(){try{const res=await fetch('/api/health');const data=await res.json();const ok=res.ok&&data.ok!==false;sideDot.classList.toggle('ok',ok);pill.classList.toggle('ok',ok);pill.innerHTML=`<i></i> ${ok?'DT lll connected':'Backend offline'}`;sideStatus.textContent=ok?'DT lll connected':'Backend offline';const name=data.model||'Pure DT lll checkpoint';sideModel.textContent=name;modelName.textContent=name;inspectorModel.textContent=name;healthText.textContent=ok?'online':'offline';healthMeter.style.width=ok?'100%':'15%'}catch(e){sideDot.classList.remove('ok');pill.classList.remove('ok');pill.innerHTML='<i></i> Backend offline';sideStatus.textContent='Backend offline';sideModel.textContent='Run server.py';healthText.textContent='offline';healthMeter.style.width='15%'}}
render();health();setInterval(health,5000);
