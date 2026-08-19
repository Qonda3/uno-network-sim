import unittest
from game_logic import is_valid_play, parse_card, advance_turn


class TestIsValidPlay(unittest.TestCase):

    def test_wild_always_valid(self):
        top_color, top_value = "Red", 5
        self.assertTrue(is_valid_play(top_color, top_value, (None, "Wild")))
        self.assertTrue(is_valid_play(top_color, top_value, (None, "Wild Draw Four")))

    def test_matching_color_is_valid(self):
        top_color, top_value = "Red", 5
        self.assertTrue(is_valid_play(top_color, top_value, ("Red", 9)))

    def test_matching_value_is_valid(self):
        top_color, top_value = "Red", 5
        self.assertTrue(is_valid_play(top_color, top_value, ("Blue", 5)))

    def test_no_match_is_invalid(self):
        top_color, top_value = "Red", 5
        self.assertFalse(is_valid_play(top_color, top_value, ("Blue", 9)))

    def test_matching_action_value_is_valid(self):
        top_color, top_value = "Red", "Skip"
        self.assertTrue(is_valid_play(top_color, top_value, ("Blue", "Skip")))


class TestParseCard(unittest.TestCase):

    def test_number_card(self):
        self.assertEqual(parse_card(["Red", "5"]), ("Red", 5))

    def test_action_card_single_word(self):
        self.assertEqual(parse_card(["Blue", "Skip"]), ("Blue", "Skip"))

    def test_action_card_two_words(self):
        self.assertEqual(parse_card(["Green", "Draw", "Two"]), ("Green", "Draw Two"))

    def test_plain_wild(self):
        self.assertEqual(parse_card(["Wild"]), (None, "Wild"))

    def test_wild_draw_four(self):
        self.assertEqual(parse_card(["Wild", "Draw", "Four"]), (None, "Wild Draw Four"))

    def test_wild_with_color_choice(self):
        # Color choice tokens shouldn't break basic card-type detection
        self.assertEqual(parse_card(["Wild", "Blue"]), (None, "Wild"))

    def test_invalid_color_returns_none(self):
        self.assertIsNone(parse_card(["Purple", "5"]))

    def test_invalid_value_returns_none(self):
        self.assertIsNone(parse_card(["Red", "Banana"]))

    def test_empty_tokens_returns_none(self):
        self.assertIsNone(parse_card([]))


class TestAdvanceTurn(unittest.TestCase):

    def make_state(self, num_players=3, turn_index=0, direction=1):
        return {
            "players": [(None, f"P{i}") for i in range(num_players)],
            "turn_index": turn_index,
            "direction": direction,
        }

    def test_advance_forward_by_one(self):
        state = self.make_state(turn_index=0, direction=1)
        advance_turn(state, 1)
        self.assertEqual(state["turn_index"], 1)

    def test_advance_wraps_around_forward(self):
        state = self.make_state(num_players=3, turn_index=2, direction=1)
        advance_turn(state, 1)
        self.assertEqual(state["turn_index"], 0)

    def test_advance_backward_with_reversed_direction(self):
        state = self.make_state(num_players=3, turn_index=1, direction=-1)
        advance_turn(state, 1)
        self.assertEqual(state["turn_index"], 0)

    def test_advance_wraps_around_backward(self):
        state = self.make_state(num_players=3, turn_index=0, direction=-1)
        advance_turn(state, 1)
        self.assertEqual(state["turn_index"], 2)

    def test_advance_by_two_for_skip(self):
        state = self.make_state(num_players=4, turn_index=0, direction=1)
        advance_turn(state, 2)
        self.assertEqual(state["turn_index"], 2)


if __name__ == "__main__":
    unittest.main()