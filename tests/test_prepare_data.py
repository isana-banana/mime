import unittest
import json
from pathlib import Path
from prepare_data import conversation_quality, normalize, synthetic_candidate_docs

class CorpusQualityTests(unittest.TestCase):
    def test_rejects_fake_personal_experience(self):
        messages = [("user", "Kamu suka kopi?"), ("assistant", "Gw tadi nongkrong di warung dekat kantor.")]
        self.assertEqual(conversation_quality(messages, "unit_test"), "assistant_personal_claim")

    def test_allows_neutral_assistant_help(self):
        messages = [("user", "Bisa bantu aku belajar?"), ("assistant", "Bisa, aku bisa bantu jelaskan pelan-pelan.")]
        self.assertEqual(conversation_quality(messages, "unit_test"), "accepted")

    def test_rejects_unverified_prices(self):
        messages = [("user", "Mau cari kos."), ("assistant", "Coba cari kamar di sana, harganya Rp1.200.000 per bulan.")]
        self.assertEqual(conversation_quality(messages, "unit_test"), "assistant_unverified_specifics")

    def test_rejects_risky_topics(self):
        messages = [("user", "Aku sedang sakit."), ("assistant", "Sebaiknya minum obat sesuai dosis.")]
        self.assertEqual(conversation_quality(messages, "unit_test"), "risky_topic")

    def test_public_lorth_source_is_held_for_manual_review(self):
        messages = [("user", "Bisa bantu aku belajar?"), ("assistant", "Bisa, aku bisa bantu jelaskan pelan-pelan.")]
        self.assertEqual(conversation_quality(messages, "lorth_chat"), "manual_review_required")

    def test_synthetic_seed_format_and_role_order(self):
        path = Path("data/synthetic/seed_v1.jsonl")
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertGreaterEqual(len(rows), 20)
        self.assertEqual(len({row["id"] for row in rows}), len(rows))
        for row in rows:
            self.assertIn(row["style"], {"casual_aku_kamu", "casual_saya_anda", "casual_gue_lo"})
            roles = [message["role"] for message in row["messages"]]
            self.assertGreaterEqual(len(roles), 4)
            self.assertEqual(roles[0], "user")
            self.assertEqual(roles[-1], "assistant")
            self.assertTrue(all(role in {"user", "assistant"} for role in roles))
            self.assertTrue(all(roles[i] != roles[i-1] for i in range(1, len(roles))))
            self.assertTrue(all(message["content"].strip() for message in row["messages"]))

    def test_synthetic_candidates_are_formatted_and_nonempty(self):
        docs = synthetic_candidate_docs(Path("data/synthetic"))
        self.assertGreaterEqual(len(docs), 300)
        self.assertTrue(all("Pengguna:" in doc and "Asisten:" in doc for doc in docs))
        self.assertTrue(all(len(doc) > 40 for doc in docs))

    def test_scenarios_keep_speaker_labels_and_are_not_chat_roles(self):
        doc, reason = normalize([("speaker1", "Halo, kamu sedang apa hari ini?"), ("speaker2", "Aku sedang membaca buku di rumah.")], scenario=True)
        self.assertEqual(reason, "accepted")
        self.assertIn("Pembicara 1:", doc)
        self.assertNotIn("Asisten:", doc)

if __name__ == "__main__":
    unittest.main()
