from collections import Counter
import math

def entropy_level(ascii_str):
    """
    Verilen ASCII glif dizgesinin entropisini (karmaşıklığını) hesaplar.
    Entropi = -∑ p(x) log2 p(x)
    """
    cleaned = ascii_str.replace("\n", "")
    counts = Counter(cleaned)
    total = sum(counts.values())

    if total == 0:
        return 0.0

    entropy = -sum((count/total) * math.log2(count/total) for count in counts.values())
    return round(entropy, 2)  # 0.0 – 3.0 arası normal değerler

