import tkinter as tk
import math
from app import config, algorithms, visualization

# --- Логіка кнопок ---
def run_dijkstra_logic():
    # Отримуємо дані з конфігурації
    verts = config.VERTICES
    edges = config.EDGES
    start = config.START_NODE

    # Викликаємо "чисту" функцію
    dist, prev, prot = algorithms.dijkstra(verts, edges, start)

    # Формуємо текст для виводу
    lines = [f"Алгоритм Дейкстри (старт із '{start}')\n"]
    lines.extend(prot)
    lines.append("\n--- ПІДСУМОК (відстані та шляхи) ---")
    
    for v in verts:
        d = dist[v]
        if d == math.inf:
            lines.append(f"{start} -> {v}: dist = inf, шлях: -")
        else:
            path = algorithms.reconstruct_path_dijkstra(prev, start, v)
            path_str = " → ".join(path) if path else "-"
            lines.append(f"{start} -> {v}: dist = {d}, шлях: {path_str}")

    show_text("Дейкстра — протокол", "\n".join(lines))


def run_floyd_logic():
    verts = config.VERTICES
    edges = config.EDGES
    
    D, NXT, prot = algorithms.floyd_warshall(verts, edges)

    lines = ["Алгоритм Флойда–Уоршела\n"]
    lines.extend(prot)

    lines.append("\n--- МАТРИЦЯ НАЙКОРОТШИХ ВІДСТАНЕЙ ---")
    # Заголовок таблиці
    header = "     " + "  ".join([f"{v:>3}" for v in verts])
    lines.append(header)
    
    for i, v in enumerate(verts):
        row = []
        for j in range(len(verts)):
            val = D[i][j]
            row.append("inf" if val == math.inf else str(int(val)))
        lines.append(f"{v:>3}: " + "  ".join([f"{x:>3}" for x in row]))

    start_node = config.START_NODE
    lines.append(f"\n--- ПРИКЛАД ВІДНОВЛЕННЯ ШЛЯХІВ від '{start_node}' ---")
    for v in verts:
        p = algorithms.reconstruct_path_floyd(NXT, verts, start_node, v)
        if p is None:
            lines.append(f"{start_node} -> {v}: шлях відсутній")
        else:
            lines.append(f"{start_node} -> {v}: " + " → ".join(p))

    show_text("Флойд–Уоршел — протокол", "\n".join(lines))


# --- Допоміжні функції GUI ---
def show_text(title: str, text: str):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("900x600")

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)

    txt = tk.Text(frame, wrap="word")
    txt.pack(side="left", fill="both", expand=True)

    sb = tk.Scrollbar(frame, command=txt.yview)
    sb.pack(side="right", fill="y")
    txt.configure(yscrollcommand=sb.set)

    txt.insert("1.0", text)
    txt.configure(state="disabled")


# --- Головна функція запуску додатка ---
def run_app():
    root = tk.Tk()
    root.title("Лабораторна робота №3 — Модульна версія")
    root.geometry("520x260")

    algo_var = tk.StringVar(value="dijkstra")

    def run_selected():
        if algo_var.get() == "dijkstra":
            run_dijkstra_logic()
        else:
            run_floyd_logic()

    # Елементи інтерфейсу
    tk.Label(root, text="Оберіть алгоритм:", font=("Arial", 14)).pack(pady=10)

    tk.Radiobutton(root, text="Алгоритм Дейкстри", variable=algo_var, value="dijkstra").pack(anchor="w", padx=30)
    tk.Radiobutton(root, text="Алгоритм Флойда–Уоршела", variable=algo_var, value="floyd").pack(anchor="w", padx=30)

    tk.Button(root, text="Виконати", width=30, command=run_selected).pack(pady=12)
    
    # Кнопка візуалізації викликає функцію з модуля visualization
    tk.Button(root, text="Показати граф з вагами", width=30, 
              command=lambda: visualization.draw_graph(config.EDGES, config.POS)).pack(pady=5)

    root.mainloop()