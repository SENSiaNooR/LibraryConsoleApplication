from typing import Optional, List
from Presentation.ConsoleUI.Components.Element import Element
from Presentation.ConsoleUI.Components.ConsoleExtension import ConsoleExtension
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition
from Presentation.ConsoleUI.Components.Text import Text


class Table(Element):
    """
    A UI Table element that renders a table at a given position.
    Allows updating its data and structure in-place.
    """

    def __init__(
        self,
        data: list[list[Element]],
        position: Optional[SizeAndPosition] = None,
        show_row_id: bool = True,
        start_row_id: int = 1
    ):
        super().__init__(position=position, linked_elements=None, focusable=False, clickable=False)
        self.data = []
        self.elements: list[Element] = []
        self.cols_lens = []
        self.rows_lens = []
        self._cols_count = 0
        self.show_row_id = show_row_id
        self.start_row_id = start_row_id
        self.build(data, position, show_row_id, start_row_id)

    def build(
        self,
        data: list[list[Element]],
        position: Optional[SizeAndPosition],
        show_row_id: bool,
        start_row_id: int
    ):
        """(Re)builds the table layout and sizes."""
        if not data:
            raise ValueError("Table data cannot be empty")
        if any(len(row) != len(data[0]) for row in data):
            raise ValueError("All rows must have the same length")

        # --- reset old state ---
        self.data = data
        self.elements = []
        self._cols_count = len(data[0]) + (1 if show_row_id else 0)
        self.show_row_id = show_row_id
        self.start_row_id = start_row_id

        # --- rebuild elements ---
        for i, row in enumerate(self.data):
            if show_row_id:
                self.elements.append(Text('' if i == 0 else f'{i + start_row_id}'))
            self.elements += row

        total_elements = len(self.elements)
        self.data = [
            tuple(self.elements[i:i + self._cols_count])
            for i in range(0, total_elements, self._cols_count)
        ]

        # --- compute cell sizes ---
        self.cols_lens = [1] * self._cols_count
        self.rows_lens = [1] * len(self.data)

        for i, row in enumerate(self.data):
            self.rows_lens[i] = max(e.position.height for e in row)
            for j, cell in enumerate(row):
                self.cols_lens[j] = max(self.cols_lens[j], cell.position.width)

        total_width = sum(self.cols_lens) + len(self.cols_lens) + 1
        total_height = sum(self.rows_lens) + len(self.rows_lens) + 1

        # --- adjust table size ---
        if position is None:
            if self.position is None:
                self.position = SizeAndPosition(0, 0, total_height, total_width)
            else:
                self.position.height = total_height
                self.position.width = total_width
        else:
            self.position = position
            self.position.height = total_height
            self.position.width = total_width

        # --- position each cell ---
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                cell.position.top = sum(self.rows_lens[:i]) + i + 1
                cell.position.left = sum(self.cols_lens[:j]) + j + 1
                cell.position.width = self.cols_lens[j]
                cell.position.height = self.rows_lens[i]

    def update(
        self,
        data: list[list[Element]],
        position: Optional[SizeAndPosition] = None,
        show_row_id: Optional[bool] = None,
        start_row_id: Optional[bool] = None
    ):
        """
        Updates the table content in-place with new data or layout.
        """
        self.build(
            data=data,
            position=position if position is not None else self.position,
            show_row_id=show_row_id if show_row_id is not None else self.show_row_id,
            start_row_id=start_row_id if start_row_id is not None else self.start_row_id
        )

    def render(self, top_offset: int = 0, left_offset: int = 0):
        for e in self.elements:
            e.render(
                top_offset=self.position.top + top_offset,
                left_offset=self.position.left + left_offset
            )

        ConsoleExtension.print_table(
            self.position.top + top_offset,
            self.position.left + left_offset,
            self.cols_lens,
            self.rows_lens
        )