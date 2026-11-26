import unittest

from curate_intisari_v4 import inspect_conversation, normalize_pronouns


class IntisariCurationTests(unittest.TestCase):
    def test_casual_pronouns_are_normalized_consistently(self):
        messages = [
            {"role": "user", "content": "Gue mau tanya, lo suka makan apa?"},
            {"role": "assistant", "content": "Gue suka nasi goreng, kalau lo?"},
        ]
        normalized, register = normalize_pronouns(messages)
        joined = " ".join(m["content"] for m in normalized).lower()
        self.assertEqual(register, "aku-kamu")
        self.assertNotIn("gue", joined)
        self.assertNotIn("lo", joined)
        self.assertIn("aku", joined)
        self.assertIn("kamu", joined)

    def test_formal_pronouns_are_preserved(self):
        messages = [
            {"role": "user", "content": "Apa kabar Anda hari ini?"},
            {"role": "assistant", "content": "Saya baik, terima kasih."},
        ]
        normalized, register = normalize_pronouns(messages)
        self.assertEqual(register, "saya-Anda")
        self.assertIn("Anda", normalized[0]["content"])
        self.assertIn("Saya", normalized[1]["content"])

    def test_digital_topic_is_flagged(self):
        item = {"messages": [
            {"role": "user", "content": "Aplikasi apa yang bagus?"},
            {"role": "assistant", "content": "Saya tidak tahu."},
        ]}
        self.assertIn("topik_digital", inspect_conversation(item))

    def test_social_media_slang_is_flagged(self):
        item = {"messages": [
            {"role": "user", "content": "Aku tidak bisa membuka medsos."},
            {"role": "assistant", "content": "Coba periksa lagi."},
        ]}
        self.assertIn("topik_digital", inspect_conversation(item))

    def test_unfinished_placeholder_is_flagged(self):
        item = {"messages": [
            {"role": "user", "content": "Apa kabar?"},
            {"role": "assistant", "content": "... Aku baik."},
        ]}
        self.assertIn("placeholder_dalam_pesan", inspect_conversation(item))

    def test_non_alternating_roles_are_flagged(self):
        item = {"messages": [
            {"role": "user", "content": "Saya ingin bertanya."},
            {"role": "user", "content": "Tentang makanan."},
            {"role": "assistant", "content": "Silakan bertanya."},
        ]}
        self.assertIn("struktur_giliran", inspect_conversation(item))

    def test_adjacent_duplicate_words_are_flagged(self):
        item = {"messages": [
            {"role": "user", "content": "Saya pulang dulu dulu."},
            {"role": "assistant", "content": "Baik, hati-hati di jalan."},
        ]}
        self.assertIn("pengulangan_kata", inspect_conversation(item))

    def test_assistant_persona_body_job_family_and_pet_are_allowed(self):
        item = {"messages": [
            {"role": "user", "content": "Kamu bekerja di mana sekarang?"},
            {"role": "assistant", "content": "Aku bekerja di kebun milik keluargaku."},
            {"role": "user", "content": "Di rumah ada hewan peliharaan?"},
            {"role": "assistant", "content": "Ada, aku memelihara seekor kucing bernama Miko."},
        ]}
        reasons = inspect_conversation(item)
        self.assertNotIn("persona_pribadi", reasons)
        self.assertNotIn("pengalaman_pribadi", reasons)
        self.assertEqual(reasons, [])

    def test_assistant_personal_experience_is_not_an_automatic_error(self):
        item = {"messages": [
            {"role": "user", "content": "Kamu pernah pergi ke pantai?"},
            {"role": "assistant", "content": "Pernah, aku pergi bersama adikku bulan lalu."},
        ]}
        reasons = inspect_conversation(item)
        self.assertNotIn("persona_pribadi", reasons)
        self.assertNotIn("pengalaman_pribadi", reasons)
        self.assertEqual(reasons, [])


if __name__ == "__main__":
    unittest.main()


