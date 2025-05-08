import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os

class CompoundInterestCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Compound Interest Calculator")
        self.root.geometry("400x300")
        
        # Language dictionary
        self.texts = {
            'en': {
                'title': "Compound Interest Calculator (USD)",
                'principal_label': "Principal Amount (USD):",
                'rate_label': "Daily Interest Rate (%):",
                'days_label': "Time Period (Days):",
                'calculate_button': "Calculate & Export",
                'success_msg': "Excel file '{}' generated successfully!",
                'error_invalid': "Please enter valid numbers.",
                'error_positive': "Please enter valid positive numbers.",
                'error_general': "An error occurred: {}",
                'language_button': "Switch to Chinese"
            },
            'zh': {
                'title': "复利计算器（美元）",
                'principal_label': "本金（美元）：",
                'rate_label': "每日利率（%）：",
                'days_label': "时间（天）：",
                'calculate_button': "计算并导出",
                'success_msg': "Excel文件 '{}' 生成成功！",
                'error_invalid': "请输入有效的数字。",
                'error_positive': "请输入有效的正数。",
                'error_general': "发生错误：{}",
                'language_button': "切换到英文"
            }
        }
        
        # Current language
        self.current_lang = 'en'
        
        # GUI Elements
        self.create_gui()

    def create_gui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set title
        self.root.title(self.texts[self.current_lang]['title'])

        # Labels and Entries
        self.principal_label = tk.Label(self.root, text=self.texts[self.current_lang]['principal_label'])
        self.principal_label.pack(pady=10)
        self.principal_entry = tk.Entry(self.root)
        self.principal_entry.pack()

        self.rate_label = tk.Label(self.root, text=self.texts[self.current_lang]['rate_label'])
        self.rate_label.pack(pady=10)
        self.rate_entry = tk.Entry(self.root)
        self.rate_entry.pack()

        self.days_label = tk.Label(self.root, text=self.texts[self.current_lang]['days_label'])
        self.days_label.pack(pady=10)
        self.days_entry = tk.Entry(self.root)
        self.days_entry.pack()

        # Calculate Button
        self.calculate_button = tk.Button(self.root, text=self.texts[self.current_lang]['calculate_button'], command=self.calculate)
        self.calculate_button.pack(pady=10)

        # Language Switch Button
        self.language_button = tk.Button(self.root, text=self.texts[self.current_lang]['language_button'], command=self.switch_language)
        self.language_button.pack(pady=10)

    def switch_language(self):
        # Toggle language
        self.current_lang = 'zh' if self.current_lang == 'en' else 'en'
        # Recreate GUI with new language
        self.create_gui()

    def calculate(self):
        try:
            # Get inputs
            principal = float(self.principal_entry.get())
            daily_rate = float(self.rate_entry.get()) / 100  # Convert percentage to decimal
            days = int(self.days_entry.get())

            if principal <= 0 or daily_rate < 0 or days <= 0:
                messagebox.showerror("Error", self.texts[self.current_lang]['error_positive'])
                return

            # Calculate daily compound interest
            data = []
            current_amount = principal

            for day in range(days + 1):
                if day == 0:
                    interest = 0
                else:
                    interest = current_amount * daily_rate
                    current_amount += interest

                data.append({
                    'Day' if self.current_lang == 'en' else '天': day,
                    'Balance (USD)' if self.current_lang == 'en' else '余额（美元）': round(current_amount, 2),
                    'Interest Earned (USD)' if self.current_lang == 'en' else '利息（美元）': round(interest, 2),
                    'Formula' if self.current_lang == 'en' else '公式': f'{round(current_amount - interest, 2)} * {daily_rate*100}%'
                })

                # Update for next iteration
                if day == 0:
                    current_amount = principal

            # Create DataFrame
            df = pd.DataFrame(data)

            # Generate Excel file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"compound_interest_{timestamp}.xlsx"
            df.to_excel(filename, index=False)

            # Show success message
            messagebox.showinfo("Success", self.texts[self.current_lang]['success_msg'].format(filename))

        except ValueError:
            messagebox.showerror("Error", self.texts[self.current_lang]['error_invalid'])
        except Exception as e:
            messagebox.showerror("Error", self.texts[self.current_lang]['error_general'].format(str(e)))

def main():
    root = tk.Tk()
    app = CompoundInterestCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()