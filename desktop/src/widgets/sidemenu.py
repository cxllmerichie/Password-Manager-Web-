class SideMenu:
    expand_to: int = 200

    def expand(self, width: int = None):
        self.setFixedWidth(self.expand_to if not width else width)

    def shrink(self) -> None:
        self.setFixedWidth(0)

    def toggle(self) -> None:
        self.expand() if self.width() == 0 else self.shrink()
