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


if __name__ == "__main__":
    unittest.main()
