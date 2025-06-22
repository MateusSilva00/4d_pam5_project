from src.gui.app import App


def main():
    print("Iniciando Sistema de Comunicação 4D-PAM5...")
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
