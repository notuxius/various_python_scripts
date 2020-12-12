def print_nums(num_of_iterations=2):
    num_to_print = 0

    if num_of_iterations < 2:
        print(f"Not enough iterations: {num_of_iterations}")
        return

    for num_of_nums_in_curr_row in range(num_of_iterations):
        for _ in range(num_of_nums_in_curr_row + 1):
            print(num_to_print, end=" ")
            num_to_print += 3

            if num_to_print > 9:
                num_to_print = int(str(num_to_print)[1:])

        print()


for iterations in [0, 1, 2, 3, 5, 10, 100]:
    print_nums(iterations)
    print()
