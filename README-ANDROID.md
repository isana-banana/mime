# MIME Chat for Android

A minimal offline Android chat shell for the MIME-ID 100K byte-level Transformer. It runs the trained weights locally using a small Java CPU inference implementation; no network permission or server is required.

## Model
- Checkpoint: `best.pt`, step 9000, validation loss 1.4162
- 91,776 trainable parameters; vocab 258; context 128; 2 layers; 4 heads
- The Android workflow downloads the successful training artifact from run `45262581204`, then exports `best.pt` into `app/src/main/assets/mime100k.bin` before compiling.

## Build
Run `gradle assembleDebug` from this directory. The APK is written to `app/build/outputs/apk/debug/app-debug.apk`.

The model is a tiny next-byte language model, not an instruction-tuned assistant. Expect rough, sometimes incoherent output. This app is an experimental inference test, not a production chatbot.
