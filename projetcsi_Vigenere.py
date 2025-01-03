import streamlit as st
import numpy as np
from collections import Counter

# Fonction pour calculer l'indice de coïncidence
def indice_coincidence(text):
    n = len(text)
    if n <= 1:
        return 0
    freq = Counter(text)
    IC = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return IC

# Fonction pour trouver la longueur probable de la clé
def longueur_cle_probable(text, max_len=20):
    ICs = []
    for k in range(1, max_len + 1):
        segments = [text[i::k] for i in range(k)]
        if any(len(segment) <= 1 for segment in segments):
            ICs.append(0)
        else:
            ICs.append(np.mean([indice_coincidence(segment) for segment in segments]))
    return ICs.index(max(ICs)) + 1 if ICs else 1

# Fonction pour chiffrer le texte
def chiffrer_vigenere(text, key):
    if len(key) == 0:
        raise ValueError("La clé ne peut pas être vide.")
    key = key.upper()
    encrypted = []
    key_len = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_len]) - ord('A')
            encrypted_char = chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
            encrypted.append(encrypted_char)
        else:
            encrypted.append(char)
    return ''.join(encrypted)

# Fonction pour déchiffrer le texte
def dechiffrer_vigenere(text, key):
    if len(key) == 0:
        raise ValueError("La clé ne peut pas être vide.")
    key = key.upper()
    decrypted = []
    key_len = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_len]) - ord('A')
            decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)
    return ''.join(decrypted)

# Estimer la clé avec analyse fréquentielle
def estimer_cle(text, key_len):
    subtexts = [''.join(text[i::key_len]) for i in range(key_len)]
    key = ''
    for subtext in subtexts:
        freq = Counter(subtext)
        most_common = freq.most_common(1)[0][0]
        shift = (ord(most_common) - ord('E')) % 26
        key += chr(shift + ord('A'))
    return key

# Estimer la clé avec indice de coïncidence
def estimer_cle_IC(text, key_len):
    subtexts = [''.join(text[i::key_len]) for i in range(key_len)]
    key = ''
    for subtext in subtexts:
        freq = Counter(subtext)
        most_common = freq.most_common(1)[0][0]
        shift = (ord(most_common) - ord('E')) % 26
        key += chr(shift + ord('A'))
    return key

# Interface Streamlit
def main():
    st.title("Chiffre de Vigenère")

    texte = st.text_area("Texte", height=150)
    texte = ''.join(filter(str.isalpha, texte)).upper()

    cle = st.text_input("Clé")

    if st.button("Chiffrer"):
        try:
            resultat = chiffrer_vigenere(texte, cle)
            st.subheader("Texte chiffré")
            st.write(resultat)
        except ValueError as e:
            st.error(str(e))

    if st.button("Déchiffrer"):
        try:
            resultat = dechiffrer_vigenere(texte, cle)
            st.subheader("Texte déchiffré")
            st.write(resultat)
        except ValueError as e:
            st.error(str(e))

    if st.button("Analyse fréquentielle"):
        key_len = longueur_cle_probable(texte)
        cle_estimee = estimer_cle(texte, key_len)
        st.subheader("Clé estimée (Analyse fréquentielle)")
        st.write(cle_estimee)

    if st.button("Analyse IC"):
        key_len = longueur_cle_probable(texte)
        cle_estimee = estimer_cle_IC(texte, key_len)
        st.subheader("Clé estimée (Indice de Coïncidence)")
        st.write(cle_estimee)

if __name__ == "__main__":
    main()
