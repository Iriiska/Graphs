"""Практика 6"""

import matplotlib.pyplot as plt
import networkx as nx
import planarity


def graph_from_matrix(matrix):
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("Матрица должна быть квадратной.")
    for i in range(n):
        for j in range(n):
            if matrix[i][j] not in (0, 1):
                raise ValueError("Допустимы только значения 0 и 1.")
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Матрица должна быть симметричной.")
        if matrix[i][i] != 0:
            raise ValueError("На диагонали должны быть нули: петли не поддерживаются.")

    graph = nx.Graph()
    graph.add_nodes_from(range(1, n + 1))
    graph.add_edges_from(
        (i + 1, j + 1)
        for i in range(n)
        for j in range(i + 1, n)
        if matrix[i][j] == 1
    )
    return graph


def check_and_draw(matrix, filename="planar_graph.png", show=True):
    graph = graph_from_matrix(matrix)

    is_planar = len(graph) == 0 or planarity.is_planar(graph)
    if not is_planar:
        print("Граф НЕ планарен. Рисунок не построен.")
        return False

    print("Граф планарен.")
    positions = nx.planar_layout(graph)
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw_networkx(
        graph, pos=positions, ax=ax, with_labels=True,
        node_color="#b8dcff", edge_color="#334155",
        node_size=600, font_size=12, width=1.8,
    )
    ax.set_title("Планарная укладка" if graph else "Пустой граф — планарен")
    ax.set_aspect("equal")
    ax.margins(0.15)
    ax.axis("off")
    fig.tight_layout()
    if filename is not None:
        fig.savefig(filename, dpi=180, bbox_inches="tight")
        print(f"Рисунок сохранён: {filename}")
    if show:
        plt.show()
    plt.close(fig)
    return True


def main():
    try:
        n = int(input("Количество вершин: "))
        if n < 0:
            raise ValueError("Количество вершин не может быть отрицательным.")
        print(f"Введите {n} строк матрицы: числа 0 и 1 через пробел.")
        matrix = [list(map(int, input().split())) for _ in range(n)]
        check_and_draw(matrix)
    except (ValueError, EOFError) as error:
        print(f"Ошибка ввода: {error}")


if __name__ == "__main__":
    main()
