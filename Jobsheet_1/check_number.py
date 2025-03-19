def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def check_number():
    try:
        num = int(input("Masukan angka: "))
        if num % 2 == 0:
            print(f"{num} adalah angka genap.")
        else:
            print(f"{num} adalah angka ganjil.")
        if is_prime(num):
            print(f"{num} adalah angka Prima.")
        else:
            print(f"{num} bukan angka Prima.")
    except ValueError:
        print("Input harus berupa angka.")


if __name__ == "__main__":
    check_number()
