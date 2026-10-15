import time
from docplex.cp.model import CpoModel

def solve_cplex_cp(n):
    model = CpoModel(name="N-Queens")

    # queens[i] la cot cua quan hau tai hang i
    queens = []
    for i in range(n):
        queens.append(model.integer_var(0, n - 1, f"Q_{i}"))

    # Cac quan hau khong cung 1 cot
    model.add(model.all_diff(queens))

    # Khong cung duong cheo chinh (queens[i] - i khac nhau)
    diag1 = []
    for i in range(n):
        diag1.append(queens[i] - i)
    model.add(model.all_diff(diag1))

    # Khong cung duong cheo phu (queens[i] + i khac nhau)
    diag2 = []
    for i in range(n):
        diag2.append(queens[i] + i)
    model.add(model.all_diff(diag2))

    # Solver giai bai toan
    start_time = time.time()
    try:
        sol = model.solve(LogVerbosity="Quiet")
        end_time = time.time()

        # In ket qua
        if sol and sol.is_solution():
            print(f"Thoi gian giai: {end_time - start_time:.4f} giay")
            print("Ban co ket qua:")
            for i in range(n):
                col = sol.get_value(queens[i])
                for j in range(n):
                    if j == col:
                        print("Q", end=" ")
                    else:
                        print(".", end=" ")
                print()
        else:
            print("Khong tim thay loi giai!")
    except Exception as e:
        print(f"Loi khi goi CPLEX CP Solver: {e}")
        print("Luu y: Cplex CP yeu cau cai dat CP Optimizer (cpoptimizer.exe) tu IBM ILOG CPLEX Optimization Studio.")

if __name__ == "__main__":
    n = 8
    solve_cplex_cp(n)
