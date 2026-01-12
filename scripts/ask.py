"""CLI: ask a question and print top evidence with (file, page) citations.

Usage:
  python scripts/ask.py "What is convolution?"

TODO: call study_copilot.search
"""

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python scripts/ask.py "your question"')
    raise SystemExit("Not implemented yet. Implement in src/study_copilot/search.py")
