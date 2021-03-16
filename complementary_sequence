#this code outputs the reverse complementary sequences of a give input sequence
#eg. “ATGATCAAG” should output “CTTGATCAT”
def Reverse(Pattern):
    complementary_string = ""
    reverse_complementary_string = ""
    base_pair = {"A":"T","T":"A","C":"G","G":"C"}
    for base in Pattern:
        complementary_string = base + complementary_string
    for bases in complementary_string:
        reverse_complementary_string += base_pair[bases]
    return reverse_complementary_string
print(Reverse("AAAACCCGGT"))


