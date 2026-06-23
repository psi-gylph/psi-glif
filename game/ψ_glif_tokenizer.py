# 🔹 Save as: ~/psi_lab/game/ψ_glif_tokenizer.py

def tokenize_ascii_glif(ascii_glif):
    token_map = {
        '.': 'α', ':': 'β', '-': 'γ', '=': 'δ',
        '+': 'ε', '*': 'ζ', '#': 'η', '%': 'θ',
        '@': 'ι', 'ψ': 'Ω', '\n': '|'
    }
    return ''.join(token_map.get(char, '?') for char in ascii_glif)

if __name__ == "__main__":
    from ascii_glif import generate_ascii_glif
    glif = generate_ascii_glif(seed="glif_seed_001")
    print("ASCII Glif:\n", glif)
    print("\nTokenized Glif:\n", tokenize_ascii_glif(glif))
