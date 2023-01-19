### -IMPORTS- ###
import math
import re
import textwrap
from operator import itemgetter
from typing import List, Optional, Dict

with open("DN2_tajnopis_viginer.txt") as f:
    vig = f.readline().strip()


### -GLOBAL STRUCTURES- ###
class Viginere:
    def __init__(self):
        self.crypto_text: str = "DAZKMACGBČPNMBCAJOSJHEEAMŠTOŽRABOHZOLAIRŽOTULČARUVPBAIOKZJGTBBFGŽČIBBTAEKKUSAGČDŽBŽEJBSŠAMZONHZŽIRUZOLAIRORJČHUAHVZŽLTRLPMBKBZAVPHMVOPEDAUKUGRUEVKKCEGCRŠLMFTCLRHPAITKDŠPMUIŽČTPJEULČOKJRNEDJSPVLSMFBASVUISEFLRŠNHZMJHZOUDFHDLOARASBBČČAHTHČIVPZJNŠFRŽPAČTPDČUUBEŽVMZEŽŽMENTBEMVOPZOLAIRŽOTULČARUBKJGBCVAUKEDAUPHVPAŠLČAGŽTBVOGDIACBCPTUUUTPAIHSA"
        self.alphabet: List[str] = list("ABCČDEFGHIJKLMNOPRSŠTUVZŽ")
        self.text_length = len(self.crypto_text)  # Dolžina kriptoteksta

        self.letter_frequency = {'A': 10.47, 'B': 1.94, 'C': 0.66, 'Č': 1.48, 'D': 3.39, 'E': 10.71, 'F': 0.11,
                                 'G': 1.64, 'H': 1.05, 'I': 9.04, 'J': 4.67, 'K': 3.7, 'L': 5.27, 'M': 3.3,
                                 'N': 6.33, 'O': 9.08, 'P': 3.37, 'R': 5.01, 'S': 5.05, 'Š': 1.0, 'T': 4.33,
                                 'U': 1.88, 'V': 3.76, 'Z': 2.1, 'Ž': 0.65}
        self.expected_IC = self.get_correlation_index(frequencies=self.letter_frequency)

        self.key = None
        self.key_length = self.find_key_length()

        self.find_key()

    # Indeks sovpadanja
    def get_correlation_index(self, frequencies):
        correlation_index = 0
        for letter in frequencies:
            correlation_index += (frequencies[letter] / 100) ** 2
        return correlation_index

    def find_repeats_return_gcd(self):
        repeats: Dict[str, List[int]] = {}
        text_length = self.text_length
        repetition_length = text_length // 2
        while repetition_length >= 3:  # Če gledam ponovitve pod 3 je največji skupni delitelj razdalj 1...
            for i in range(0, text_length - repetition_length):
                pattern = self.crypto_text[i: i + repetition_length + 1]
                findings = re.findall(string=self.crypto_text, pattern=pattern)
                indices_of_repeats = [i.start() for i in re.finditer(pattern, self.crypto_text)]
                if (len(findings) > 1 and repetition_length > 1) or (len(findings) > 2 and repetition_length == 1):
                    # Če je že našlo tako ponavljanje na večji besedi ga ignoriraj (npr MVOP bi štelo tudi MVO, VOP itd.)
                    found_already = False
                    for p in repeats:
                        if pattern in p:
                            found_already = True
                    if found_already:
                        continue
                    repeats[pattern] = indices_of_repeats
            repetition_length -= 1
        distances = []
        for key in repeats:
            for i in range(len(repeats[key]) - 1):
                distances.append(repeats[key][i + 1] - repeats[key][i])
        return math.gcd(*distances)

    def get_frequencies(self, string):
        freq = {}
        length = len(string)
        for letter in string:
            if letter not in freq:
                freq[letter] = 100 / length
            else:
                freq[letter] += 100 / length
        return freq

    def find_key_length(self):
        key_length = None
        distances_gcd = self.find_repeats_return_gcd()
        correlations_by_key_length = {}
        for m in range(1, distances_gcd + 1):
            correlations = []
            split_text = textwrap.wrap(self.crypto_text, math.ceil(self.text_length / m))
            for row in split_text:
                frequency = self.get_frequencies(row)
                ic = self.get_correlation_index(frequencies=frequency)
                correlations.append(ic)
            correlations_by_key_length[m] = sum(correlations) / len(correlations)

        best_m = None
        for m in correlations_by_key_length:
            if best_m is None:
                best_m = correlations_by_key_length[m]
                key_length = m
            if abs(correlations_by_key_length[m] - self.expected_IC) < abs(best_m - self.expected_IC):
                best_m = correlations_by_key_length[m]
                key_length = m
        return key_length

    def find_key(self):
        # Razdeli besedilo v besede v velikosti ključa
        key = ""
        split_strings = textwrap.wrap(self.crypto_text, self.key_length)
        columns = []
        for i in range(self.key_length):
            column = "".join([word[i] for word in split_strings if len(word) > i])
            columns.append(column)

        for i in range(self.key_length):
            best_comparison = math.inf
            potential_letter = []
            # Združi vsako i-to črko v niz
            for index, letter in enumerate(self.alphabet):
                test_column = self.decode_by_single_letter(string=columns[i], move_by=index)

                print(len(test_column), test_column)
                freq = self.get_frequencies(string=test_column)
                comparison = self.compare_frequencies(frequency=freq)
                print(letter, comparison)
                if comparison < best_comparison:
                    potential_letter = letter
                    best_comparison = comparison
                print("----")
            key += potential_letter
        print(key)
        self.key = key

    def decode_by_single_letter(self, string, move_by):
        new_text = ""
        for letter in string:
            index_of_letter = self.alphabet.index(letter)
            new_index = index_of_letter - move_by
            new_text += self.alphabet[new_index]
        return new_text

    def decode_total(self):
        decoded = ""
        for i, letter in enumerate(self.crypto_text):
            move_by = self.alphabet.index(self.key[i % self.key_length])
            new_index = self.alphabet.index(letter) - move_by
            decoded += self.alphabet[new_index]
        print(decoded[:201], "\n", decoded[200:])

    def compare_frequencies(self, frequency):
        delta = 0
        for letter in frequency:
            delta += abs(frequency[letter] - self.letter_frequency[letter])
        return delta


viginer = Viginere()
viginer.decode_total()
