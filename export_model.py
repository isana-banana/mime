"""Export a MIME-ID 300K checkpoint to the Android float32 asset format."""
import argparse
import struct
import torch

NAMES = ["token_embedding.weight", "position_embedding.weight"]
for i in range(3):
    NAMES += [
        f"blocks.{i}.ln1.weight", f"blocks.{i}.ln1.bias",
        f"blocks.{i}.attn.qkv.weight", f"blocks.{i}.attn.qkv.bias",
        f"blocks.{i}.attn.proj.weight", f"blocks.{i}.attn.proj.bias",
        f"blocks.{i}.ln2.weight", f"blocks.{i}.ln2.bias",
        f"blocks.{i}.mlp.net.0.weight", f"blocks.{i}.mlp.net.0.bias",
        f"blocks.{i}.mlp.net.2.weight", f"blocks.{i}.mlp.net.2.bias",
    ]
NAMES += ["final_norm.weight", "final_norm.bias"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoint")
    parser.add_argument("output")
    args = parser.parse_args()
    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    expected = {"vocab_size": 258, "block_size": 128, "n_embd": 96,
                "n_layer": 3, "n_head": 4, "n_ff": 256, "dropout": 0.1}
    if checkpoint["config"] != expected:
        raise ValueError(f"Unexpected model config: {checkpoint['config']}")
    if checkpoint["parameter_count"] != 298656:
        raise ValueError("Checkpoint is not the expected 298,656-parameter model.")
    state = checkpoint["model"]
    with open(args.output, "wb") as output:
        output.write(b"MIME300K")
        output.write(struct.pack(">I", len(NAMES)))
        for name in NAMES:
            tensor = state[name].detach().cpu().float().contiguous()
            raw = tensor.numpy().astype(">f4", copy=False).tobytes()
            output.write(struct.pack(">I", tensor.numel()))
            output.write(raw)
    print(f"Exported {len(NAMES)} tensors from step {checkpoint['step']} to {args.output}")

if __name__ == "__main__":
    main()
