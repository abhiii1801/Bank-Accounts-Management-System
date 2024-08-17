from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

class Receipts:

    def create_transaction_receipt(self, sender_name, sender_accnum, sender_acc_type, sender_bank, 
                                   receiver_name, receiver_accnum, receiver_bank, 
                                   transaction_amount, transaction_datetime,transaction_id):
        self.file_path = f"receipts/transaction_receipt{datetime.now().strftime('%H-%M-%S')}.pdf"
        c = canvas.Canvas(self.file_path, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 48)
        c.drawCentredString(width / 2.0, height - 1.5 * inch, "BANKSPHERE")

        # Subtitle
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2.0, height - 1.75 * inch, "Your Financial World, Simplified.")

        # Transaction Receipt Heading
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2.0, height - 2.25 * inch, "Transaction Receipt")
        
        # Underline the Transaction Receipt heading
        c.line(inch, height - 2.3 * inch, width - inch, height - 2.3 * inch)

        # Draw a line below the title and subtitle
        c.line(inch, height - 2.5 * inch, width - inch, height - 2.5 * inch)

        # Spacing for transaction details
        y_position = height - 2.75 * inch
        line_height = 18

        # Sender Details
        c.setFont("Helvetica-Bold", 12)
        c.drawString(inch, y_position, "Sender's Details:")
        y_position -= line_height
        c.setFont("Helvetica", 12)

        sender_details = [
            ("Sender's Name", sender_name),
            ("Sender's Account Number", sender_accnum),
            ("Sender's Account Type", sender_acc_type),
            ("Sender's Bank", sender_bank)
        ]

        for label, value in sender_details:
            c.drawString(inch, y_position, f"{label}: {value}")
            y_position -= line_height

        # Draw a line after sender details
        c.line(inch, y_position, width - inch, y_position)
        y_position -= line_height

        # Receiver Details
        c.setFont("Helvetica-Bold", 12)
        c.drawString(inch, y_position, "Receiver's Details:")
        y_position -= line_height
        c.setFont("Helvetica", 12)

        receiver_details = [
            ("Receiver's Name", receiver_name),
            ("Receiver's Account Number", receiver_accnum),
            ("Receiver's Bank", receiver_bank)
        ]

        for label, value in receiver_details:
            c.drawString(inch, y_position, f"{label}: {value}")
            y_position -= line_height

        # Draw a line after receiver details
        c.line(inch, y_position, width - inch, y_position)
        y_position -= line_height

        # Transaction Details
        c.setFont("Helvetica-Bold", 12)
        c.drawString(inch, y_position, "Transaction Details:")
        y_position -= line_height
        c.setFont("Helvetica", 12)

        c.drawString(inch, y_position, f"Transaction Amount: {transaction_amount}")
        y_position -= line_height
        c.drawString(inch, y_position, f"Transaction Date and Time: {transaction_datetime}")
        y_position -= line_height
        c.drawString(inch, y_position, f"Transaction ID: {transaction_id}")

        # Draw a line at the bottom
        y_position -= line_height
        c.line(inch, y_position, width - inch, y_position)

        # Footer
        y_position -= line_height
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2.0, y_position, "Thank you for banking with us!")

        # Save the PDF file
        c.save()

        return 1

    def print_passbook(self, name, transactions):
        self.file_path = f"receipts/passbook_{datetime.now().strftime('%H-%M-%S')}.pdf"
        c = canvas.Canvas(self.file_path, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 48)
        c.drawCentredString(width / 2.0, height - 1.5 * inch, "BANKSPHERE")

        # User's Name
        c.setFont("Helvetica-Bold", 16)
        c.drawString(inch, height - 2.25 * inch, f"Name: {name}")

        # Table Header
        data = [["Transaction ID", "Sender", "Receiver", "Amount", "Datetime"]]

        # Add transactions to the table
        for transaction in transactions:
            data.append([
                transaction[0],  # Transaction ID
                transaction[1],  # Sender
                transaction[2],  # Receiver
                f"{transaction[3]:,.2f}",  # Amount
                transaction[4]  # Datetime
            ])

        # Create the table
        table = Table(data, colWidths=[1.5 * inch] * 5)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Position the table
        table.wrapOn(c, width, height)
        table.drawOn(c, inch-0.3*inch, height - 3 * inch - len(data) * 0.25 * inch)

        # Footer
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2.0, inch, "Thank you for banking with us!")

        # Save the PDF file
        c.save()

        return 1

