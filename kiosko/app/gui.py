import tkinter as tk
from tkinter import ttk, messagebox
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.pago import Pago
from app.models.cliente import Cliente

class KioscoGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600")

        # Cargar productos desde la BD
        self.productos = Producto.listar_todos()
        self.carrito = []

        self.init_ui()

    def init_ui(self):
        # Panel izquierdo (menú de productos)
        left = tk.Frame(self.root)
        left.pack(side='left', fill='both', expand=True)

        # Panel derecho (carrito)
        right = tk.Frame(self.root, bd=2, relief='sunken', width=320)
        right.pack(side='right', fill='y')

        # Título
        tk.Label(left, text="Menú", font=('Arial', 14)).pack(pady=5)

        # Tabla productos
        cols = ("id", "nombre", "precio")
        self.tree = ttk.Treeview(left, columns=cols, show='headings', height=20)

        for c in cols:
            self.tree.heading(c, text=c.capitalize())

        self.tree.column("id", width=40)
        self.tree.pack(fill='both', expand=True)

        # Insertar productos
        for p in self.productos:
            self.tree.insert(
                '',
                'end',
                iid=str(p['id']),
                values=(p['id'], p['nombre'], float(p['precio']))
            )

        # Botones productos
        btn_frame = tk.Frame(left)
        btn_frame.pack(pady=6)

        tk.Button(btn_frame, text="Agregar", command=self.add_to_cart).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Quitar", command=self.remove_selected).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Ver pedidos", command=self.ver_pedidos).grid(row=0, column=2, padx=5)

        # Entrada nombre cliente
        tk.Label(right, text="Nombre del cliente:").pack(pady=3)
        self.entry_nombre = tk.Entry(right, width=30)
        self.entry_nombre.pack()

        # Carrito
        tk.Label(right, text="Carrito", font=('Arial', 12)).pack(pady=5)
        self.txt_carrito = tk.Text(right, height=20, width=40)
        self.txt_carrito.pack()

        # Botones de pago y limpiar
        tk.Button(right, text="Pagar (Efectivo)", command=self.pagar).pack(pady=8)
        tk.Button(right, text="Limpiar", command=self.limpiar_carrito).pack()

    # -----------------------
    #      AGREGAR PRODUCTO
    # -----------------------
    def add_to_cart(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un producto")
            return

        prod = Producto.obtener_por_id(int(sel))

        # Agregar al carrito
        self.carrito.append({
            'id': prod['id'],
            'nombre': prod['nombre'],
            'precio': float(prod['precio']),
            'cantidad': 1
        })

        self.refresh_carrito()

    # -----------------------
    #      QUITAR PRODUCTO
    # -----------------------
    def remove_selected(self):
        sel = self.tree.focus()
        if not sel:
            return

        pid = int(sel)
        self.carrito = [c for c in self.carrito if c['id'] != pid]

        self.refresh_carrito()

    # -----------------------
    #  REFRESCAR CARRITO
    # -----------------------
    def refresh_carrito(self):
        self.txt_carrito.delete('1.0', tk.END)
        total = 0

        for p in self.carrito:
            line = f"{p['nombre']} x{p['cantidad']} - ${p['precio'] * p['cantidad']:.2f}\n"
            self.txt_carrito.insert(tk.END, line)
            total += p['precio'] * p['cantidad']

        self.txt_carrito.insert(tk.END, f"\nTotal: ${total:.2f}")

    # -----------------------
    #     LIMPIAR CARRITO
    # -----------------------
    def limpiar_carrito(self):
        self.carrito = []
        self.refresh_carrito()

    # -----------------------
    #     PAGAR / CREAR PEDIDO
    # -----------------------
    def pagar(self):
        if not self.carrito:
            messagebox.showwarning("Atención", "Carrito vacío")
            return

        nombre = self.entry_nombre.get().strip() or "Cliente"

        # Crear cliente
        cliente = Cliente(nombre=nombre)
        cliente_id = cliente.crear()

        # Preparar items
        items = [
            {'id': it['id'], 'precio': it['precio'], 'cantidad': it['cantidad']}
            for it in self.carrito
        ]

        # Crear pedido
        pedido = Pedido.crear_desde_carrito(cliente_id, items)

        # Registrar pago
        Pago.procesar_pago_simple(pedido['id'], pedido['total'])

        # Confirmación
        messagebox.showinfo(
            "Listo",
            f"Pedido {pedido['id']} creado\nTotal: ${pedido['total']:.2f}"
        )

        # Reset
        self.limpiar_carrito()
        self.entry_nombre.delete(0, tk.END)

    # -----------------------
    #        VER PEDIDOS
    # -----------------------
    def ver_pedidos(self):
        top = tk.Toplevel(self.root)
        top.title("Pedidos")

        cols = ("id", "cliente_id", "fecha", "total", "estado")
        tree = ttk.Treeview(top, columns=cols, show='headings')

        for c in cols:
            tree.heading(c, text=c.capitalize())

        tree.pack(fill='both', expand=True)

        try:
            rows = Pedido.listar_todos()
        except Exception:
            messagebox.showerror("Error", "No se pudo obtener pedidos")
            rows = []

        for r in rows:
            tree.insert(
                '',
                'end',
                values=(
                    r['id'],
                    r['cliente_id'],
                    str(r['fecha']),
                    float(r['total']),
                    r['estado']
                )
            )
