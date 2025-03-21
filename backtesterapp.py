import sys
import os
import subprocess
import time
import psutil
import pandas as pd
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk  # Import ttk for progress bar
from threading import Thread, Event
from datetime import datetime  # Import datetime for timestamp
import shutil  # Import shutil for file operations
import requests  # Import requests for HTTP requests
from PIL import Image, ImageTk  # Import PIL for better image handling
import ctypes  # Import ctypes to set AppUserModelID
import json  # Import json for handling JSON data
#import hashlib  # Import hashlib for generating machine fingerprint

import subprocess


#import chardet
#from io import StringIO
#import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
#import locale

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QMessageBox, QLabel, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QTextEdit, QLineEdit, QFormLayout,
    QHBoxLayout, QCheckBox, QScrollArea, QComboBox, QDateEdit,
    QSpinBox, QTableView, QAbstractItemView, QInputDialog, QDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QIcon
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


#from multiprocessing import Process

import numpy as np
import math

##############



def check_expiry(expiry_date: str):
    """
    Exits the program if the current date is past the specified expiry date.
    
    :param expiry_date: The expiry date in "YYYY-MM-DD" format.
    """
    current_date = datetime.now().date()
    expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

    if current_date > expiry_date:
        print(f"Program expired! Contact Purple. Exiting...")
        sys.exit(1)


def next_sunday(date_str):
    # Parse input date
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")

    # Calculate days until the next Sunday (0=Monday, ..., 6=Sunday)
    days_until_sunday = (6 - date_obj.weekday()) % 7
    days_until_sunday = 7 if days_until_sunday == 0 else days_until_sunday  # Ensure it moves to next Sunday

    # Get the next Sunday
    next_sunday_date = date_obj + timedelta(days=days_until_sunday)

    # Return in the same format
    return next_sunday_date.strftime("%Y.%m.%d")

def next_friday(date_str):
    # Parse input date
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")

    # Calculate days until the next Friday (4 = Friday)
    days_until_friday = (4 - date_obj.weekday()) % 7
    days_until_friday = 7 if days_until_friday == 0 else days_until_friday  # Ensure it moves to next Friday

    # Get the next Friday
    next_friday_date = date_obj + timedelta(days=days_until_friday)

    # Return in the same format
    return next_friday_date.strftime("%Y.%m.%d")

def log_to_file(message):
    filename = "targetedLogs.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as file:
        file.write(f"[{timestamp}] {message}\n")

##############

