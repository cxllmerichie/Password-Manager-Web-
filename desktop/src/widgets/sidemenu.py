class SideMenu:
    expand_to: int = 200

    def expand(self, width: int = None):
        self.resize(self.expand_to if not width else width, self.height())

    def shrink(self) -> None:
        self.resize(0, self.height())

    def toggle(self) -> None:
        self.expand() if self.width() == 0 else self.shrink()
