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
