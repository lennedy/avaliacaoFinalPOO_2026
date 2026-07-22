import tkinter as tk
from tkinter import messagebox, simpledialog

from contaBancaria.ContaBancaria import (
    Cliente,
    Endereco,
    ContaCorrente,
    ContaPoupanca,
)


class BancoApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema Bancário - POO em Python")
        self.janela.geometry("1100x700")

        endereco1 = Endereco("Nevaldo", "10", "Ceará-Mirim", "Planalto")
        cliente1 = Cliente("João", "111.101.011-01", endereco1)

        endereco2 = Endereco("Nevaldo", "10", "Ceará-Mirim", "Massaranduba")
        cliente2 = Cliente("Marcos", "222.202.022-02", endereco2)

        endereco3 = Endereco("Nevaldo", "10", "Ceará-Mirim", "Novo Horizonte")
        cliente3 = Cliente("Samuel", "333.303.033-03", endereco3)

        endereco4 = Endereco("Nevaldo", "10", "Natal", "Aurora")
        cliente4 = Cliente("Dhimy", "555.505.055-05", endereco4)

        # Lista utilizada para exibir os clientes na interface.
        self.clientes = [
            cliente1,
            cliente2,
            cliente3,
            cliente4,
        ]

        self.contas = [
            ContaCorrente(cliente1, 1001, 500, 500, 10, 100, "Pacote Ouro"),
            ContaPoupanca(cliente2, 1002, 1000, 10, 200, "Pacote Platina"),
            ContaPoupanca(cliente1, 1003, 300, 2, 300, "Pacote Diamante"),
            ContaCorrente(cliente4, 1004, 20, 500, 10, 400, "Pacote Mestre"),
        ]

        self.criar_interface()

    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="Banco Python - Contas Bancárias",
            font=("Arial", 18, "bold"),
        )
        titulo.pack(pady=12)

        # Área com a lista de clientes.
        self.frame_clientes = tk.LabelFrame(
            self.janela,
            text="Clientes",
            padx=10,
            pady=10,
        )
        self.frame_clientes.pack(fill="x", padx=15, pady=(0, 10))

        # Área que mantém os cartões das contas.
        self.frame_contas = tk.LabelFrame(
            self.janela,
            text="Contas bancárias",
            padx=10,
            pady=10,
        )
        self.frame_contas.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.atualizar_tela()

    def atualizar_tela(self):
        self.atualizar_lista_clientes()
        self.atualizar_lista_contas()

    def atualizar_lista_clientes(self):
        for widget in self.frame_clientes.winfo_children():
            widget.destroy()

        for cliente in self.clientes:
            frame_cliente = tk.Frame(
                self.frame_clientes,
                borderwidth=1,
                relief="solid",
                padx=8,
                pady=8,
            )
            frame_cliente.pack(side="left", padx=8, pady=4)

            tk.Label(
                frame_cliente,
                text=cliente.get_nome(),
                font=("Arial", 12, "bold"),
            ).pack(pady=(0, 5))

            tk.Button(
                frame_cliente,
                text="Quantidade de contas",
                width=20,
                command=lambda c=cliente: self.exibir_quantidade_contas(c),
            ).pack(pady=2)

            tk.Button(
                frame_cliente,
                text="Saldo total",
                width=20,
                command=lambda c=cliente: self.exibir_saldo_total(c),
            ).pack(pady=2)

    def atualizar_lista_contas(self):
        for widget in self.frame_contas.winfo_children():
            widget.destroy()

        for conta in self.contas:
            frame = tk.Frame(
                self.frame_contas,
                borderwidth=2,
                relief="groove",
                padx=10,
                pady=10,
            )
            frame.pack(side="left", padx=10, pady=10)

            tipo_conta = conta.get_tipo_conta()

            tk.Label(
                frame,
                text=conta.get_titular(),
                font=("Arial", 14, "bold"),
            ).pack()

            tk.Label(
                frame,
                text=f"Conta: {conta.get_numero()}",
            ).pack()

            tk.Label(
                frame,
                text=f"Tipo: {tipo_conta}",
                font=("Arial", 11, "italic"),
            ).pack(pady=(2, 0))

            tk.Label(
                frame,
                text=f"Saldo: R$ {conta.get_saldo():.2f}",
                font=("Arial", 12),
            ).pack(pady=5)

            tk.Button(
                frame,
                text="Depositar",
                width=17,
                command=lambda c=conta: self.depositar(c),
            ).pack(pady=2)

            tk.Button(
                frame,
                text="Sacar",
                width=17,
                command=lambda c=conta: self.sacar(c),
            ).pack(pady=2)

            tk.Button(
                frame,
                text="Transferir",
                width=17,
                command=lambda c=conta: self.transferir(c),
            ).pack(pady=2)

            # Novo botão que abre a janela da operação PIX.
            tk.Button(
                frame,
                text="PIX",
                width=17,
                command=lambda c=conta: self.abrir_janela_pix(c),
            ).pack(pady=2)

            tk.Button(
                frame,
                text="Exibir Dados",
                width=17,
                command=lambda c=conta: self.exibir_dados(c),
            ).pack(pady=2)

            tk.Button(
                frame,
                text="Cobrar Tarifa",
                width=17,
                command=lambda c=conta: self.cobrar_tarifa(c),
            ).pack(pady=2)

            pode_render = tipo_conta in (
                "Conta Poupança",
                "Conta Poupanca",
                "Conta Investimento",
            )

            tk.Button(
                frame,
                text="Render",
                width=17,
                state=tk.NORMAL if pode_render else tk.DISABLED,
                command=lambda c=conta: self.render_conta(c),
            ).pack(pady=2)

    def exibir_quantidade_contas(self, cliente):
        quantidade = cliente.quantidade_contas()

        messagebox.showinfo(
            "Quantidade de contas",
            f"O cliente {cliente.get_nome()} possui {quantidade} conta(s).",
        )

    def exibir_saldo_total(self, cliente):
        saldo_total = cliente.consultar_saldo_total()

        messagebox.showinfo(
            "Saldo total",
            f"Saldo total de {cliente.get_nome()}: R$ {saldo_total:.2f}",
        )

    def depositar(self, conta):
        valor = simpledialog.askfloat(
            "Depósito",
            "Digite o valor do depósito:",
            parent=self.janela,
        )

        if valor is not None:
            if conta.depositar(valor):
                messagebox.showinfo("Sucesso", "Depósito realizado.")
            else:
                messagebox.showerror("Erro", "Valor inválido.")

        self.atualizar_tela()

    def sacar(self, conta):
        valor = simpledialog.askfloat(
            "Saque",
            "Digite o valor do saque:",
            parent=self.janela,
        )

        if valor is not None:
            if conta.sacar(valor):
                messagebox.showinfo("Sucesso", "Saque realizado.")
            else:
                messagebox.showerror("Erro", "Saldo insuficiente.")

        self.atualizar_tela()

    def transferir(self, conta_origem):
        valor = simpledialog.askfloat(
            "Transferência",
            "Digite o valor:",
            parent=self.janela,
        )

        if valor is None:
            return

        numero_destino = simpledialog.askinteger(
            "Transferência",
            "Digite o número da conta destino:",
            parent=self.janela,
        )

        if numero_destino is None:
            return

        conta_destino = self.buscar_conta(numero_destino)

        if conta_destino is None:
            messagebox.showerror("Erro", "Conta destino não encontrada.")
            return

        if conta_origem == conta_destino:
            messagebox.showerror(
                "Erro",
                "Não é possível transferir para a mesma conta.",
            )
            return

        if conta_origem.transferir(valor, conta_destino):
            messagebox.showinfo("Sucesso", "Transferência realizada.")
        else:
            messagebox.showerror("Erro", "Saldo insuficiente.")

        self.atualizar_tela()

    def buscar_conta(self, numero):
        for conta in self.contas:
            if conta.get_numero() == numero:
                return conta

        return None

    def abrir_janela_pix(self, conta_origem):
        janela_pix = tk.Toplevel(self.janela)
        janela_pix.title("Realizar PIX")
        janela_pix.geometry("360x240")
        janela_pix.resizable(False, False)
        janela_pix.transient(self.janela)
        janela_pix.grab_set()

        tk.Label(
            janela_pix,
            text="Realizar PIX",
            font=("Arial", 16, "bold"),
        ).pack(pady=12)

        tk.Label(
            janela_pix,
            text=f"Conta de origem: {conta_origem.get_numero()}",
        ).pack()

        frame_formulario = tk.Frame(janela_pix)
        frame_formulario.pack(pady=12)

        tk.Label(
            frame_formulario,
            text="Valor:",
            width=16,
            anchor="e",
        ).grid(row=0, column=0, padx=5, pady=6)

        entrada_valor = tk.Entry(frame_formulario, width=18)
        entrada_valor.grid(row=0, column=1, padx=5, pady=6)

        tk.Label(
            frame_formulario,
            text="Conta destino:",
            width=16,
            anchor="e",
        ).grid(row=1, column=0, padx=5, pady=6)

        entrada_destino = tk.Entry(frame_formulario, width=18)
        entrada_destino.grid(row=1, column=1, padx=5, pady=6)

        tk.Button(
            janela_pix,
            text="Confirmar PIX",
            width=18,
            command=lambda: self.realizar_pix(
                conta_origem,
                entrada_valor.get(),
                entrada_destino.get(),
                janela_pix,
            ),
        ).pack(pady=8)

        entrada_valor.focus_set()

    def realizar_pix(
        self,
        conta_origem,
        valor_informado,
        numero_destino_informado,
        janela_pix,
    ):
        try:
            # Permite que o aluno digite 10,50 ou 10.50.
            valor = float(valor_informado.replace(",", "."))
            numero_destino = int(numero_destino_informado)
        except ValueError:
            messagebox.showerror(
                "Erro",
                "Informe um valor e um número de conta válidos.",
                parent=janela_pix,
            )
            return

        if valor <= 0:
            messagebox.showerror(
                "Erro",
                "O valor do PIX deve ser maior que zero.",
                parent=janela_pix,
            )
            return

        conta_destino = self.buscar_conta(numero_destino)

        if conta_destino is None:
            messagebox.showerror(
                "Erro",
                "Conta destino não encontrada.",
                parent=janela_pix,
            )
            return

        if conta_origem == conta_destino:
            messagebox.showerror(
                "Erro",
                "Não é possível realizar PIX para a mesma conta.",
                parent=janela_pix,
            )
            return

        try:
            resultado = conta_origem.pix(valor, conta_destino)
        except AttributeError:
            messagebox.showerror(
                "Erro",
                "O método pix(valor, conta_destino) não foi implementado nesta conta.",
                parent=janela_pix,
            )
            return

        if resultado:
            messagebox.showinfo(
                "PIX",
                "pix realizado",
                parent=janela_pix,
            )
            janela_pix.destroy()
        else:
            messagebox.showerror(
                "PIX",
                "Não houve saldo suficiente",
                parent=janela_pix,
            )

        self.atualizar_tela()

    def exibir_dados(self, conta):
        messagebox.showinfo("Dados da Conta", conta.exibir_dados())

    def cobrar_tarifa(self, conta):
        if conta.get_tipo_conta() != "Conta Corrente":
            messagebox.showwarning(
                "Operação indisponível",
                "A cobrança de tarifa está disponível somente para Conta Corrente.",
            )
            return

        if conta.cobrar_tarifa():
            messagebox.showinfo("Sucesso", "Tarifa cobrada.")
        else:
            messagebox.showerror(
                "Erro",
                "Saldo insuficiente para cobrar a tarifa.",
            )

        self.atualizar_tela()

    def render_conta(self, conta):
        tipo_conta = conta.get_tipo_conta()

        try:
            if tipo_conta in ("Conta Poupança", "Conta Poupanca"):
                conta.render_juros()

            elif tipo_conta == "Conta Investimento":
                conta.render_investimento()

            else:
                messagebox.showwarning(
                    "Operação indisponível",
                    "Esta conta não permite rendimento.",
                )
                return

            messagebox.showinfo(
                "Sucesso",
                f"Rendimento aplicado à {tipo_conta}.",
            )

        except AttributeError:
            messagebox.showerror(
                "Erro de implementação",
                f"O método de rendimento da {tipo_conta} não foi implementado.",
            )
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível aplicar o rendimento.\n\nDetalhes: {erro}",
            )

        self.atualizar_tela()


if __name__ == "__main__":
    janela = tk.Tk()
    app = BancoApp(janela)
    janela.mainloop()
