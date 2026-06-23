from collections import Counter

def entropy_level(ascii_str):
    """
    ASCII glifin karakter dağılımına göre kaba entropi seviyesi döner (0.0 - 1.0).
    """
    cleaned = ascii_str.replace('\n', '')
    if not cleaned:
        return 0.0
    total = len(cleaned)
    counter = Counter(cleaned)
    probs = [count / total for count in counter.values()]
    entropy = -sum(p * __import__('math').log2(p) for p in probs)
    return round(entropy / 5.0, 3)  # 0-1 arası normalize edilir (maks. 5 bit kabul)
