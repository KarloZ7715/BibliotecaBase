import csv
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Text
from tkinter.ttk import Combobox
from tkinter import filedialog


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="", database="bibliotecaamz"
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None


class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel Administrativo")
        self.root.geometry("800x200")
        self.root.configure(bg="#87CEEB")
        self.user_id = None

        self.login_window()

        self.menu_frame = tk.Frame(self.root, bg="white", height=50)
        self.menu_frame.pack(fill=tk.X)

        self.sections = {
            "Usuarios": ["Agregar Usuario", "Gestionar Usuarios"],
            "Libros": ["Nuevo Libro", "Gestionar Libros"],
            "Pedidos": ["Gestionar Pedidos"],
            "Categorías": ["Agregar Categoría", "Gestionar Categorías"],
            "Autores": ["Agregar Autor", "Gestionar Autores"],
            "Registros": ["Visualizar Registros", "Filtrar Registros"],
            "Otros": ["Cerrar Sesión"],
        }

        self.buttons = {}
        self.submenu = None
        self.timer_id = None

        for section, callback in self.sections.items():
            btn = tk.Label(
                self.menu_frame,
                text=section,
                bg="white",
                fg="black",
                padx=20,
                pady=10,
                font=("Arial", 12),
            )
            btn.pack(side=tk.LEFT, padx=5)
            btn.bind("<Enter>", lambda event, s=section: self.on_hover(event, s))
            btn.bind("<Leave>", lambda event: self.on_leave(event))
            btn.bind("<Button-1>")
            self.buttons[section] = btn

    def on_hover(self, event, section):
        event.widget.config(bg="#87CEEB", fg="white")
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.show_submenu(section, event.widget)

    def on_leave(self, event):
        event.widget.config(bg="white", fg="black")
        if not self.submenu:
            return
        self.schedule_submenu_close()

    def show_submenu(self, section, parent):
        if self.submenu:
            self.submenu.destroy()

        self.submenu = tk.Toplevel(self.root)
        self.submenu.overrideredirect(True)
        self.submenu.geometry(
            f"150x{len(self.sections[section]) * 30}+{parent.winfo_rootx()}+{parent.winfo_rooty() + 50}"
        )
        self.submenu.configure(bg="white")
        self.submenu.bind("<Enter>", lambda e: self.cancel_submenu_close())
        self.submenu.bind("<Leave>", lambda e: self.schedule_submenu_close())

        for option in self.sections[section]:
            btn = tk.Button(
                self.submenu,
                text=option,
                bg="white",
                fg="black",
                bd=0,
                font=("Arial", 10),
                anchor="w",
                activebackground="#4682B4",
                activeforeground="white",
                command=lambda opt=option: self.open_window(section, opt),
            )
            btn.pack(fill=tk.X, padx=10, pady=2)

    def hide_submenu(self):
        if self.submenu:
            self.submenu.destroy()
            self.submenu = None

    def schedule_submenu_close(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.timer_id = self.root.after(200, self.hide_submenu)

    def cancel_submenu_close(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def open_window(self, section, option):
        if section == "Usuarios" and option == "Agregar Usuario":
            self.agregar_usuario()
        elif section == "Usuarios" and option == "Gestionar Usuarios":
            self.gestionar_usuarios()
        elif section == "Libros" and option == "Nuevo Libro":
            self.nuevo_libro()
        elif section == "Libros" and option == "Gestionar Libros":
            self.gestionar_libros()
        elif section == "Categorías" and option == "Agregar Categoría":
            self.agregar_categoria()
        elif section == "Categorías" and option == "Gestionar Categorías":
            self.gestionar_categorias()
        elif section == "Autores" and option == "Agregar Autor":
            self.agregar_autor()
        elif section == "Autores" and option == "Gestionar Autores":
            self.gestionar_autores()
        elif section == "Pedidos" and option == "Gestionar Pedidos":
            self.gestionar_pedidos()
        elif section == "Registros" and option == "Visualizar Registros":
            self.visualizar_registros()
        elif section == "Registros" and option == "Filtrar Registros":
            self.filtrar_registros()
        elif section == "Otros" and option == "Cerrar Sesión":
            self.logout()

    def login_window(self):
        login_win = tk.Toplevel(self.root)
        login_win.title("Iniciar Sesión")
        login_win.geometry("300x200")
        login_win.transient(self.root)
        login_win.grab_set()
        login_win.focus_set()
        login_win.protocol("WM_DELETE_WINDOW", self.on_login_close)

        tk.Label(login_win, text="Correo:").pack(pady=5)
        email_entry = tk.Entry(login_win)
        email_entry.pack(pady=5)

        tk.Label(login_win, text="Contraseña:").pack(pady=5)
        password_entry = tk.Entry(login_win, show="*")
        password_entry.pack(pady=5)

        def login():
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            if self.authenticate_user(email, password):
                if self.user_role == "admin":
                    login_win.destroy()
                else:
                    messagebox.showerror(
                        "Acceso Denegado",
                        "Solo los administradores pueden acceder a esta interfaz.",
                    )
            else:
                messagebox.showerror("Error", "Correo o contraseña incorrectos.")

        tk.Button(login_win, text="Iniciar Sesión", command=login).pack(pady=10)

    def on_login_close(self):
        self.root.destroy()

    def authenticate_user(self, email, password):
        try:
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_usuario, rol FROM usuarios WHERE correo = %s AND contraseña = %s",
                (email, password),
            )
            user = cursor.fetchone()
            if user:
                self.user_id = user["id_usuario"]
                self.user_role = user["rol"]
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al autenticar al usuario: {e}")
            return False
        finally:
            if connection:
                connection.close()

    def registrar_accion(self, accion, detalles):
        try:
            # print(f"Registrando acción: {accion}, detalles: {detalles}")
            connection = create_connection()
            cursor = connection.cursor()
            cursor.callproc("registrar_accion", (self.user_id, accion, detalles))
            connection.commit()
            connection.close()
            print("Acción registrada correctamente.")
        except Exception as e:
            print(f"Error al registrar la acción: {e}")

    def agregar_usuario(self):
        window = tk.Toplevel(self.root)
        window.title("Agregar Usuario")
        window.geometry("300x300")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        fields = ["Nombre", "Correo", "Contraseña", "Dirección", "Teléfono"]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(window, text=field, bg="white", font=("Arial", 10)).grid(
                row=i, column=0, pady=5, padx=10, sticky="w"
            )
            entry = tk.Entry(window, font=("Arial", 10))
            entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
            entries[field] = entry

        tk.Label(window, text="Rol", bg="white", font=("Arial", 10)).grid(
            row=len(fields), column=0, pady=5, padx=10, sticky="w"
        )

        rol_combobox = Combobox(window, values=["admin", "cliente"], font=("Arial", 10))
        rol_combobox.grid(row=len(fields), column=1, pady=5, padx=10, sticky="w")
        rol_combobox.set("cliente")

        label_exito = tk.Label(
            window, text="", bg="white", fg="green", font=("Arial", 10)
        )
        label_exito.grid(row=len(fields) + 1, column=0, columnspan=2, pady=5)

        def guardar_usuario():
            datos = {campo: entry.get().strip() for campo, entry in entries.items()}
            datos["Rol"] = rol_combobox.get().strip()
            for campo, valor in datos.items():
                if not valor:
                    messagebox.showerror("Error", f"El campo {campo} está vacío.")
                    return
            try:
                int(datos["Teléfono"])
            except ValueError:
                messagebox.showerror("Error", "El campo Teléfono debe ser un número.")
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                query = """
                INSERT INTO usuarios (nombre, correo, contraseña, direccion, telefono, rol)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        datos["Nombre"],
                        datos["Correo"],
                        datos["Contraseña"],
                        datos["Dirección"],
                        datos["Teléfono"],
                        datos["Rol"],
                    ),
                )
                connection.commit()
                connection.close()

                self.registrar_accion(
                    "Inserción", f"Usuario {datos['Nombre']} agregado"
                )
                label_exito.config(text="Usuario guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}")

        tk.Button(
            window,
            text="Guardar",
            bg="#4682B4",
            fg="white",
            font=("Arial", 10),
            command=guardar_usuario,
        ).grid(row=len(fields) + 1, column=1, pady=10)

    def gestionar_usuarios(self):
        window = tk.Toplevel(self.root)
        window.title("Gestionar Usuarios")
        window.geometry("1370x720")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        columns = [
            "ID",
            "Nombre",
            "Correo",
            "Contraseña",
            "Dirección",
            "Teléfono",
            "Rol",
        ]
        tree = ttk.Treeview(window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        tree.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            window, text="Seleccione un usuario para modificar o eliminar", bg="white"
        ).pack()
        frame = tk.Frame(window, bg="white")
        frame.pack()
        fields = ["Nombre", "Correo", "Contraseña", "Dirección", "Teléfono"]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(frame, text=field, bg="white", font=("Arial", 10)).grid(
                row=i, column=0, pady=5, padx=10, sticky="w"
            )
            entry = tk.Entry(frame, font=("Arial", 10))
            entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")
            entries[field] = entry

        tk.Label(frame, text="Rol", bg="white", font=("Arial", 10)).grid(
            row=len(fields), column=0, pady=5, padx=10, sticky="w"
        )
        rol_combo = Combobox(frame, values=["admin", "cliente"], font=("Arial", 10))
        rol_combo.grid(row=len(fields), column=1, pady=5, padx=10, sticky="w")

        selected_user = None

        def cargar_usuarios():
            tree.delete(*tree.get_children())
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            for usuario in usuarios:
                tree.insert(
                    "",
                    "end",
                    values=(
                        usuario["id_usuario"],
                        usuario["nombre"],
                        usuario["correo"],
                        usuario["contraseña"],
                        usuario["dirección"],
                        usuario["teléfono"],
                        usuario["rol"],
                    ),
                )
            connection.close()

        def seleccionar_usuario(event):
            nonlocal selected_user
            item = tree.focus()
            selected_user = tree.item(item)["values"]
            if selected_user:
                for i, field in enumerate(fields):
                    entries[field].delete(0, tk.END)
                    entries[field].insert(0, selected_user[i + 1])
                rol_combo.set(selected_user[-1])

        def actualizar_usuario():
            if not selected_user:
                messagebox.showerror("Error", "Seleccione un usuario para actualizar.")
                return

            datos = {field: entry.get().strip() for field, entry in entries.items()}
            datos["Rol"] = rol_combo.get().strip()
            for field, value in datos.items():
                if not value:
                    messagebox.showerror("Error", f"El campo {field} está vacío.")
                    return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                query = """
                UPDATE usuarios SET nombre=%s, correo=%s, contraseña=%s, direccion=%s, telefono=%s, rol=%s WHERE id_usuario=%s
                """
                cursor.execute(query, (*datos.values(), selected_user[0]))
                connection.commit()
                connection.close()
                cargar_usuarios()
                self.registrar_accion(
                    "Actualización", f"Usuario {datos['Nombre']} actualizado"
                )
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el usuario: {e}")

        def eliminar_usuario():
            if not selected_user:
                messagebox.showerror("Error", "Seleccione un usuario para eliminar.")
                return

            confirm = messagebox.askyesno(
                "Confirmación", "¿Está seguro de que desea eliminar este usuario"
            )
            if not confirm:
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                query = "DELETE FROM usuarios WHERE id_usuario=%s"
                cursor.execute(query, (selected_user[0],))
                connection.commit()
                connection.close()
                cargar_usuarios()
                self.registrar_accion(
                    "Eliminación", f"Usuario {selected_user[1]} eliminado"
                )
                for entry in entries.values():
                    entry.delete(0, tk.END)
                rol_combo.set("")
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")

        cargar_usuarios()
        tree.bind("<ButtonRelease-1>", seleccionar_usuario)

        tk.Button(
            window,
            text="Actualizar",
            bg="green",
            fg="white",
            command=actualizar_usuario,
        ).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(
            window, text="Eliminar", bg="red", fg="white", command=eliminar_usuario
        ).pack(side=tk.RIGHT, padx=10, pady=10)

    def nuevo_libro(self):
        window = tk.Toplevel(self.root)
        window.title("Nuevo Libro")
        window.geometry("500x550")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        fields = [
            "Título",
            "Descripción",
            "Autor",
            "Categoría",
            "Precio",
            "Stock",
            "Imagen URL",
            "Fecha Publicación",
            "ISBN",
        ]

        entries = {}
        autores = {}
        categorias = {}

        def cargar_datos():
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT id_autor, nombre FROM autores")
            for autor in cursor.fetchall():
                autores[autor["nombre"]] = autor["id_autor"]

            cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias")
            for categoria in cursor.fetchall():
                categorias[categoria["nombre_categoria"]] = categoria["id_categoria"]

            connection.close()

            entries["Autor"]["values"] = list(autores.keys())
            entries["Categoría"]["values"] = list(categorias.keys())

        for i, field in enumerate(fields):
            tk.Label(window, text=field, bg="white", font=("Arial", 10)).grid(
                row=i, column=0, pady=5, padx=10, sticky="w"
            )
            if field == "Descripción":
                entry = Text(window, height=5, width=30, font=("Arial", 10))
                entry.grid(row=i, column=1, pady=5, padx=10)

            elif field == "Autor":
                entry = Combobox(window, state="readonly")
                entry.grid(row=i, column=1, pady=5, padx=10)
            elif field == "Categoría":
                entry = Combobox(window, state="readonly")
                entry.grid(row=i, column=1, pady=5, padx=10)
            else:
                entry = tk.Entry(window, font=("Arial", 10))
                entry.grid(row=i, column=1, pady=5, padx=10)
            entries[field] = entry

        label_exito = tk.Label(
            window, text="", bg="white", fg="green", font=("Arial", 10)
        )
        label_exito.grid(row=len(fields) + 1, column=0, columnspan=2, pady=5)

        def guardar_libro():
            datos = {}
            for campo, widget in entries.items():
                if isinstance(widget, Text):
                    datos[campo] = widget.get("1.0", tk.END).strip()
                else:
                    datos[campo] = widget.get().strip()

            for campo, valor in datos.items():
                if not valor:
                    messagebox.showerror("Error", f"El campo {campo} está vacío")
                    return

            try:
                float(datos["Precio"])
                int(datos["Stock"])
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Precio debe ser númerico y Stock debe ser un número entero",
                )
                return

            id_autor = autores.get(datos["Autor"])
            id_categoria = categorias.get(datos["Categoría"])

            if id_autor is None or id_categoria is None:
                messagebox.showerror(
                    "Error", "Autor o Categoría seleccionados no son válidos."
                )
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                query = """
                INSERT INTO libros (titulo, descripcion, id_autor, id_categoria, precio, stock, imagen_url, fecha_publicacion, isbn)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        datos["Título"],
                        datos["Descripción"],
                        id_autor,
                        id_categoria,
                        datos["Precio"],
                        datos["Stock"],
                        datos["Imagen URL"],
                        datos["Fecha Publicación"],
                        datos["ISBN"],
                    ),
                )
                connection.commit()
                connection.close()
                self.registrar_accion(
                    "Insercción",
                    f"Libro {datos['Título']} agregado correctamente",
                )
                label_exito.config(text="Libro guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el libro: {e}")

        tk.Button(
            window,
            text="Guardar",
            bg="#4682B4",
            fg="white",
            font=("Arial", 10),
            command=guardar_libro,
        ).grid(row=len(fields), column=1, pady=10)

        cargar_datos()

    def gestionar_libros(self):
        window = tk.Toplevel(self.root)
        window.title("Gestionar Libros")
        window.geometry("1100x500")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        autores = {}
        categorias = {}

        tree = ttk.Treeview(
            window,
            columns=(
                "ID",
                "Título",
                "Descripción",
                "Autor",
                "Categoría",
                "Precio",
                "Stock",
                "Imagen URL",
                "Fecha Publicación",
                "ISBN",
            ),
            show="headings",
            height=15,
        )

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=4, sticky="ns")

        def cargar_datos():
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT id_autor, nombre FROM autores")
            for autor in cursor.fetchall():
                autores[autor["nombre"]] = autor["id_autor"]

            cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias")
            for categoria in cursor.fetchall():
                categorias[categoria["nombre_categoria"]] = categoria["id_categoria"]

            query = """
            SELECT l.id_libro, l.titulo, l.descripcion, a.nombre AS autor, c.nombre_categoria AS categoria, l.precio, l.stock, l.imagen_url, l.fecha_publicacion, l.isbn
            FROM libros l
            JOIN autores a ON l.id_autor = a.id_autor
            JOIN categorias c ON l.id_categoria = c.id_categoria
            """
            cursor.execute(query)
            libros = cursor.fetchall()
            connection.close()

            for row in tree.get_children():
                tree.delete(row)
            for libro in libros:
                tree.insert("", "end", values=tuple(libro.values()))

        def editar_libro():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Selecciona un libro para editar.")
                return

            libro = tree.item(selected_item)["values"]

            edit_window = tk.Toplevel(window)
            edit_window.title("Editar Libro")
            edit_window.geometry("500x550")
            edit_window.configure(bg="white")

            fields = [
                "Título",
                "Descripción",
                "Autor",
                "Categoría",
                "Precio",
                "Stock",
                "Imagen URL",
                "Fecha Publicación",
                "ISBN",
            ]

            entries = {}

            for i, field in enumerate(fields):
                tk.Label(edit_window, text=field, bg="white", font=("Arial", 10)).grid(
                    row=i, column=0, pady=5, padx=10, sticky="w"
                )
                if field == "Descripción":
                    entry = Text(edit_window, height=5, width=30, font=("Arial", 10))
                    entry.insert("1.0", libro[i + 1])
                    entry.grid(row=i, column=1, pady=5, padx=10)
                elif field == "Autor":
                    entry = Combobox(edit_window, state="readonly")
                    entry["values"] = list(autores.keys())
                    entry.set(libro[3])
                    entry.grid(row=i, column=1, pady=5, padx=10)
                elif field == "Categoría":
                    entry = Combobox(edit_window, state="readonly")
                    entry["values"] = list(categorias.keys())
                    entry.set(libro[4])
                    entry.grid(row=i, column=1, pady=5, padx=10)
                else:
                    entry = tk.Entry(edit_window, font=("Arial", 10))
                    entry.insert(0, libro[i + 1])
                    entry.grid(row=i, column=1, pady=5, padx=10)
                entries[field] = entry

            def guardar_cambios():
                datos = {}
                for campo, widget in entries.items():
                    if isinstance(widget, Text):
                        datos[campo] = widget.get("1.0", tk.END).strip()
                    else:
                        datos[campo] = widget.get().strip()

                for campo, valor in datos.items():
                    if not valor:
                        messagebox.showerror("Error", f"El campo {campo} está vacio.")
                        return

                try:
                    float(datos["Precio"])
                    int(datos["Stock"])
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        "Precio deber ser numérico y Stock debe ser un número entero.",
                    )
                    return

                id_autor = autores.get(datos["Autor"])
                id_categoria = categorias.get(datos["Categoría"])

                if id_autor is None or id_categoria is None:
                    messagebox.showerror(
                        "Error", "Autor o categoría seleccionados no son válidos."
                    )
                    return

                try:
                    connection = create_connection()
                    cursor = connection.cursor()
                    query = """
                    UPDATE libros
                    SET titulo = %s, descripcion = %s, id_autor = %s, id_categoria = %s, precio = %s,
                        stock = %s, imagen_url = %s, fecha_publicacion = %s, isbn = %s
                    WHERE id_libro = %s
                    """
                    cursor.execute(
                        query,
                        (
                            datos["Título"],
                            datos["Descripción"],
                            id_autor,
                            id_categoria,
                            datos["Precio"],
                            datos["Stock"],
                            datos["Imagen URL"],
                            datos["Fecha Publicación"],
                            datos["ISBN"],
                            libro[0],
                        ),
                    )
                    connection.commit()
                    connection.close()
                    self.registrar_accion(
                        "Actualización",
                        f"Libro {datos['Título']} actualizado correctamente",
                    )
                    cargar_datos()
                    messagebox.showinfo("Éxito", "Libro actualizado correctamente.")
                    edit_window.destroy()
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"No se pudo actualizar el libro: {e}"
                    )

            tk.Button(
                edit_window,
                text="Guardar Cambios",
                bg="#4682B4",
                fg="white",
                font=("Arial", 10),
                command=guardar_cambios,
            ).grid(row=len(fields), column=1, pady=10)

        def eliminar_libro():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Selecciona un libro para eliminar")
                return

            libro_id = tree.item(selected_item)["values"]
            id_libro = libro_id[0]

            confirm = messagebox.askyesno(
                "Confirmar", "¿Estás seguro de que deseas eliminar este libro?"
            )
            if not confirm:
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                query = "DELETE FROM libros WHERE id_libro = %s"
                cursor.execute(query, (id_libro,))
                connection.commit()
                connection.close()
                self.registrar_accion(
                    "Eliminación", f"Libro {libro_id} eliminado correctamente"
                )
                messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
                cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el libro: {e}")

        tk.Button(
            window, text="Editar", bg="blue", fg="white", command=editar_libro
        ).grid(row=1, column=0, pady=10)
        tk.Button(
            window, text="Eliminar", bg="red", fg="white", command=eliminar_libro
        ).grid(row=1, column=1, pady=10)
        tk.Button(
            window, text="Actualizar", bg="green", fg="white", command=cargar_datos
        ).grid(row=1, column=2, pady=10)

        cargar_datos()

    def agregar_categoria(self):
        window = tk.Toplevel(self.root)
        window.title("Agregar Categoría")
        window.geometry("400x100")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        tk.Label(
            window, text="Nombre de Categoría", bg="white", font=("Arial", 10)
        ).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        nombre_categoria = tk.Entry(window, font=("Arial", 10), width=30)
        nombre_categoria.grid(row=0, column=1, pady=10, padx=10)

        def guardar_categoria():
            nombre = nombre_categoria.get().strip()
            if not nombre:
                messagebox.showerror(
                    "Error", "El campo 'Nombre de Categoría' está vacío."
                )
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO categorias (nombre_categoria) VALUES (%s)", (nombre,)
                )
                connection.commit()
                connection.close()
                self.registrar_accion(
                    "Inserción", f"Categoría {nombre} agregada correctamente"
                )
                messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la categoría {e}")

        tk.Button(
            window,
            text="Guardar",
            bg="#4682B4",
            fg="white",
            font=("Arial", 10),
            command=guardar_categoria,
        ).grid(row=2, column=1, pady=20)

    def gestionar_categorias(self):
        window = tk.Toplevel(self.root)
        window.title("Gestionar Categorias")
        window.geometry("600x500")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        tree = ttk.Treeview(
            window, columns=("ID", "Nombre"), show="headings", height=15
        )
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.column("ID", width=50)
        tree.column("Nombre", width=200)
        tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky="ns")

        tk.Label(
            window, text="Nombre de Categoría", bg="white", font=("Arial", 10)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        nombre_categoria = tk.Entry(window, font=("Arial", 10), width=30)
        nombre_categoria.grid(row=1, column=1, padx=10, pady=10)

        def cargar_categoria():
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categorias")
            categorias = cursor.fetchall()
            connection.close()

            for row in tree.get_children():
                tree.delete(row)
            for categoria in categorias:
                tree.insert(
                    "",
                    "end",
                    values=(categoria["id_categoria"], categoria["nombre_categoria"]),
                )

        def seleccionar_categoria(event):
            item = tree.focus()
            if not item:
                return
            datos = tree.item(item, "values")
            nombre_categoria.delete(0, tk.END)
            nombre_categoria.insert(0, datos[1])

        def actualizar_categoria():
            item = tree.focus()
            if not item:
                messagebox.showerror(
                    "Error", "Selecciona una categoría para actualizar."
                )
                return

            id_categoria = tree.item(item, "values")[0]
            nuevo_nombre = nombre_categoria.get().strip()
            if not nuevo_nombre:
                messagebox.showerror(
                    "Error", "El campo 'Nombre de Categoría' está vacío."
                )
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE categorias SET nombre_categoria = %s WHERE id_categoria = %s",
                    (nuevo_nombre, id_categoria),
                )
                connection.commit()
                connection.close()
                self.registrar_accion(
                    "Actualización", f"Categoría {nuevo_nombre} actualizada"
                )
                cargar_categoria()
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente.")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo actualizar la categoría: {e}"
                )

        def eliminar_categoria():
            item = tree.focus()
            if not item:
                messagebox.showerror("Error", "Selecciona una categoría para eliminar.")
                return

            id_categoria = tree.item(item, "values")[0]
            confirm = messagebox.askyesno(
                "Confirmar", "¿Estás seguro de que deseas eliminar esta categoría?"
            )
            if not confirm:
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,)
                )
                connection.commit()
                connection.close()
                self.registrar_accion(
                    "Eliminación", f"Categoría {id_categoria} eliminada"
                )
                cargar_categoria()
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la categoría: {e}")

        tk.Button(
            window, text="Eliminar", bg="red", fg="white", command=eliminar_categoria
        ).grid(row=2, column=1, pady=10)
        tk.Button(
            window,
            text="Actualizar",
            bg="green",
            fg="white",
            command=actualizar_categoria,
        ).grid(row=2, column=0, pady=10)

        tree.bind("<ButtonRelease-1>", seleccionar_categoria)
        cargar_categoria()

    def agregar_autor(self):
        window = tk.Toplevel(self.root)
        window.title("Agregar Autor")
        window.geometry("500x300")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        tk.Label(window, text="Nombre*", bg="white", font=("Arial", 10)).grid(
            row=0, column=0, pady=10, padx=10, sticky="w"
        )
        nombre = tk.Entry(window, font=("Arial", 10), width=30)
        nombre.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(window, text="Biografía", bg="white", font=("Arial", 10)).grid(
            row=1, column=0, pady=10, padx=10, sticky="w"
        )
        biografia = tk.Text(window, font=("Arial", 10), width=30, height=5)
        biografia.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(
            window,
            text="Fecha de Nacimiento (YYYY-MM-DD)*",
            bg="white",
            font=("Arial", 10),
        ).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        fecha_nacimiento = tk.Entry(window, font=("Arial", 10), width=30)
        fecha_nacimiento.grid(row=2, column=1, pady=10, padx=10)

        def guardar_autor():
            nombre_valor = nombre.get().strip()
            biografia_valor = biografia.get("1.0", "end").strip()
            fecha_valor = fecha_nacimiento.get().strip()

            if not nombre_valor or not fecha_valor:
                messagebox.showerror(
                    "Error",
                    "Los campos 'Nombre' y 'Fecha de Nacimiento' son obligatorios",
                )
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO autores (nombre, biografia, fecha_nacimiento) VALUES (%s, %s, %s)",
                    (nombre_valor, biografia_valor, fecha_valor),
                )
                connection.commit()
                connection.close()
                self.registrar_accion(
                    "Inserción", f"Autor {nombre_valor} agregado correctamente"
                )
                messagebox.showinfo("Éxito", "Autor agregado correctamente.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el autor: {e}")

        tk.Button(
            window,
            text="Guardar",
            bg="#4682B4",
            fg="white",
            font=("Arial", 10),
            command=guardar_autor,
        ).grid(row=3, column=1, pady=20)

    def gestionar_autores(self):
        window = tk.Toplevel(self.root)
        window.title("Gestionar Autores")
        window.geometry("700x500")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        tree = ttk.Treeview(
            window,
            columns=("ID", "Nombre", "Fecha de Nacimiento"),
            show="headings",
            height=15,
        )
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Fecha de Nacimiento", text="Fecha de Nacimiento")
        tree.column("ID", width=50)
        tree.column("Nombre", width=200)
        tree.column("Fecha de Nacimiento", width=150)
        tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        tk.Label(window, text="Nombre", bg="white", font=("Arial", 10)).grid(
            row=1, column=0, pady=10, padx=10, sticky="w"
        )
        nombre = tk.Entry(window, font=("Arial", 10), width=30)
        nombre.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(
            window,
            text="Fecha de Nacimiento (YYYY-MM-DD)",
            bg="white",
            font=("Arial", 10),
        ).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        fecha_nacimiento = tk.Entry(window, font=("Arial", 10), width=30)
        fecha_nacimiento.grid(row=2, column=1, pady=10, padx=10)

        def cargar_autores():
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM autores")
            autores = cursor.fetchall()
            connection.close()

            for row in tree.get_children():
                tree.delete(row)
            for autor in autores:
                tree.insert(
                    "",
                    "end",
                    values=(
                        autor["id_autor"],
                        autor["nombre"],
                        autor["fecha_nacimiento"],
                    ),
                )

        def seleccionar_autor(event):
            item = tree.focus()
            if not item:
                return
            datos = tree.item(item, "values")
            nombre.delete(0, tk.END)
            nombre.insert(0, datos[1])
            fecha_nacimiento.delete(0, tk.END)
            fecha_nacimiento.insert(0, datos[2])

        def actualizar_autor():
            item = tree.focus()
            if not item:
                messagebox.showerror("Error", "Selecciona un autor para actualizar.")
                return

            id_autor = tree.item(item, "values")[0]
            nuevo_nombre = nombre.get().strip()
            nueva_fecha = fecha_nacimiento.get().strip()

            if not nuevo_nombre or not nueva_fecha:
                messagebox.showerror(
                    "Error",
                    "Los campos 'Nombre' y 'Fecha de Nacimiento' son obligatorios.",
                )
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE autores SET nombre = %s, fecha_nacimiento = %s WHERE id_autor = %s",
                    (nuevo_nombre, nueva_fecha, id_autor),
                )
                connection.commit()
                connection.close()
                self.registrar_accion(
                    "Actualización", f"Autor {nuevo_nombre} actualizado"
                )
                cargar_autores()
                messagebox.showinfo("Éxito", "Autor actualizado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el autor: {e}")

        def eliminar_autor():
            item = tree.focus()
            if not item:
                messagebox.showerror("Error", "Selecciona un autor para eliminar.")
                return

            id_autor = tree.item(item, "values")[0]
            confirm = messagebox.askyesno(
                "Confirmar", "¿Estás seguro de que deseas eliminar este autor?"
            )
            if not confirm:
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM autores WHERE id_autor = %s", (id_autor))
                connection.commit()
                connection.close()
                self.registrar_accion("Eliminación", f"Autor {id_autor} eliminado")
                messagebox.showinfo("Éxito", "Autor eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el autor: {e}")

        def editar_biografia():
            item = tree.focus()
            if not item:
                messagebox.showerror(
                    "Error", "Selecciona un autor para editar su biografía."
                )
                return

            id_autor = tree.item(item, "values")[0]

            def guardar_biografia():
                nueva_biografia = biografia_text.get("1.0", "end").strip()
                try:
                    connection = create_connection()
                    cursor = connection.cursor()
                    cursor.execute(
                        "UPDATE autores SET biografia = %s WHERE id_autor = %s",
                        (nueva_biografia, id_autor),
                    )
                    self.registrar_accion(
                        "Actualización",
                        f"Biografía del autor {id_autor} actualizada",
                    )
                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Éxito", "Biografía actualizada correctamente.")
                    bio_window.destroy()
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"No se pudo actualizar la biografía: {e}"
                    )

            bio_window = tk.Toplevel(window)
            bio_window.title("Editar Biografía")
            bio_window.geometry("400x300")
            bio_window.transient(window)
            bio_window.grab_set()

            tk.Label(bio_window, text="Biografía", font=("Arial", 10)).pack(pady=10)
            biografia_text = tk.Text(
                bio_window, font=("Arial", 10), width=40, height=10, wrap="word"
            )
            biografia_text.pack(pady=10)

            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT biografia FROM autores WHERE id_autor = %s", (id_autor,)
            )
            biografia = cursor.fetchone()["biografia"]
            connection.close()
            biografia_text.insert("1.0", biografia)

            tk.Button(bio_window, text="Guardar", command=guardar_biografia).pack(
                pady=10
            )

        tk.Button(
            window, text="Actualizar", bg="green", fg="white", command=actualizar_autor
        ).grid(row=3, column=0, pady=10)
        tk.Button(
            window, text="Eliminar", bg="red", fg="white", command=eliminar_autor
        ).grid(row=3, column=1, pady=10)
        tk.Button(
            window,
            text="Editar Biografía",
            bg="blue",
            fg="white",
            command=editar_biografia,
        ).grid(row=3, column=2, pady=10)

        tree.bind("<ButtonRelease-1>", seleccionar_autor)
        cargar_autores()

    def gestionar_pedidos(self):
        window = tk.Toplevel(self.root)
        window.title("Gestionar Pedidos")
        window.geometry("900x720")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        tree = ttk.Treeview(
            window,
            columns=("ID-Pedido", "ID-Nombre", "Total", "Fecha del Pedido", "Estado"),
            show="headings",
            height=15,
        )

        tree.heading("ID-Pedido", text="ID-Pedido")
        tree.heading("ID-Nombre", text="ID-Nombre")
        tree.heading("Total", text="Total")
        tree.heading("Fecha del Pedido", text="Fecha del Pedido")
        tree.heading("Estado", text="Estado")
        tree.column("ID-Pedido", width=100)
        tree.column("ID-Nombre", width=100)
        tree.column("Total", width=100)
        tree.column("Fecha del Pedido", width=150)
        tree.column("Estado", width=120)
        tree.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=4, sticky="ns")

        tk.Label(window, text="ID-Pedido", bg="white", font=("Arial", 10)).grid(
            row=1, column=0, pady=10, padx=10, sticky="w"
        )
        id_pedido = tk.Entry(window, font=("Arial", 10), width=30, state="readonly")
        id_pedido.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(window, text="ID-Nombre", bg="white", font=("Arial", 10)).grid(
            row=2, column=0, pady=10, padx=10, sticky="w"
        )
        id_nombre = tk.Entry(window, font=("Arial", 10), width=30, state="readonly")
        id_nombre.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(window, text="Total", bg="white", font=("Arial", 10)).grid(
            row=3, column=0, pady=10, padx=10, sticky="w"
        )
        total = tk.Entry(window, font=("Arial", 10), width=30, state="readonly")
        total.grid(row=3, column=1, pady=10, padx=10)

        tk.Label(window, text="Fecha del Pedido", bg="white", font=("Arial", 10)).grid(
            row=4, column=0, pady=10, padx=10, sticky="w"
        )
        fecha_pedido = tk.Entry(window, font=("Arial", 10), width=30, state="readonly")
        fecha_pedido.grid(row=4, column=1, pady=10, padx=10)

        tk.Label(window, text="Estado", bg="white", font=("Arial", 10)).grid(
            row=5, column=0, pady=10, padx=10, sticky="w"
        )
        estado = ttk.Combobox(window, font=("Arial", 10), width=27, state="readonly")
        estado["values"] = ["Pendiente", "En proceso", "Completado"]
        estado.grid(row=5, column=1, pady=10, padx=10)

        def cargar_pedidos():
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pedidos")
            pedidos = cursor.fetchall()
            connection.close()

            for row in tree.get_children():
                tree.delete(row)
            for pedido in pedidos:
                tree.insert(
                    "",
                    "end",
                    values=(
                        pedido["id_pedido"],
                        pedido["id_usuario"],
                        pedido["total"],
                        pedido["fecha_pedido"],
                        pedido["estado"],
                    ),
                )

        def seleccionar_pedido(event):
            item = tree.focus()
            if not item:
                return

            datos = tree.item(item, "values")
            id_pedido.configure(state="normal")
            id_pedido.delete(0, tk.END)
            id_pedido.insert(0, datos[0])
            id_pedido.configure(state="readonly")

            id_nombre.configure(state="normal")
            id_nombre.delete(0, tk.END)
            id_nombre.insert(0, datos[1])
            id_nombre.configure(state="readonly")

            total.configure(state="normal")
            total.delete(0, tk.END)
            total.insert(0, datos[2])
            total.configure(state="readonly")

            fecha_pedido.configure(state="normal")
            fecha_pedido.delete(0, tk.END)
            fecha_pedido.insert(0, datos[3])
            fecha_pedido.configure(state="readonly")

            estado.set(datos[4])

        def actualizar_estado():
            item = tree.focus()
            if not item:
                messagebox.showerror("Error", "Selecciona un pedido para actualizar.")
                return

            id_pedido_valor = tree.item(item, "values")[0]
            nuevo_estado = estado.get()

            if not nuevo_estado:
                messagebox.showerror("Error", "Debes seleccionar un estado.")
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE pedidos SET estado = %s WHERE id_pedido = %s",
                    (nuevo_estado, id_pedido_valor),
                )
                connection.commit()
                connection.close()
                self.registrar_accion(
                    "Actualización",
                    f"Estado del pedido {id_pedido_valor} actualizado",
                )
                cargar_pedidos()
                messagebox.showinfo(
                    "Éxito", "Estado del pedido actualizado correctamente."
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo actualizar el estado del pedid: {e}"
                )

        tk.Button(
            window,
            text="Actualizar Estado",
            bg="#4682B4",
            fg="white",
            font=("Arial", 10),
            command=actualizar_estado,
        ).grid(row=6, column=1, pady=20)

        tree.bind("<ButtonRelease-1>", seleccionar_pedido)
        cargar_pedidos()

    def visualizar_registros(self):
        window = tk.Toplevel(self.root)
        window.title("Visualizar Registros")
        window.geometry("1200x600")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        frame_tree = tk.Frame(window, bg="white")
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree = ttk.Treeview(
            frame_tree,
            columns=("ID", "Usuario", "Tipo", "Fecha", "Hora", "Detalles"),
            show="headings",
            height=20,
        )
        tree.heading("ID", text="ID")
        tree.heading("Usuario", text="Usuario")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Hora", text="Hora")
        tree.heading("Detalles", text="Detalles")
        tree.column("ID", width=50)
        tree.column("Usuario", width=100)
        tree.column("Tipo", width=120)
        tree.column("Fecha", width=100)
        tree.column("Hora", width=80)
        tree.column("Detalles", width=250)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame_controls = tk.Frame(window, bg="white")
        frame_controls.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(
            frame_controls, text="Buscar Detalles: ", bg="white", font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(frame_controls, font=("Arial", 10), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        def buscar_registros():
            query = search_entry.get().strip()
            if not query:
                cargar_registros()
                return

            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM registros WHERE detalles LIKE %s OR accion LIKE %s",
                (f"%{query}%", f"%{query}%"),
            )
            registros = cursor.fetchall()
            connection.close()

            for row in tree.get_children():
                tree.delete(row)
            for registro in registros:
                tree.insert(
                    "",
                    "end",
                    values=(
                        registro["id_registro"],
                        registro["id_usuario"],
                        registro["accion"],
                        registro["fecha"],
                        registro["hora"],
                        registro["detalles"],
                    ),
                )

        search_button = tk.Button(
            frame_controls,
            text="Buscar",
            bg="#4682B4",
            fg="white",
            font=("Arial", 10),
            command=buscar_registros,
        )
        search_button.pack(side=tk.LEFT, padx=5)

        def cargar_registros():
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_registro, id_usuario, accion, DATE_FORMAT(fecha, '%Y-%m-%d') AS fecha, hora, detalles FROM registros ORDER BY fecha DESC, hora DESC"
            )
            registros = cursor.fetchall()
            connection.close()

            for row in tree.get_children():
                tree.delete(row)
            for registro in registros:
                tree.insert(
                    "",
                    "end",
                    values=(
                        registro["id_registro"],
                        registro["id_usuario"],
                        registro["accion"],
                        registro["fecha"],
                        registro["hora"],
                        registro["detalles"],
                    ),
                )

        tk.Button(
            frame_controls,
            text="Actualizar Tabla",
            bg="green",
            fg="white",
            command=cargar_registros,
        ).pack(side=tk.LEFT, padx=5)

        # tk.Button(
        #     frame_controls,
        #     text="Imprimir Tabla",
        #     bg="orange",
        #     fg="white",
        #     command=lambda: imprimir_tabla(tree),
        # ).pack(side=tk.LEFT, padx=5)

        # def imprimir_tabla(treeview):
        #     registros = [
        #         treeview.item(child)["values"] for child in treeview.get_children()
        #     ]

        #     if registros:
        #         print("\n".join(map(str, registros)))
        #         messagebox.showinfo("Imprimir", "Registros impresos correctamente.")
        #     else:
        #         messagebox.showwarning("Imprimir", "No hay registros para imprimir.")

        cargar_registros()

    def filtrar_registros(self):
        window = tk.Toplevel(self.root)
        window.title("Filtrar Registros")
        window.geometry("800x720")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()
        window.focus_set()

        tk.Label(window, text="Usuario (Nombre)", bg="white").grid(
            row=0, column=0, padx=10, pady=10
        )
        usuario_entry = tk.Entry(window, width=30)
        usuario_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(window, text="Tipo de Acción", bg="white").grid(
            row=1, column=0, padx=10, pady=10
        )
        accion_entry = ttk.Combobox(
            window, width=20, values=["", "Inserción", "Actualización", "Eliminación"]
        )
        accion_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(window, text="Fecha desde (YYYY-MM-DD)", bg="white").grid(
            row=2, column=0, padx=10, pady=10
        )
        fecha_desde_entry = tk.Entry(window, width=20)
        fecha_desde_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(window, text="Fecha hasta (YYYY-MM-DD)", bg="white").grid(
            row=3, column=0, padx=10, pady=10
        )
        fecha_hasta_entry = tk.Entry(window, width=20)
        fecha_hasta_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(window, text="Buscar en Detalles", bg="white").grid(
            row=4, column=0, padx=10, pady=10
        )
        detalles_entry = tk.Entry(window, width=30)
        detalles_entry.grid(row=4, column=1, padx=10, pady=10)

        tree = ttk.Treeview(
            window,
            columns=("ID", "Usuario", "Tipo Acción", "Fecha", "Hora", "Detalles"),
            show="headings",
            height=15,
        )
        tree.heading("ID", text="ID")
        tree.heading("Usuario", text="Usuario")
        tree.heading("Tipo Acción", text="Tipo Acción")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Hora", text="Hora")
        tree.heading("Detalles", text="Detalles")
        tree.column("ID", width=50)
        tree.column("Usuario", width=100)
        tree.column("Tipo Acción", width=100)
        tree.column("Fecha", width=100)
        tree.column("Hora", width=100)
        tree.column("Detalles", width=200)
        tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=3, sticky="ns")

        def aplicar_filtros():
            try:
                connection = create_connection()
                cursor = connection.cursor(dictionary=True)

                query = """
                SELECT r.id_registro, u.nombre AS usuario, 
                    r.accion, DATE_FORMAT(r.fecha, '%Y-%m-%d') AS fecha, r.hora, r.detalles
                FROM registros r
                JOIN usuarios u ON r.id_usuario = u.id_usuario
                WHERE 1=1
                """
                params = []

                if usuario_entry.get().strip():
                    query += " AND u.nombre = %s"
                    params.append(usuario_entry.get().strip())
                if accion_entry.get().strip():
                    query += " AND r.accion = %s"
                    params.append(accion_entry.get().strip())
                if fecha_desde_entry.get().strip():
                    query += " AND fecha >= %s"
                    params.append(fecha_desde_entry.get().strip())
                if fecha_hasta_entry.get().strip():
                    query += " AND fecha <= %s"
                    params.append(fecha_hasta_entry.get().strip())
                if detalles_entry.get().strip():
                    query += " AND LOWER(r.detalles) LIKE LOWER(%s)"
                    params.append(f"%{detalles_entry.get().strip()}%")

                # print(f"Consulta SQL: {query}")
                # print(f"Parámetros: {params}")

                cursor.execute(query, params)
                registros = cursor.fetchall()

                for row in tree.get_children():
                    tree.delete(row)

                for registro in registros:
                    tree.insert(
                        "",
                        "end",
                        values=(
                            registro["id_registro"],
                            registro["usuario"],
                            registro["accion"],
                            registro["fecha"],
                            registro["hora"],
                            registro["detalles"],
                        ),
                    )
            except Exception as e:
                print(f"Error al aplicar filtros: {e}")
                messagebox.showerror("Error", f"Error al aplicar filtros: {e}")
            finally:
                if connection:
                    connection.close()

        def exportar_csv():
            try:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
                )
                if not file_path:
                    return

                with open(file_path, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (["ID", "Usuario", "Tipo Acción", "Fecha", "Hora", "Detalles"])
                    )

                    for row_id in tree.get_children():
                        row = tree.item(row_id)["values"]
                        writer.writerow(row)

                messagebox.showinfo("Éxito", "Registros exportados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar los registros: {e}")

        def restablecer_filtros():
            usuario_entry.delete(0, tk.END)
            accion_entry.set("")
            fecha_desde_entry.delete(0, tk.END)
            fecha_hasta_entry.delete(0, tk.END)
            detalles_entry.delete(0, tk.END)
            aplicar_filtros()

        tk.Button(
            window,
            text="Aplicar Filtros",
            bg="blue",
            fg="white",
            command=aplicar_filtros,
        ).grid(row=5, column=0, pady=10)

        tk.Button(
            window,
            text="Restablecer Filtros",
            bg="orange",
            fg="white",
            command=restablecer_filtros,
        ).grid(row=5, column=1, pady=10)

        tk.Button(
            window, text="Exportar CSV", bg="green", fg="white", command=exportar_csv
        ).grid(row=5, column=2, pady=10)

        aplicar_filtros()

    def logout(self):
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de cerrar sesión?")
        if confirm:
            self.user_id = None
            self.user_role = None
            self.login_window()
        else:
            return


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPanel(root)
    root.mainloop()
