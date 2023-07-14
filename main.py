n = 3
SUCCESS = True

class State:
    def __init__(self):
        self.board = [[0] * n for _ in range(n)]
        self.g = 0
        self.f = 0
        self.came_from = None

    @staticmethod
    def heuristic(from_state, to_state):
        """
        Tính giá trị heuristic từ trạng thái hiện tại đến trạng thái mục tiêu.

        Parameters:
        - from_state (State): Trạng thái hiện tại.
        - to_state (State): Trạng thái mục tiêu.

        Returns:
        - ret (int): Giá trị heuristic.
        """
        ret = 0
        for i in range(n):
            for j in range(n):
                if from_state.board[i][j] != to_state.board[i][j]:
                    ret += 1
        return ret

    def __eq__(self, other):
        """
        So sánh hai trạng thái xem có bằng nhau hay không.

        Parameters:
        - other (State): Trạng thái để so sánh.

        Returns:
        - (bool): Kết quả so sánh.
        """
        for i in range(n):
            for j in range(n):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

    def print_state(self):
        """
        In ra trạng thái hiện tại và giá trị g, f của nó.
        """
        for i in range(n):
            for j in range(n):
                print(self.board[i][j], end=" ")
            print()
        print("g =", self.g, "| f =", self.f)

output = []

def lowerF(a, b):
    """
    Hàm so sánh f giữa hai trạng thái a và b.

    Parameters:
    - a (State): Trạng thái a.
    - b (State): Trạng thái b.

    Returns:
    - (bool): True nếu f của a nhỏ hơn f của b, ngược lại False.
    """
    return a.f < b.f

def isinset(a, b):
    """
    Kiểm tra xem trạng thái a có trong tập hợp b hay không.

    Parameters:
    - a (State): Trạng thái a.
    - b (List[State]): Tập hợp các trạng thái.

    Returns:
    - (bool): True nếu a có trong tập hợp b, ngược lại False.
    """
    for item in b:
        if a == item:
            return True
    return False

def addNeighbor(current, goal, newi, newj, posi, posj, openset, closedset):
    """
    Thêm trạng thái hàng xóm vào tập openset nếu nó thỏa mãn các điều kiện.

    Parameters:
    - current (State): Trạng thái hiện tại.
    - goal (State): Trạng thái mục tiêu.
    - newi (int): Vị trí hàng của hàng xóm mới.
    - newj (int): Vị trí cột của hàng xóm mới.
    - posi (int): Vị trí hàng của ô trống.
    - posj (int): Vị trí cột của ô trống.
    - openset (List[State]): Tập openset.
    - closedset (List[State]): Tập closedset.
    """
    newstate = State()
    newstate.board = [row[:] for row in current.board]
    newstate.board[newi][newj], newstate.board[posi][posj] = newstate.board[posi][posj], newstate.board[newi][newj]
    if not isinset(newstate, closedset) and not isinset(newstate, openset):
        newstate.g = current.g + 1
        newstate.f = newstate.g + State.heuristic(newstate, goal)
        temp = State()
        temp.__dict__ = current.__dict__.copy()
        newstate.came_from = temp
        openset.append(newstate)

def neighbors(current, goal, openset, closedset):
    """
    Tìm các trạng thái hàng xóm của trạng thái hiện tại và thêm vào tập openset.

    Parameters:
    - current (State): Trạng thái hiện tại.
    - goal (State): Trạng thái mục tiêu.
    - openset (List[State]): Tập openset.
    - closedset (List[State]): Tập closedset.
    """
    posi, posj = None, None
    for i in range(n):
        for j in range(n):
            if current.board[i][j] == 0:
                posi = i
                posj = j
                break
        if posi is not None:
            break
    i, j = posi, posj
    if i - 1 >= 0:
        addNeighbor(current, goal, i - 1, j, posi, posj, openset, closedset)
    if i + 1 < n:
        addNeighbor(current, goal, i + 1, j, posi, posj, openset, closedset)
    if j + 1 < n:
        addNeighbor(current, goal, i, j + 1, posi, posj, openset, closedset)
    if j - 1 >= 0:
        addNeighbor(current, goal, i, j - 1, posi, posj, openset, closedset)

def reconstruct_path(current, came_from):
    """
    Xây dựng lại đường đi từ trạng thái hiện tại về trạng thái ban đầu.

    Parameters:
    - current (State): Trạng thái hiện tại.
    - came_from (List[State]): Danh sách các trạng thái đã đi qua để đến trạng thái hiện tại.

    Returns:
    - (bool): True nếu thành công, False nếu thất bại.
    """
    temp = current
    while temp is not None:
        came_from.append(temp)
        temp = temp.came_from
    return SUCCESS

def get_move(current, next):
    """
    Lấy hướng di chuyển từ trạng thái hiện tại đến trạng thái tiếp theo.

    Parameters:
    - current (State): Trạng thái hiện tại.
    - next (State): Trạng thái tiếp theo.

    Returns:
    - (str): Hướng di chuyển.
    """
    if current is None or next is None:
        return ""
    curr_i, curr_j = find_zero_position(current)
    next_i, next_j = find_zero_position(next)
    if curr_i > next_i:
        return "UP"
    elif curr_i < next_i:
        return "DOWN"
    elif curr_j > next_j:
        return "LEFT"
    elif curr_j < next_j:
        return "RIGHT"
    return ""

def find_zero_position(state):
    """
    Tìm vị trí của ô trống trong trạng thái.

    Parameters:
    - state (State): Trạng thái.

    Returns:
    - (tuple): Vị trí của ô trống (i, j).
    """
    for i in range(n):
        for j in range(n):
            if state.board[i][j] == 0:
                return i, j
    return -1, -1

def astar(start, goal):
    """
    Thuật toán A* để tìm đường đi từ trạng thái start đến trạng thái goal.

    Parameters:
    - start (State): Trạng thái ban đầu.
    - goal (State): Trạng thái mục tiêu.

    Returns:
    - (bool): True nếu tìm thấy đường đi, False nếu không tìm thấy.
    """
    openset = []
    closedset = []
    start.g = 0
    start.f = start.g + State.heuristic(start, goal)
    openset.append(start)
    while openset:
        openset.sort(key=lambda x: x.f)
        current = openset[0]
        if current == goal:
            return reconstruct_path(current, output)
        openset.pop(0)
        closedset.append(current)
        neighbors(current, goal, openset, closedset)
    return not SUCCESS

if __name__ == "__main__":
    start = State()
    goal = State()
    goal.board = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]
    with open("inp.txt", "r") as input_file:
        for i in range(n):
            start.board[i] = list(map(int, input_file.readline().split()))
    if astar(start, goal) == SUCCESS:
        for state in reversed(output):
            state.print_state()
        with open("out.txt", "w") as output_file:
            output_file.write(str(len(output) - 1) + "\n")
            moves = []
            for i in range(len(output) - 1):
                moves.append(get_move(output[i+1], output[i]))
            output_file.write(" ".join(moves))
        
        print("SUCCESS")
    else:
        print("FAIL")
