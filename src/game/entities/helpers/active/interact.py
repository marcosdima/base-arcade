from ..helper import Helper
from .....engine import Interaction


class Interact(Helper):
    def setup(self):
        super().setup()

        self.interactions: list[Interaction] = []
        self._current: Interaction | None = None


    def add(self, interaction: Interaction):
        # Prevent duplicates.
        if interaction in self.interactions:
            return

        # Add and sort interactions by priority.
        self.interactions.append(interaction)
        self._sort()

        # If there is no current interaction yet, set the highest priority one.
        if self._current is None:
            self._set_current(self.interactions[0])


    def remove(self, interaction: Interaction):
        # Ignore if the interaction is not in the list.
        if interaction not in self.interactions:
            return

        # Remove the interaction.
        removed_index = self.interactions.index(interaction)
        self.interactions.remove(interaction)

        # If it was the current interaction, change it to the next best one.
        if interaction is self._current:
            if not self.interactions:
                self._set_current(None)
            else:
                self._set_current(self.interactions[0])



    def clear(self):
        self._set_current(None)
        self.interactions.clear()


    def next(self):
        if not self.interactions:
            return

        current_index = self.interactions.index(self._current)
        self._set_current(self.interactions[(current_index + 1) % len(self.interactions)])


    def previous(self):
        if not self.interactions:
            return

        current_index = self.interactions.index(self._current)
        self._set_current(self.interactions[(current_index - 1) % len(self.interactions)])


    def execute(self):
        current = self.current()
        if current:
            current.execute()


    def _sort(self):
        self.interactions.sort(key=lambda i: i.priority, reverse=True)


    def _set_current(self, interaction: Interaction | None):
        if interaction is self._current:
            return

        if self._current:
            self._current.blur()

        self._current = interaction

        if self._current:
            self._current.focus()


    def current(self) -> Interaction | None:
        if not self.interactions:
            return None

        return self._current