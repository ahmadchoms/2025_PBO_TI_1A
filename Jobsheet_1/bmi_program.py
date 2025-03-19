def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    if height_m <= 0:
        raise ValueError("Tinggi harus lebih besar dari 0.")
    return weight / (height_m ** 2)


def bmi_program():
    try:
        weight = float(input("Masukan berat (kg): "))
        height_cm = float(input("Masukan tinggi (cm): "))
        bmi = calculate_bmi(weight, height_cm)
        print(f"Nilai berat: {weight} kg, tinggi: {height_cm} cm")
        print(f"Nilai BMI mu: {bmi:.2f}")

        if bmi < 18.5:
            print("Kategori BMI: Underweight")
        elif 18.5 <= bmi < 24.9:
            print("Kategori BMI: Normal weight")
        elif 25 <= bmi < 29.9:
            print("Kategori BMI: Overweight")
        else:
            print("Kategori BMI: Obesity")
    except ValueError as e:
        print(f"Input invalid: {e}")


if __name__ == "__main__":
    bmi_program()