class CSVProcessorApp_for_auto(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creator XML")
        self.setGeometry(100, 100, 1200, 800)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Set the window icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon file not found at {icon_path}")

        # Tabs
        self.main_tabs = QTabWidget()
        self.layout.addWidget(self.main_tabs)

        # Create tabs for both functionalities
        self.creator_xml_tab = QWidget()

        # Add tabs in the desired order
        self.main_tabs.addTab(self.creator_xml_tab, "Creator XML")

        # Initialize Creator XML UI
        self.init_creator_xml_ui()

    # ----------------------- Creator XML UI -----------------------
    def init_creator_xml_ui(self):
        layout = QVBoxLayout()
        self.creator_xml_tab.setLayout(layout)

        # Create input fields and buttons
        form_layout = QFormLayout()

        # Initialize file lists
        self.forward_files = []
        self.backward_files = []
        self.set_file_contents = {}

        # Forward XML Files
        self.forward_file_path = QTextEdit()
        self.forward_file_path.setReadOnly(True)
        self.forward_file_path.setFixedHeight(50)
        forward_browse_button = QPushButton("Browse")
        forward_browse_button.clicked.connect(self.browse_forward_file)
        forward_layout = QHBoxLayout()
        forward_layout.addWidget(self.forward_file_path)
        forward_layout.addWidget(forward_browse_button)
        form_layout.addRow("Forward XML File(s):", forward_layout)

        # Backward XML Files
        self.backward_file_path = QTextEdit()
        self.backward_file_path.setReadOnly(True)
        self.backward_file_path.setFixedHeight(50)
        backward_browse_button = QPushButton("Browse")
        backward_browse_button.clicked.connect(self.browse_backward_file)
        backward_layout = QHBoxLayout()
        backward_layout.addWidget(self.backward_file_path)
        backward_layout.addWidget(backward_browse_button)
        form_layout.addRow("Backward XML File(s):", backward_layout)

        # Set Files
        self.set_file_path = QTextEdit()
        self.set_file_path.setReadOnly(True)
        self.set_file_path.setFixedHeight(50)
        set_browse_button = QPushButton("Browse")
        set_browse_button.clicked.connect(self.browse_set_files)
        set_layout = QHBoxLayout()
        set_layout.addWidget(self.set_file_path)
        set_layout.addWidget(set_browse_button)
        form_layout.addRow("Set File(s):", set_layout)

        # Folder Name
        self.folder_name = QLineEdit('ADXBB')
        form_layout.addRow("Folder Name for .set Files:", self.folder_name)

        # Balance
        self.balance = QLineEdit("100000")
        form_layout.addRow("Balance:", self.balance)

        # Drawdown
        self.drawdown = QLineEdit("1000")
        form_layout.addRow("Target Drawdown:", self.drawdown)

        # Date Inputs
        date_layout = QHBoxLayout()

        # Start Date
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date_edit)

        # Forward Date
        self.forward_date_edit = QDateEdit()
        self.forward_date_edit.setCalendarPopup(True)
        self.forward_date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("Forward Date:"))
        date_layout.addWidget(self.forward_date_edit)

        # End Date
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date_edit)

        layout.addLayout(form_layout)
        layout.addLayout(date_layout)

        # Process Button
        process_button = QPushButton("Process Files")
        process_button.clicked.connect(self.process_files)
        layout.addWidget(process_button)

        # Search and Controls
        controls_layout = QHBoxLayout()

        # Search Box
        controls_layout.addWidget(QLabel("Search:"))
        self.search_var = QLineEdit()
        self.search_var.textChanged.connect(self.update_filter)
        controls_layout.addWidget(self.search_var)

        # Show/Hide Columns Button
        columns_button = QPushButton("Show/Hide Columns")
        columns_button.clicked.connect(self.show_hide_columns)
        controls_layout.addWidget(columns_button)

        # Remove Duplicates Button
        remove_duplicates_button = QPushButton("Remove Duplicates")
        remove_duplicates_button.clicked.connect(self.remove_duplicates)
        controls_layout.addWidget(remove_duplicates_button)

        layout.addLayout(controls_layout)

        # Results Table
        self.table_widget = QTableWidget()
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table_widget)

        # Pagination Controls
        self.pagination_layout = QHBoxLayout()
        layout.addLayout(self.pagination_layout)

        # Download Buttons
        download_layout = QHBoxLayout()
        download_selected_button = QPushButton("Download Selected")
        download_selected_button.clicked.connect(self.download_selected)
        download_layout.addWidget(download_selected_button)

        download_all_button = QPushButton("Download All > Profit")
        download_all_button.clicked.connect(self.download_all_above_profit)
        download_layout.addWidget(download_all_button)

        # NEW DOWNLOAD BUTTON FOR MAX ORIGINAL DD
        download_all_dd_button = QPushButton("Download All ≤ Max Original DD")
        download_all_dd_button.clicked.connect(self.download_all_below_max_dd)
        download_layout.addWidget(download_all_dd_button)

        # NEW DOWNLOAD BUTTON FOR MIN PROFIT AND MAX ORIGINAL DD
        download_profit_dd_button = QPushButton("Download All Profit ≥ Min and Max Original DD ≤ Max")
        download_profit_dd_button.clicked.connect(self.download_all_profit_and_dd)
        download_layout.addWidget(download_profit_dd_button)

        layout.addLayout(download_layout)

        # Initialize variables
        self.full_data = None
        self.qualifying_data = None
        self.filtered_data = None
        self.set_file_contents = {}  # Map base_name to set file content and path
        self.duplicates_removed = False
        self.current_page = 1
        self.rows_per_page = 50

        # All Columns
        self.all_columns = [
            ('Base_Name', 'Base Name'),
            ('Pass', 'Pass'),
            ('Profit_Match_Percent', 'Profit Match (%)'),
            ('Total_Original_Profit', 'Total Original Profit'),
            ('Max_Original_DD', 'Max Original DD'),
            ('Lot_Multiplier', 'Lot Multiplier'),
            ('Total_Estimated_Profit', 'Total Estimated Profit'),
            ('Total_Estimated_DD', 'Total Estimated DD'),
            ('Recovery_Factor_back', 'Recovery Factor Back'),
            ('Recovery_Factor_fwd', 'Recovery Factor Fwd'),
            ('Trades_back', 'Trades Back'),
            ('Trades_fwd', 'Trades Fwd'),
            ('Combined_Trades', 'Combined Trades'),
            ('Score', 'Score')
        ]

        # Initially visible columns
        self.visible_columns = [
            'Base_Name', 'Pass', 'Profit_Match_Percent', 'Total_Original_Profit',
            'Max_Original_DD', 'Lot_Multiplier', 'Total_Estimated_Profit', 'Total_Estimated_DD',
            'Trades_back', 'Trades_fwd', 'Combined_Trades', 'Score'
        ]

        self.configure_table_columns()

    def browse_forward_file(self, default_file=None):
        # If default_file is provided, use it; otherwise, open the file dialog
        if default_file:
            files = [default_file]
        else:
            files, _ = QFileDialog.getOpenFileNames(self, "Select Backward XML File(s)", "", "XML Files (*.xml)")



        if files:
            self.forward_files = files
            # Display filenames
            filenames = [os.path.basename(fp) for fp in files]
            try:
                self.forward_file_path.setText("\n".join(filenames))
            except:
                pass

    def browse_backward_file(self, default_file=None):
        # If default_file is provided, use it; otherwise, open the file dialog
        if default_file:
            files = [default_file]
        else:
            files, _ = QFileDialog.getOpenFileNames(self, "Select Backward XML File(s)", "", "XML Files (*.xml)")

        if files:
            self.backward_files = files
            # Display filenames
            filenames = [os.path.basename(fp) for fp in files]

            try:
                self.backward_file_path.setText("\n".join(filenames))

            except:
                pass

            # Extract dates from one of the backward files and populate the date inputs
            print('-----')
            print('-creatorxml inputing backward file')
            print('-auto-adjusting dates')
            start_date, forward_date, end_date = self.extract_dates_from_xml(files[0])
            if start_date and forward_date and end_date:
                self.start_date_edit.setDate(QDate.fromString(start_date, 'yyyy-MM-dd'))
                self.forward_date_edit.setDate(QDate.fromString(forward_date, 'yyyy-MM-dd'))
                self.end_date_edit.setDate(QDate.fromString(end_date, 'yyyy-MM-dd'))
            else:
                QMessageBox.warning(self, "Date Extraction", f"Could not extract dates from {files[0]}. Please enter dates manually.")

    def browse_set_files(self, default_file=None):
        # If default_file is provided, use it; otherwise, open the file dialog
        if default_file:
            files = [default_file]
        else:

            files, _ = QFileDialog.getOpenFileNames(self, "Select Set File(s)", "", "Set Files (*.set)")

        print('-----')
        print('-creatorxml inputing set file')
        if files:
            # Clear previous set files
            self.set_file_contents = {}
            # Display filenames
            filenames = [os.path.basename(fp) for fp in files]


            # print(self.set_file_path)
            # print(type(self.set_file_path))
            # print(filenames)
            try:
                self.set_file_path.setText("\n".join(filenames))
            except:
                pass





            # Read each set file and store content and path
            for file_path in files:
                base_name = os.path.basename(file_path)[:-4]  # Remove '.set'
                if file_path:
                    # Try different encodings
                    encodings_to_try = ['utf-16', 'utf-16-le', 'utf-16-be', 'utf-8-sig', 'utf-8']
                    for encoding in encodings_to_try:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                lines = f.readlines()
                            # If successful, break out of loop
                            break
                        except (UnicodeDecodeError, UnicodeError):
                            continue
                    else:
                        QMessageBox.warning(self, "Encoding Error", f"Could not read file {file_path} with any known encoding.")
                        continue

                    # Clean up lines
                    set_content = [line.replace('\ufeff', '').strip('\n').strip('\r') + '\n' for line in lines]
                    # Store both content and file_path
                    self.set_file_contents[base_name] = {'content': set_content, 'file_path': file_path}

    def extract_dates_from_xml(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            soup = BeautifulSoup(content, 'xml')

            # Extract dates from the <Title> tag
            title_tag = soup.find('Title')
            if title_tag:
                title_text = title_tag.get_text(strip=True)
                # Extract dates from the title text
                # Example format: "creator11-4_v03 XAUUSD,M1 2024.08.04-2024.10.26"
                date_pattern = r'(\d{4}\.\d{2}\.\d{2})-(\d{4}\.\d{2}\.\d{2})'
                match = re.search(date_pattern, title_text)
                if match:
                    date_from_str = match.group(1)
                    date_to_str = match.group(2)

                    # Parse dates
                    date_format = '%Y.%m.%d'
                    start_date = datetime.strptime(date_from_str, date_format)
                    end_date = datetime.strptime(date_to_str, date_format)

                    # Calculate the midpoint date and set forward_date
                    delta = end_date - start_date
                    midpoint = start_date + delta / 2

                    return start_date.strftime('%Y-%m-%d'), midpoint.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while extracting dates from {file_path}: {e}")
        # If dates cannot be extracted, return None
        return None, None, None

    def calculate_weeks(self, date1_str, date2_str):
        date_format = '%Y-%m-%d'
        date1 = datetime.strptime(date1_str, date_format)
        date2 = datetime.strptime(date2_str, date_format)
        date_difference = (date2 - date1).days
        weeks = date_difference / 7
        return weeks

    def process_files(self, automationCall=None ):
        print('processing_files')
        # Get input values
        forward_files = self.forward_files
        backward_files = self.backward_files
        set_files = self.set_file_contents
        folder_name = self.folder_name
        balance = self.balance
        drawdown = self.drawdown












        # Validate inputs
        if not forward_files or not backward_files:
            QMessageBox.critical(self, "Input Error", "Please provide forward and backward files.")
            return

        if not set_files:
            QMessageBox.critical(self, "Input Error", "Please provide the .set files.")
            return

        if not folder_name:
            QMessageBox.critical(self, "Input Error", "Please provide a folder name for the new .set files.")
            return

        try:
            try:
                balance = float(balance.text())
                drawdown = float(drawdown.text())
            except:
                try:
                    balance = float(balance)
                    drawdown = float(drawdown)
                except:
                    try:
                        balance = int(balance)
                        drawdown = int(drawdown)
                    except:
                        balance = int(balance.text())
                        drawdown = int(drawdown.text())

        except ValueError:
            QMessageBox.critical(self, "Input Error", "Balance and Drawdown must be numbers.")
            return

        # Build mappings
        backward_files_dict = {}
        for path in backward_files:
            filename = os.path.basename(path)
            if filename.endswith('.xml'):
                base_filename = filename[:-4]  # Remove '.xml'
                backward_files_dict[base_filename] = path

        forward_files_dict = {}
        for path in forward_files:
            filename = os.path.basename(path)
            if filename.endswith('.forward.xml'):
                base_filename = filename[:-12]  # Remove '.forward.xml'
                forward_files_dict[base_filename] = path

        # Pair the files
        file_pairs = []
        for base_name, backward_path in backward_files_dict.items():
            if base_name in forward_files_dict:
                forward_path = forward_files_dict[base_name]
                file_pairs.append((base_name, forward_path, backward_path))
            else:
                print(f"No matching forward file for {backward_path}")
                QMessageBox.warning(self, "File Pairing", f"No matching forward file for {backward_path}")

        if not file_pairs:
            QMessageBox.critical(self, "Input Error", "No matching forward and backward file pairs found.")
            return

        # Check if set files are available for all base names
        missing_sets = [base_name for base_name, _, _ in file_pairs if base_name not in set_files]
        if missing_sets:
            QMessageBox.critical(self, "Set File Error", f"Set files missing for the following base names: {', '.join(missing_sets)}")
            return

        # Reset current page
        self.current_page = 1
        self.duplicates_removed = False

        # Process the files
        all_results = []
        self.pass_parameters = {}

        for base_name, forward_file, backward_file in file_pairs:
            try:
                # Use dates from the date input fields (already populated)
                start_date = self.start_date_edit.date().toString('yyyy-MM-dd')
                forward_date = self.forward_date_edit.date().toString('yyyy-MM-dd')
                end_date = self.end_date_edit.date().toString('yyyy-MM-dd')

                # Validate date order
                if not (start_date < forward_date < end_date):
                    QMessageBox.critical(self, "Date Error", f"Please ensure that Start Date < Forward Date < End Date for file {backward_file}. Skipping this pair.")
                    continue

                # Process the files
                result_df, pass_params = self.process_xml_files(
                    base_name,
                    forward_file,
                    backward_file,
                    start_date,
                    end_date,
                    forward_date,
                    balance,
                    drawdown
                )

                all_results.append(result_df)
                self.pass_parameters.update(pass_params)
            except Exception as e:
                QMessageBox.critical(self, "Processing Error", f"Error processing files {forward_file} and {backward_file}: {str(e)}")
                continue

        if not all_results:
            QMessageBox.critical(self, "Processing Error", "No data was processed.")
            return

        # Concatenate all results
        self.full_data = pd.concat(all_results, ignore_index=True)

        print('saving full data..')
        self.full_data.to_csv('fullData.csv', index=False)


        if self.full_data.empty:
            QMessageBox.critical(self, "Processing Error", "No data was processed. Please check if the XML files contain data and have matching 'Pass' values.")
            return
        self.filtered_data = self.full_data.copy()

        if automationCall == True:
            print('done processing..')
            #QApplication.quit()



        self.display_creator_results(self.filtered_data)
    def process_xml_files(self, base_name, forward_file_path, backward_file_path, start_date, end_date, forward_date, balance, drawdown):
        # Read file content
        with open(forward_file_path, 'r', encoding='utf-8') as f:
            forward_content = f.read()
        with open(backward_file_path, 'r', encoding='utf-8') as f:
            backward_content = f.read()

        # Parse XML content
        soup_forward = BeautifulSoup(forward_content, 'xml')
        soup_backward = BeautifulSoup(backward_content, 'xml')

        # Calculate time differences
        g15 = self.calculate_weeks(start_date, forward_date)
        g16 = self.calculate_weeks(forward_date, end_date)
        if g16 != 0:
            g17 = g15 / g16
        else:
            g17 = 0  # Avoid division by zero

        # Extract data into DataFrames
        back_df = self.extract_data_to_df(soup_backward, suffix='_back')
        fwd_df = self.extract_data_to_df(soup_forward, suffix='_fwd')

        # Ensure 'Pass' columns are strings
        back_df['Pass'] = back_df['Pass'].astype(str)
        fwd_df['Pass'] = fwd_df['Pass'].astype(str)

        # Merge datasets on "Pass"
        merged_data = pd.merge(back_df, fwd_df, on="Pass", how='inner')

        if merged_data.empty:
            raise ValueError(f"No matching passes found in backward and forward files for {base_name}.")

        # Initial balance
        initial_balance = float(balance)

        # Ensure numeric types
        numeric_columns = ['Profit_back', 'Profit_fwd', 'Recovery_Factor_back', 'Recovery_Factor_fwd',
                           'Equity_DD_percent_back', 'Equity_DD_percent_fwd']
        for col in numeric_columns:
            if col in merged_data.columns:
                merged_data[col] = pd.to_numeric(merged_data[col], errors='coerce')

        # Remove rows with NaN or infinite values in critical columns
        critical_columns = ['Profit_back', 'Recovery_Factor_back']
        merged_data = merged_data.replace([np.inf, -np.inf], np.nan)  # Replace infinite with NaN
        merged_data = merged_data.dropna(subset=critical_columns)

        # Perform calculations

        # Profit Match (%)
        def calculate_profit_match(row):
            if row['Profit_back'] != 0 and g17 != 0:
                return (row['Profit_fwd'] / (row['Profit_back'] / g17)) * 100
            else:
                return 0

        merged_data['Profit_Match_Percent'] = merged_data.apply(calculate_profit_match, axis=1)

        # Total Original Profit
        merged_data['Total_Original_Profit'] = merged_data['Profit_back'] + merged_data['Profit_fwd']

        # Max Original DD Calculation (Adjusted)
        merged_data['Max_Original_DD_back'] = merged_data['Profit_back'] / merged_data['Recovery_Factor_back']
        merged_data['Max_Original_DD_fwd'] = merged_data['Profit_fwd'] / merged_data['Recovery_Factor_fwd']
        merged_data['Max_Original_DD'] = merged_data[['Max_Original_DD_back', 'Max_Original_DD_fwd']].max(axis=1)

        # Lot Multiplier (Updated Function)
        def calculate_lot_multiplier(row):
            if pd.notnull(row['Max_Original_DD']) and row['Max_Original_DD'] != 0:
                target_drawdown = float(drawdown)
                min_dd = target_drawdown - 25  # Adjusted acceptable range
                max_dd = target_drawdown + 25

                # Initial calculation using Target Drawdown
                initial_lot_multiplier = target_drawdown / row['Max_Original_DD']
                if pd.isnull(initial_lot_multiplier) or math.isinf(initial_lot_multiplier) or initial_lot_multiplier <= 0:
                    return None  # Return None if the initial_lot_multiplier is invalid

                # Use higher precision
                lot_multiplier = round(initial_lot_multiplier, 4)
                total_estimated_dd = lot_multiplier * row['Max_Original_DD']

                # Adjust lot_multiplier to get Total_Estimated_DD within desired range
                max_iterations = 10000  # Increase iterations to allow finer adjustments
                iterations = 0
                adjustment_step = 0.0001  # Smaller adjustment step

                # Adjust lot_multiplier
                if total_estimated_dd < min_dd:
                    # Increase lot_multiplier
                    while total_estimated_dd < min_dd and iterations < max_iterations:
                        lot_multiplier += adjustment_step
                        total_estimated_dd = lot_multiplier * row['Max_Original_DD']
                        iterations += 1
                    lot_multiplier = max(lot_multiplier, 0)
                elif total_estimated_dd > max_dd:
                    # Decrease lot_multiplier
                    while total_estimated_dd > max_dd and lot_multiplier > 0 and iterations < max_iterations:
                        lot_multiplier -= adjustment_step
                        total_estimated_dd = lot_multiplier * row['Max_Original_DD']
                        iterations += 1
                    lot_multiplier = max(lot_multiplier, 0)

                # After adjustment, check if total_estimated_dd is within the desired range
                if min_dd <= total_estimated_dd <= max_dd:
                    return round(lot_multiplier, 4)
                else:
                    return None  # Return None if unable to find a suitable lot_multiplier
            else:
                return None

        merged_data['Lot_Multiplier'] = merged_data.apply(calculate_lot_multiplier, axis=1)

        # Total Estimated Profit
        merged_data['Total_Estimated_Profit'] = merged_data.apply(
            lambda row: row['Total_Original_Profit'] * row['Lot_Multiplier'] if pd.notnull(row['Lot_Multiplier']) else None, axis=1
        )

        # Total Estimated DD
        merged_data['Total_Estimated_DD'] = merged_data.apply(
            lambda row: row['Max_Original_DD'] * row['Lot_Multiplier'] if pd.notnull(row['Lot_Multiplier']) else None, axis=1
        )

        # Recovery Factor Score
        merged_data['Recovery_Factor_Score'] = merged_data['Recovery_Factor_back'] + merged_data['Recovery_Factor_fwd']

        # Profit Proportionality Score
        merged_data['Profit_Proportionality'] = (merged_data['Profit_fwd'] / merged_data['Profit_back']) * 100
        merged_data['Profit_Proportionality_Score'] = 100 - abs(merged_data['Profit_Proportionality'] - 100)

        # Consistency in Equity Drawdown
        merged_data['Consistency_in_Equity_DD'] = 100 - abs(merged_data['Equity_DD_percent_back'] - merged_data['Equity_DD_percent_fwd']) * 10

        # Score
        merged_data['Score'] = (
            0.35 * merged_data['Profit_Proportionality_Score'] +
            0.5 * merged_data['Recovery_Factor_Score'] +
            0.15 * merged_data['Consistency_in_Equity_DD']
        )

        # Combined trades and filtering
        merged_data['Trades_back'] = pd.to_numeric(merged_data['Trades_back'], errors='coerce')
        merged_data['Trades_fwd'] = pd.to_numeric(merged_data['Trades_fwd'], errors='coerce')
        merged_data['Combined_Trades'] = merged_data['Trades_back'] + merged_data['Trades_fwd']
        # COMMENTED OUT AS PER YOUR REQUEST
        # merged_data = merged_data[merged_data['Combined_Trades'] >= 30]

        # Add Base_Name column
        merged_data['Base_Name'] = base_name

        # Select and round columns for final display
        final_results = merged_data.copy()
        final_results = final_results.round(2)

        # Remove rows where Lot_Multiplier could not be calculated
        final_results = final_results[final_results['Lot_Multiplier'].notnull()]

        # Sort by Total Estimated Profit descending
        final_results = final_results.sort_values(by='Total_Estimated_Profit', ascending=False)

        # Store parameters for each pass
        param_columns = [col for col in back_df.columns if col not in ['Pass', 'Result_back', 'Profit_back', 'Recovery_Factor_back', 'Equity_DD_percent_back', 'Trades_back']]
        # Remove '_back' suffix
        param_columns_no_suffix = [col[:-5] if col.endswith('_back') else col for col in param_columns]
        param_columns_mapping = dict(zip(param_columns, param_columns_no_suffix))
        # Normalize parameter names to match .set file (remove underscores, lowercase)
        param_columns_mapping_normalized = {k: v.replace('_', '').lower() for k, v in param_columns_mapping.items()}

        # Prepare parameters DataFrame
        merged_data_params = merged_data[['Pass'] + param_columns].rename(columns=param_columns_mapping_normalized)
        # Add Base_Name to params
        merged_data_params['Base_Name'] = base_name
        pass_params = merged_data_params.set_index(['Base_Name', 'Pass']).to_dict('index')

        # Return final_results and pass_params
        return final_results, pass_params

    def extract_data_to_df(self, soup, suffix=''):
        rows = soup.find_all('Row')
        data = []
        headers = []
        is_first_row = True

        for row in rows:
            cells = row.find_all('Cell')
            cell_values = [cell.get_text(strip=True) for cell in cells]

            if is_first_row:
                headers = [header.strip().replace(' ', '_').replace('%', 'percent') + suffix for header in cell_values]
                is_first_row = False
            else:
                data.append(cell_values)

        df = pd.DataFrame(data, columns=headers)

        # Ensure 'Pass' is included
        if 'Pass' + suffix not in df.columns:
            # Try to find a column that might be 'Pass'
            possible_pass_columns = [col for col in df.columns if 'pass' in col.lower()]
            if possible_pass_columns:
                df.rename(columns={possible_pass_columns[0]: 'Pass'}, inplace=True)
            else:
                # If not found, rename the first column to 'Pass'
                df.rename(columns={df.columns[0]: 'Pass'}, inplace=True)
        else:
            df.rename(columns={'Pass' + suffix: 'Pass'}, inplace=True)

        # Convert numeric columns to appropriate data types
        numeric_cols = ['Profit', 'Recovery_Factor', 'Trades', 'Equity_DD_percent']
        numeric_cols = [col + suffix for col in numeric_cols]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    def configure_table_columns(self):
        # Configure visible columns
        self.table_widget.setColumnCount(len(self.visible_columns))
        headers = [col_name for col_key, col_name in self.all_columns if col_key in self.visible_columns]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def display_creator_results(self, data):
        # Ensure that data is a DataFrame
        if not isinstance(data, pd.DataFrame):
            QMessageBox.critical(self, "Data Error", "Processed data is not in the expected format.")
            return

        # Clear previous results
        self.table_widget.setRowCount(0)

        # Calculate total pages
        total_items = len(data)
        total_pages = (total_items + self.rows_per_page - 1) // self.rows_per_page

        # Ensure current page is within bounds
        if self.current_page > total_pages:
            self.current_page = total_pages
        if self.current_page < 1:
            self.current_page = 1

        # Get the data for the current page
        start_index = (self.current_page - 1) * self.rows_per_page
        end_index = start_index + self.rows_per_page
        page_data = data.iloc[start_index:end_index]

        # Insert new results
        self.table_widget.setRowCount(len(page_data))
        for row_idx, (_, row) in enumerate(page_data.iterrows()):
            for col_idx, col_key in enumerate(self.visible_columns):
                value = row.get(col_key, '')
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row_idx, col_idx, item)

        # Update pagination controls
        self.update_pagination_controls(total_pages)

    def update_filter(self, text):
        search_term = text.lower()
        if self.full_data is not None:
            if search_term == '':
                self.filtered_data = self.full_data.copy()
            else:
                self.filtered_data = self.full_data[self.full_data.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)]
            self.current_page = 1  # Reset to first page
            self.display_creator_results(self.filtered_data)

    def update_pagination_controls(self, total_pages):
        # Clear previous controls
        for i in reversed(range(self.pagination_layout.count())):
            widget = self.pagination_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Previous button
        if self.current_page > 1:
            prev_button = QPushButton("Previous")
            prev_button.clicked.connect(self.go_to_previous_page)
            self.pagination_layout.addWidget(prev_button)

        # Page info
        page_label = QLabel(f"Page {self.current_page} of {total_pages}")
        self.pagination_layout.addWidget(page_label)

        # Next button
        if self.current_page < total_pages:
            next_button = QPushButton("Next")
            next_button.clicked.connect(self.go_to_next_page)
            self.pagination_layout.addWidget(next_button)

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_creator_results(self.filtered_data)

    def go_to_next_page(self):
        total_items = len(self.filtered_data)
        total_pages = (total_items + self.rows_per_page - 1) // self.rows_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_creator_results(self.filtered_data)

    def remove_duplicates(self):
        if self.full_data is None:
            QMessageBox.critical(self, "No Data", "No data available to remove duplicates.")
            return

        if not self.duplicates_removed:
            # Remove duplicates from full_data
            self.full_data = self.full_data.drop_duplicates(subset=['Trades_back', 'Trades_fwd', 'Total_Original_Profit', 'Base_Name'])
            self.filtered_data = self.full_data.copy()

            # Apply search filter if any
            search_term = self.search_var.text().lower()
            if search_term != '':
                self.filtered_data = self.filtered_data[self.filtered_data.apply(lambda row: row.astype(str).str.lower().str.contains(search_term).any(), axis=1)]

            self.current_page = 1
            self.display_creator_results(self.filtered_data)
            self.duplicates_removed = True
            #QMessageBox.information(self, "Duplicates Removed", "Duplicate rows have been removed.")
        else:
            pass
            #QMessageBox.information(self, "Already Removed", "Duplicates have already been removed from the dataset.")

    def show_hide_columns(self):
        window = QDialog(self)
        window.setWindowTitle("Show/Hide Columns")
        window.setGeometry(300, 300, 300, 400)

        layout = QVBoxLayout(window)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)

        self.column_vars = {}
        for col_key, col_name in self.all_columns:
            var = QCheckBox(col_name)
            var.setChecked(col_key in self.visible_columns)
            scroll_area_layout.addWidget(var)
            self.column_vars[col_key] = var

        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_area_widget)

        layout.addWidget(scroll_area)

        # Apply Button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.apply_column_changes(window))
        layout.addWidget(apply_button)

        window.exec_()

    def apply_column_changes(self, window):
        self.visible_columns = [col_key for col_key, var in self.column_vars.items() if var.isChecked()]
        self.configure_table_columns()
        self.display_creator_results(self.filtered_data)
        window.close()

    def download_selected(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.critical(self, "Selection Error", "Please select one or more rows to download.")
            return

        # Get the folder name provided by the user
        folder_name = self.folder_name.text()
        if not folder_name:
            QMessageBox.critical(self, "Input Error", "Please provide a folder name for the new .set files.")
            return

        # Create a folder in the same directory as the first set file
        first_set_file_info = next(iter(self.set_file_contents.values()), None)
        if first_set_file_info:
            set_file_directory = os.path.dirname(first_set_file_info['file_path'])
        else:
            set_file_directory = os.getcwd()
        folder_path = os.path.join(set_file_directory, folder_name)

        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        for selected_row in selected_rows:
            row_index = selected_row.row()
            pass_value = self.table_widget.item(row_index, self.visible_columns.index('Pass')).text()
            base_name = self.table_widget.item(row_index, self.visible_columns.index('Base_Name')).text()
            pass_value_str = str(pass_value)
            pass_params = self.pass_parameters.get((base_name, pass_value_str))

            if not pass_params:
                QMessageBox.critical(self, "Data Error", f"Parameters for the selected pass ({pass_value}) are not available.")
                continue  # Skip to the next selected item

            # Get the corresponding set file content
            set_file_info = self.set_file_contents.get(base_name)
            if not set_file_info:
                QMessageBox.critical(self, "Set File Error", f"No set file content available for base name {base_name}.")
                continue
            set_file_content = set_file_info['content']

            # Prepare a dictionary of parameter names and values
            param_values = {}
            for key, value in pass_params.items():
                # Skip non-parameter keys
                if key in ['Pass', 'Base_Name']:
                    continue
                # Normalize key by removing underscores and converting to lowercase
                key_normalized = key.replace('_', '').lower()
                param_values[key_normalized] = value

            # Parse the .set file content
            new_set_content = []
            for line in set_file_content:
                stripped_line = line.strip()
                if '=' in stripped_line and '||' in stripped_line:
                    key, value = stripped_line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    parts = value.split('||')
                    if parts[-1].strip() == 'Y':
                        # Normalize key for matching
                        key_normalized = key.replace('_', '').lower()
                        # Check if key is in param_values
                        if key_normalized in param_values:
                            # Replace the first part (value) with the pass parameter value
                            parts[0] = str(param_values[key_normalized])
                            new_value = '||'.join(parts)
                            new_line = f"{key}={new_value}\n"
                            new_set_content.append(new_line)
                        else:
                            new_set_content.append(line)
                    else:
                        new_set_content.append(line)
                else:
                    new_set_content.append(line)

            # Save the new .set file
            set_filename = f"{base_name}_{pass_value}.set"
            save_path = os.path.join(folder_path, set_filename)

            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(new_set_content)

        QMessageBox.information(self, "Download Complete", f"Modified .set files saved successfully in {folder_path}.")

    # def download_all_above_profit(self, default_file=None):
    #     # If default_file is provided, use it; otherwise, open the file d

    #     print('-download_all_above_profit')
    #     if default_file:

    #         threshold, ok = round(float(default_file), 2), True
    #     else:
    #         threshold, ok = QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0)



    #         print(QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0))
    #     print(ok)
    #     if not ok:
    #         return  # User cancelled

    #     # Filter the data based on the threshold
    #     qualifying_data = self.full_data[self.full_data['Total_Estimated_Profit'] >= threshold]

    #     if qualifying_data.empty:
    #         QMessageBox.information(self, "No Results", f"No entries found with Total Estimated Profit >= {threshold}.")
    #         return


    # 	# Get the folder name provided by the user
    #     folder_name = self.folder_name.text()
    #     if not folder_name:
    #         QMessageBox.critical(self, "Input Error", "Please provide a folder name for the new .set files.")
    #         return

    #     # Create a folder in the same directory as the first set file
    #     first_set_file_info = next(iter(self.set_file_contents.values()), None)
    #     if first_set_file_info:
    #         set_file_directory = os.path.dirname(first_set_file_info['file_path'])
    #     else:
    #         set_file_directory = os.getcwd()
    #     folder_path = os.path.join(set_file_directory, folder_name)

    #     # Create the folder if it doesn't exist
    #     os.makedirs(folder_path, exist_ok=True)

    #     # Iterate through the qualifying rows and download
    #     for index, row in qualifying_data.iterrows():
    #         pass_value = row['Pass']
    #         base_name = row['Base_Name']
    #         pass_value_str = str(pass_value)
    #         pass_params = self.pass_parameters.get((base_name, pass_value_str))

    #         if not pass_params:
    #             QMessageBox.critical(self, "Data Error", f"Parameters for the pass ({pass_value}) are not available.")
    #             continue  # Skip to the next row

    #         # Get the corresponding set file content
    #         set_file_info = self.set_file_contents.get(base_name)
    #         if not set_file_info:
    #             QMessageBox.critical(self, "Set File Error", f"No set file content available for base name {base_name}.")
    #             continue
    #         set_file_content = set_file_info['content']

    #         # Prepare a dictionary of parameter names and values
    #         param_values = {}
    #         for key, value in pass_params.items():
    #             # Skip non-parameter keys
    #             if key in ['Pass', 'Base_Name']:
    #                 continue
    #             # Normalize key by removing underscores and converting to lowercase
    #             key_normalized = key.replace('_', '').lower()
    #             param_values[key_normalized] = value

    #         # Parse the .set file content
    #         new_set_content = []
    #         for line in set_file_content:
    #             stripped_line = line.strip()
    #             if '=' in stripped_line and '||' in stripped_line:
    #                 key, value = stripped_line.split('=', 1)
    #                 key = key.strip()
    #                 value = value.strip()
    #                 parts = value.split('||')
    #                 if parts[-1].strip() == 'Y':
    #                     # Normalize key for matching
    #                     key_normalized = key.replace('_', '').lower()
    #                     # Check if key is in param_values
    #                     if key_normalized in param_values:
    #                         # Replace the first part (value) with the pass parameter value
    #                         parts[0] = str(param_values[key_normalized])
    #                         new_value = '||'.join(parts)
    #                         new_line = f"{key}={new_value}\n"
    #                         new_set_content.append(new_line)
    #                     else:
    #                         new_set_content.append(line)
    #                 else:
    #                     new_set_content.append(line)
    #             else:
    #                 new_set_content.append(line)

    #         # Save the new .set file
    #         set_filename = f"{base_name}_{pass_value}.set"
    #         save_path = os.path.join(folder_path, set_filename)

    #         with open(save_path, 'w', encoding='utf-8') as f:
    #             f.writelines(new_set_content)
    #     print(f"All qualifying .set files saved successfully in {folder_path}.")
    #     QApplication.quit()
    #     QMessageBox.information(self, "Download Complete", f"All qualifying .set files saved successfully in {folder_path}.")


    def download_all_above_profit(self, default_file=None):

        print('-download_all_above_profit')
        if default_file:

            threshold, ok = round(float(default_file), 2), True
        else:
            threshold, ok = QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0)



            print(QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0))
        print(ok)
        if not ok:
            return  # User cancelled

        try:
            self.full_data['Total_Estimated_Profit'] = pd.to_numeric(self.full_data['Total_Estimated_Profit'], errors='coerce')
            try:
                self.qualifying_data['Total_Estimated_Profit'] = pd.to_numeric(self.qualifying_data['Total_Estimated_Profit'], errors='coerce')
            except:
                pass
        except:
            pass
        # Filter the data based on the threshold
        try:
            if self.qualifying_data is None or (isinstance(self.qualifying_data, pd.DataFrame) and self.qualifying_data.empty):

                qualifying_data = self.full_data[self.full_data['Total_Estimated_Profit'] >= threshold]
            else:
                qualifying_data = self.qualifying_data[self.qualifying_data['Total_Estimated_Profit'] >= threshold]
        except:
            if getattr(self, "qualifying_data", None) is None or self.qualifying_data.empty:
                qualifying_data = self.full_data[self.full_data['Total_Estimated_Profit'] >= threshold]
            else:
                qualifying_data = self.qualifying_data[self.qualifying_data['Total_Estimated_Profit'] >= threshold]


        self.qualifying_data = qualifying_data.copy()

        if qualifying_data.empty:
            return


    def download_all_below_max_dd(self, default_file=None):
        # If default_file is provided, use it; otherwise, open the file d

        print('-download_all_below_max_dd')
        if default_file:

            threshold, ok = round(float(default_file),2), True
        else:
            threshold, ok = QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0)

            print(QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0))
        print(ok)
        if not ok:
            return  # User cancelled

        # Filter the data based on the threshold




        self.full_data['Max_Original_DD'] = pd.to_numeric(self.full_data['Max_Original_DD'], errors='coerce')
        try:
            self.qualifying_data['Max_Original_DD'] = pd.to_numeric(self.qualifying_data['Max_Original_DD'], errors='coerce')
        except:
            pass
        try:

            if self.qualifying_data is None or (isinstance(self.qualifying_data, pd.DataFrame) and self.qualifying_data.empty):

                qualifying_data = self.full_data[self.full_data['Max_Original_DD'] <= threshold]
            else:
                qualifying_data = self.qualifying_data[self.qualifying_data['Max_Original_DD'] <= threshold]
        except:
            if getattr(self, "qualifying_data", None) is None or self.qualifying_data.empty:

                qualifying_data = self.full_data[self.full_data['Max_Original_DD'] <= threshold]
            else:
                qualifying_data = self.qualifying_data[self.qualifying_data['Max_Original_DD'] <= threshold]

        self.qualifying_data = qualifying_data.copy()

        if qualifying_data.empty:
            #QMessageBox.information(self, "No Results", f"No entries found with Max Original DD ≤ {threshold}.")
            return

        # Proceed to download
        self.qualifying_data = qualifying_data.copy()
        #self.download_qualifying_set_files(qualifying_data)

    def download_all_profit_and_dd(self,min_profit, max_dd):
        """msg to engineer NOT INCLUDED IN FULL AUTOMATION"""
        # Prompt the user to enter the profit threshold
        # min_profit, ok1 = QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0)
        # if not ok1:
        #     return  # User cancelled
        # # Prompt the user to enter the max original DD threshold
        # max_dd, ok2 = QInputDialog.getDouble(self, "Max Original DD", "Enter the maximum Max Original DD to download:", min=0)
        # if not ok2:
        #     return  # User cancelled


        min_profit = float(min_profit)
        # Prompt the user to enter the max original DD threshold
        max_dd = float(max_dd)

        # Filter the data based on both thresholds
        try:
            if self.qualifying_data is None or (isinstance(self.qualifying_data, pd.DataFrame) and self.qualifying_data.empty):

                qualifying_data = self.full_data[
                (self.full_data['Total_Estimated_Profit'] >= min_profit) &
                (self.full_data['Max_Original_DD'] <= max_dd)
            ]
            else:
                qualifying_data = self.qualifying_data[
                (self.qualifying_data['Total_Estimated_Profit'] >= min_profit) &
                (self.qualifying_data['Max_Original_DD'] <= max_dd)
            ]
        except:
            if getattr(self, "qualifying_data", None) is None or self.qualifying_data.empty:

                qualifying_data = self.full_data[
                (self.full_data['Total_Estimated_Profit'] >= min_profit) &
                (self.full_data['Max_Original_DD'] <= max_dd)
            ]
            else:
                qualifying_data = self.qualifying_data[
                (self.qualifying_data['Total_Estimated_Profit'] >= min_profit) &
                (self.qualifying_data['Max_Original_DD'] <= max_dd)
            ]


        self.qualifying_data = qualifying_data.copy()
        if qualifying_data.empty:
            print(f"No entries found with Total Estimated Profit ≥ {min_profit} and Max Original DD ≤ {max_dd}.")
            return

        # Proceed to download

        #self.download_qualifying_set_files(qualifying_data)

    def download_qualifying_set_files(self, qualifying_data):
        # Get the folder name provided by the user

        print('download_qualifying_set_files')
        folder_name = self.folder_name.text()

        print(folder_name)
        if not folder_name:
            QMessageBox.critical(self, "Input Error", "Please provide a folder name for the new .set files.")
            return

        # Create a folder in the same directory as the first set file
        first_set_file_info = next(iter(self.set_file_contents.values()), None)
        if first_set_file_info:
            set_file_directory = os.path.dirname(first_set_file_info['file_path'])
        else:
            set_file_directory = os.getcwd()
        folder_path = os.path.join(set_file_directory, folder_name)

        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # Iterate through the qualifying rows and download
        for index, row in qualifying_data.iterrows():
            #print('itterating')
            pass_value = row['Pass']
            base_name = row['Base_Name']
            pass_value_str = str(pass_value)
            pass_params = self.pass_parameters.get((base_name, pass_value_str))

            if not pass_params:
                #QMessageBox.critical(self, "Data Error", f"Parameters for the pass ({pass_value}) are not available.")
                continue  # Skip to the next row

            # Get the corresponding set file content
            set_file_info = self.set_file_contents.get(base_name)
            if not set_file_info:
                #QMessageBox.critical(self, "Set File Error", f"No set file content available for base name {base_name}.")
                continue
            set_file_content = set_file_info['content']

            # Prepare a dictionary of parameter names and values
            param_values = {}
            for key, value in pass_params.items():
                # Skip non-parameter keys
                if key in ['Pass', 'Base_Name']:
                    continue
                # Normalize key by removing underscores and converting to lowercase
                key_normalized = key.replace('_', '').lower()
                param_values[key_normalized] = value

            # Parse the .set file content
            new_set_content = []
            for line in set_file_content:
                #print('itterating 2')
                stripped_line = line.strip()
                if '=' in stripped_line and '||' in stripped_line:
                    key, value = stripped_line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    parts = value.split('||')
                    if parts[-1].strip() == 'Y':
                        # Normalize key for matching
                        key_normalized = key.replace('_', '').lower()
                        # Check if key is in param_values
                        if key_normalized in param_values:
                            # Replace the first part (value) with the pass parameter value
                            parts[0] = str(param_values[key_normalized])
                            new_value = '||'.join(parts)
                            new_line = f"{key}={new_value}\n"
                            new_set_content.append(new_line)
                        else:
                            new_set_content.append(line)
                    else:
                        new_set_content.append(line)
                else:
                    new_set_content.append(line)

            # Save the new .set file
            #print('pass')
            set_filename = f"{base_name}_{pass_value}.set"
            save_path = os.path.join(folder_path, set_filename)
            #print('pass1')
            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(new_set_content)
            #print('pass2')
        print(f"All qualifying .set files saved successfully in {folder_path}.")
        return
        #QApplication.quit()
        #QMessageBox.information(self, "Download Complete", f"All qualifying .set files saved successfully in {folder_path}.")

    ##############

    def download_all_profit_greater_than_dd_and_trades(self, default_file=None):
        # If default_file is provided, use it; otherwise, open the file d

        print('-download_all_below_max_dd')
        if default_file:

            min_trades, ok = float(default_file), True
        else:
            min_trades, ok = QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0)



            print(QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0))
        print(ok)
        if not ok:
            return  # User cancelled

        # Filter the data based on the threshold
        self.full_data['Total_Estimated_Profit'] = pd.to_numeric(self.full_data['Total_Estimated_Profit'], errors='coerce')
        self.full_data['Max_Original_DD'] = pd.to_numeric(self.full_data['Max_Original_DD'], errors='coerce')
        self.full_data['Combined_Trades'] = pd.to_numeric(self.full_data['Combined_Trades'], errors='coerce')
        try:
            self.qualifying_data['Total_Estimated_Profit'] = pd.to_numeric(self.qualifying_data['Total_Estimated_Profit'], errors='coerce')
            self.qualifying_data['Max_Original_DD'] = pd.to_numeric(self.qualifying_data['Max_Original_DD'], errors='coerce')
            self.qualifying_data['Combined_Trades'] = pd.to_numeric(self.qualifying_data['Combined_Trades'], errors='coerce')
        except:
            pass

        # Filter data where Total_Estimated_Profit > Max_Original_DD and Combined_Trades >= min_trades
        try:
            if self.qualifying_data is None or (isinstance(self.qualifying_data, pd.DataFrame) and self.qualifying_data.empty):

                qualifying_data = self.full_data[
                (self.full_data['Total_Estimated_Profit'] > self.full_data['Max_Original_DD']) &
                (self.full_data['Combined_Trades'] >= min_trades)
            ]
            else:
                qualifying_data = self.qualifying_data[
                (self.qualifying_data['Total_Estimated_Profit'] > self.qualifying_data['Max_Original_DD']) &
                (self.qualifying_data['Combined_Trades'] >= min_trades)
            ]
        except:
            if getattr(self, "qualifying_data", None) is None or self.qualifying_data.empty:

                qualifying_data = self.full_data[
                (self.full_data['Total_Estimated_Profit'] > self.full_data['Max_Original_DD']) &
                (self.full_data['Combined_Trades'] >= min_trades)
            ]
            else:
                qualifying_data = self.qualifying_data[
                (self.qualifying_data['Total_Estimated_Profit'] > self.qualifying_data['Max_Original_DD']) &
                (self.qualifying_data['Combined_Trades'] >= min_trades)
            ]

        self.qualifying_data = qualifying_data.copy()
        if qualifying_data.empty:
            #QMessageBox.information(self, "No Results", f"No entries found with Max Original DD ≤ {min_trades}.")
            return

        # Proceed to download
        self.qualifying_data = qualifying_data.copy()
        #self.download_qualifying_set_files(qualifying_data)

    def download_all_profit_greater_than_dd(self):
        # If default_file is provided, use it; otherwise, open the file d

        # print('-download_all_below_max_dd')
        # if default_file:

        #     min_trades, ok = float(default_file), True
        # else:
        #     min_trades, ok = QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0)



        #     print(QInputDialog.getDouble(self, "Total Estimated Profit", "Enter the minimum Total Estimated Profit to download:", min=0))
        # print(ok)
        # if not ok:
        #     return  # User cancelled

        try:

            # Filter the data based on the threshold
            self.full_data['Total_Estimated_Profit'] = pd.to_numeric(self.full_data['Total_Estimated_Profit'], errors='coerce')
            self.full_data['Max_Original_DD'] = pd.to_numeric(self.full_data['Max_Original_DD'], errors='coerce')
            self.full_data['Combined_Trades'] = pd.to_numeric(self.full_data['Combined_Trades'], errors='coerce')
            try:
                self.qualifying_data['Total_Estimated_Profit'] = pd.to_numeric(self.qualifying_data['Total_Estimated_Profit'], errors='coerce')
                self.qualifying_data['Max_Original_DD'] = pd.to_numeric(self.qualifying_data['Max_Original_DD'], errors='coerce')
                self.qualifying_data['Combined_Trades'] = pd.to_numeric(self.qualifying_data['Combined_Trades'], errors='coerce')
            except:
                pass
        except:
            pass

        # Filter data where Total_Estimated_Profit > Max_Original_DD and Combined_Trades >= min_trades

        try:
            if self.qualifying_data is None or (isinstance(self.qualifying_data, pd.DataFrame) and self.qualifying_data.empty):

                qualifying_data = self.full_data[
                    (self.full_data['Total_Estimated_Profit'] > self.full_data['Max_Original_DD'])
                ]
            else:
                qualifying_data = self.qualifying_data[
                    (self.qualifying_data['Total_Estimated_Profit'] > self.qualifying_data['Max_Original_DD'])
                ]

        except:
            if getattr(self, "qualifying_data", None) is None or self.qualifying_data.empty:

                qualifying_data = self.full_data[
                    (self.full_data['Total_Estimated_Profit'] > self.full_data['Max_Original_DD'])
                ]
            else:
                qualifying_data = self.qualifying_data[
                    (self.qualifying_data['Total_Estimated_Profit'] > self.qualifying_data['Max_Original_DD'])
                ]


        self.qualifying_data = qualifying_data.copy()
        if qualifying_data.empty:

            return

        # Proceed to download

        #self.download_qualifying_set_files(qualifying_data)
    ##############

