"""Export a MIME-ID 300K checkpoint to the Android float32 asset format."""
import argparse
import struct
from pathlib import Path
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

EXPECTED_SHAPES = {
    "token_embedding.weight": (258, 96),
    "position_embedding.weight": (128, 96),
    "final_norm.weight": (96,),
    "final_norm.bias": (96,),
}
for i in range(3):
    EXPECTED_SHAPES.update({
        f"blocks.{i}.ln1.weight": (96,),
        f"blocks.{i}.ln1.bias": (96,),
        f"blocks.{i}.attn.qkv.weight": (288, 96),
        f"blocks.{i}.attn.qkv.bias": (288,),
        f"blocks.{i}.attn.proj.weight": (96, 96),
        f"blocks.{i}.attn.proj.bias": (96,),
        f"blocks.{i}.ln2.weight": (96,),
        f"blocks.{i}.ln2.bias": (96,),
        f"blocks.{i}.mlp.net.0.weight": (256, 96),
        f"blocks.{i}.mlp.net.0.bias": (256,),
        f"blocks.{i}.mlp.net.2.weight": (96, 256),
        f"blocks.{i}.mlp.net.2.bias": (96,),
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoint")
    parser.add_argument("output")
    args = parser.parse_args()

    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    expected = {"vocab_size": 258, "block_size": 128, "n_embd": 96,
                "n_layer": 3, "n_head": 4, "n_ff": 256, "dropout": 0.1}
    if checkpoint.get("config") != expected:
        raise ValueError(f"Unexpected model config: {checkpoint.get('config')}")
    if checkpoint.get("parameter_count") != 298656:
        raise ValueError("Checkpoint is not the expected 298,656-parameter model.")
    if int(checkpoint.get("step", 0)) < 1:
        raise ValueError("Checkpoint has no completed training step.")

    state = checkpoint["model"]
    missing = [name for name in NAMES if name not in state]
    if missing:
        raise ValueError(f"Checkpoint is missing tensors: {missing}")
    for name, shape in EXPECTED_SHAPES.items():
        actual = tuple(state[name].shape)
        if actual != shape:
            raise ValueError(f"Unexpected shape for {name}: {actual}, expected {shape}")
        if not torch.isfinite(state[name]).all():
            raise ValueError(f"Non-finite values found in tensor {name}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as output:
        output.write(b"MIME300K")
        output.write(struct.pack(">I", len(NAMES)))
        for name in NAMES:
            tensor = state[name].detach().cpu().float().contiguous()
            raw = tensor.numpy().astype(">f4", copy=False).tobytes()
            output.write(struct.pack(">I", tensor.numel()))
            output.write(raw)

    expected_bytes = 12 + sum(4 + 4 * torch.tensor(EXPECTED_SHAPES[name]).prod().item() for name in NAMES)
    actual_bytes = output_path.stat().st_size
    if actual_bytes != expected_bytes:
        raise RuntimeError(f"Export size mismatch: {actual_bytes} != {expected_bytes}")
    print(f"Exported {len(NAMES)} validated tensors from training step {checkpoint['step']} "
          f"to {output_path} ({actual_bytes} bytes)")


if __name__ == "__main__":
    main()
