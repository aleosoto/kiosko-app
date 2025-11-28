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
        try:
            self.productos = Producto.listar_todos()
        except Exception as e:
            messagebox.showerror("Error DB", "No se pudo leer productos. Revisa configuración en app/config.py")
            self.productos = []
        self.carrito = []
        self.init_ui()

    def init_ui(self):
        left = tk.Frame(self.root)
        left.pack(side='left', fill='both', expand=True)
        right = tk.Frame(self.root, bd=2, relief='sunken', width=320)
        right.pack(side='right', fill='y')

        tk.Label(left, text="Menú", font=('Arial', 14)).pack(pady=5)
        cols = ("id","nombre","precio")
        self.tree = ttk.Treeview(left, columns=cols, show='headings', height=20)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.column("id", width=40)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)

        for p in self.productos:
            self.tree.insert('', 'end', iid=str(p['id']), values=(p['id'], p['nombre'], float(p['precio'])))

        btn_frame = tk.Frame(left)
        btn_frame.pack(pady=6)
        add_btn = tk.Button(btn_frame, text="Agregar al carrito", command=self.add_to_cart)
        add_btn.grid(row=0, column=0, padx=4)
        rem_btn = tk.Button(btn_frame, text="Quitar selección", command=self.remove_selected)
        rem_btn.grid(row=0, column=1, padx=4)
        view_btn = tk.Button(btn_frame, text="Ver pedidos", command=self.ver_pedidos)
        view_btn.grid(row=0, column=2, padx=4)

        tk.Label(right, text="Nombre del cliente:", font=('Arial', 10)).pack(pady=2)
        self.entry_nombre = tk.Entry(right, width=30)
        self.entry_nombre.pack(pady=2)

        tk.Label(right, text="Carrito", font=('Arial', 12)).pack(pady=5)
        self.txt_carrito = tk.Text(right, height=20, width=40)
        self.txt_carrito.pack(padx=6)
        tk.Button(right, text="Pagar (Efectivo)", command=self.pagar).pack(pady=8)
        tk.Button(right, text="Limpiar carrito", command=self.limpiar_carrito).pack()

    def add_to_cart(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un producto")
            return
        prod = Producto.obtener_por_id(int(sel))
        if not prod:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        item = {'id': prod['id'], 'nombre': prod['nombre'], 'precio': float(prod['precio']), 'cantidad': 1}
        self.carrito.append(item)
        self.refresh_carrito()

    def remove_selected(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un producto")
            return
        pid = int(sel)
        for i, it in enumerate(self.carrito):
            if it['id'] == pid:
                del self.carrito[i]
                break
        self.refresh_carrito()

    def refresh_carrito(self):
        self.txt_carrito.delete('1.0', tk.END)
        total = 0
        for p in self.carrito:
            line = f"{p['nombre']} x{p.get('cantidad',1)} - ${p['precio'] * p.get('cantidad',1):.2f}\n"
            self.txt_carrito.insert(tk.END, line)
            total += p['precio'] * p.get('cantidad',1)
        self.txt_carrito.insert(tk.END, f"\nTotal: ${total:.2f}")

    def limpiar_carrito(self):
        self.carrito = []
        self.refresh_carrito()

    def pagar(self):
        if not self.carrito:
            messagebox.showwarning("Atención", "Carrito vacío")
            return

        # Obtener nombre del cliente
        nombre_cliente = self.entry_nombre.get().strip()
        if not nombre_cliente:
            nombre_cliente = "Cliente"

        # Crear cliente con el nombre
        cliente = Cliente(nombre=nombre_cliente)
        cliente_id = cliente.crear()

        # Preparar items correctamente
        items = [{'id': it['id'], 'precio': it.get('precio', 0)} for it in self.carrito]

        # Crear pedido con cliente real
        pedido = Pedido.crear_desde_carrito(cliente_id, items)

        # Registrar el pago
        Pago.procesar_pago_simple(pedido['id'], pedido['total'])

        messagebox.showinfo(
            "Listo",
            f"Pedido {pedido['id']} creado a nombre de {nombre_cliente}\n"
            f"Total: ${pedido['total']:.2f}"
        )

        self.carrito = []
        self.entry_nombre.delete(0, tk.END)
        self.refresh_carrito()

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
        except Exception as e:
            messagebox.showerror("Error", "No se pudo obtener pedidos")
            rows = []

        for r in rows:
            tree.insert('', 'end', values=(r['id'], r['cliente_id'], str(r['fecha']), float(r['total']), r['estado']))