def create_filesets_list(input_folder_path, backtester_report_folder_path):
    '''create list of fileSets
    example output:
    [['C:\\Users\\Admin\\AppData\\Roaming\\MetaQuotes\\Terminal\\D0E8209F77C8CF37AD8BF550E51FF075\\test3\\backtester_report_20241112_235932\\US30_ADXBB.forward.xml',
      'C:\\Users\\Admin\\AppData\\Roaming\\MetaQuotes\\Terminal\\D0E8209F77C8CF37AD8BF550E51FF075\\test3\\backtester_report_20241112_235932\\US30_ADXBB.xml',
        'C:\\Users\\Admin\\AppData\\Roaming\\MetaQuotes\\Terminal\\D0E8209F77C8CF37AD8BF550E51FF075\\test3\\US30_ADXBB.set']]'''
    input_folder_path = input_folder_path
    backtester_report_folder_path = backtester_report_folder_path

    dir_list = os.listdir(backtester_report_folder_path)
    print(dir_list)
    fileSets_list = []
    for f in dir_list:
        temp_list = []
        if '.forward.xml' in f:
            temp_list.append(backtester_report_folder_path + f)
            temp_list.append(backtester_report_folder_path + f.split('.forward')[0] + '.xml')
            temp_list.append(input_folder_path + f.split('.forward')[0] + '.set')
            fileSets_list.append(temp_list)
    print('CHECK CHECK CHECK!!')
    print(fileSets_list)
    print(len(fileSets_list))
    print('CHECK CHECK CHECK!!')
    return fileSets_list

####################################################################

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def check_license_key():


    return True
    # URL of the license key file on GitHub
    LICENSE_URL = 'https://raw.githubusercontent.com/joeadams101/creator-license/refs/heads/main/license_keys.txt'  # Replace with your URL

    try:
        response = requests.get(LICENSE_URL)
        if response.status_code == 200:
            valid_keys = response.text.strip().split('\n')
        else:
            messagebox.showerror("Error", "Unable to retrieve license keys.")
            return False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return False

    # Prompt the user to enter the license key
    license_key = simpledialog.askstring("License Key", "Please enter your license key:")
    if not license_key:
        messagebox.showerror("Error", "No license key entered.")
        return False

    if license_key.strip() in [key.strip() for key in valid_keys]:
        print("License key is valid.")
        return True
    else:
        messagebox.showerror("Error", "Invalid license key.")
        return False


def extract_symbol_from_set_filename(set_file_name):
    # Extract symbol from the set file name
    # Assuming the symbol is the substring before the first underscore '_'
    symbol = set_file_name.split('_')[0]
    return symbol.upper()


