"""Run a DT lll checkpoint on CPU."""
import argparse, torch
from model import TinyTransformer

def main():
    p=argparse.ArgumentParser(); p.add_argument("--checkpoint",required=True); p.add_argument("--prompt",required=True); p.add_argument("--max-new-tokens",type=int,default=160); p.add_argument("--temperature",type=float,default=.7); p.add_argument("--top-k",type=int,default=40); p.add_argument("--quantize",choices=["none","int8"],default="none"); args=p.parse_args()
    model,tok,_=TinyTransformer.from_checkpoint(args.checkpoint); model.eval()
    if args.quantize=="int8": model=torch.ao.quantization.quantize_dynamic(model,{torch.nn.Linear},dtype=torch.qint8)
    ids=torch.tensor([tok.encode(f"User: {args.prompt}\nAssistant:",add_eos=False)],dtype=torch.long)
    with torch.no_grad():
        for _ in range(args.max_new_tokens):
            x=ids[:,-model.cfg.context_length:]; logits,_=model(x); logits=logits[:,-1,:]/max(args.temperature,1e-5); values,indices=torch.topk(logits,args.top_k); probs=torch.softmax(values,dim=-1); next_id=indices.gather(-1,torch.multinomial(probs,1)); ids=torch.cat([ids,next_id],dim=1)
            if next_id.item()==tok.EOS: break
    print(tok.decode(ids[0].tolist()))
if __name__=="__main__": main()
