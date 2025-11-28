# app/gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.user import Cliente
from app.models.pago import Pago

class KioscoGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600")
        self.productos = Producto.listar_todos()
        self.carrito = []
        self.init_ui()

    def init_ui(self):
        left = tk.Frame(self.root)
        left.pack(side='left', fill='both', expand=True)
        right = tk.Frame(self.root, bd=2, relief='sunken', width=300)
        right.pack(side='right', fill='y')

        tk.Label(left, text="Menú").pack()
        self.tree = ttk.Treeview(left, columns=("precio",), show='headings')
        self.tree.heading("precio", text="Precio")
        self.tree.pack(fill='both', expand=True)
        for p in self.productos:
            self.tree.insert('', 'end', iid=p['id'], values=(p['nombre'], p['precio']))

        add_btn = tk.Button(left, text="Agregar al carrito", command=self.add_to_cart)
        add_btn.pack(pady=10)

        tk.Label(right, text="Carrito").pack()
        self.txt_carrito = tk.Text(right, height=20, width=35)
        self.txt_carrito.pack()
        tk.Button(right, text="Pagar", command=self.pagar).pack(pady=10)

    def add_to_cart(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un producto")
            return
        prod = Producto.obtener_por_id(int(sel))
        self.carrito.append(prod)
        self.refresh_carrito()

    def refresh_carrito(self):
        self.txt_carrito.delete('1.0', tk.END)
        total = 0
        for p in self.carrito:
            self.txt_carrito.insert(tk.END, f"{p['nombre']} - ${p['precio']}\n")
            total += float(p['precio'])
        self.txt_carrito.insert(tk.END, f"\nTotal: ${total:.2f}")

    def pagar(self):
        if not self.carrito:
            messagebox.showwarning("Atención", "Carrito vacío")
            return
        # Simplificación: cliente anónimo
        cliente = Cliente(nombre="Anonimo")
        cliente.crear_en_bd()
        pedido = Pedido.crear_desde_carrito(cliente_id=None, items=self.carrito)
        Pago.procesar_pago_simple(pedido['id'], sum(float(i['precio']) for i in self.carrito))
        messagebox.showinfo("Listo", f"Pedido {pedido['id']} creado y pago procesado.")
        self.carrito.clear()
        self.refresh_carrito()
