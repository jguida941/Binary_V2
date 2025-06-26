import sys
import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QGridLayout, QGroupBox,
    QTextEdit, QApplication, QTabWidget, QFrame, QButtonGroup,
    QRadioButton, QSpinBox, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer, QSequentialAnimationGroup
from PyQt6.QtGui import QPalette, QColor, QFont, QClipboard


class AnimatedButton(QPushButton):
    """Custom button with hover animations"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._color = QColor(255, 255, 255)
        self._animation = QPropertyAnimation(self, b"color")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._color = QColor(80, 80, 80)

    def get_color(self):
        return getattr(self, "_color", QColor(255, 255, 255))

    def set_color(self, color):
        self._color = color
        self.update_style()

    color = pyqtProperty(QColor, get_color, set_color)

    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb({self._color.red()}, {self._color.green()}, {self._color.blue()});
                border: 2px solid #555;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
                color: white;
            }}
            QPushButton:hover {{
                border: 2px solid #888;
            }}
            QPushButton:pressed {{
                background-color: #444;
            }}
        """)

    def enterEvent(self, event):
        self._animation.setStartValue(self._color)
        self._animation.setEndValue(QColor(100, 100, 100))
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setStartValue(self._color)
        self._animation.setEndValue(QColor(80, 80, 80))
        self._animation.start()
        super().leaveEvent(event)


class BitBox(QPushButton):
    """Interactive bit box widget with animations and sci-fi styling."""

    def __init__(self, power, parent=None):
        super().__init__(parent)
        self.power = power
        self.value = 0
        self.manual_mode = False

        # Internal layout for rich text labels
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 10, 5, 10)
        layout.setSpacing(2)
        
        self.value_label = QLabel("0")
        self.power_label = QLabel(f"2<sup>{power}</sup>")
        self.decimal_value_label = QLabel(f"({2**power})")

        layout.addStretch(1)
        for label in [self.value_label, self.power_label, self.decimal_value_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            layout.addWidget(label)
        layout.addStretch(1)

        # Animation for color transition
        self._animation = QPropertyAnimation(self, b"color")
        self._animation.setDuration(300)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._color = QColor(30, 30, 30) # Dark base color

        self.setFixedSize(110, 120)
        self.clicked.connect(self.toggle)

        # Add drop shadow for depth
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(shadow)
        
        self.update_display()

    @property
    def color(self) -> QColor:
        return getattr(self, "_color", QColor(30, 30, 30))

    def get_color(self):
        return getattr(self, "_color", QColor(30, 30, 30))

    def set_color(self, color):
        self._color = color
        self.update_display()

    color = pyqtProperty(QColor, get_color, set_color)

    def set_value(self, value):
        """Set bit value with a glowing animation."""
        old_value = self.value
        self.value = value
        if old_value != value:
            if value == 1:
                # Animate to a bright, glowing green
                self._animation.setStartValue(QColor(30, 30, 30))
                self._animation.setEndValue(QColor(10, 255, 150))
            else:
                # Animate back to the dark, inactive state
                self._animation.setStartValue(self.color)
                self._animation.setEndValue(QColor(30, 30, 30))
            self._animation.start()
        
        # Immediate visual update
        self.update_display()

    def toggle(self):
        """Toggle bit value if in manual mode"""
        if self.manual_mode:
            self.set_value(1 - self.value)

    def update_display(self):
        """Update visual appearance with a sci-fi theme."""
        bg_color = self._color
        
        if self.value == 1:
            border_color = f"rgba({bg_color.red()}, {bg_color.green()}, {bg_color.blue()}, 0.9)"
            value_text_color = "white"
            power_text_color = "#ddd"
        else:
            border_color = "#444"
            value_text_color = "#666"
            power_text_color = "#555"

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(50, 50, 50, 255), stop: 1 rgba(30, 30, 30, 255)
                );
                border: 3px solid {border_color};
                border-radius: 15px;
                font-family: 'Fira Mono', 'JetBrains Mono', 'Inconsolata', monospace;
                text-align: center;
            }}
            QPushButton:hover {{
                border: 3px solid #00ffaa;
            }}
        """)

        # Update labels with rich text
        self.value_label.setText(f"<b style='font-size: 24pt; color: {value_text_color};'>{self.value}</b>")
        self.power_label.setText(f"<span style='font-size: 12pt; color: {power_text_color};'>2<sup>{self.power}</sup></span>")
        self.decimal_value_label.setText(f"<span style='font-size: 10pt; color: #888;'>({2**self.power})</span>")


class DisplayCard(QFrame):
    """A styled card for displaying a base conversion result with animation."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("displayCard")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 5, 10, 10)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.value_label = QLineEdit("0")
        self.value_label.setReadOnly(True)
        self.value_label.setObjectName("cardValue")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.copy_button = QPushButton("Copy")
        self.copy_button.setObjectName("copyButton")
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.copy_button)

        # Animation setup
        self._color = QColor("transparent")
        self._animation = QPropertyAnimation(self.value_label, b"styleSheet")
        self._animation.setDuration(400)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def update_value(self, text):
        self.value_label.setText(text)
        
        # Animate the background color for a pulse effect
        start_style = "background-color: #00c864; border: 1px solid #444; border-radius: 5px; color: white; padding: 8px;"
        end_style = "background-color: #333; border: 1px solid #444; border-radius: 5px; color: white; padding: 8px;"
        
        self._animation.setStartValue(start_style)
        self._animation.setEndValue(end_style)
        self._animation.start()

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.value_label.text())
        self.copy_button.setText("Copied!")
        QTimer.singleShot(1200, lambda: self.copy_button.setText("Copy"))


