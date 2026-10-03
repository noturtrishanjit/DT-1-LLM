"""Train DT lll on JSONL records: {prompt, response, kind?}."""
import argparse, json, math, random
from pathlib import Path
import torch
from torch.utils.data import Dataset, DataLoader
from model import ByteTokenizer, ModelConfig, TinyTransformer, count_parameters

class JsonlDataset(Dataset):
    def __init__(self, path, tokenizer, context_length):
        self.samples=[]; self.tokenizer=tokenizer; self.context_length=context_length
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            row=json.loads(line); text=f"User: {row['prompt']}\nAssistant: {row['response']}"
            ids=tokenizer.encode(text)[:context_length]
            if len(ids)>2: self.samples.append(torch.tensor(ids,dtype=torch.long))
        if not self.samples: raise ValueError("No usable JSONL records found")
    def __len__(self): return len(self.samples)
    def __getitem__(self,i):
        ids=self.samples[i]; x=ids[:-1]; y=ids[1:]
        return x,y

def collate(batch):
    n=max(len(x) for x,_ in batch); xs=torch.full((len(batch),n),258,dtype=torch.long); ys=torch.full((len(batch),n),-100,dtype=torch.long)
    for i,(x,y) in enumerate(batch): xs[i,:len(x)]=x; ys[i,:len(y)]=y
    return xs,ys

def main():
    p=argparse.ArgumentParser(); p.add_argument("--data",required=True); p.add_argument("--out",default="checkpoints/best.pt"); p.add_argument("--resume",default=None); p.add_argument("--steps",type=int,default=1000); p.add_argument("--batch-size",type=int,default=8); p.add_argument("--lr",type=float,default=3e-4); p.add_argument("--device",default="cpu"); p.add_argument("--d-model",type=int,default=256); p.add_argument("--n-heads",type=int,default=8); p.add_argument("--n-layers",type=int,default=4); p.add_argument("--d-ff",type=int,default=1024); p.add_argument("--seed",type=int,default=7); args=p.parse_args()
    random.seed(args.seed); torch.manual_seed(args.seed); device=torch.device(args.device)
    tok=ByteTokenizer(); cfg=ModelConfig(vocab_size=tok.vocab_size, d_model=args.d_model, n_heads=args.n_heads, n_layers=args.n_layers, d_ff=args.d_ff); model=TinyTransformer(cfg).to(device)
    start_step=1; resume_loss=math.inf
    if args.resume:
        ckpt=torch.load(args.resume,map_location=device,weights_only=False); model.load_state_dict(ckpt["model"]); start_step=int(ckpt.get("step",0))+1; resume_loss=float(ckpt.get("loss",math.inf)); print(f"resumed from step {start_step-1}")
    print(f"parameters: {count_parameters(model):,}")
    data=JsonlDataset(args.data,tok,cfg.context_length); loader=DataLoader(data,batch_size=args.batch_size,shuffle=True,collate_fn=collate); opt=torch.optim.AdamW(model.parameters(),lr=args.lr,weight_decay=0.1); it=iter(loader); best=resume_loss
    for step in range(start_step,args.steps+1):
        try: x,y=next(it)
        except StopIteration: it=iter(loader); x,y=next(it)
        x,y=x.to(device),y.to(device); model.train(); _,loss=model(x,y); opt.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
        if step==1 or step%50==0: print(f"step {step:>5} | loss {loss.item():.4f}")
        if loss.item()<best:
            best=loss.item(); Path(args.out).parent.mkdir(parents=True,exist_ok=True); torch.save({"config":cfg.__dict__,"model":model.state_dict(),"step":step,"loss":best},args.out)
    print(f"saved {args.out}")
if __name__=="__main__": main()