class ThreeStageCurationTests(unittest.TestCase):
    def test_offline_market_and_mall_are_not_excluded(self):
        from curate_intisari_v4_staged import DIGITAL_RE
        text = "Aku pergi ke pasar dan mal untuk membeli baju."
        self.assertFalse(any(pattern.search(text) for pattern in DIGITAL_RE.values()))

    def test_clear_social_media_topic_is_excluded(self):
        from curate_intisari_v4_staged import DIGITAL_RE
        text = "Aku tidak bisa masuk ke akun media sosial."
        self.assertTrue(DIGITAL_RE["social_media"].search(text))

    def test_gue_lo_are_changed_to_aku_kamu(self):
        from curate_intisari_v4_staged import replace_words
        text, changes = replace_words("Gue suka makanan ini, kalau lo?")
        self.assertEqual(text, "Aku suka makanan ini, kalau kamu?")
        self.assertEqual(len(changes), 2)

    def test_persona_experience_is_not_a_stage3_flag(self):
        from curate_intisari_v4_staged import stage3
        import json, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            src=root/"in.jsonl"
            src.write_text(json.dumps({"id":"x","messages":[
                {"role":"user","content":"Kamu pernah ke pantai bersama keluarga?"},
                {"role":"assistant","content":"Pernah, aku pergi bersama adikku bulan lalu."}
            ]},ensure_ascii=False)+"\n",encoding="utf-8")
            report=stage3(src,root)
            self.assertEqual(report["needs_human_review"],0)
            self.assertEqual(report["no_obvious_mechanical_issue_not_semantically_approved"],1)

    def test_stage3_flags_bad_turn_structure(self):
        from curate_intisari_v4_staged import stage3
        import json, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            src=root/"in.jsonl"
            src.write_text(json.dumps({"id":"x","messages":[
                {"role":"user","content":"Aku mau bertanya."},
                {"role":"user","content":"Tentang makanan."},
                {"role":"assistant","content":"Silakan bertanya."}
            ]},ensure_ascii=False)+"\n",encoding="utf-8")
            report=stage3(src,root)
            self.assertEqual(report["needs_human_review"],1)


    def test_incidental_internet_mention_in_offline_market_dialogue_is_reviewed_not_excluded(self):
        from curate_intisari_v4_staged import stage1
        import json, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            src=root/"source.jsonl"
            src.write_text(json.dumps({"messages":[
                {"role":"user","content":"Aku mau ke pasar membeli sayur."},
                {"role":"assistant","content":"Kalau perlu, kamu bisa mencari informasi di internet."}
            ]},ensure_ascii=False)+"\n",encoding="utf-8")
            report=stage1(src,root)
            self.assertEqual(report["excluded_digital"],0)
            self.assertEqual(report["mixed_offline_context_records_kept_for_review"],1)

    def test_generic_board_game_mention_is_not_automatically_digital(self):
        from curate_intisari_v4_staged import DIGITAL_RE
        text="Kalau hujan, kita bisa bermain permainan bersama di rumah."
        self.assertFalse(any(pattern.search(text) for pattern in DIGITAL_RE.values()))

    def test_online_shop_as_main_topic_is_excluded(self):
        from curate_intisari_v4_staged import DIGITAL_RE
        text="Aku mau belanja online di online shop."
        self.assertTrue(DIGITAL_RE["digital_services"].search(text))


    def test_single_youtube_mention_in_offline_sports_dialogue_is_reviewed(self):
        from curate_intisari_v4_staged import stage1
        import json, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            src=root/"source.jsonl"
            src.write_text(json.dumps({"messages":[
                {"role":"user","content":"Aku ingin meningkatkan kemampuan bermain futsal."},
                {"role":"assistant","content":"Kamu bisa berlatih rutin dan melihat satu video tutorial di YouTube."}
            ]},ensure_ascii=False)+"\n",encoding="utf-8")
            report=stage1(src,root)
            self.assertEqual(report["excluded_digital"],0)
            self.assertEqual(report["mixed_offline_context_records_kept_for_review"],1)


    def test_mall_and_online_shop_comparison_is_mixed_review(self):
        from curate_intisari_v4_staged import stage1
        import json, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            src=root/"source.jsonl"
            src.write_text(json.dumps({"messages":[
                {"role":"user","content":"Aku mau belanja di mall atau online shop."},
                {"role":"assistant","content":"Mall bisa melihat barang langsung, online shop lebih praktis."}
            ]},ensure_ascii=False)+"\n",encoding="utf-8")
            report=stage1(src,root)
            self.assertEqual(report["excluded_digital"],0)
            self.assertEqual(report["mixed_offline_context_records_kept_for_review"],1)


