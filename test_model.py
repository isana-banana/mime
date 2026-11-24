"""Smoke-test a trained MIME-ID checkpoint and print deterministic text samples."""
import argparse
import math
import torch
from model import BOS_ID, EOS_ID, ModelConfig, TinyLanguageModel

@torch.no_grad()
def generate(model, prompt, max_new_tokens=100, temperature=0.75, top_k=40):
    device = next(model.parameters()).device
    prompt_bytes = list(prompt.encode("utf-8"))
    idx = torch.tensor([[BOS_ID, *prompt_bytes]], dtype=torch.long, device=device)
    generated = []
    for _ in range(max_new_tokens):
        logits, _ = model(idx[:, -model.config.block_size:])
        logits = logits[:, -1, :] / temperature
        logits[:, BOS_ID] = -float("inf")
        if top_k:
            values, _ = torch.topk(logits, min(top_k, logits.size(-1)))
            logits[logits < values[:, [-1]]] = -float("inf")
        probs = torch.softmax(logits, dim=-1)
        next_token = int(torch.multinomial(probs, 1).item())
        if next_token == EOS_ID:
            break
        if not 0 <= next_token <= 255:
            raise RuntimeError(f"Unexpected generated token ID: {next_token}")
        generated.append(next_token)
        idx = torch.cat((idx, torch.tensor([[next_token]], device=device)), dim=1)
    raw = bytes(generated)
    decoded = raw.decode("utf-8", errors="replace")
    return decoded, decoded.count("\ufffd"), len(raw)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="checkpoints/best.pt")
    parser.add_argument("--expected-step", type=int, default=6000)
    args = parser.parse_args()
    torch.manual_seed(2026)
    ckpt = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    assert ckpt["parameter_count"] == 298656, ckpt.get("parameter_count")
    assert ckpt["step"] >= args.expected_step, ckpt.get("step")
    assert math.isfinite(ckpt["val_loss"]), ckpt.get("val_loss")
    config = ModelConfig(**ckpt["config"])
    model = TinyLanguageModel(config)
    model.load_state_dict(ckpt["model"], strict=True)
    model.eval()
    assert model.parameter_count() == 298656
    x = torch.tensor([[BOS_ID, *"Halo".encode("utf-8")]], dtype=torch.long)
    logits, _ = model(x)
    assert logits.shape == (1, x.shape[1], 258), logits.shape
    assert torch.isfinite(logits).all(), "Model produced non-finite logits"
    print(f"CHECKPOINT_OK step={ckpt['step']} params={model.parameter_count():,} val_loss={ckpt['val_loss']:.4f}")
    prompts = ["Halo, apa kabar?", "Saya sedang belajar", "Pada pagi hari", "Apa yang bisa kita lakukan hari ini?"]
    total_replacements, total_bytes = 0, 0
    for prompt in prompts:
        output, replacements, byte_count = generate(model, prompt)
        total_replacements += replacements
        total_bytes += byte_count
        print(f"\nPROMPT: {prompt}\nOUTPUT: {output}")
        print(f"UTF8_REPLACEMENTS: {replacements}/{byte_count} bytes")
    ratio = total_replacements / max(1, total_bytes)
    print(f"UTF8_REPLACEMENT_RATIO: {ratio:.4f}")
    if ratio > 0.10:
        raise RuntimeError("Too many invalid UTF-8 byte sequences in generated samples.")
    print("SMOKE_TEST_PASSED (technical only; human review is still required for fluency)")

if __name__ == "__main__":
    main()
