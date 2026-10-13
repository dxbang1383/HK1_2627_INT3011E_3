from pysat.solvers import Glucose3
import math

next_var = 1

# Biểu diễn suy ra 
def implies(a, b):
    return [-a, b]

def new_var():
    global next_var
    current_id = next_var
    next_var = next_var + 1
    return current_id

def var(i, j, n) :
    return i * n + j + 1

def at_least_one(variables):
    return [variables]

# Đầu vào var : là list chứa các ô có ràng buộc AMO với nhau 
# Tức là 2 cặp bất kì trong biến đều không cùng có giá trị true (and của 2 cặp = false)
# OR của phủ định 2 mệnh đề -a or -b
# Với sequential thì có 4 dòng mệnh đề
def at_most_one(variables):

    l = len(variables)
    if l == 1 : return []
    if l == 2 : return [[- variables[0], - variables[1]]]
    else :
        clauses = []
        new_param = []

        len_binary = math.ceil(math.log2(l))

        for i in range(len_binary):
            new_param.append(new_var())

        for i in range(l):
            target = variables[i]
            temp_number = i  # Tạo bản sao của số i để chia dần

            for j in range(len_binary):
                # Lấy bit
                bit_value = temp_number % 2
                
                temp_number = temp_number // 2

                if bit_value == 1:
                    clauses.append(implies(target, new_param[j]))

                else:
                    clauses.append(implies(target, -new_param[j]))

        return clauses

# EO = AMO + ALO
def exactly_one(variables):
    return at_least_one(variables) + at_most_one(variables)

# Chuyển bài toán thành mệnh đề 
def convert_to_clause(n):
    global next_var
    next_var = n * n + 1
    clauses = []
    ## Chuyển hàng thành clauses
    for i in range(n): 

        # Lấy các chỉ số của các ô trên 1 hàng 
        row_vars = []
        for j in range(n):
            row_vars.append(var(i, j, n))
            
        clauses = clauses + exactly_one(row_vars)

    ## Chuyển cột thành claudes
    for j in range(n):

        col_vars = []

        for i in range(n):
            col_vars.append(var(i, j, n))

        clauses = clauses + exactly_one(col_vars)

    ## Chuyển các đường chéo thành clauses (AMO)
    
    # 1. Đường chéo xuôi song song với (0, 0) và (n, n)
    for diff in range(-(n - 2), n - 1):
        x_vars = []
        
        for i in range(n):
            j = i - diff
            
            if j >= 0 and j < n:
                x_vars.append(var(i, j, n))
                
        clauses = clauses + at_most_one(x_vars)

    #2 Đường chéo song song với (n, 0) (0, n)
    for sum in range(1, 2 * n - 2):
        x_vars = []

        for i in range(n):
            j = sum - i

            if j >= 0 and j < n:
                x_vars.append(var(i, j, n))

        clauses = clauses + at_most_one(x_vars)

    return clauses

if __name__ == "__main__":
    n = 9
    clauses = convert_to_clause(n)

    print(f"So luong menh de la : {len(clauses)}")
    print(clauses)

    solver = Glucose3()

    for c in clauses:
        solver.add_clause(c)


    if solver.solve():
        model = solver.get_model()

        for i in range(n):
            for j in range(n):
                if var(i, j, n) in model:
                    print("Q", end=" ")
                else:
                    print(".", end=" ")
            print()

    else:
        print("Khong tim thay loi giai!")