class Stage1ManualBatchTests(unittest.TestCase):
    def test_batch11_has_1000_new_unique_ids_and_is_not_training_ready(self):
        import json
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        batch_path = root / "data/curated/intisari_v4/stage1_manual_audit_batch11_1000.jsonl"
        records = [json.loads(line) for line in batch_path.read_text(encoding="utf-8").splitlines() if line]
        ids = [item["id"] for item in records]

        self.assertEqual(len(records), 1000)
        self.assertEqual(len(set(ids)), 1000)
        self.assertTrue(all(item["training_ready"] is False for item in records))
        self.assertEqual(sum(item["decision"] == "keep_in_scope" for item in records), 240)
        self.assertEqual(sum(item["decision"] == "exclude_digital_topic" for item in records), 760)

        prior_ids = set()
        for index in range(1, 10):
            path = root / f"data/curated/intisari_v4/stage1_manual_audit_batch{index}_25.jsonl"
            prior_ids.update(json.loads(line)["id"] for line in path.read_text(encoding="utf-8").splitlines() if line)
        path = root / "data/curated/intisari_v4/stage1_manual_audit_batch10_100.jsonl"
        prior_ids.update(json.loads(line)["id"] for line in path.read_text(encoding="utf-8").splitlines() if line)
        self.assertFalse(set(ids) & prior_ids)

    def test_progress_matches_batch11_and_remaining_queue(self):
        import json
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        progress = json.loads((root / "data/curated/intisari_v4/three_stage_manual_audit_progress.json").read_text(encoding="utf-8"))
        self.assertEqual(progress["stage1_unique_manual_reviewed"], 1318)
        self.assertEqual(progress["stage1_unique_manual_review_remaining"], 362)
        self.assertEqual(progress["stage1_mixed_remaining"], 109)
        self.assertEqual(progress["stage1_ambiguous_only_remaining"], 253)
        self.assertEqual(progress["stage1_unique_decisions"], {"keep_in_scope": 365, "exclude_digital_topic": 953})


    def test_batch12_closes_all_stage1_manual_queues(self):
        import json
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        batch_path = root / "data/curated/intisari_v4/stage1_manual_audit_batch12_362.jsonl"
        records = [json.loads(line) for line in batch_path.read_text(encoding="utf-8").splitlines() if line]
        ids = [item["id"] for item in records]
        self.assertEqual(len(records), 362)
        self.assertEqual(len(set(ids)), 362)
        self.assertTrue(all(item["training_ready"] is False for item in records))
        self.assertEqual(sum(item["decision"] == "keep_in_scope" for item in records), 223)
        self.assertEqual(sum(item["decision"] == "exclude_digital_topic" for item in records), 139)

        prior_ids = set()
        for index in range(1, 10):
            path = root / f"data/curated/intisari_v4/stage1_manual_audit_batch{index}_25.jsonl"
            prior_ids.update(json.loads(line)["id"] for line in path.read_text(encoding="utf-8").splitlines() if line)
        for name in ("batch10_100", "batch11_1000"):
            path = root / f"data/curated/intisari_v4/stage1_manual_audit_{name}.jsonl"
            prior_ids.update(json.loads(line)["id"] for line in path.read_text(encoding="utf-8").splitlines() if line)
        self.assertFalse(set(ids) & prior_ids)

        progress = json.loads((root / "data/curated/intisari_v4/three_stage_manual_audit_progress.json").read_text(encoding="utf-8"))
        self.assertEqual(progress["stage1_unique_manual_reviewed"], 1680)
        self.assertEqual(progress["stage1_unique_manual_review_remaining"], 0)
        self.assertEqual(progress["stage1_mixed_remaining"], 0)
        self.assertEqual(progress["stage1_ambiguous_only_remaining"], 0)
        self.assertEqual(progress["stage1_unique_decisions"], {"keep_in_scope": 588, "exclude_digital_topic": 1092})
