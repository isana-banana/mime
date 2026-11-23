"""Export MIME-ID PyTorch checkpoint to the compact float32 asset used by Android."""
import argparse, struct
import torch

NAMES = ["token_embedding.weight", "position_embedding.weight"]
for i in range(2):
    NAMES += [f"blocks.{i}.ln1.weight", f"blocks.{i}.ln1.bias",
              f"blocks.{i}.attn.qkv.weight", f"blocks.{i}.attn.qkv.bias",
              f"blocks.{i}.attn.proj.weight", f"blocks.{i}.attn.proj.bias",
              f"blocks.{i}.ln2.weight", f"blocks.{i}.ln2.bias",
              f"blocks.{i}.mlp.net.0.weight", f"blocks.{i}.mlp.net.0.bias",
              f"blocks.{i}.mlp.net.2.weight", f"blocks.{i}.mlp.net.2.bias"]
NAMES += ["final_norm.weight", "final_norm.bias"]

def main():
    p=argparse.ArgumentParser(); p.add_argument("checkpoint"); p.add_argument("output"); a=p.parse_args()
    ck=torch.load(a.checkpoint,map_location="cpu",weights_only=False)
    assert ck["config"] == {"vocab_size":258,"block_size":128,"n_embd":64,"n_layer":2,"n_head":4,"dropout":0.1}
    with open(a.output,"wb") as f:
        f.write(b"MIME100K")
        f.write(struct.pack(">I",len(NAMES)))
        for name in NAMES:
            t=ck["model"][name].detach().float().contiguous().view(-1)
            f.write(struct.pack(">I",t.numel()))
            f.write(struct.pack(">"+ "f"*t.numel(),*t.tolist()))
    print(f"Exported {len(NAMES)} tensors from step {ck['step']} to {a.output}")
if __name__=="__main__": main()
