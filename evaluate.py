"""Small smoke evaluator; pair with human review and javac for serious testing."""
import argparse,json,re,subprocess,tempfile
from pathlib import Path
import torch
from model import TinyTransformer

def generate(model,tok,prompt,max_new=120):
    ids=torch.tensor([tok.encode(f"User: {prompt}\nAssistant:",add_eos=False)])
    with torch.no_grad():
        for _ in range(max_new):
            logits,_=model(ids[:,-model.cfg.context_length:]); nxt=logits[:,-1,:].argmax(-1,keepdim=True); ids=torch.cat([ids,nxt],1)
            if nxt.item()==tok.EOS: break
    return tok.decode(ids[0].tolist()).split("Assistant:",1)[-1]

def main():
    p=argparse.ArgumentParser();p.add_argument("--checkpoint",required=True);p.add_argument("--data",required=True);args=p.parse_args();model,tok,_=TinyTransformer.from_checkpoint(args.checkpoint);model.eval();rows=[json.loads(x) for x in Path(args.data).read_text().splitlines() if x.strip()]; scores=[]
    for r in rows:
        out=generate(model,tok,r["prompt"]); answer=r["answer"].lower(); ok=answer in out.lower(); scores.append(ok); print(f"[{r.get('kind','general'):5}] {'PASS' if ok else 'MISS'} | {r['prompt']}\n  {out[:240].replace(chr(10),' ')}")
    print(f"\nsubstring score: {sum(scores)}/{len(scores)}")
if __name__=="__main__": main()