class CustomBaseCard(QFrame):
    """A dedicated, styled card for the Base-N conversion."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("displayCard")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 5, 10, 10)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # --- Value and Selector Layout ---
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        control_layout.setContentsMargins(0,0,0,0)
        control_layout.setSpacing(5)

        self.base_selector = QSpinBox()
        self.base_selector.setRange(2, 36)
        self.base_selector.setValue(10)
        self.base_selector.setObjectName("baseSelector")
        
        self.value_label = QLineEdit("0")
        self.value_label.setReadOnly(True)
        self.value_label.setObjectName("cardValue")

        control_layout.addWidget(self.base_selector)
        control_layout.addWidget(self.value_label)
        # --- End ---

        self.copy_button = QPushButton("Copy")
        self.copy_button.setObjectName("copyButton")
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
        layout.addWidget(self.title_label)
        layout.addWidget(control_widget)
        layout.addWidget(self.copy_button)

        # Animation setup
        self._animation = QPropertyAnimation(self.value_label, b"styleSheet")
        self._animation.setDuration(400)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def update_value(self, text):
        self.value_label.setText(text)
        
        start_style = "background-color: #00c864; border: 1px solid #444; border-radius: 5px; color: white; padding: 8px;"
        end_style = "background-color: #333; border: 1px solid #444; border-radius: 5px; color: white; padding: 8px;"
        
        self._animation.setStartValue(start_style)
        self._animation.setEndValue(end_style)
        self._animation.start()

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.value_label.text())
        self.copy_button.setText("Copied!")
        QTimer.singleShot(1200, lambda: self.copy_button.setText("Copy"))


class BinaryVisualizerTab(QWidget):
    """
    Educational binary visualizer tab for math learning GUI.
    Features interactive binary conversion, multiple base outputs,
    visual animations, and quiz mode.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Define all attributes listed as being defined outside __init__
        self.decimal_input = None
        self.manual_mode_checkbox = None
        self.bits_container = None
        self.twos_complement_checkbox = None
        self.mode_group = None
        self.division_radio = None
        self.powers_radio = None
        self.explanation_text = None
        self.binary_output = None
        self.binary_copy_btn = None
        self.octal_output = None
        self.octal_copy_btn = None
        self.hex_output = None
        self.hex_copy_btn = None
        self.base_selector = None
        self.custom_base_output = None
        self.custom_copy_btn = None
        self.quiz_button = None
        self.quiz_label = None
        self.quiz_question = None
        self.quiz_input = None
        self.quiz_submit = None
        self.manual_mode = False
        self.show_twos_complement = False
        self.quiz_score = 0
        self.quiz_total = 0
        self.quiz_answer = 0
        self.bit_boxes = []
        self.num_bits = 8
        self.total_sum_label = None
        self.debug_log = None
        self.range_label = None
        self.invert_button = None

        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        """Initialize the user interface with a binary-centric layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- 1. Top Control Area (Decimal Input + Manual Edit) ---
        top_controls_layout = QHBoxLayout()
        input_group = QGroupBox("Decimal Input")
        input_layout = QHBoxLayout()
        self.decimal_input = QLineEdit()
        self.decimal_input.setPlaceholderText("Enter decimal (0-255)")
        self.decimal_input.textChanged.connect(self.on_decimal_changed)
        input_layout.addWidget(QLabel("Decimal:"))
        input_layout.addWidget(self.decimal_input)
        input_group.setLayout(input_layout)

        self.manual_mode_checkbox = QCheckBox("Manual Bit Edit Mode")
        self.manual_mode_checkbox.stateChanged.connect(self.toggle_manual_mode)

        self.invert_button = QPushButton("Invert Sign (±)")
        self.invert_button.setToolTip("Apply two's complement to the current number")
        self.invert_button.clicked.connect(self.invert_sign)

        self.range_label = QLabel("Range: 0 to 255")
        self.range_label.setStyleSheet("color: #999; font-style: italic;")

        top_controls_layout.addWidget(input_group)
        top_controls_layout.addWidget(self.manual_mode_checkbox)
        top_controls_layout.addWidget(self.invert_button)
        top_controls_layout.addWidget(self.range_label)
        top_controls_layout.addStretch()
        main_layout.addLayout(top_controls_layout)

        # --- 2. Center Binary Strip ---
        binary_strip_layout = QVBoxLayout()
        binary_strip_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # MSB/LSB Labels
        msb_lsb_label = QLabel("← Most Significant Bit (MSB)        Binary Value        Least Significant Bit (LSB) →")
        msb_lsb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msb_lsb_label.setStyleSheet("font-style: italic; color: #999;")
        binary_strip_layout.addWidget(msb_lsb_label)

        self.bits_container = QHBoxLayout()
        self.bits_container.setSpacing(10)
        self.bits_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for i in range(self.num_bits):
            power = self.num_bits - 1 - i
            bit_box = BitBox(power)
            # Use a lambda that correctly captures the power for the slot
            bit_box.clicked.connect(lambda p=power: self.on_bit_clicked(p))
            # Tooltip: "Bit 7: 2⁷ = 128"
            tooltip = f"Bit {power}: 2^{power} = {2**power} — This bit is {'active' if bit_box.value == 1 else 'inactive'}"
            bit_box.setToolTip(tooltip)
            self.bit_boxes.append(bit_box)
            self.bits_container.addWidget(bit_box)
        
        binary_strip_layout.addLayout(self.bits_container)
        main_layout.addLayout(binary_strip_layout)
        
        # --- 3. Total Sum Bar ---
        self.total_sum_label = QLabel("Active Bits: 0 = 0")
        self.total_sum_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_sum_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0f8; padding: 10px;")
        main_layout.addWidget(self.total_sum_label)

        # --- 4. Tabbed Panels for Other Sections ---
        tab_widget = QTabWidget()
        
        # Create widgets for each tab (stubs for now)
        base_conversions_widget = self.create_base_conversions_panel()
        explanation_widget = self.create_explanation_panel()
        quiz_widget = self.create_quiz_panel()
        debug_widget = self.create_debug_panel()

        tab_widget.addTab(base_conversions_widget, "🔁 Base Conversions")
        tab_widget.addTab(explanation_widget, "📘 Explanation")
        tab_widget.addTab(quiz_widget, "❓ Quiz Mode")
        tab_widget.addTab(debug_widget, "🐞 Debug Log")
        
        main_layout.addWidget(tab_widget)
        
        self.decimal_input.setText("0") # Set initial text
        self.update_all_outputs(0)
        self.log_message("UI Initialized and ready.")

    def create_base_conversions_panel(self):
        """Creates the panel for base conversions using stylish display cards."""
        panel = QWidget()
        layout = QGridLayout(panel)
        layout.setSpacing(15)

        self.binary_card = DisplayCard("Binary")
        self.octal_card = DisplayCard("Octal")
        self.hex_card = DisplayCard("Hexadecimal")
        self.custom_base_card = CustomBaseCard("Base-N")

        # Connect the selector's value changed signal from the new custom card
        self.custom_base_card.base_selector.valueChanged.connect(self.update_all_outputs)
        
        layout.addWidget(self.binary_card, 0, 0)
        layout.addWidget(self.octal_card, 0, 1)
        layout.addWidget(self.hex_card, 1, 0)
        layout.addWidget(self.custom_base_card, 1, 1)
        
        return panel

    def create_explanation_panel(self):
        """Creates the panel for conversion explanations."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        self.mode_group = QButtonGroup(self)
        self.division_radio = QRadioButton("Division Method")
        self.powers_radio = QRadioButton("Powers of 2 Method")
        self.powers_radio.setChecked(True)
        self.mode_group.addButton(self.division_radio)
        self.mode_group.addButton(self.powers_radio)
        self.mode_group.buttonClicked.connect(self.update_explanation)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.division_radio)
        radio_layout.addWidget(self.powers_radio)
        radio_layout.addStretch()
        
        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        self.explanation_text.setMinimumHeight(150)
        
        layout.addLayout(radio_layout)
        layout.addWidget(self.explanation_text)
        return panel

    def create_quiz_panel(self):
        """Creates the panel for the quiz mode."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        self.quiz_button = AnimatedButton("Start Quiz")
        self.quiz_button.clicked.connect(self.start_quiz)
        
        self.quiz_label = QLabel("Score: 0/0")
        self.quiz_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.quiz_question = QLabel("What is 1101 in decimal?")
        self.quiz_question.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.quiz_input = QLineEdit()
        self.quiz_input.setPlaceholderText("Enter your answer")
        
        self.quiz_submit = AnimatedButton("Submit")
        self.quiz_submit.clicked.connect(self.check_quiz_answer)

        # Initially hide quiz elements until started
        self.quiz_label.hide()
        self.quiz_question.hide()
        self.quiz_input.hide()
        self.quiz_submit.hide()
        
        layout.addWidget(self.quiz_button)
        layout.addWidget(self.quiz_label)
        layout.addWidget(self.quiz_question)
        layout.addWidget(self.quiz_input)
        layout.addWidget(self.quiz_submit)
        layout.addStretch()
        
        return panel

    def create_debug_panel(self):
        """Creates the panel for debug logging."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        self.debug_log = QTextEdit()
        self.debug_log.setReadOnly(True)
        self.debug_log.setFontFamily("monospace")
        self.debug_log.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        
        clear_button = QPushButton("Clear Log")
        clear_button.clicked.connect(lambda: self.debug_log.clear())
        
        layout.addWidget(self.debug_log)
        layout.addWidget(clear_button)
        return panel

    def apply_dark_theme(self):
        """Apply dark theme styling to the widget"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #ddd;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                border: 2px solid #444;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #0f8;
            }
            QLineEdit {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
                color: white;
            }
            QLineEdit:read-only {
                background-color: #2a2a2a;
                color: #aaa;
            }
            QCheckBox, QRadioButton {
                spacing: 10px;
                font-size: 13px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QLabel {
                color: #ddd;
            }
            QSpinBox {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            #displayCard {
                border: 1px solid #555;
                border-radius: 8px;
                background-color: #2a2a2a;
            }
            #cardTitle {
                font-weight: bold;
                color: #0f8;
                padding: 5px;
            }
            #cardValue {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 16px;
                padding: 8px;
                border: 1px solid #444;
                border-radius: 5px;
                background-color: #333;
                color: white;
            }
            #copyButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
            #copyButton:hover {
                background-color: #5a5a5a;
            }
            #copyButton:pressed {
                background-color: #6a6a6a;
            }
        """)

    def on_decimal_changed(self, text):
        """Handle decimal input changes, validate, and update the UI."""
        self.log_message(f"Decimal input changed: '{text}'")

        if not text:
            self.decimal_input.setStyleSheet("border: 2px solid #00ffaa; background-color: #333; color: white; padding: 5px; border-radius: 5px;")
            self.invert_button.setEnabled(True)
            self.update_bits_from_decimal(0)
            self.update_all_outputs(0)
            return

        try:
            value = int(text)
            # An 8-bit space can represent numbers from -128 to 255.
            if -128 <= value <= 255:
                # Input is within the valid representable range
                self.decimal_input.setStyleSheet("border: 2px solid #00ffaa; background-color: #333; color: white; padding: 5px; border-radius: 5px;")
                self.update_bits_from_decimal(value)
                self.update_all_outputs(value)

                # Enable the invert button only if the negation is also representable.
                # The only number whose negation is not representable in 8 bits is -128.
                if value == -128:
                     self.invert_button.setEnabled(False)
                else:
                     self.invert_button.setEnabled(True)
            else:
                # Number is out of the representable range
                self.decimal_input.setStyleSheet("border: 2px solid #ff4444; background-color: #333; color: white; padding: 5px; border-radius: 5px;")
                self.invert_button.setEnabled(False)
        
        except ValueError:
            # Input is not a valid integer
            self.decimal_input.setStyleSheet("border: 2px solid #ff4444; background-color: #333; color: white; padding: 5px; border-radius: 5px;")
            self.invert_button.setEnabled(False)

    def update_bits_from_decimal(self, value):
        """Update the bit boxes from a decimal value, handling two's complement."""
        # Use bitwise AND to get the correct 8-bit pattern for any integer
        binary_str = f"{value & ((1 << self.num_bits) - 1):0{self.num_bits}b}"
        
        for i, bit_char in enumerate(binary_str):
            bit_value = int(bit_char)
            bit_box = self.bit_boxes[i]
            if bit_box.value != bit_value:
                bit_box.set_value(bit_value)
    
    def on_bit_clicked(self, power):
        """Handle bit box click in manual mode"""
        if not self.manual_mode:
            return
        
        self.log_message(f"Bit {power} manually clicked.")

        # Find the bit box with the matching power and toggle its value
        for bit_box in self.bit_boxes:
            if bit_box.power == power:
                bit_box.toggle()
                break
        
        # After toggling the bit, recalculate everything from the new bit state
        self.update_decimal_from_bits()

    def update_decimal_from_bits(self):
        """Update the decimal input from the current bit values and refresh the UI."""
        if not self.manual_mode:
            return
        
        current_val = 0
        # Determine if the number is signed based on the MSB
        is_signed = self.bit_boxes[0].value == 1

        if is_signed:
            # Calculate signed value using two's complement
            current_val = -128
            for bit_box in self.bit_boxes[1:]:
                if bit_box.value == 1:
                    current_val += 2 ** bit_box.power
        else:
            # Calculate unsigned value
            for bit_box in self.bit_boxes:
                if bit_box.value == 1:
                    current_val += 2 ** bit_box.power
        
        # Block signals to prevent on_decimal_changed from firing in a loop
        self.decimal_input.blockSignals(True)
        self.decimal_input.setText(str(current_val))
        self.decimal_input.blockSignals(False)

        # Manually call the update functions since the signal was blocked
        self.update_all_outputs(current_val)
        self.log_message(f"Manual bit edit updated decimal to {current_val}")

    def toggle_manual_mode(self, state):
        """Enable or disable manual bit editing mode"""
        self.manual_mode = bool(state)
        self.log_message(f"Manual mode {'enabled' if self.manual_mode else 'disabled'}.")
        self.decimal_input.setReadOnly(self.manual_mode)
        for bit_box in self.bit_boxes:
            bit_box.manual_mode = self.manual_mode

    def invert_sign(self):
        """Inverts the sign of the number in the decimal input using two's complement."""
        try:
            value = int(self.decimal_input.text())
            inverted_value = -value
            self.decimal_input.setText(str(inverted_value))
            self.log_message(f"Inverted {value} to {inverted_value}")
        except ValueError:
            self.log_message("Cannot invert non-numeric input.")

    def update_all_outputs(self, value):
        """Update all display values based on the current decimal value"""
        # Unsigned representation for pattern-based conversions
        unsigned_pattern_val = value & 0xff

        self.binary_card.update_value(f"{unsigned_pattern_val:08b}")
        self.octal_card.update_value(f"{unsigned_pattern_val:o}")
        self.hex_card.update_value(f"{unsigned_pattern_val:x}")
        self.custom_base_card.update_value(self.convert_to_base(unsigned_pattern_val, self.custom_base_card.base_selector.value()))

        # Update Explanation & Sum Label
        self.update_explanation(value)
        self.update_total_sum_label(value)

    @staticmethod
    def convert_to_base(num, base):
        """Convert decimal number to specified base"""
        if num == 0:
            return "0"

        digits = "0123456789ABCDEF"
        result = ""

        while num > 0:
            result = digits[num % base] + result
            num //= base

        return result

    def update_explanation(self, value):
        """Update conversion explanation based on selected mode"""
        try:
            value = int(self.decimal_input.text()) if self.decimal_input.text() else 0

            if self.division_radio.isChecked():
                self.show_division_method(value)
            else:
                self.show_powers_method(value)

        except ValueError:
            self.explanation_text.clear()

    def show_division_method(self, value):
        """Generate explanation using the division method in a styled HTML table."""
        original_value = value
        
        if value < 0:
            self.explanation_text.setHtml("<h3>Division method is typically used for unsigned integers.</h3>"
                                          f"<p>The binary pattern for {original_value} is <span class='result-binary'>{original_value & 0xff:08b}</span>.</p>")
            return
        
        binary_representation = bin(original_value)[2:]
        
        html = f"""
        <style>
            .explanation-table {{ width: 100%; border-collapse: collapse; font-family: 'Consolas', monospace; }}
            .explanation-table th, .explanation-table td {{ text-align: center; padding: 8px; border-bottom: 1px solid #444; }}
            .explanation-table th {{ color: #0f8; }}
            .remainder {{ color: #00ffaa; font-weight: bold; }}
            .result-binary {{ 
                color: #00ffaa; 
                background-color: #2e2e2e; 
                padding: 3px 6px; 
                border-radius: 5px;
                border: 1px solid #00ffaa;
                font-family: 'Consolas', monospace;
            }}
        </style>
        <h3>Converting {original_value} to binary using division method:</h3>
        <table class='explanation-table'>
            <tr><th>Operation</th><th>Result</th><th>Remainder</th></tr>
        """
        
        if original_value == 0:
            html += "<tr><td>0 ÷ 2</td><td>0</td><td class='remainder'>0</td></tr>"

        temp_val = original_value
        while temp_val > 0:
            quotient = temp_val // 2
            remainder = temp_val % 2
            html += f"<tr><td>{temp_val} ÷ 2</td><td>{quotient}</td><td class='remainder'>{remainder}</td></tr>"
            temp_val = quotient
            
        html += "</table>"
        html += f"<p>Reading remainders from bottom to top gives: <span class='result-binary'>{binary_representation}</span></p>"
        self.explanation_text.setHtml(html)

    def show_powers_method(self, value):
        """Generate explanation using the powers of 2 method with styled HTML."""
        original_value = value

        html = f"""
        <style>
            .powers-explanation {{ font-family: 'Consolas', monospace; font-size: 14px; }}
            .power-term {{ color: #00ffaa; }}
            .result-binary {{ 
                color: #00ffaa; 
                background-color: #2e2e2e; 
                padding: 3px 6px; 
                border-radius: 5px;
                border: 1px solid #00ffaa;
                font-family: 'Consolas', monospace;
            }}
        </style>
        <div class='powers-explanation'>
        <h3>Converting {original_value} to binary using powers of 2:</h3>
        """

        if value < 0:
            html += "<p>For negative numbers, we use two's complement notation.</p>"
            unsigned_eq = value & 0xff
            html += (f"<p>The 8-bit pattern for {original_value} is the same as for the unsigned integer {unsigned_eq}.</p>"
                     f"<p>This is calculated as <b>-2<sup>7</sup></b> plus the value of the other active bits.</p>")

        else: # Unsigned
            if value == 0:
                html += "<p>0 = <span class='result-binary'>0</span> (no powers of 2 needed)</p>"
            else:
                remaining = value
                parts = []
                for i in range(self.num_bits - 1, -1, -1):
                    power_val = 2 ** i
                    if remaining >= power_val:
                        parts.append(f"<span class='power-term'>2<sup>{i}</sup></span>")
                        remaining -= power_val
                
                explanation = f"{original_value} = {' + '.join(parts)}"
                html += f"<p>{explanation} = <span class='result-binary'>{bin(original_value)[2:]}</span></p>"
        
        html += "</div>"
        self.explanation_text.setHtml(html)

    def update_total_sum_label(self, value):
        """Updates the label that shows the sum of active bit values, handling two's complement."""
        active_parts = []
        
        # Determine if we should calculate the sum explanation using signed logic
        is_signed_view = self.bit_boxes[0].value == 1

        if is_signed_view:
            # Signed number calculation explanation
            total = -128
            active_parts.append(f"(-2<sup>7</sup>)")
            
            for bit_box in self.bit_boxes[1:]:
                if bit_box.value == 1:
                    power = bit_box.power
                    total += 2**power
                    active_parts.append(f"2<sup>{power}</sup>")
        else:
            # Unsigned number calculation
            total = 0
            for bit_box in self.bit_boxes:
                if bit_box.value == 1:
                    power = bit_box.power
                    total += 2**power
                    active_parts.append(f"2<sup>{power}</sup>")
        
        if not active_parts:
            self.total_sum_label.setText("Active Bits: 0 = 0")
        else:
            sum_str = " + ".join(active_parts)
            self.total_sum_label.setText(f"Active Bits: {sum_str} = {value}")

    def copy_to_clipboard(self, text):
        """Copy text to the system clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        # Show feedback
        sender = self.sender()
        if isinstance(sender, QPushButton):
            original_text = sender.text()
            sender.setText("Copied!")
            QTimer.singleShot(1000, lambda: sender.setText(original_text))

    def start_quiz(self):
        """Start a new quiz question"""
        # Generate random binary number
        self.quiz_answer = random.randint(0, 255)
        binary = bin(self.quiz_answer)[2:].zfill(8)

        self.quiz_question.setText(f"What is {binary} in decimal?")
        self.quiz_input.clear()
        self.quiz_input.setFocus()
        self.quiz_submit.setEnabled(True)

    def check_quiz_answer(self):
        """Check the quiz answer"""
        try:
            user_answer = int(self.quiz_input.text())
            self.quiz_total += 1

            if user_answer == self.quiz_answer:
                self.quiz_score += 1
                QMessageBox.information(self, "Correct!",
                                        f"Great job! {bin(self.quiz_answer)[2:].zfill(8)} = {self.quiz_answer}")
            else:
                QMessageBox.warning(self, "Incorrect",
                                    f"Sorry! {bin(self.quiz_answer)[2:].zfill(8)} = {self.quiz_answer}\n"
                                    f"You answered: {user_answer}")

            self.quiz_label.setText(f"Score: {self.quiz_score}/{self.quiz_total}")
            self.quiz_submit.setEnabled(False)
            self.quiz_input.clear()

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")

    def log_message(self, message):
        """Appends a message to the debug log."""
        if self.debug_log:
            self.debug_log.append(f"LOG: {message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create main window with tabs
    main_window = QTabWidget()
    main_window.setWindowTitle("Math Learning GUI")
    main_window.resize(1000, 800)

    # Add Binary Visualizer tab
    binary_tab = BinaryVisualizerTab()
    main_window.addTab(binary_tab, "Binary Visualizer")

    # Apply dark theme to tab widget
    main_window.setStyleSheet("""
        QTabWidget::pane {
            border: 1px solid #444;
            background-color: #1a1a1a;
        }
        QTabBar::tab {
            background-color: #2a2a2a;
            color: #ddd;
            padding: 10px 20px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #1a1a1a;
            color: #0f8;
        }
    """)

    main_window.show()
    sys.exit(app.exec())