import tkinter as tk
from tkinter import messagebox, ttk


class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Order System")
        self.root.geometry("500x550")
        self.root.resizable(True, True)  # Allow resizing for better accessibility

        self.menu = {
            "Pizza": 40,
            "Pasta": 50,
            "Burger": 60,
            "Salad": 70,
            "Coffee": 80
        }

        self.order_items = []
        self.total_bill = 0

        # Create main container and canvas for scrolling
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Create canvas for scrolling
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create frame inside canvas
        self.content_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Create widgets
        self.create_widgets()

        # Make mouse wheel scroll
        self.content_frame.bind("<Enter>", self.bind_mouse_wheel)
        self.content_frame.bind("<Leave>", self.unbind_mouse_wheel)

    def bind_mouse_wheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def unbind_mouse_wheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_widgets(self):
        # Welcome label
        welcome_label = tk.Label(
            self.content_frame,
            text="Welcome to our restaurant! Here is your menu:",
            font=("Helvetica", 14, "bold")
        )
        welcome_label.pack(pady=10)

        # Menu frame
        menu_frame = tk.LabelFrame(self.content_frame, text="Menu", padx=10, pady=10)
        menu_frame.pack(pady=10, padx=20, fill="x")

        # Display menu items
        for item, price in self.menu.items():
            item_frame = tk.Frame(menu_frame)
            item_frame.pack(fill="x", pady=5)

            tk.Label(item_frame, text=item, width=10, anchor="w").pack(side="left")
            tk.Label(item_frame, text=f"Rs.{price}", width=10).pack(side="right")

        # Order section
        order_frame = tk.LabelFrame(self.content_frame, text="Place Your Order", padx=10, pady=10)
        order_frame.pack(pady=10, padx=20, fill="x")

        # Item selection
        tk.Label(order_frame, text="Select Item:").grid(row=0, column=0, padx=5, pady=5)

        self.item_var = tk.StringVar()
        item_combobox = ttk.Combobox(
            order_frame,
            textvariable=self.item_var,
            values=list(self.menu.keys()),
            state="readonly",
            width=15
        )
        item_combobox.grid(row=0, column=1, padx=5, pady=5)
        item_combobox.current(0)

        # Add item button
        add_button = tk.Button(
            order_frame,
            text="Add to Order",
            command=self.add_item,
            bg="#4CAF50", fg="white"
        )
        add_button.grid(row=0, column=2, padx=5, pady=5)

        # Order listbox - no scrollbar
        self.order_listbox = tk.Listbox(
            order_frame,
            height=5,
            selectbackground="#a6a6a6",
            width=40
        )
        self.order_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # Remove item button
        remove_button = tk.Button(
            order_frame,
            text="Remove Selected",
            command=self.remove_item,
            bg="#f44336", fg="white"
        )
        remove_button.grid(row=2, column=0, columnspan=3, pady=5)

        # Bill section
        bill_frame = tk.LabelFrame(self.content_frame, text="Your Bill", padx=10, pady=10)
        bill_frame.pack(pady=10, padx=20, fill="x")

        self.bill_text = tk.Text(
            bill_frame,
            height=6,
            state="disabled",
            bg="#f0f0f0"
        )
        self.bill_text.pack(fill="x")

        # Button frame
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=20)

        # Calculate bill button
        calc_button = tk.Button(
            button_frame,
            text="Calculate Total Bill",
            command=self.calculate_bill,
            bg="#2196F3", fg="white",
            font=("Helvetica", 10, "bold"),
            width=15
        )
        calc_button.pack(side="left", padx=5)

        # Confirm order button
        confirm_button = tk.Button(
            button_frame,
            text="Confirm Order",
            command=self.confirm_order,
            bg="#9C27B0", fg="white",
            font=("Helvetica", 10, "bold"),
            width=15
        )
        confirm_button.pack(side="left", padx=5)

    def add_item(self):
        item = self.item_var.get()
        if item:
            self.order_items.append(item)
            self.order_listbox.insert(tk.END, f"{item} - Rs.{self.menu[item]}")
            messagebox.showinfo("Order Updated", f"Added {item} to your order", parent=self.root)

    def remove_item(self):
        try:
            selected_index = self.order_listbox.curselection()[0]
            item_text = self.order_listbox.get(selected_index)
            item = item_text.split(" - ")[0]  # Extract item name
            self.order_listbox.delete(selected_index)
            self.order_items.remove(item)
        except IndexError:
            messagebox.showerror("Error", "No item selected for removal", parent=self.root)

    def calculate_bill(self):
        if not self.order_items:
            messagebox.showerror("Error", "Your order is empty!", parent=self.root)
            return

        # Calculate total
        self.total_bill = sum(self.menu[item] for item in self.order_items)

        # Update bill display
        self.bill_text.config(state="normal")
        self.bill_text.delete(1.0, tk.END)

        self.bill_text.insert(tk.END, "Items Ordered:\n")
        self.bill_text.insert(tk.END, "-" * 30 + "\n")

        for item in self.order_items:
            price = self.menu[item]
            self.bill_text.insert(tk.END, f"{item:20} Rs.{price}\n")

        self.bill_text.insert(tk.END, "-" * 30 + "\n")
        self.bill_text.insert(tk.END, f"{'TOTAL':20} Rs.{self.total_bill}")
        self.bill_text.config(state="disabled")

    def confirm_order(self):
        if not self.order_items:
            messagebox.showerror("Error", "Your order is empty!", parent=self.root)
            return

        if self.total_bill == 0:  # If user didn't calculate bill first
            self.calculate_bill()

        items_str = ", ".join(self.order_items)
        messagebox.showinfo(
            "Order Confirmed",
            f"Your order of {items_str} has been placed!\n\nTotal Bill: Rs.{self.total_bill}",
            parent=self.root
        )

        # Reset for new order
        self.order_items = []
        self.total_bill = 0
        self.order_listbox.delete(0, tk.END)
        self.bill_text.config(state="normal")
        self.bill_text.delete(1.0, tk.END)
        self.bill_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()