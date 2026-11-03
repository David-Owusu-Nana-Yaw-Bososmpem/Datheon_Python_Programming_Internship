#!/usr/bin/env python3
"""
Terminal Hangman Game
- Random word from English word list (length >= 5)
- 6 incorrect guesses allowed
- ASCII gallows updates with each mistake
- Tracks guessed letters; no penalty for duplicates
"""

import random
import os
import sys

# Look for the word list in the same folder as this script
WORD_LIST_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "google-10000-english-no-swears.txt"
)

# ASCII art stages for the gallows (0 = empty, 6 = fully hanged)
HANGMAN_STAGES = [
    # 0 wrong
    r"""
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    # 1 wrong - head
    r"""
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    # 2 wrong - body
    r"""
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    # 3 wrong - one arm
    r"""
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    # 4 wrong - both arms
    r"""
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========
    """,
    # 5 wrong - one leg
    r"""
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========
    """,
    # 6 wrong - both legs (game over)
    r"""
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========
    """,
]


def load_words(path: str, min_length: int = 5) -> list[str]:
    """Load and filter words from the text file."""
    words = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if len(word) >= min_length and word.isalpha():
                    words.append(word)
    except FileNotFoundError:
        print(f"Error: Word list not found at:\n  {path}")
        print("\nPlease put 'google-10000-english-no-swears.txt' in the same folder as hangman.py")
        sys.exit(1)

    if not words:
        print("Error: No suitable words found in the list.")
        sys.exit(1)
    return words


def clear_screen() -> None:
    """Clear the terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


def display_game(
    secret: str,
    guessed: set[str],
    mistakes: int,
    max_mistakes: int = 6,
) -> None:
    """Print the current game state."""
    clear_screen()
    print("=" * 40)
    print("           H A N G M A N")
    print("=" * 40)
    print(HANGMAN_STAGES[mistakes])
    print()

    # Masked word
    display = " ".join(letter if letter in guessed else "_" for letter in secret)
    print(f"  Word:  {display}")
    print()

    # Guessed letters
    sorted_guessed = sorted(guessed)
    print(f"  Guessed letters: {' '.join(sorted_guessed) if sorted_guessed else '(none)'}")
    print(f"  Mistakes remaining: {max_mistakes - mistakes}")
    print("=" * 40)


def get_guess(guessed: set[str]) -> str:
    """Prompt user for a single letter guess, with validation."""
    while True:
        raw = input("\n  Enter a letter: ").strip().lower()
        if len(raw) != 1:
            print("  Please enter exactly one letter.")
            continue
        if not raw.isalpha():
            print("  Please enter a letter (a-z).")
            continue
        if raw in guessed:
            print(f"  You already guessed '{raw}'. Try a different letter.")
            continue
        return raw


def play_round(words: list[str]) -> bool:
    """
    Play one round of Hangman.
    Returns True if the player wants to play again.
    """
    secret = random.choice(words)
    guessed: set[str] = set()
    mistakes = 0
    max_mistakes = 6

    while True:
        display_game(secret, guessed, mistakes, max_mistakes)

        # Check win
        if all(letter in guessed for letter in secret):
            print("\n  ★★★  YOU WIN!  ★★★")
            print(f"  The word was: {secret.upper()}")
            break

        # Check loss
        if mistakes >= max_mistakes:
            print("\n  ✗✗✗  GAME OVER  ✗✗✗")
            print(f"  The word was: {secret.upper()}")
            break

        guess = get_guess(guessed)
        guessed.add(guess)

        if guess in secret:
            print(f"\n  Good guess! '{guess}' is in the word.")
        else:
            mistakes += 1
            print(f"\n  Sorry, '{guess}' is not in the word.")

        input("  Press Enter to continue...")

    # Ask to play again
    print()
    while True:
        again = input("  Play again? (y/n): ").strip().lower()
        if again in ("y", "yes"):
            return True
        if again in ("n", "no"):
            return False
        print("  Please enter 'y' or 'n'.")


def main() -> None:
    print("Loading word list...")
    words = load_words(WORD_LIST_PATH, min_length=5)
    print(f"Loaded {len(words)} words. Starting game...\n")
    input("Press Enter to begin...")

    while True:
        if not play_round(words):
            break

    clear_screen()
    print("\n  Thanks for playing Hangman! Goodbye.\n")


if __name__ == "__main__":
    main()