def run_creator_oos_generator_for_automation(params_creator_oos, stop_event, progress_var,progress_label, total_set_files, start_button, stop_button):
    def update_progress(value, message):
        progress_var.set(value)
        progress_label.config(text=message)
    try:
        # Unpack parameters
        MT5_PATH = params_creator_oos['MT5_PATH']
        MT5_DATA_FOLDER = params_creator_oos['MT5_DATA_FOLDER']
        SET_FILES_FOLDER = str(params_creator_oos['SET_FILES_FOLDER']) + '\\ADXBB'
        CUSTOM_REPORT_FOLDER_BASE = params_creator_oos['CUSTOM_REPORT_FOLDER_BASE']
        FROM_DATE = params_creator_oos['FROM_DATE']
        TO_DATE = params_creator_oos['TO_DATE']
        DEPOSIT = params_creator_oos['DEPOSIT']
        LEVERAGE = params_creator_oos['LEVERAGE']
        PERIOD = params_creator_oos['PERIOD']
        EXPERT_ADVISOR = params_creator_oos['EXPERT_ADVISOR']
        EXECUTION_MODE = params_creator_oos['EXECUTION_MODE']
        MODEL = params_creator_oos['MODEL']




        print('%%%%%%%%%%%%%%%%')
        print(CUSTOM_REPORT_FOLDER_BASE)


        #############################################################################################
        # Create a timestamped report folder (relative path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        CUSTOM_REPORT_FOLDER_NAME = f"creator_oos_report_{timestamp}"
        # Relative path from MT5_DATA_FOLDER
        CUSTOM_REPORT_FOLDER_RELATIVE = os.path.join(CUSTOM_REPORT_FOLDER_BASE, CUSTOM_REPORT_FOLDER_NAME)
        CUSTOM_REPORT_FOLDER_FULL = os.path.join(MT5_DATA_FOLDER, CUSTOM_REPORT_FOLDER_RELATIVE)
        os.makedirs(CUSTOM_REPORT_FOLDER_FULL, exist_ok=True)
        print(f"Created report folder: {CUSTOM_REPORT_FOLDER_FULL}")

        MT5_PROFILES_TESTER = os.path.join(MT5_DATA_FOLDER, r"MQL5\Profiles\Tester")
        # Ensure MT5 Profiles Tester folder exists
        os.makedirs(MT5_PROFILES_TESTER, exist_ok=True)

        # Check for .set files
        set_files = [f for f in os.listdir(SET_FILES_FOLDER) if f.endswith('.set')]
        if not set_files:
            print(f"No .set files found in '{SET_FILES_FOLDER}'")
            #messagebox.showerror("Error", f"No .set files found in '{SET_FILES_FOLDER}'")
            # Re-enable the Start Test button and disable Stop Test button
            start_button_full_automation.config(state=tk.NORMAL)
            stop_button_full_automation.config(state=tk.DISABLED)
            return None, CUSTOM_REPORT_FOLDER_FULL

        total_files = len(set_files)
        progress_step = 100 / total_files  # For progress bar increment

        # Initialize progress
        progress_var.set(0)
        current_progress = 0

        # Backtesting Automation
        for index, set_file in enumerate(set_files):





            if stop_event.is_set():
                print("Backtesting stopped by user.")
                messagebox.showinfo("Stopped", "Backtesting stopped by user.")
                # Re-enable the Start Test button and disable Stop Test button
                start_button_full_automation.config(state=tk.NORMAL)
                stop_button_full_automation.config(state=tk.DISABLED)
                return None, CUSTOM_REPORT_FOLDER_FULL

            print(f"\nProcessing set file: {set_file}")



            SET_FILE_NAME = os.path.splitext(set_file)[0]

            # Extract symbol from the set file name
            symbol = extract_symbol_from_set_filename(SET_FILE_NAME)
            if not symbol:
                print(f"Could not extract symbol from set file '{set_file}'. Skipping.")
                continue

            print(f"Extracted symbol '{symbol}' from set file.")

            # Copy the .set file using shutil.copy for reliability
            src_set_file = os.path.join(SET_FILES_FOLDER, set_file)
            dest_set_file = os.path.join(MT5_PROFILES_TESTER, set_file)
            try:
                shutil.copy(src_set_file, dest_set_file)
                print(f"Copied '{set_file}' to '{MT5_PROFILES_TESTER}'")
            except Exception as e:
                print(f"Failed to copy '{set_file}': {e}")
                messagebox.showerror("Error", f"Failed to copy '{set_file}': {e}")
                continue  # Proceed to the next .set file

            # Generate the .ini file
            INI_FILE = os.path.join(MT5_DATA_FOLDER, f"temp_{SET_FILE_NAME}.ini")
            report_filename = SET_FILE_NAME  # Do not add any extension
            # Report path relative to MT5_DATA_FOLDER
            report_path_relative = os.path.join(CUSTOM_REPORT_FOLDER_BASE, CUSTOM_REPORT_FOLDER_NAME, report_filename)
            # Ensure backslashes are correctly formatted
            report_path_relative = report_path_relative.replace('/', '\\')

            with open(INI_FILE, 'w') as ini_file:
                ini_file.write("; start strategy tester\n")
                ini_file.write("[Tester]\n")
                ini_file.write(f"Expert={EXPERT_ADVISOR}\n")
                ini_file.write(f"ExpertParameters={set_file}\n")
                ini_file.write(f"Symbol={symbol}\n")
                ini_file.write(f"Period={PERIOD}\n")
                ini_file.write(f"Model={MODEL}\n")
                ini_file.write(f"ExecutionMode={EXECUTION_MODE}\n")
                ini_file.write("Optimization=0\n")  # No optimization
                ini_file.write("OptimizationCriterion=0\n")  # Not used
                ini_file.write("ForwardMode=0\n")  # No forward testing
                ini_file.write("DateEnable=true\n")
                ini_file.write(f"FromDate={FROM_DATE}\n")
                ini_file.write(f"ToDate={TO_DATE}\n")
                # Use relative report path, without quotes
                ini_file.write(f"Report={report_path_relative}\n")
                ini_file.write("ReplaceReport=true\n")
                ini_file.write(f"Deposit={DEPOSIT}\n")
                ini_file.write(f"Leverage={LEVERAGE}\n")
                # Do not specify ReportFormat

            print(f"Generated .ini file at '{INI_FILE}' with Report path '{report_path_relative}'")

            # Ensure MT5 is not running
            print("Ensuring no previous MT5 instances are running...")
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == 'terminal64.exe':
                    proc.kill()
                    print(f"Killed process {proc.pid} ({proc.info['name']})")
            print("Waiting for MT5 to fully close...")
            time.sleep(5)

            if stop_event.is_set():
                print("Backtesting stopped by user.")
                messagebox.showinfo("Stopped", "Backtesting stopped by user.")
                # Re-enable the Start Test button and disable Stop Test button
                start_button_full_automation.config(state=tk.NORMAL)
                stop_button_full_automation.config(state=tk.DISABLED)
                return None, CUSTOM_REPORT_FOLDER_FULL

            # Start MT5
            print(f"Starting MT5 with config '{INI_FILE}'")
            try:
                mt5_process = subprocess.Popen([MT5_PATH, f"/config:{INI_FILE}"])
                print(f"Started MT5 process with PID {mt5_process.pid}")
            except Exception as e:
                print(f"Failed to start MT5: {e}")
                messagebox.showerror("Error", f"Failed to start MT5: {e}")
                continue  # Proceed to the next .set file

            # Wait for any file to be created in the report folder
            max_wait_seconds = 7200  # 2 hours
            wait_counter = 0
            report_exists = False
            print("Waiting for report file to be created...")

            # Full path to the report folder
            report_folder_full_path = os.path.join(MT5_DATA_FOLDER, os.path.dirname(report_path_relative))

            # Initial list of files in the report folder
            initial_files = set(os.listdir(report_folder_full_path))

            while wait_counter < max_wait_seconds:
                if stop_event.is_set():
                    print("Backtesting stopped by user.")
                    mt5_process.kill()
                    messagebox.showinfo("Stopped", "Backtesting stopped by user.")
                    # Re-enable the Start Test button and disable Stop Test button
                    start_button_full_automation.config(state=tk.NORMAL)
                    stop_button_full_automation.config(state=tk.DISABLED)
                    return None, CUSTOM_REPORT_FOLDER_FULL

                # Get the current list of files
                current_files = set(os.listdir(report_folder_full_path))
                # Check for new files
                new_files = current_files - initial_files
                if new_files:
                    report_exists = True
                    print(f"Report file(s) created: {new_files}")
                    break

                time.sleep(5)
                wait_counter += 5
                print(f"Waited {wait_counter} seconds for report file to be created...")

            if not report_exists:
                print("Report file was not created within expected time. Forcing MT5 to close...")
                mt5_process.kill()
                messagebox.showerror("Error", f"Report file was not created for '{set_file}'.")
                continue  # Proceed to the next .set file

            # Close MT5
            print("Closing MT5...")
            mt5_process.kill()
            print("MT5 closed.")

            # Delete the .ini file
            if os.path.exists(INI_FILE):
                os.remove(INI_FILE)
                print(f"Deleted temporary .ini file '{INI_FILE}'")

            # Update progress bar


            current_progress = current_progress + progress_step
            #progress_var.set(current_progress)
            update_progress(current_progress, 'run_creator_oos_generator_for_automation')


            # Wait before starting the next test
            print("Waiting before starting the next test...")
            time.sleep(5)

        # After all backtests are done, process the reports and generate Excel summary
        if not stop_event.is_set():
            print("All backtests are completed.")
            progress_var.set(100)
            print("Processing reports and generating Excel file...")
            current_progress = 100
            #progress_var.set(current_progress)
            update_progress(current_progress, "Processing reports and generating Excel file...")

            # Define the Excel summary file path inside the report folder
            OUTPUT_EXCEL_FILE = os.path.join(CUSTOM_REPORT_FOLDER_FULL, "total_net_profit_summary.xlsx")

            # List of report files
            report_files = [f for f in os.listdir(CUSTOM_REPORT_FOLDER_FULL) if f.endswith('.htm') or f.endswith('.html')]
            if not report_files:
                print(f"No HTML report files found in '{CUSTOM_REPORT_FOLDER_FULL}'")
                messagebox.showerror("Error", f"No HTML report files found in '{CUSTOM_REPORT_FOLDER_FULL}'")
                # Re-enable the Start Test button and disable Stop Test button
                start_button_full_automation.config(state=tk.NORMAL)
                stop_button_full_automation.config(state=tk.DISABLED)
                return None, CUSTOM_REPORT_FOLDER_FULL
            if len(report_files) == 0:
                return None, CUSTOM_REPORT_FOLDER_FULL
            total_net_profit_summary = []  # To store extracted data and set file names

            for report_file in report_files:
                if stop_event.is_set():
                    print("Processing stopped by user.")
                    messagebox.showinfo("Stopped", "Processing stopped by user.")
                    # Re-enable the Start Test button and disable Stop Test button
                    start_button_full_automation.config(state=tk.NORMAL)
                    stop_button_full_automation.config(state=tk.DISABLED)
                    return None, CUSTOM_REPORT_FOLDER_FULL

                report_path = os.path.join(CUSTOM_REPORT_FOLDER_FULL, report_file)
                print(f"Processing report: {report_file}")

                # Open the file in binary mode and let BeautifulSoup detect encoding
                try:
                    with open(report_path, 'rb') as file:
                        content = file.read()
                        soup = BeautifulSoup(content, 'html.parser')
                except Exception as e:
                    print(f"Failed to read report file '{report_path}': {e}")
                    continue  # Proceed to the next report file

                set_file_name = os.path.splitext(report_file)[0]

                # Initialize variables
                total_net_profit_value = None
                max_consec_losses_count = None
                max_consec_losses_amount = None

                # Extract 'Total Net Profit'
                total_net_profit_label = soup.find('td', string=re.compile(r'Total Net Profit', re.IGNORECASE))
                if total_net_profit_label:
                    total_net_profit_cell = total_net_profit_label.find_next_sibling('td')
                    if total_net_profit_cell:
                        profit_text = total_net_profit_cell.get_text(strip=True)
                        print(f"Extracted Total Net Profit text in {report_file}: '{profit_text}'")
                        # Remove any commas or currency symbols
                        profit_text_clean = re.sub(r'[^\d\.-]', '', profit_text)
                        try:
                            total_net_profit_value = float(profit_text_clean)
                            print(f"Converted Total Net Profit value in {report_file}: {total_net_profit_value}")
                        except ValueError:
                            print(f"Could not convert Total Net Profit value to float in {report_file}")
                    else:
                        print(f"Total Net Profit value not found next to label in {report_file}")
                else:
                    print(f"Total Net Profit label not found in {report_file}")

                # Extract 'Maximum consecutive losses ($):'
                max_consec_losses_label = soup.find('td', string=re.compile(r'Maximum consecutive losses', re.IGNORECASE))
                if max_consec_losses_label:
                    max_consec_losses_cell = max_consec_losses_label.find_next_sibling('td')
                    if max_consec_losses_cell:
                        max_consec_losses_text = max_consec_losses_cell.get_text(strip=True)
                        print(f"Extracted Max Consecutive Losses text in {report_file}: '{max_consec_losses_text}'")
                        # Use regex to extract the count and amount
                        match = re.match(r'(\d+)\s*\(([-\d\s.,]+)\)', max_consec_losses_text)
                        if match:
                            # Extract count
                            max_consec_losses_count = int(match.group(1))
                            # Extract amount and clean it
                            max_consec_losses_amount_text = match.group(2)
                            max_consec_losses_amount_clean = re.sub(r'[^\d\.-]', '', max_consec_losses_amount_text)
                            try:
                                max_consec_losses_amount = float(max_consec_losses_amount_clean)
                                print(f"Extracted Max Consecutive Losses count: {max_consec_losses_count}, amount: {max_consec_losses_amount}")
                            except ValueError:
                                print(f"Could not convert Max Consecutive Losses amount to float in {report_file}")
                                max_consec_losses_amount = None
                        else:
                            print(f"Could not parse Max Consecutive Losses text in {report_file}")
                    else:
                        print(f"Max Consecutive Losses value not found next to label in {report_file}")
                else:
                    print(f"Max Consecutive Losses label not found in {report_file}")

                # Append data to the summary list
                total_net_profit_summary.append({
                    'SetFile': set_file_name,
                    'TotalNetProfit': total_net_profit_value,
                    'MaxConsecutiveLossesCount': max_consec_losses_count,
                    'MaxConsecutiveLossesAmount': max_consec_losses_amount
                })

            # Create a DataFrame for the summary

            summary_df = pd.DataFrame(total_net_profit_summary)
            try:
                if not summary_df.empty:
                    # Remove entries with None or NaN values in 'TotalNetProfit'
                    summary_df = summary_df.dropna(subset=['TotalNetProfit'])
                    # Convert numeric columns to numeric types
                    summary_df['TotalNetProfit'] = pd.to_numeric(summary_df['TotalNetProfit'], errors='coerce')
                    summary_df['MaxConsecutiveLossesCount'] = pd.to_numeric(summary_df['MaxConsecutiveLossesCount'], errors='coerce')
                    summary_df['MaxConsecutiveLossesAmount'] = pd.to_numeric(summary_df['MaxConsecutiveLossesAmount'], errors='coerce')
                    # Sort by 'TotalNetProfit' descending
                    summary_df = summary_df.sort_values(by='TotalNetProfit', ascending=False)
                else:
                    print("No data extracted.")
                    summary_df = pd.DataFrame()
            except:
                print("No data extracted.")
                summary_df = pd.DataFrame()
            # Ensure the directory exists
            output_dir = os.path.dirname(OUTPUT_EXCEL_FILE)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # Write to Excel inside the report folder
            try:
                with pd.ExcelWriter(OUTPUT_EXCEL_FILE, engine='openpyxl') as writer:
                    if not summary_df.empty:
                        summary_df.to_excel(writer, sheet_name='Summary', index=False)
                print(f"Excel file created: {OUTPUT_EXCEL_FILE}")
                print(f"Testing completed!\nExcel file created:\n{OUTPUT_EXCEL_FILE}")

            except Exception as e:
                print(f"Failed to write Excel file '{OUTPUT_EXCEL_FILE}': {e}")
                #messagebox.showerror("Error", f"Failed to write Excel file '{OUTPUT_EXCEL_FILE}': {e}")
            print('chck1')
            # Re-enable the Start Test button and disable Stop Test button
            start_button_full_automation.config(state=tk.NORMAL)
            stop_button_full_automation.config(state=tk.DISABLED)
            print(summary_df)
            print(CUSTOM_REPORT_FOLDER_FULL)
            print('chck2')

            return summary_df, CUSTOM_REPORT_FOLDER_FULL

    except Exception as e:
        print('chck3')
        print(f"An unexpected error occurred: {e}")
        #messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        # Re-enable the Start Test button and disable Stop Test button
        start_button_full_automation.config(state=tk.NORMAL)
        stop_button_full_automation.config(state=tk.DISABLED)
        return None, CUSTOM_REPORT_FOLDER_FULL


