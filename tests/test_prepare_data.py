import unittest
from prepare_data import conversation_quality, normalize

class CorpusQualityTests(unittest.TestCase):
    def test_rejects_fake_personal_experience(self):
        messages = [("user", "Kamu suka kopi?"), ("assistant", "Gw tadi nongkrong di warung dekat kantor.")]
        self.assertEqual(conversation_quality(messages, "lorth_chat"), "assistant_personal_claim")

    def test_allows_neutral_assistant_help(self):
        messages = [("user", "Bisa bantu aku belajar?"), ("assistant", "Bisa, aku bisa bantu jelaskan pelan-pelan.")]
        self.assertEqual(conversation_quality(messages, "lorth_chat"), "accepted")

    def test_rejects_unverified_prices(self):
        messages = [("user", "Mau cari kos."), ("assistant", "Coba cari kamar di sana, harganya Rp1.200.000 per bulan.")]
        self.assertEqual(conversation_quality(messages, "lorth_chat"), "assistant_unverified_specifics")

    def test_rejects_risky_topics(self):
        messages = [("user", "Aku sedang sakit."), ("assistant", "Sebaiknya minum obat sesuai dosis.")]
        self.assertEqual(conversation_quality(messages, "lorth_chat"), "risky_topic")

    def test_scenarios_keep_speaker_labels_and_are_not_chat_roles(self):
        doc, reason = normalize([("speaker1", "Halo, kamu sedang apa hari ini?"), ("speaker2", "Aku sedang membaca buku di rumah.")], scenario=True)
        self.assertEqual(reason, "accepted")
        self.assertIn("Pembicara 1:", doc)
        self.assertNotIn("Asisten:", doc)

if __name__ == "__main__":
    unittest.main()
