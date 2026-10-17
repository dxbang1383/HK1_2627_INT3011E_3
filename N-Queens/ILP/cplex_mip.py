import time
from docplex.mp.model import Model

def solve_cplex_mip(n):
    # 1. Khoi tao model CPLEX MIP
    model = Model(name="N-Queens-CPLEX")

    # 2. Tao bien nhi phan: x[i, j] = 1 neu dat quan hau tai (i, j), nguoc lai = 0
    x = {}
    for i in range(n):
        for j in range(n):
            x[i, j] = model.binary_var(name=f"x_{i}_{j}")

    # 3. Rang buoc 1: Moi hang co dung 1 quan hau (tong hang = 1)
    for i in range(n):
        row_vars = []
        for j in range(n):
            row_vars.append(x[i, j])
        model.add_constraint(model.sum(row_vars) == 1)

    # 4. Rang buoc 2: Moi cot co dung 1 quan hau (tong cot = 1)
    for j in range(n):
        col_vars = []
        for i in range(n):
            col_vars.append(x[i, j])
        model.add_constraint(model.sum(col_vars) == 1)

    # 5. Rang buoc 3: Duong cheo chinh co toi da 1 quan hau (tong <= 1)
    for diff in range(-(n - 1), n):
        diag_vars = []
        for i in range(n):
            j = i - diff
            if 0 <= j < n:
                diag_vars.append(x[i, j])
        if len(diag_vars) > 1:
            model.add_constraint(model.sum(diag_vars) <= 1)

    # 6. Rang buoc 4: Duong cheo phu co toi da 1 quan hau (tong <= 1)
    for total in range(2 * n - 1):
        diag_vars = []
        for i in range(n):
            j = total - i
            if 0 <= j < n:
                diag_vars.append(x[i, j])
        if len(diag_vars) > 1:
            model.add_constraint(model.sum(diag_vars) <= 1)

    # 7. Solver giai bai toan
    start_time = time.time()
    solution = model.solve(log_output=False)
    end_time = time.time()

    # 8. In ket qua
    if solution:
        print(f"Thoi gian giai: {end_time - start_time:.4f} giay")
        print("Ban co ket qua:")
        for i in range(n):
            for j in range(n):
                if solution.get_value(x[i, j]) > 0.5:
                    print("Q", end=" ")
                else:
                    print(".", end=" ")
            print()
    else:
        print("Khong tim thay loi giai!")

if __name__ == "__main__":
    n = 8
    solve_cplex_mip(n)
