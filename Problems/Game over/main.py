scores = input().split()

incorrect_ = [index for index, answer in enumerate(scores) if answer == "I"]

if len(incorrect_) < 3:
    print("You won")
    print(scores.count("C"))
else:
    print("Game over")
    print(scores[:incorrect_[2]].count("C"))