def run_full_automation(params, stop_event, progress_var,progress_label, total_set_files, start_button, stop_button):
    def update_progress(value, message):
        progress_var.set(value)
        progress_label.config(text=message)


    log_to_file(params)
    try:
        # Unpack parameters
        MT5_PATH = params['MT5_PATH']
        MT5_DATA_FOLDER = params['MT5_DATA_FOLDER']
        SET_FILES_FOLDER = params['SET_FILES_FOLDER']
        SET_FILE_LIST = params['SET_FILE_LIST']
        CUSTOM_REPORT_FOLDER_BASE = ''
        FROM_DATE = params['FROM_DATE']
        TO_DATE = params['TO_DATE']
        FORWARD_DATE = params['FORWARD_DATE']
        DEPOSIT = params['DEPOSIT']
        LEVERAGE = params['LEVERAGE']
        PERIOD = params['PERIOD']
        EXPERT_ADVISOR = params['EXPERT_ADVISOR']
        EXECUTION_MODE = params['EXECUTION_MODE']
        MODEL = params['MODEL']
        OPTIMIZATION = params['OPTIMIZATION']
        FORWARD_MODE = params['FORWARD_MODE']
        OPTIMIZATION_CRITERION = params['OPTIMIZATION_CRITERION']

        REMOVE_DUPLICATES = params['REMOVE_DUPLICATES']

        CUSTOM_REPORT_FOLDER_NAME_DICT = {}




        # ###########################################################################################
        # ##########################################################################################################
        # ##########################################################################################################
        # progress_step = 0
        # current_progress = 0
        # set_file_folder_CustomReportFolder_dict = {}

        # for SET_FILES_FOLDER in SET_FILE_LIST:
        #     params_creator_oos = {
        #             'MT5_PATH': params['MT5_PATH'],
        #             'MT5_DATA_FOLDER': params['MT5_DATA_FOLDER'],
        #             'SET_FILES_FOLDER': SET_FILES_FOLDER,
        #             'CUSTOM_REPORT_FOLDER_BASE': SET_FILES_FOLDER.split('\\')[-1],
        #             'FROM_DATE': params['FROM_DATE_CREATE_OOS'],
        #             'TO_DATE': params['TO_DATE_CREATE_OOS'],
        #             'DEPOSIT': params['DEPOSIT_CREATE_OOS'],
        #             'LEVERAGE': params['LEVERAGE_CREATE_OOS'],
        #             'PERIOD': params['PERIOD_CREATE_OOS'],
        #             'EXPERT_ADVISOR': params['EXPERT_ADVISOR'],
        #             'EXECUTION_MODE': params['EXECUTION_MODE_CREATE_OOS'],
        #             'MODEL': params['MODEL_CREATE_OOS'],
        #         }
        #     current_progress = current_progress + progress_step

        #     print('---CREATE OOS FULL AUTO processing {SET_FILES_FOLDER}')
        #     update_progress(current_progress, f"initialing run_creator_oos_generator_for_automation..")


        #     print('-running create oos flow')
        #     summary_df , CUSTOM_REPORT_FOLDER_FULL= run_creator_oos_generator_for_automation(params_creator_oos, stop_event, progress_var, progress_label, total_set_files, start_button, stop_button)
        #     print('-create oos flow done')

        #     set_file_folder_CustomReportFolder_dict[SET_FILES_FOLDER] = CUSTOM_REPORT_FOLDER_FULL

        #     print('----------------------------------')
        #     print(CUSTOM_REPORT_FOLDER_FULL)
        #     print(summary_df)


        #     df_filtered = summary_df[summary_df['TotalNetProfit'] > 0 ]

        #     #df_filtered = summary_df

        #     filtered_setfile_list = df_filtered['SetFile'].tolist()
        #     print('filtered')
        #     print(filtered_setfile_list)



        # ####################################################################################################

        # for SET_FILES_FOLDER in SET_FILE_LIST:
        #     set_file_folder_CustomReportFolder_dict


        #     path1_set_files = f'{SET_FILES_FOLDER}\\ADXBB'
        #     CUSTOM_REPORT_FOLDER_FULL =  set_file_folder_CustomReportFolder_dict[SET_FILES_FOLDER]
        #     path2_filtered_set_files = f'{CUSTOM_REPORT_FOLDER_FULL}\\ADXBB'



        #     # List all files in path1_set_files
        #     set_file_list = os.listdir(path1_set_files)


        #     # Ensure the destination directory exists
        #     os.makedirs(path2_filtered_set_files, exist_ok=True)

        #     ADXBB_filtered = f'{CUSTOM_REPORT_FOLDER_FULL}\\ADXBB_Filtered'
        #     os.makedirs(ADXBB_filtered, exist_ok=True)
        #     # Copy files
        #     for file_name in filtered_setfile_list:

        #         file_name = file_name + '.set'

        #         src_file = os.path.join(path1_set_files, file_name)
        #         dst_file = os.path.join(path2_filtered_set_files, file_name)

        #         if os.path.isfile(src_file):  # Ensure it's a file
        #             shutil.copy(src_file, dst_file)


        #         src_file = os.path.join(path1_set_files, file_name)
        #         dst_file2 = os.path.join(ADXBB_filtered, file_name)

        #         if os.path.isfile(src_file):  # Ensure it's a file
        #             shutil.copy(src_file, dst_file2)



        # ######################################################################################################

        # if len(filtered_setfile_list) > 0:
        #     progress_step = 0
        #     for SET_FILES_FOLDER in SET_FILE_LIST:
        #         SET_FILES_FOLDER_base = SET_FILES_FOLDER.split('\\')[-1]

        #         CUSTOM_REPORT_FOLDER_FULL =  set_file_folder_CustomReportFolder_dict[SET_FILES_FOLDER]

        #         print('-')
        #         print('-')
        #         print('-')
        #         print(SET_FILES_FOLDER)
        #         print(CUSTOM_REPORT_FOLDER_FULL)

        #         params_creator_oos = {
        #                 'MT5_PATH': params['MT5_PATH'],
        #                 'MT5_DATA_FOLDER': params['MT5_DATA_FOLDER'],
        #                 'SET_FILES_FOLDER': CUSTOM_REPORT_FOLDER_FULL,
        #                 'CUSTOM_REPORT_FOLDER_BASE': SET_FILES_FOLDER_base + "\\" + CUSTOM_REPORT_FOLDER_FULL.split('\\')[-1],
        #                 'FROM_DATE': params['FROM_DATE'],
        #                 'TO_DATE': params['TO_DATE_CREATE_OOS'],
        #                 'DEPOSIT': params['DEPOSIT_CREATE_OOS'],
        #                 'LEVERAGE': params['LEVERAGE_CREATE_OOS'],
        #                 'PERIOD': params['PERIOD_CREATE_OOS'],
        #                 'EXPERT_ADVISOR': params['EXPERT_ADVISOR'],
        #                 'EXECUTION_MODE': params['EXECUTION_MODE_CREATE_OOS'],
        #                 'MODEL': params['MODEL_CREATE_OOS'],
        #             }
        #         current_progress = current_progress + progress_step

        #         print('---CREATE OOS FULL AUTO processing {SET_FILES_FOLDER}')
        #         update_progress(current_progress, f"initialing run_creator_oos_generator_for_automation..")

        #         print('-running create oos flow2')
        #         summary_df , CUSTOM_REPORT_FOLDER_FULL= run_creator_oos_generator_for_automation(params_creator_oos, stop_event, progress_var, progress_label, total_set_files, start_button, stop_button)


        #         # Source folder path
        #         source_folder = CUSTOM_REPORT_FOLDER_FULL

        #         # Destination path
        #         destination_path = SET_FILES_FOLDER

        #         # Move the folder
        #         try:
        #             shutil.move(source_folder, destination_path)
        #             print(f"Folder moved from {source_folder} to {destination_path}")
        #         except FileNotFoundError as e:
        #             print(f"Error: {e}")
        #         except PermissionError as e:
        #             print(f"Permission Error: {e}")
        #         except Exception as e:
        #             print(f"An error occurred: {e}")


        #         # Current folder name

        #         CUSTOM_REPORT_FOLDER_moved = CUSTOM_REPORT_FOLDER_FULL.split('\\')[-1]
        #         current_folder = f"{SET_FILES_FOLDER}\\{CUSTOM_REPORT_FOLDER_moved}"

        #         # New folder name
        #         new_folder = f"{SET_FILES_FOLDER}\\{CUSTOM_REPORT_FOLDER_moved}_OOS Filtered Report"

        #         try:
        #             # Rename the folder
        #             os.rename(current_folder, new_folder)
        #             print(f"Folder renamed from {current_folder} to {new_folder}")
        #         except FileNotFoundError as e:
        #             print(f"Error: The folder does not exist. {e}")
        #         except FileExistsError as e:
        #             print(f"Error: The new folder name already exists. {e}")
        #         except PermissionError as e:
        #             print(f"Permission Error: {e}")
        #         except Exception as e:
        #             print(f"An unexpected error occurred: {e}")


        #         print('-create oos flow2 done')

        #         print(summary_df)
        # return
        # ##########################################################################################################
        # ##########################################################################################################
        # ##########################################################################################################
        # ##########################################################################################################
        # ##########################################################################################################

        for SET_FILES_FOLDER in SET_FILE_LIST:


            # Create a timestamped report folder (relative path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            CUSTOM_REPORT_FOLDER_NAME = f"backtester_report_{timestamp}"

            CUSTOM_REPORT_FOLDER_NAME_DICT[SET_FILES_FOLDER] = CUSTOM_REPORT_FOLDER_NAME

            CUSTOM_REPORT_FOLDER_BASE = SET_FILES_FOLDER.split('\\')[-1]
            print('----####')
            print(CUSTOM_REPORT_FOLDER_BASE)
            # Relative path from MT5_DATA_FOLDER
            CUSTOM_REPORT_FOLDER_RELATIVE = os.path.join(CUSTOM_REPORT_FOLDER_BASE, CUSTOM_REPORT_FOLDER_NAME)
            CUSTOM_REPORT_FOLDER_FULL = os.path.join(MT5_DATA_FOLDER, CUSTOM_REPORT_FOLDER_RELATIVE)
            os.makedirs(CUSTOM_REPORT_FOLDER_FULL, exist_ok=True)
            print(f"Created report folder: {CUSTOM_REPORT_FOLDER_FULL}")




            print('----####')
            print(SET_FILES_FOLDER)
            MT5_PROFILES_TESTER = os.path.join(MT5_DATA_FOLDER, r"MQL5\Profiles\Tester")
            # Ensure MT5 Profiles Tester folder exists
            os.makedirs(MT5_PROFILES_TESTER, exist_ok=True)

            # Check for .set files
            set_files = [f for f in os.listdir(SET_FILES_FOLDER) if f.endswith('.set')]
            if not set_files:
                print(f"No .set files found in '{SET_FILES_FOLDER}'")
                #messagebox.showerror("Error", f"No .set files found in '{SET_FILES_FOLDER}'")
                # Re-enable the Start Test button and disable Stop Test button
                start_button.config(state=tk.NORMAL)
                stop_button.config(state=tk.DISABLED)

                continue

            total_files = len(set_files)
            progress_step = 100 / total_files  # For progress bar increment

            # Initialize progress
            progress_var.set(0)
            current_progress = 0

            update_progress(current_progress, 'Full Automation.. Initializing.')

            # Backtesting Automation
            for index, set_file in enumerate(set_files):
                if stop_event.is_set():
                    print("Backtesting stopped by user.")
                    messagebox.showinfo("Stopped", "Backtesting stopped by user.")
                    # Re-enable the Start Test button and disable Stop Test button
                    start_button.config(state=tk.NORMAL)
                    stop_button.config(state=tk.DISABLED)
                    return

                print(f"\nProcessing set file: {set_file}")
                update_progress(current_progress, f"\nProcessing set file: {set_file}")
                SET_FILE_NAME = os.path.splitext(set_file)[0]

                # Extract symbol from the set file name
                symbol = extract_symbol_from_set_filename(SET_FILE_NAME)
                if not symbol:
                    print(f"Could not extract symbol from set file '{set_file}'. Skipping.")
                    continue

                print(f"Extracted symbol '{symbol}' from set file.")

                # Copy the .set file using shutil.copy for reliability
                src_set_file = os.path.join(SET_FILES_FOLDER, set_file)
                dest_set_file = os.path.join(MT5_PROFILES_TESTER, set_file)
                try:
                    shutil.copy(src_set_file, dest_set_file)
                    print(f"Copied '{set_file}' to '{MT5_PROFILES_TESTER}'")
                except Exception as e:
                    print(f"Failed to copy '{set_file}': {e}")
                    messagebox.showerror("Error", f"Failed to copy '{set_file}': {e}")
                    continue  # Proceed to the next .set file

                # Generate the .ini file
                INI_FILE = os.path.join(MT5_DATA_FOLDER, f"temp_{SET_FILE_NAME}.ini")
                report_filename = SET_FILE_NAME  # Do not add any extension
                # Report path relative to MT5_DATA_FOLDER
                report_path_relative = os.path.join(CUSTOM_REPORT_FOLDER_BASE, CUSTOM_REPORT_FOLDER_NAME, report_filename)
                # Ensure backslashes are correctly formatted
                report_path_relative = report_path_relative.replace('/', '\\')

                with open(INI_FILE, 'w') as ini_file:
                    ini_file.write("; start strategy tester\n")
                    ini_file.write("[Tester]\n")
                    ini_file.write(f"Expert={EXPERT_ADVISOR}\n")
                    ini_file.write(f"ExpertParameters={set_file}\n")
                    ini_file.write(f"Symbol={symbol}\n")
                    ini_file.write(f"Period={PERIOD}\n")
                    ini_file.write(f"Model={MODEL}\n")
                    ini_file.write(f"ExecutionMode={EXECUTION_MODE}\n")
                    ini_file.write(f"Optimization={OPTIMIZATION}\n")
                    ini_file.write(f"OptimizationCriterion={OPTIMIZATION_CRITERION}\n")
                    ini_file.write(f"ForwardMode={FORWARD_MODE}\n")
                    ini_file.write(f"ForwardDate={FORWARD_DATE}\n")
                    ini_file.write("DateEnable=true\n")
                    ini_file.write(f"FromDate={FROM_DATE}\n")
                    ini_file.write(f"ToDate={TO_DATE}\n")
                    # Use relative report path, without quotes
                    ini_file.write(f"Report={report_path_relative}\n")
                    ini_file.write("ReplaceReport=true\n")
                    ini_file.write(f"Deposit={DEPOSIT}\n")
                    ini_file.write(f"Leverage={LEVERAGE}\n")
                    # Do not specify ReportFormat

                print(f"Generated .ini file at '{INI_FILE}' with Report path '{report_path_relative}'")

                # Ensure MT5 is not running
                print("Ensuring no previous MT5 instances are running...")
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] and proc.info['name'].lower() == 'terminal64.exe':
                        proc.kill()
                        print(f"Killed process {proc.pid} ({proc.info['name']})")
                print("Waiting for MT5 to fully close...")
                time.sleep(5)

                if stop_event.is_set():
                    print("Backtesting stopped by user.")
                    messagebox.showinfo("Stopped", "Backtesting stopped by user.")
                    # Re-enable the Start Test button and disable Stop Test button
                    start_button.config(state=tk.NORMAL)
                    stop_button.config(state=tk.DISABLED)
                    return

                # Start MT5
                print(f"Starting MT5 with config '{INI_FILE}'")
                try:
                    mt5_process = subprocess.Popen([MT5_PATH, f"/config:{INI_FILE}"])
                    print(f"Started MT5 process with PID {mt5_process.pid}")
                except Exception as e:
                    print(f"Failed to start MT5: {e}")
                    messagebox.showerror("Error", f"Failed to start MT5: {e}")
                    continue  # Proceed to the next .set file

                # Wait for any file to be created in the report folder
                max_wait_seconds = 7200  # 2 hours
                wait_counter = 0
                report_exists = False
                print("Waiting for report file to be created...")

                # Full path to the report folder
                report_folder_full_path = os.path.join(MT5_DATA_FOLDER, os.path.dirname(report_path_relative))

                # Initial list of files in the report folder
                initial_files = set(os.listdir(report_folder_full_path))

                while wait_counter < max_wait_seconds:
                    if stop_event.is_set():
                        print("Backtesting stopped by user.")
                        mt5_process.kill()
                        messagebox.showinfo("Stopped", "Backtesting stopped by user.")
                        # Re-enable the Start Test button and disable Stop Test button
                        start_button.config(state=tk.NORMAL)
                        stop_button.config(state=tk.DISABLED)
                        return

                    # Get the current list of files
                    current_files = set(os.listdir(report_folder_full_path))
                    # Check for new files
                    new_files = current_files - initial_files
                    if new_files:
                        report_exists = True
                        print(f"Report file(s) created: {new_files}")
                        break

                    time.sleep(5)
                    wait_counter += 5
                    print(f"Waited {wait_counter} seconds for report file to be created...")

                if not report_exists:
                    print("Report file was not created within expected time. Forcing MT5 to close...")
                    mt5_process.kill()
                    messagebox.showerror("Error", f"Report file was not created for '{set_file}'.")
                    continue  # Proceed to the next .set file

                # Close MT5
                print("Closing MT5...")
                mt5_process.kill()
                print("MT5 closed.")

                # Delete the .ini file
                if os.path.exists(INI_FILE):
                    os.remove(INI_FILE)
                    print(f"Deleted temporary .ini file '{INI_FILE}'")

                # Update progress bar
                current_progress += progress_step

                update_progress(current_progress, 'Running Backtester flow.')

                # Wait before starting the next test
                print("Waiting before starting the next test...")
                time.sleep(5)

        # After all backtests are done
        if not stop_event.is_set():
            print("All backtests are completed.")


            progress_var.set(100)
            update_progress(current_progress, "All backtests are completed.")
            #messagebox.showinfo("Success", f"Testing completed!\nReports are saved in:\n{CUSTOM_REPORT_FOLDER_FULL}")
            # Re-enable the Start Test button and disable Stop Test button

            ######################################################################################################################################## HERE IS THE CREATORXML AUTOMATION
            print('..initializing creatorxml')

            current_progress = 0
            progress_step = 0
            update_progress(current_progress, "All backtests are completed.")





            BALANCE = params['CREATORXML_PARAM1_BALANCE']
            TARGET_DRAWDOWN = params['CREATORXML_PARAM2_TARGET_DRAWDOWN']
            MIN_TOT_EST_PROFIT = params['CREATORXML_PARAM3_MIN_TOT_EST_PROFIT']

            CHECKBOX_SELECTION = params['CHECKBOX_SELECTION']

            CHECKBOX_SELECTION_TOTESTPROF = params['CHECKBOX_SELECTION_TOTESTPROF']
            CHECKBOX_SELECTION_MAXORIGDD = params['CHECKBOX_SELECTION_MAXORIGDD']
            CHECKBOX_SELECTION_TRADES_FILTER = params["CHECKBOX_SELECTION_TRADES_FILTER"]
            CHECKBOX_SELECTION_TOTESTPROF_GR_TOTESTDD = params["CHECKBOX_SELECTION_TOTESTPROF_GR_TOTESTDD"]



            MAX_ORIGINAL_DD_VALUE = params['MAX_ORIGINAL_DD_VALUE']
            TOTAL_EST_PROF_VALUE = params['TOTAL_EST_PROF_VALUE']
            TRADES_FILTER_VALUE = params['TRADES_FILTER_VALUE']

            print('------------- creatorxml PARAMS ------------------')
            print(BALANCE)
            print(TARGET_DRAWDOWN)
            #print(MIN_TOT_EST_PROFIT)
            print('------------- creatorxml PARAMS ------------------')
            app = QApplication(sys.argv)
            window = CSVProcessorApp_for_auto()
            for SET_FILES_FOLDER in SET_FILE_LIST:

                print('------------- CREATORXML LOOPING')

                input_folder_path = SET_FILES_FOLDER + "\\"
                backtester_report_folder_path = input_folder_path + CUSTOM_REPORT_FOLDER_NAME_DICT[SET_FILES_FOLDER] + '\\'
                fileSets_list = create_filesets_list(input_folder_path, backtester_report_folder_path)

                print(input_folder_path)
                print(backtester_report_folder_path)
                print(fileSets_list)

                if len(fileSets_list) == 0:
                    progress_step =  100/ 1
                else:
                    if len(fileSets_list) == 0:
                        progress_step =  100/ len(fileSets_list)



                for file in fileSets_list:
                    print('creating CSVProcessorApp_for_auto instance-----------')

                    print('-'*80)
                    current_progress = current_progress + progress_step
                    update_progress(current_progress, f"creatorxml processing {file}")

                    window.forward_file_path = file[0]
                    window.backward_file_path = file[1]
                    window.set_file_path = file[2]

                    window.balance = BALANCE
                    window.drawdown = TARGET_DRAWDOWN
                    ################################
                    window.browse_forward_file(window.forward_file_path)
                    window.browse_backward_file(window.backward_file_path)
                    window.browse_set_files(window.set_file_path)

                    window.process_files(True)
                    print('len of full_data ' + str(len(window.full_data)))
                    print('-removing duplicates')




                    if REMOVE_DUPLICATES:
                        window.remove_duplicates()
                        print('---remove_duplicates()')

                    window.full_data.to_csv('fullData_rmDups.csv', index=False)
                    print('len of full_data ' + str(len(window.full_data)))




                    window.qualifying_data = window.full_data.copy()

                    if CHECKBOX_SELECTION_MAXORIGDD:
                        print('action - download_all_below_max_dd')
                        window.download_all_below_max_dd(MAX_ORIGINAL_DD_VALUE)
                    if CHECKBOX_SELECTION_TOTESTPROF:
                        print('action - download_all_above_profit')
                        window.download_all_above_profit(TOTAL_EST_PROF_VALUE)
                    if CHECKBOX_SELECTION_TRADES_FILTER:
                        window.download_all_profit_greater_than_dd_and_trades(TRADES_FILTER_VALUE)
                    if CHECKBOX_SELECTION_TOTESTPROF_GR_TOTESTDD:
                        window.download_all_profit_greater_than_dd()


                    window.download_qualifying_set_files(window.qualifying_data)


                    # sys.exit(app.exec_())
                    time.sleep(1)
                    print('- CREATORXML DONE'*30)
            ####################################################################### CREATE OOS FULL AUTO
            current_progress = 0

            ###########################################################################################
            ##########################################################################################################
            ##########################################################################################################
            set_file_folder_CustomReportFolder_dict = {}

            for SET_FILES_FOLDER in SET_FILE_LIST:
                print('1 oos flow loop')

                params_creator_oos = {
                        'MT5_PATH': params['MT5_PATH'],
                        'MT5_DATA_FOLDER': params['MT5_DATA_FOLDER'],
                        'SET_FILES_FOLDER': SET_FILES_FOLDER,
                        'CUSTOM_REPORT_FOLDER_BASE': SET_FILES_FOLDER.split('\\')[-1],
                        'FROM_DATE': params['FROM_DATE_CREATE_OOS'],
                        'TO_DATE': params['TO_DATE_CREATE_OOS'],
                        'DEPOSIT': params['DEPOSIT_CREATE_OOS'],
                        'LEVERAGE': params['LEVERAGE_CREATE_OOS'],
                        'PERIOD': params['PERIOD_CREATE_OOS'],
                        'EXPERT_ADVISOR': params['EXPERT_ADVISOR'],
                        'EXECUTION_MODE': params['EXECUTION_MODE_CREATE_OOS'],
                        'MODEL': params['MODEL_CREATE_OOS'],
                    }
                current_progress = current_progress + progress_step
                
                log_to_file(params_creator_oos)

                print('---CREATE OOS FULL AUTO processing {SET_FILES_FOLDER}')
                update_progress(current_progress, f"initialing run_creator_oos_generator_for_automation..")


                print('-running create oos flow')
                summary_df , CUSTOM_REPORT_FOLDER_FULL= run_creator_oos_generator_for_automation(params_creator_oos, stop_event, progress_var, progress_label, total_set_files, start_button, stop_button)
                print(SET_FILE_LIST)
                try:
                    if summary_df == None:
                        print('- summary_df is None - continuing')
                        continue
                except:
                    print("summary_df 'None' erroe")
                    try:
                        if summary_df.empty:
                            print('- summary_df is empty - continuing')
                            continue
                    except:
                        print("- summary_df 'empty' error")
                        pass
                print('-create oos flow done')

                set_file_folder_CustomReportFolder_dict[SET_FILES_FOLDER] = CUSTOM_REPORT_FOLDER_FULL

                print('----------------------------------')
                print(CUSTOM_REPORT_FOLDER_FULL)
                print(summary_df)


                df_filtered = summary_df[summary_df['TotalNetProfit'] > 0 ]

                #df_filtered = summary_df

                filtered_setfile_list = df_filtered['SetFile'].tolist()
                print('filtered')
                print(filtered_setfile_list)



            ####################################################################################################

            for SET_FILES_FOLDER in SET_FILE_LIST:
                #set_file_folder_CustomReportFolder_dict


                path1_set_files = f'{SET_FILES_FOLDER}\\ADXBB'
                CUSTOM_REPORT_FOLDER_FULL =  set_file_folder_CustomReportFolder_dict[SET_FILES_FOLDER]
                path2_filtered_set_files = f'{CUSTOM_REPORT_FOLDER_FULL}\\ADXBB'



                # List all files in path1_set_files
                set_file_list = os.listdir(path1_set_files)


                # Ensure the destination directory exists
                os.makedirs(path2_filtered_set_files, exist_ok=True)

                ADXBB_filtered = f'{CUSTOM_REPORT_FOLDER_FULL}\\ADXBB_Filtered'
                os.makedirs(ADXBB_filtered, exist_ok=True)
                # Copy files
                for file_name in filtered_setfile_list:

                    file_name = file_name + '.set'

                    src_file = os.path.join(path1_set_files, file_name)
                    dst_file = os.path.join(path2_filtered_set_files, file_name)

                    if os.path.isfile(src_file):  # Ensure it's a file
                        shutil.copy(src_file, dst_file)


                    src_file = os.path.join(path1_set_files, file_name)
                    dst_file2 = os.path.join(ADXBB_filtered, file_name)

                    if os.path.isfile(src_file):  # Ensure it's a file
                        shutil.copy(src_file, dst_file2)



            ###################################################################################################### 2nd oos

            if len(filtered_setfile_list) > 0:
                progress_step = 0
                for SET_FILES_FOLDER in SET_FILE_LIST:
                    print('2 oos flow loop')
                    SET_FILES_FOLDER_base =  os.path.basename(SET_FILES_FOLDER) #SET_FILES_FOLDER.split('\\')[-1]
                    print('1-!!!!!')
                    CUSTOM_REPORT_FOLDER_FULL =  set_file_folder_CustomReportFolder_dict[SET_FILES_FOLDER]
                    CUSTOM_REPORT_FOLDER_FULL_base = os.path.basename(CUSTOM_REPORT_FOLDER_FULL)

                    print('-')
                    print('-')
                    print('-')
                    print(SET_FILES_FOLDER)
                    print(CUSTOM_REPORT_FOLDER_FULL)
                    print('2-!!!!!')

                    params_creator_oos = {
                            'MT5_PATH': params['MT5_PATH'],
                            'MT5_DATA_FOLDER': params['MT5_DATA_FOLDER'],
                            'SET_FILES_FOLDER': CUSTOM_REPORT_FOLDER_FULL,
                            'CUSTOM_REPORT_FOLDER_BASE': SET_FILES_FOLDER_base + "\\" + CUSTOM_REPORT_FOLDER_FULL_base,
                            'FROM_DATE': params['FROM_DATE'],
                            'TO_DATE': params['TO_DATE_CREATE_OOS'],
                            'DEPOSIT': params['DEPOSIT_CREATE_OOS'],
                            'LEVERAGE': params['LEVERAGE_CREATE_OOS'],
                            'PERIOD': params['PERIOD_CREATE_OOS'],
                            'EXPERT_ADVISOR': params['EXPERT_ADVISOR'],
                            'EXECUTION_MODE': params['EXECUTION_MODE_CREATE_OOS'],
                            'MODEL': params['MODEL_CREATE_OOS'],
                        }
                    print('3-!!!!!')
                    current_progress = current_progress + progress_step

                    print('---CREATE OOS FULL AUTO processing {SET_FILES_FOLDER}')
                    update_progress(current_progress, f"initialing run_creator_oos_generator_for_automation..")

                    print('-running create oos flow2')
                    summary_df , CUSTOM_REPORT_FOLDER_FULL= run_creator_oos_generator_for_automation(params_creator_oos, stop_event, progress_var, progress_label, total_set_files, start_button, stop_button)
                    try:
                        if summary_df == None:
                            print('- summary_df is None - continuing')
                            continue
                    except:
                        print("summary_df 'None' erroe")
                        try:
                            if summary_df.empty:
                                print('- summary_df is empty - continuing')
                                continue
                        except:
                            print("- summary_df 'empty' error")
                            pass

                    print('pass 1')
                    # Source folder path

                    source_folder = CUSTOM_REPORT_FOLDER_FULL

                    # Destination path
                    destination_path = SET_FILES_FOLDER


                    print('pass 2')
                    # Move the folder
                    try:
                        shutil.move(source_folder, destination_path)
                        print(f"Folder moved from {source_folder} to {destination_path}")
                    except FileNotFoundError as e:
                        print(f"Error: {e}")
                    except PermissionError as e:
                        print(f"Permission Error: {e}")
                    except Exception as e:
                        print(f"An error occurred: {e}")

                    print('pass 3')
                    # Current folder name

                    # CUSTOM_REPORT_FOLDER_moved = CUSTOM_REPORT_FOLDER_FULL.split('\\')[-1]
                    # current_folder = f"{SET_FILES_FOLDER}\\{CUSTOM_REPORT_FOLDER_moved}"

                    # # New folder name
                    # new_folder = f"{SET_FILES_FOLDER}\\{CUSTOM_REPORT_FOLDER_moved}_OOS Filtered Report"

                    ###########################



                    # Extracting the current folder name
                    CUSTOM_REPORT_FOLDER_moved = os.path.basename(CUSTOM_REPORT_FOLDER_FULL)
                    print('pass 4')
                    # Defining the current folder path
                    current_folder = os.path.join(SET_FILES_FOLDER, CUSTOM_REPORT_FOLDER_moved)
                    print('pass 5')

                    # Constructing the new folder name
                    new_folder = os.path.join(SET_FILES_FOLDER, f"{CUSTOM_REPORT_FOLDER_moved}_OOS Filtered Report")
                    print('pass 6')



                    try:
                        # Rename the folder
                        os.rename(current_folder, new_folder)
                        print(f"Folder renamed from {current_folder} to {new_folder}")
                    except FileNotFoundError as e:
                        print(f"Error: The folder does not exist. {e}")
                    except FileExistsError as e:
                        print(f"Error: The new folder name already exists. {e}")
                    except PermissionError as e:
                        print(f"Permission Error: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                    except:
                        print(f'error renaming {current_folder}')
                        print(f"current folder is : {current_folder}")
                        print(f"new folder is : {new_folder}")

                    print('-create oos flow2 done')

                    print(summary_df)

            else:
                print('2nd oos filtered filelist has len of 0')
            #return
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            print('2nd oos completed')



            current_progress = 100
            update_progress(current_progress, f"COMPLETED")

            print('-'*80)

            ########################################################################################################################################

            start_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        # Re-enable the Start Test button and disable Stop Test button
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        return

# ---------------------------------
# Application Initialization
# ---------------------------------

def initialize_application():
    # Check the license before starting the main application
    if check_license_key():
        create_gui()
        root.mainloop()
    else:
        sys.exit()

# ---------------------------------
# GUI Setup
# ---------------------------------

def create_gui():
    global root
    root = tk.Tk()
    root.title("MetaTrader 5 Automation Tool")





    # Set the window icon using both iconbitmap and iconphoto
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        try:
            # Set iconbitmap for window title bar
            root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Failed to set window iconbitmap: {e}")

        try:
            # Set iconphoto for better compatibility, especially for taskbar
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Failed to set window iconphoto: {e}")
    else:
        print(f"Icon file not found at {icon_path}")

    # Set the AppUserModelID to ensure the taskbar uses the correct icon
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"mycompany.myproduct.subproduct.version")
        except Exception as e:
            print(f"Failed to set AppUserModelID: {e}")

    # Create menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)


    root.geometry("800x600+0+0")

    # Menus for Creator OOS Generator and Backtester
    # creator_menu = tk.Menu(menu_bar, tearoff=0)
    # menu_bar.add_cascade(label="Creator OOS Generator", menu=creator_menu)

    # backtester_menu = tk.Menu(menu_bar, tearoff=0)
    # menu_bar.add_cascade(label="Backtester", menu=backtester_menu)

    full_automation_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Full Automation", menu=full_automation_menu)

    # DDAnalyzer_menu = tk.Menu(menu_bar, tearoff=0)
    # menu_bar.add_cascade(label="DDAnalyzer", menu=DDAnalyzer_menu)

    # CreatorXML_menu = tk.Menu(menu_bar, tearoff=0)
    # menu_bar.add_cascade(label="CreatorXML", menu=CreatorXML_menu)

    # Placeholder functions for saving settings (to be defined later)

    # Create notebook (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # # Create frames for each tab
    # creator_frame = tk.Frame(notebook)
    # backtester_frame = tk.Frame(notebook)
    # full_automation_frame = tk.Frame(notebook)
    # #dd_analyzer_frame = tk.Frame(notebook)
    # creaorxml_frame = tk.Frame(notebook)

    # notebook.add(creator_frame, text='Creator OOS Generator')
    # notebook.add(backtester_frame, text='Backtester')
    # notebook.add(full_automation_frame, text='Full Automation')
    # #notebook.add(dd_analyzer_frame, text='DDAnalyzer')
    # notebook.add(creaorxml_frame, text='CreatorXML')

    def create_scrollable_frame(notebook, tab_name):
        """Create a scrollable frame for a notebook tab with both horizontal and vertical scrollbars."""
        container = tk.Frame(notebook)
        canvas = tk.Canvas(container)
        v_scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        h_scrollbar = tk.Scrollbar(container, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollable_frame = tk.Frame(canvas)

        # Configure the canvas for scrolling
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Function to dynamically set the length of the horizontal scrollbar
        # def update_scrollbar_length(event=None):
        #     window_width = container.winfo_width()
        #     h_scrollbar.configure(width=window_width // 2)

        def update_scrollbar_length(event=None):
            window_width = container.winfo_width()  # Get the container's width
            h_scrollbar.place(x=0, y=container.winfo_height() - 20, width=window_width // 2)  # Set length


        # Update scroll region when the frame content changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", on_frame_configure)
        container.bind("<Configure>", update_scrollbar_length)  # Update scrollbar length on window resize

        # Pack the widgets
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM)  # The length will now adjust dynamically

        # Add to notebook
        container.pack(fill=tk.BOTH, expand=True)
        notebook.add(container, text=tab_name)

        return scrollable_frame

    # Create scrollable frames for each tab
    #creator_frame = create_scrollable_frame(notebook, "Creator OOS Generator")
    #backtester_frame = create_scrollable_frame(notebook, "Backtester")
    full_automation_frame = create_scrollable_frame(notebook, "Full Automation")
    #creatorxml_frame = create_scrollable_frame(notebook, "CreatorXML")

    # Variables specific to Creator OOS Generator
    # mt5_path_var_creator = tk.StringVar(value=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    # mt5_data_folder_var_creator = tk.StringVar(value=os.path.expanduser(r"C:\Users\Admin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"))
    # set_files_folder_var_creator = tk.StringVar(value=os.path.join(mt5_data_folder_var_creator.get(), r""))
    # custom_report_folder_base_var_creator = tk.StringVar(value="custom_reports")
    # from_date_var_creator = tk.StringVar(value="2019.01.01")
    # to_date_var_creator = tk.StringVar(value="2020.01.01")
    # deposit_var_creator = tk.StringVar(value="100000")
    # leverage_var_creator = tk.StringVar(value="100")
    # period_var_creator = tk.StringVar(value="M1")
    # model_var_creator = tk.StringVar(value="4")
    # expert_advisor_var_creator = tk.StringVar(value="creator11-4_v03.ex5")
    # execution_mode_var_creator = tk.StringVar(value="100")

    # Variables specific to Backtester
    # mt5_path_var_backtester = tk.StringVar(value=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    # mt5_data_folder_var_backtester = tk.StringVar(value=os.path.expanduser(r"C:\Users\Admin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"))
    # set_files_folder_var_backtester = tk.StringVar(value=os.path.join(mt5_data_folder_var_backtester.get(), r""))
    # custom_report_folder_base_var_backtester = tk.StringVar(value="custom_reports")
    # from_date_var_backtester = tk.StringVar(value="2019.01.01")
    # to_date_var_backtester = tk.StringVar(value="2020.01.01")
    # forward_date_var_backtester = tk.StringVar(value="2021.01.01")
    # deposit_var_backtester = tk.StringVar(value="100000")
    # leverage_var_backtester = tk.StringVar(value="100")
    # period_var_backtester = tk.StringVar(value="M1")
    # model_var_backtester = tk.StringVar(value="4")
    # expert_advisor_var_backtester = tk.StringVar(value="creator11-4_v03.ex5")
    # execution_mode_var_backtester = tk.StringVar(value="100")
    # optimization_var_backtester = tk.StringVar(value="0 - Optimization disabled")
    # forward_mode_var_backtester = tk.StringVar(value="0 - Off")
    # optimization_criterion_var_backtester = tk.StringVar(value="0 - Balance Max")

    # Variables specific to full auto

    set_file_list = []

    mt5_path_var_full_automation = tk.StringVar(value=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    mt5_data_folder_var_full_automation = tk.StringVar(value=os.path.expanduser(r"C:\Users\Admin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"))
    set_files_folder_var_full_automation = tk.StringVar(value=os.path.join(mt5_data_folder_var_full_automation.get(), r""))




    custom_report_folder_base_var_full_automation = tk.StringVar(value="custom_reports")
    from_date_var_full_automation = tk.StringVar(value="2024.08.14")
    to_date_var_full_automation = tk.StringVar(value="2024.11.03")
    forward_date_var_full_automation = tk.StringVar(value="")
    deposit_var_full_automation = tk.StringVar(value="100000")
    leverage_var_full_automation = tk.StringVar(value="100")
    period_var_full_automation = tk.StringVar(value="M1")
    model_var_full_automation = tk.StringVar(value="1")
    expert_advisor_var_full_automation = tk.StringVar(value="creator11-4_v03.ex5")
    execution_mode_var_full_automation = tk.StringVar(value="100")
    optimization_var_full_automation = tk.StringVar(value="2 - Fast genetic based algorithm")
    forward_mode_var_full_automation = tk.StringVar(value="1 - 1/2 of the testing period")
    optimization_criterion_var_full_automation = tk.StringVar(value="0 - Balance Max")


    creator_xml_var_full_automation_1 = tk.StringVar(value="100000")
    creator_xml_var_full_automation_2 = tk.StringVar(value="1000")
    creator_xml_var_full_automation_3 = tk.StringVar(value="2000")
    # Use a StringVar to control the checkboxes
    checkbox_selection = tk.StringVar(value='maxOriginalDd')
    creator_xml_var_full_automation_maxOriginalDd_value = tk.StringVar(value="4000")
    creator_xml_var_full_automation_totalEstimatedProfit_value = tk.StringVar(value="2000")
    creator_xml_var_full_automation_TRADES_value = tk.StringVar(value="12")

    # mt5_path_var_full_automation_create_oos = tk.StringVar(value=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    # mt5_data_folder_var_full_automation_create_oos = tk.StringVar(value=os.path.expanduser(r"C:\Users\Admin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"))
    # set_files_folder_var_full_automation_create_oos = set_files_folder_var_full_automation
    # custom_report_folder_base_var_full_automation_create_oos = tk.StringVar(value="custom_reports")
    from_date_var_full_automation_create_oos = tk.StringVar(value="")
    to_date_var_full_automation_create_oos = tk.StringVar(value="")
    deposit_var_full_automation_create_oos = tk.StringVar(value="100000")
    leverage_var_full_automation_create_oos = tk.StringVar(value="100")
    period_var_full_automation_create_oos = tk.StringVar(value="M1")
    model_var_full_automation_create_oos = tk.StringVar(value="4")

    execution_mode_var_full_automation_create_oos = tk.StringVar(value="100")




    # Functions to browse for paths for Creator OOS Generator
    # def browse_mt5_path_creator():
    #     path = filedialog.askopenfilename(title="Select MT5 Terminal", filetypes=[("Executable Files", "*.exe")])
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         mt5_path_var_creator.set(normalized_path)

    # def browse_mt5_data_folder_creator():
    #     path = filedialog.askdirectory(title="Select MT5 Data Folder")
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         mt5_data_folder_var_creator.set(normalized_path)

    #         # Update Set Files Folder default path based on new Data Folder
    #         #set_files_folder_var_creator.set(os.path.join(path, r"new stuff\set files"))
    #         set_files_folder_var_creator.set(os.path.normpath(os.path.join(normalized_path, r"new stuff\set files")))

    # def browse_set_files_folder_creator():
    #     path = filedialog.askdirectory(title="Select Set Files Folder")
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         set_files_folder_var_creator.set(normalized_path)

    # def browse_set_files_folder_creator_for_oos():
    #     path = filedialog.askdirectory(title="Select Set Files Folder")
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         set_files_folder_var_creator.set(normalized_path)

    # def browse_expert_advisor_creator():
    #     path = filedialog.askopenfilename(title="Select Expert Advisor File", filetypes=[("EA Files", "*.ex5;*.ex4")])
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         expert_advisor_var_creator.set(os.path.basename(normalized_path))

    # Functions to browse for paths for Backtester
    # def browse_mt5_path_backtester():
    #     path = filedialog.askopenfilename(title="Select MT5 Terminal", filetypes=[("Executable Files", "*.exe")])
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         mt5_path_var_backtester.set(normalized_path)

    # def browse_mt5_data_folder_backtester():
    #     path = filedialog.askdirectory(title="Select MT5 Data Folder")
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         mt5_data_folder_var_backtester.set(normalized_path)
    #         # Update Set Files Folder default path based on new Data Folder
    #         #set_files_folder_var_backtester.set(os.path.join(path, r"new stuff\set files"))
    #         set_files_folder_var_backtester.set(os.path.normpath(os.path.join(normalized_path, r"new stuff\set files")))

    # def browse_set_files_folder_backtester():
    #     path = filedialog.askdirectory(title="Select Set Files Folder")
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         set_files_folder_var_backtester.set(normalized_path)

    # def browse_expert_advisor_backtester():
    #     path = filedialog.askopenfilename(title="Select Expert Advisor File", filetypes=[("EA Files", "*.ex5;*.ex4")])
    #     if path:
    #         normalized_path = os.path.normpath(path)
    #         expert_advisor_var_backtester.set(os.path.basename(normalized_path))
    #

    # Functions to browse for paths for full_automation
    def browse_mt5_path_full_automation():
        path = filedialog.askopenfilename(title="Select MT5 Terminal", filetypes=[("Executable Files", "*.exe")])
        if path:
            normalized_path = os.path.normpath(path)
            mt5_path_var_full_automation.set(normalized_path)

    def browse_mt5_data_folder_full_automation():
        path = filedialog.askdirectory(title="Select MT5 Data Folder")
        if path:
            normalized_path = os.path.normpath(path)
            mt5_data_folder_var_full_automation.set(normalized_path)
            # Update Set Files Folder default path based on new Data Folder
            #set_files_folder_var_full_automation.set(os.path.join(path, r"new stuff\set files"))
            set_files_folder_var_full_automation.set(os.path.normpath(os.path.join(normalized_path, r"new stuff\set files")))

    def browse_set_files_folder_full_automation():
        path = filedialog.askdirectory(title="Select Set Files Folder")
        if path:
            normalized_path = os.path.normpath(path)
            set_files_folder_var_full_automation.set(normalized_path)

    def browse_expert_advisor_full_automation():
        path = filedialog.askopenfilename(title="Select Expert Advisor File", filetypes=[("EA Files", "*.ex5;*.ex4")])
        if path:
            normalized_path = os.path.normpath(path)
            expert_advisor_var_full_automation.set(os.path.basename(normalized_path))

    # Function to extract code from selected option
    def extract_code(selected_option):
        return selected_option.split(' - ')[0]

    # Functions to save and load settings for Creator OOS Generator
    # def save_creator_settings():
    #     creator_settings = {
    #         'mt5_path': mt5_path_var_creator.get(),
    #         'mt5_data_folder': mt5_data_folder_var_creator.get(),
    #         'set_files_folder': set_files_folder_var_creator.get(),
    #         'custom_report_folder_base': custom_report_folder_base_var_creator.get(),
    #         'from_date': from_date_var_creator.get(),
    #         'to_date': to_date_var_creator.get(),
    #         'deposit': deposit_var_creator.get(),
    #         'leverage': leverage_var_creator.get(),
    #         'period': period_var_creator.get(),
    #         'model': model_var_creator.get(),
    #         'execution_mode': execution_mode_var_creator.get(),
    #         'expert_advisor': expert_advisor_var_creator.get(),
    #     }
    #     with open('creator_oos_settings.json', 'w') as f:
    #         json.dump(creator_settings, f)
    #     messagebox.showinfo("Settings Saved", "Creator OOS Generator settings have been saved as default.")

    # def load_creator_settings():
    #     try:
    #         with open('creator_oos_settings.json', 'r') as f:
    #             creator_settings = json.load(f)
    #         mt5_path_var_creator.set(creator_settings['mt5_path'])
    #         mt5_data_folder_var_creator.set(creator_settings['mt5_data_folder'])
    #         set_files_folder_var_creator.set(creator_settings['set_files_folder'])
    #         custom_report_folder_base_var_creator.set(creator_settings['custom_report_folder_base'])
    #         from_date_var_creator.set(creator_settings['from_date'])
    #         to_date_var_creator.set(creator_settings['to_date'])
    #         deposit_var_creator.set(creator_settings['deposit'])
    #         leverage_var_creator.set(creator_settings['leverage'])
    #         period_var_creator.set(creator_settings['period'])
    #         model_var_creator.set(creator_settings['model'])
    #         execution_mode_var_creator.set(creator_settings['execution_mode'])
    #         expert_advisor_var_creator.set(creator_settings['expert_advisor'])
    #     except FileNotFoundError:
    #         pass

    # Functions to save and load settings for Backtester
    # def save_backtester_settings():
    #     backtester_settings = {
    #         'mt5_path': mt5_path_var_backtester.get(),
    #         'mt5_data_folder': mt5_data_folder_var_backtester.get(),
    #         'set_files_folder': set_files_folder_var_backtester.get(),
    #         'custom_report_folder_base': custom_report_folder_base_var_backtester.get(),
    #         'from_date': from_date_var_backtester.get(),
    #         'to_date': to_date_var_backtester.get(),
    #         'forward_date': forward_date_var_backtester.get(),
    #         'deposit': deposit_var_backtester.get(),
    #         'leverage': leverage_var_backtester.get(),
    #         'period': period_var_backtester.get(),
    #         'model': model_var_backtester.get(),
    #         'execution_mode': execution_mode_var_backtester.get(),
    #         'expert_advisor': expert_advisor_var_backtester.get(),
    #         'optimization': optimization_var_backtester.get(),
    #         'forward_mode': forward_mode_var_backtester.get(),
    #         'optimization_criterion': optimization_criterion_var_backtester.get(),
    #     }
    #     with open('backtester_settings.json', 'w') as f:
    #         json.dump(backtester_settings, f)
    #     messagebox.showinfo("Settings Saved", "Backtester settings have been saved as default.")

    # def load_backtester_settings():
    #     try:
    #         with open('backtester_settings.json', 'r') as f:
    #             backtester_settings = json.load(f)
    #         mt5_path_var_backtester.set(backtester_settings['mt5_path'])
    #         mt5_data_folder_var_backtester.set(backtester_settings['mt5_data_folder'])
    #         set_files_folder_var_backtester.set(backtester_settings['set_files_folder'])
    #         custom_report_folder_base_var_backtester.set(backtester_settings['custom_report_folder_base'])
    #         from_date_var_backtester.set(backtester_settings['from_date'])
    #         to_date_var_backtester.set(backtester_settings['to_date'])
    #         forward_date_var_backtester.set(backtester_settings['forward_date'])
    #         deposit_var_backtester.set(backtester_settings['deposit'])
    #         leverage_var_backtester.set(backtester_settings['leverage'])
    #         period_var_backtester.set(backtester_settings['period'])
    #         model_var_backtester.set(backtester_settings['model'])
    #         execution_mode_var_backtester.set(backtester_settings['execution_mode'])
    #         expert_advisor_var_backtester.set(backtester_settings['expert_advisor'])
    #         optimization_var_backtester.set(backtester_settings['optimization'])
    #         forward_mode_var_backtester.set(backtester_settings['forward_mode'])
    #         optimization_criterion_var_backtester.set(backtester_settings['optimization_criterion'])
    #     except FileNotFoundError:
    #         pass

    # Add "Save as Default" options to the menus
    # creator_menu.add_command(label="Save as Default", command=save_creator_settings)
    # backtester_menu.add_command(label="Save as Default", command=save_backtester_settings)

    # Functions to start and stop the process for Creator OOS Generator
    # def start_process_creator():
    #     # Disable the Start Test button and enable Stop Test button
    #     start_button_creator.config(state=tk.DISABLED)
    #     stop_button_creator.config(state=tk.NORMAL)

    #     # Collect parameters from the GUI inputs
    #     params = {
    #         'MT5_PATH': mt5_path_var_creator.get(),
    #         'MT5_DATA_FOLDER': mt5_data_folder_var_creator.get(),
    #         'SET_FILES_FOLDER': set_files_folder_var_creator.get(),
    #         'CUSTOM_REPORT_FOLDER_BASE': custom_report_folder_base_var_creator.get(),
    #         'FROM_DATE': from_date_var_creator.get(),
    #         'TO_DATE': to_date_var_creator.get(),
    #         'DEPOSIT': deposit_var_creator.get(),
    #         'LEVERAGE': leverage_var_creator.get(),
    #         'PERIOD': period_var_creator.get(),
    #         'EXPERT_ADVISOR': expert_advisor_var_creator.get(),
    #         'EXECUTION_MODE': execution_mode_var_creator.get(),
    #         'MODEL': model_var_creator.get()
    #     }

    #     # Initialize stop event
    #     global stop_event_creator
    #     stop_event_creator = Event()

    #     # Get total number of set files for progress bar
    #     set_files = [f for f in os.listdir(params['SET_FILES_FOLDER']) if f.endswith('.set')]
    #     total_set_files = len(set_files)

    #     # Start the process in a separate thread to keep the GUI responsive
    #     Thread(target=run_creator_oos_generator, args=(params, stop_event_creator, progress_var_creator, total_set_files, start_button_creator, stop_button_creator), daemon=True).start()

    # def stop_process_creator():
    #     # Set the stop event to signal the thread to stop
    #     stop_event_creator.set()
    #     print("Stop event set.")
    #     # Re-enable the Start Test button and disable Stop Test button
    #     start_button_creator.config(state=tk.NORMAL)
    #     stop_button_creator.config(state=tk.DISABLED)
    #     messagebox.showinfo("Stopped", "The backtesting process has been stopped.")

    # Functions to start and stop the process for Backtester
    # def start_process_backtester():
    #     # Disable the Start Test button and enable Stop Test button
    #     start_button_backtester.config(state=tk.DISABLED)
    #     stop_button_backtester.config(state=tk.NORMAL)

    #     # Collect parameters from the GUI inputs
    #     params = {
    #         'MT5_PATH': mt5_path_var_backtester.get(),
    #         'MT5_DATA_FOLDER': mt5_data_folder_var_backtester.get(),
    #         'SET_FILES_FOLDER': set_files_folder_var_backtester.get(),
    #         'CUSTOM_REPORT_FOLDER_BASE': custom_report_folder_base_var_backtester.get(),
    #         'FROM_DATE': from_date_var_backtester.get(),
    #         'TO_DATE': to_date_var_backtester.get(),
    #         'FORWARD_DATE': forward_date_var_backtester.get(),
    #         'DEPOSIT': deposit_var_backtester.get(),
    #         'LEVERAGE': leverage_var_backtester.get(),
    #         'PERIOD': period_var_backtester.get(),
    #         'EXPERT_ADVISOR': expert_advisor_var_backtester.get(),
    #         'EXECUTION_MODE': execution_mode_var_backtester.get(),
    #         'MODEL': model_var_backtester.get(),
    #         'OPTIMIZATION': extract_code(optimization_var_backtester.get()),
    #         'FORWARD_MODE': extract_code(forward_mode_var_backtester.get()),
    #         'OPTIMIZATION_CRITERION': extract_code(optimization_criterion_var_backtester.get())
    #     }

    #     # Initialize stop event
    #     global stop_event_backtester
    #     stop_event_backtester = Event()

    #     # Get total number of set files for progress bar
    #     set_files = [f for f in os.listdir(params['SET_FILES_FOLDER']) if f.endswith('.set')]
    #     total_set_files = len(set_files)

    #     # Start the process in a separate thread to keep the GUI responsive
    #     Thread(target=run_backtester, args=(params, stop_event_backtester, progress_var_backtester, total_set_files, start_button_backtester, stop_button_backtester), daemon=True).start()

    # def stop_process_backtester():
    #     # Set the stop event to signal the thread to stop
    #     stop_event_backtester.set()
    #     print("Stop event set.")
    #     # Re-enable the Start Test button and disable Stop Test button
    #     start_button_backtester.config(state=tk.NORMAL)
    #     stop_button_backtester.config(state=tk.DISABLED)
    #     messagebox.showinfo("Stopped", "The backtesting process has been stopped.")


    # Functions to start and stop the process for full auto
    def start_process_full_automation():
        # Disable the Start Test button and enable Stop Test button
        print('---start_process_full_automation')
        start_button_full_automation.config(state=tk.DISABLED)
        stop_button_full_automation.config(state=tk.NORMAL)

        # Collect parameters from the GUI inputs
        params = {
            'MT5_PATH': mt5_path_var_full_automation.get(),
            'MT5_DATA_FOLDER': mt5_data_folder_var_full_automation.get(),
            'SET_FILES_FOLDER': set_file_list[0],
            'CUSTOM_REPORT_FOLDER_BASE': set_file_list[0],
            'SET_FILE_LIST': set_file_list,
            'FROM_DATE': from_date_var_full_automation.get(),
            'TO_DATE': to_date_var_full_automation.get(),
            'FORWARD_DATE': forward_date_var_full_automation.get(),
            'DEPOSIT': deposit_var_full_automation.get(),
            'LEVERAGE': leverage_var_full_automation.get(),
            'PERIOD': period_var_full_automation.get(),
            'EXPERT_ADVISOR': expert_advisor_var_full_automation.get(),
            'EXECUTION_MODE': execution_mode_var_full_automation.get(),
            'MODEL': model_var_full_automation.get(),
            'OPTIMIZATION': extract_code(optimization_var_full_automation.get()),
            'FORWARD_MODE': extract_code(forward_mode_var_full_automation.get()),
            'OPTIMIZATION_CRITERION': extract_code(optimization_criterion_var_full_automation.get()),
            'CREATORXML_PARAM1_BALANCE': extract_code(creator_xml_var_full_automation_1.get()),
            'CREATORXML_PARAM2_TARGET_DRAWDOWN': extract_code(creator_xml_var_full_automation_2.get()),
            'CREATORXML_PARAM3_MIN_TOT_EST_PROFIT': extract_code(creator_xml_var_full_automation_3.get()),

            'MAX_ORIGINAL_DD_VALUE': creator_xml_var_full_automation_maxOriginalDd_value.get(),
            'TOTAL_EST_PROF_VALUE': creator_xml_var_full_automation_totalEstimatedProfit_value.get(),

            'TRADES_FILTER_VALUE': creator_xml_var_full_automation_TRADES_value.get(),


            'SET_FILES_FOLDER_CREATE_OOS': set_files_folder_var_full_automation.get(),
            'CUSTOM_REPORT_FOLDER_BASE_CREATE_OOS': custom_report_folder_base_var_full_automation.get(),
            'FROM_DATE_CREATE_OOS': next_sunday(to_date_var_full_automation.get()),
            'TO_DATE_CREATE_OOS': next_friday(next_sunday(to_date_var_full_automation.get())),
            'DEPOSIT_CREATE_OOS': deposit_var_full_automation_create_oos.get(),
            'LEVERAGE_CREATE_OOS': leverage_var_full_automation_create_oos.get(),
            'PERIOD_CREATE_OOS': period_var_full_automation_create_oos.get(),

            'EXECUTION_MODE_CREATE_OOS': execution_mode_var_full_automation_create_oos.get(),
            'MODEL_CREATE_OOS': model_var_full_automation_create_oos.get(),

            'REMOVE_DUPLICATES': remove_duplicates_var,
            'CHECKBOX_SELECTION': checkbox_selection.get(),

            'CHECKBOX_SELECTION_TOTESTPROF': totalEstimatedProfit_checkbox.get(),
            'CHECKBOX_SELECTION_MAXORIGDD':maxOriginalDd_checkbox.get(),
            'CHECKBOX_SELECTION_TRADES_FILTER': tradesFilter_checkbox.get(),
            'CHECKBOX_SELECTION_TOTESTPROF_GR_TOTESTDD' : allTtotalProfiltsGrTotEstDD_checkbox.get()

        }
        log_to_file(params)



        # Initialize stop event
        global stop_event_full_automation
        stop_event_full_automation = Event()

        # Get total number of set files for progress bar
        set_files = [f for f in os.listdir(params['SET_FILES_FOLDER']) if f.endswith('.set')]
        total_set_files = len(set_files)

        # Start the process in a separate thread to keep the GUI responsive
        Thread(target=run_full_automation, args=(params, stop_event_full_automation, progress_var_full_automation,progress_label, total_set_files, start_button_full_automation, stop_button_full_automation), daemon=True).start()

    def stop_process_full_automation():
        # Set the stop event to signal the thread to stop
        stop_event_full_automation.set()
        print("Stop event set.")
        # Re-enable the Start Test button and disable Stop Test button
        start_button_full_automation.config(state=tk.NORMAL)
        stop_button_full_automation.config(state=tk.DISABLED)
        messagebox.showinfo("Stopped", "The backtesting process has been stopped.")

    # Layout for Creator OOS Generator Tab
    row = 0

    

    # full auto - POl ########################

    row = 0
    tk.Label(full_automation_frame, text="-----BACKTESTER PARAMS-----").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    row += 1
    # Inputs for full_automation_frame
    tk.Label(full_automation_frame, text="MT5 Terminal Path:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Entry(full_automation_frame, textvariable=mt5_path_var_full_automation, width=50).grid(row=row, column=1, padx=5, pady=5)
    tk.Button(full_automation_frame, text="Browse", command=browse_mt5_path_full_automation).grid(row=row, column=2, padx=5, pady=5)
    row += 1

    tk.Label(full_automation_frame, text="MT5 Data Folder:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Entry(full_automation_frame, textvariable=mt5_data_folder_var_full_automation, width=50).grid(row=row, column=1, padx=5, pady=5)
    tk.Button(full_automation_frame, text="Browse", command=browse_mt5_data_folder_full_automation).grid(row=row, column=2, padx=5, pady=5)
    row += 1

    # tk.Label(full_automation_frame, text="Set Files Folder:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=set_files_folder_var_full_automation, width=50).grid(row=row, column=1, padx=5, pady=5)
    # tk.Button(full_automation_frame, text="Browse", command=browse_set_files_folder_full_automation).grid(row=row, column=2, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Custom Report Folder Base Name:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=custom_report_folder_base_var_full_automation, width=50).grid(row=row, column=1, padx=5, pady=5)
    # row += 1

    # def browse_for_set_files():
    #     # Open a file dialog and allow multiple file selection
    #     files = filedialog.askopenfilenames(title="Select Files")


    #     if files:
    #         files = os.path.normpath(files)


    #     if files:
    #         set_file_list.extend(files)  # Add selected files to the list
    #         update_file_list_display()  # Update the display


    def browse_for_set_file_folder():
        # Open a file dialog to select a folder
        folder = filedialog.askdirectory(title="Select Folder")

        if folder:
            folder = os.path.normpath(folder)

        if folder:  # Check if a folder was selected
            set_file_list.append(folder)  # Add the selected folder to the list
            update_file_list_display()  # Update the display


    def open_delete_window():
        """Open a new window to select and delete targets."""
        def delete_selected():
            """Delete selected targets from the main list."""
            selected_items = delete_listbox.curselection()
            for index in reversed(selected_items):  # Reverse to avoid index shifting
                del set_file_list[index]
            update_file_list_display()
            delete_window.destroy()

        # Create a new window for deleting targets
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Target")
        delete_window.geometry("800x300")

        tk.Label(delete_window, text="Select Targets to Delete:").pack(pady=5)

        delete_listbox = tk.Listbox(delete_window, selectmode=tk.MULTIPLE, width=110, height=10)
        delete_listbox.pack(padx=10, pady=10)

        # Populate the listbox with the current targets
        for file in set_file_list:
            delete_listbox.insert(tk.END, file)

        tk.Button(delete_window, text="Delete Selected", command=delete_selected).pack(pady=10)


    def update_file_list_display():
        # Clear the listbox and update it with the latest file list
        file_listbox.delete(0, tk.END)
        for file in set_file_list:
            file_listbox.insert(tk.END, file)
    # Label and Browse Button

    tk.Label(full_automation_frame, text="Select Target .set Files:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Button(full_automation_frame, text="Add .set folder target", command=browse_for_set_file_folder).grid(row=row, column=1, padx=5, pady=5)
    row += 1
    # Listbox to display selected files
    file_listbox = tk.Listbox(full_automation_frame, width=100, height=5)
    file_listbox.grid(row=row, column=0, columnspan=3, padx=5, pady=5)

    row += 1

    tk.Button(full_automation_frame, text="Delete Target", command=open_delete_window).grid(row=row, column=0, columnspan=3, pady=5)

    row += 1

    tk.Label(full_automation_frame, text="From Date (YYYY.MM.DD):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Entry(full_automation_frame, textvariable=from_date_var_full_automation).grid(row=row, column=1, padx=5, pady=5)
    row += 1

    tk.Label(full_automation_frame, text="To Date (YYYY.MM.DD):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Entry(full_automation_frame, textvariable=to_date_var_full_automation).grid(row=row, column=1, padx=5, pady=5)
    row += 1

    # tk.Label(full_automation_frame, text="Forward Date (YYYY.MM.DD, leave blank if using Forward Mode):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=forward_date_var_full_automation).grid(row=row, column=1, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Deposit:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=deposit_var_full_automation).grid(row=row, column=1, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Leverage:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=leverage_var_full_automation).grid(row=row, column=1, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Period:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=period_var_full_automation).grid(row=row, column=1, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Model (1= 1M OHCL, 4=ETWRT):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=model_var_full_automation).grid(row=row, column=1, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Execution Mode:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=execution_mode_var_full_automation).grid(row=row, column=1, padx=5, pady=5)
    # row += 1

    # # Optimization options
    # optimization_options = [
    #     "0 - Optimization disabled",
    #     "1 - Slow complete algorithm",
    #     "2 - Fast genetic based algorithm",
    #     "3 - All symbols selected in Market Watch"
    # ]

    # tk.Label(full_automation_frame, text="Optimization:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # optimization_combobox = ttk.Combobox(
    #     full_automation_frame, textvariable=optimization_var_full_automation,
    #     values=optimization_options, state='readonly'
    # )
    # optimization_combobox.grid(row=row, column=1, padx=5, pady=5)
    # optimization_combobox.current(2)  # Set default selection to first option
    # row += 1

    # # Forward Mode options
    # forward_mode_options = [
    #     "0 - Off",
    #     "1 - 1/2 of the testing period",
    #     "2 - 1/3 of the testing period",
    #     "3 - 1/4 of the testing period",
    #     "4 - Custom interval specified using ForwardDate"
    # ]

    # tk.Label(full_automation_frame, text="Forward Mode:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # forward_mode_combobox = ttk.Combobox(
    #     full_automation_frame, textvariable=forward_mode_var_full_automation,
    #     values=forward_mode_options, state='readonly'
    # )
    # forward_mode_combobox.grid(row=row, column=1, padx=5, pady=5)
    # forward_mode_combobox.current(1)
    # row += 1

    # # Optimization Criterion options with updated names
    # optimization_criterion_options = [
    #     "0 - Balance Max",
    #     "1 - Profit Factor Max",
    #     "2 - Expected Payoff Max",
    #     "3 - Drawdown Min",
    #     "4 - Recovery Factor Max",
    #     "5 - Sharpe Ratio Max",
    #     "6 - Custom Max",
    #     "7 - Complex Criterion Max"
    # ]








    # tk.Label(full_automation_frame, text="Optimization Criterion:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # optimization_criterion_combobox = ttk.Combobox(
    #     full_automation_frame, textvariable=optimization_criterion_var_full_automation,
    #     values=optimization_criterion_options, state='readonly'
    # )
    # optimization_criterion_combobox.grid(row=row, column=1, padx=5, pady=5)
    # optimization_criterion_combobox.current(0)
    # row += 1

    tk.Label(full_automation_frame, text="Expert Advisor File Name:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Entry(full_automation_frame, textvariable=expert_advisor_var_full_automation, width=50).grid(row=row, column=1, padx=5, pady=5)
    tk.Button(full_automation_frame, text="Browse", command=browse_expert_advisor_full_automation).grid(row=row, column=2, padx=5, pady=5)
    row += 1


    ############################ creatorxml parameters
    # tk.Label(full_automation_frame, text="-----CREATOR_XML PARAMS-----").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="balance:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=creator_xml_var_full_automation_1).grid(row=row, column=1, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="target drawdown:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=creator_xml_var_full_automation_2).grid(row=row, column=1, padx=5, pady=5)
    # row += 1
    ##############






    # # First checkbox
    # tk.Label(
    #     full_automation_frame, text="Download All ≥ Total Estimated Profit"
    # ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=creator_xml_var_full_automation_totalEstimatedProfit_value).grid(row=row, column=1, padx=5, pady=5)

    # # tk.Checkbutton(
    # #     full_automation_frame,
    # #     text="",
    # #     variable=checkbox_selection,
    # #     onvalue="totalEstimatedProfit",
    # #     offvalue="none",
    # # ).grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # row += 1

    # # Second checkbox
    # tk.Label(full_automation_frame, text="Download All ≤ Max Original DD").grid(
    #     row=row, column=0, sticky=tk.W, padx=5, pady=5
    # )
    # tk.Entry(full_automation_frame, textvariable=creator_xml_var_full_automation_maxOriginalDd_value).grid(row=row, column=1, padx=5, pady=5)
    # tk.Checkbutton(
    #     full_automation_frame,
    #     text="",
    #     variable=checkbox_selection,
    #     onvalue="maxOriginalDd",
    #     offvalue="none",
    # ).grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # row += 1

    def on_trades_filter_checkbox_change(*args):
        if tradesFilter_checkbox.get():
            totalEstimatedProfit_checkbox.set(False)
            #print('-')
            maxOriginalDd_checkbox.set(False)
            allTtotalProfiltsGrTotEstDD_checkbox.set(False)
            tradesFilter_checkbox.set(True)



    def on_other_checkboxes_change_ab(*args):
        #print('!!!')
        save_a = totalEstimatedProfit_checkbox.get()
        save_b = maxOriginalDd_checkbox.get()
        if totalEstimatedProfit_checkbox.get() or maxOriginalDd_checkbox.get():




            allTtotalProfiltsGrTotEstDD_checkbox.set(False)
            tradesFilter_checkbox.set(False)
            totalEstimatedProfit_checkbox.set(save_a)
            maxOriginalDd_checkbox.set(save_b)

            #print(f'on_other_checkboxes_change {totalEstimatedProfit_checkbox.get()} - {maxOriginalDd_checkbox.get()}')

    def on_trades_filter_checkbox_change_d(*args):
        if tradesFilter_checkbox.get():
            totalEstimatedProfit_checkbox.set(False)
            #print('-')
            maxOriginalDd_checkbox.set(False)
            tradesFilter_checkbox.set(False)

            allTtotalProfiltsGrTotEstDD_checkbox.set(True)


    # tk.Label(full_automation_frame, text="Download All ≥ Total Estimated Profit").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=creator_xml_var_full_automation_totalEstimatedProfit_value).grid(row=row, column=1, padx=5, pady=5)

    totalEstimatedProfit_checkbox = tk.BooleanVar(value=True)
    ##totalEstimatedProfit_checkbox.trace_add("write", on_other_checkboxes_change_ab)  # Add the callback
    # Add the checkbox
    # tk.Checkbutton(
    #     full_automation_frame,
    #     text="",
    #     variable=totalEstimatedProfit_checkbox,
    #     onvalue=True,  # Value when checked
    #     offvalue=False,  # Value when unchecked
    # ).grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)


    row += 1




    # tk.Label(full_automation_frame, text="Download All ≤ Max Original DD").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=creator_xml_var_full_automation_maxOriginalDd_value).grid(row=row, column=1, padx=5, pady=5)
    # Add the checkbox
    maxOriginalDd_checkbox = tk.BooleanVar(value=True)
    #maxOriginalDd_checkbox.trace_add("write", on_other_checkboxes_change_ab)
    # tk.Checkbutton(
    #     full_automation_frame,
    #     text="",
    #     variable=maxOriginalDd_checkbox,
    #     onvalue=True,  # Value when checked
    #     offvalue=False,  # Value when unchecked
    # ).grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # row += 1

    ##############################################




    #tk.Label(full_automation_frame, text="Download All Total Trades >= X Trades").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    #tk.Entry(full_automation_frame, textvariable=creator_xml_var_full_automation_TRADES_value).grid(row=row, column=1, padx=5, pady=5)
    # Add the checkbox
    tradesFilter_checkbox = tk.BooleanVar(value=True)
    #tradesFilter_checkbox.trace_add("write", on_trades_filter_checkbox_change)  # Add the callback

    # tk.Checkbutton(
    #     full_automation_frame,
    #     text="",
    #     variable= tradesFilter_checkbox,
    #     onvalue=True,  # Value when checked
    #     offvalue=False,  # Value when unchecked
    # ).grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # row += 1



    #tk.Label(full_automation_frame, text="Download All Total Profit > Max_Original_DD").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    ##tk.Entry(full_automation_frame, textvariable=creator_xml_var_full_automation_3).grid(row=row, column=1, padx=5, pady=5)
    #Add the checkbox
    allTtotalProfiltsGrTotEstDD_checkbox = tk.BooleanVar(value=True)
    #allTtotalProfiltsGrTotEstDD_checkbox.trace_add("write", on_trades_filter_checkbox_change_d)
    # tk.Checkbutton(
    #     full_automation_frame,
    #     text="",
    #     variable=allTtotalProfiltsGrTotEstDD_checkbox,
    #     onvalue=True,  # Value when checked
    #     offvalue=False,  # Value when unchecked
    # ).grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # row += 1


    # Define a variable to track the state of the checkbox
    remove_duplicates_var = tk.BooleanVar(value=True)  # Default is unchecked (False)

    # Add the checkbox
    # tk.Checkbutton(
    #     full_automation_frame,
    #     text="Remove Duplicates",
    #     variable=remove_duplicates_var,
    #     onvalue=True,  # Value when checked
    #     offvalue=False,  # Value when unchecked
    # ).grid(row=row, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # row += 1


    # Start and Stop buttons
    global start_button_full_automation, stop_button_full_automation
    start_button_full_automation = tk.Button(full_automation_frame, text="Start Test", command=start_process_full_automation, width=15, bg="green", fg="white")
    start_button_full_automation.grid(row=row, column=1, pady=10, sticky='e')

    stop_button_full_automation = tk.Button(full_automation_frame, text="Stop Test", command=stop_process_full_automation, state=tk.DISABLED, width=15, bg="red", fg="white")
    stop_button_full_automation.grid(row=row, column=1+1, pady=10, sticky='w')
    row += 1

    # Progress bar
    progress_var_full_automation = tk.DoubleVar()
    progress_bar_full_automation = ttk.Progressbar(full_automation_frame, variable=progress_var_full_automation, maximum=100, length=400)
    progress_bar_full_automation.grid(row=row, column=0, columnspan=3, sticky='we', padx=5, pady=10)

    progress_label = tk.Label(
    full_automation_frame,
    text="waiting for action..",  # Initial text
    font=("Arial", 10),
    bg="white"
                            )
    progress_label.place(in_=progress_bar_full_automation, relx=0.5, rely=0.5, anchor="center")  # Position it centered


    row += 1




    # Inputs for Creator OOS Generator for automation

    row = 0

    # tk.Label(full_automation_frame, text="-----CREATOR OOS GEN PARAMS-----").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Set Files Folder:").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=set_files_folder_var_full_automation_create_oos, width=50).grid(row=row, column=1+3, padx=5, pady=5)
    # tk.Button(full_automation_frame, text="Browse", command=browse_set_files_folder_creator_for_oos).grid(row=row, column=2+3, padx=5, pady=5)
    #row += 1

    # tk.Label(full_automation_frame, text="Custom Report Folder Base Name:").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=custom_report_folder_base_var_full_automation_create_oos, width=50).grid(row=row, column=1+3, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="From Date (YYYY.MM.DD):").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=from_date_var_full_automation_create_oos).grid(row=row, column=1+3, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="To Date (YYYY.MM.DD):").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=to_date_var_full_automation_create_oos).grid(row=row, column=1+3, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Deposit:").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=deposit_var_full_automation_create_oos).grid(row=row, column=1+3, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Leverage:").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=leverage_var_full_automation_create_oos).grid(row=row, column=1+3, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Period:").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=period_var_full_automation_create_oos).grid(row=row, column=1+3, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Model (1= 1M OHCL, 4=ETWRT):").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=model_var_full_automation_create_oos).grid(row=row, column=1+3, padx=5, pady=5)
    # row += 1

    # tk.Label(full_automation_frame, text="Execution Mode:").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    # tk.Entry(full_automation_frame, textvariable=execution_mode_var_full_automation_create_oos).grid(row=row, column=1+3, padx=5, pady=5)
    # row += 1

    #tk.Label(full_automation_frame, text="Expert Advisor File Name:").grid(row=row, column=0+3, sticky=tk.W, padx=5, pady=5)
    #tk.Entry(full_automation_frame, textvariable=expert_advisor_var_full_automation, width=50).grid(row=row, column=1+3, padx=5, pady=5)
    #tk.Button(full_automation_frame, text="Browse", command=browse_expert_advisor_creator).grid(row=row, column=2+3, padx=5, pady=5)
    row += 1


    ##########################################

    # # Inputs for ddAnalyzer
    # global start_button_ddAnalyzer
    # start_button_ddAnalyzer = tk.Button(dd_analyzer_frame, text="DD Analyzer App", command=launch_ddanalyzer, width=15, bg="green", fg="white")
    # start_button_ddAnalyzer.grid(row=row, column=1, pady=10, sticky='e')



    ##########################################

    #inputs for creatorxml tab

    # global start_button_creaorxml
    # start_button_creaorxml = tk.Button(creaorxml_frame, text="CreatorXML App", command=creatorXml_subprocess, width=15, bg="green", fg="white")
    # start_button_creaorxml.grid(row=row, column=1, pady=10, sticky='e')


    #########################################

    # Load saved settings






    # load_creator_settings()
    # load_backtester_settings()

# Start the application initialization
check_expiry("2025-03-30")
initialize_application()
