"""Generate a continuation using a trained MIME-ID checkpoint."""
import argparse

import torch

from model import BOS_ID, EOS_ID, ModelConfig, TinyLanguageModel


@torch.no_grad()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="checkpoints/best.pt")
    parser.add_argument("--prompt", default="Bahasa Indonesia adalah")
    parser.add_argument("--max-new-tokens", type=int, default=200)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--top-k", type=int, default=40)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "mps"])
    args = parser.parse_args()

    if args.device == "auto":
        device = "cuda" if torch.cuda.is_available() else (
            "mps" if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() else "cpu"
        )
    else:
        device = args.device
    device = torch.device(device)

    checkpoint = torch.load(args.checkpoint, map_location=device, weights_only=False)
    config = ModelConfig(**checkpoint["config"])
    model = TinyLanguageModel(config).to(device)
    model.load_state_dict(checkpoint["model"])
    model.eval()

    prompt_ids = list(args.prompt.encode("utf-8"))
    idx = torch.tensor([[BOS_ID, *prompt_ids]], dtype=torch.long, device=device)

    for _ in range(args.max_new_tokens):
        context = idx[:, -config.block_size:]
        logits, _ = model(context)
        logits = logits[:, -1, :] / max(args.temperature, 1e-5)
        logits[:, EOS_ID] = -float("inf")  # EOS is reserved for document boundaries.
        logits[:, BOS_ID] = -float("inf")  # Do not emit a new document-start marker.
        if args.top_k > 0:
            k = min(args.top_k, logits.size(-1))
            values, _ = torch.topk(logits, k)
            logits[logits < values[:, [-1]]] = -float("inf")
        probs = torch.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1)
        idx = torch.cat((idx, next_id), dim=1)

    generated = idx[0, len(prompt_ids) + 1:].tolist()
    output_bytes = bytes(token for token in generated if 0 <= token <= 255)
    print(args.prompt + output_bytes.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
