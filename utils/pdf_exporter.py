from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "AgriScope Report", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def clean_ascii(text):
    return text.encode('ascii', errors='ignore').decode('ascii')

def export_to_pdf(region, crops_df, filename="AgriScope_Report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    region_clean = clean_ascii(region)
    pdf.cell(0, 10, f"Region: {region_clean}", ln=True)

    for crop in crops_df["Crop"].unique():
        crop_clean = clean_ascii(str(crop))  # make sure it's a string
        crop_data = crops_df[crops_df["Crop"] == crop]
        avg_prod = crop_data["Production (1000 tons)"].mean()
        line = clean_ascii(f"- {crop_clean} - Avg Production: {avg_prod:.2f}k tons")
        pdf.cell(0, 10, line, ln=True)

    os.makedirs("exports", exist_ok=True)
    save_path = os.path.join("exports", filename)
    pdf.output(save_path)

    return save_path
