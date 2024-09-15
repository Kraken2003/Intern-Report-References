import os
import streamlit as st
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.exceptions import HttpResponseError

load_dotenv()

def analyze_invoice(file):
    endpoint = os.getenv("DOCINTELLI_ENDPOINT")
    key = os.getenv("DOCINTELLI_KEY")

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-invoice", analyze_request=file, locale="en-US", content_type="application/octet-stream"
    )
    invoices: AnalyzeResult = poller.result()

    if invoices.documents:
        for idx, invoice in enumerate(invoices.documents):
            st.write(f"--------Analyzing invoice #{idx + 1}--------")
            if invoice.fields:
                vendor_name = invoice.fields.get("VendorName")
                if vendor_name:
                    st.write(f"Vendor Name: {vendor_name.get('content')} has confidence: {vendor_name.get('confidence')}")
                vendor_address = invoice.fields.get("VendorAddress")
                if vendor_address:
                    st.write(
                        f"Vendor Address: {vendor_address.get('content')} has confidence: {vendor_address.get('confidence')}"
                    )
                vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
                if vendor_address_recipient:
                    st.write(
                        f"Vendor Address Recipient: {vendor_address_recipient.get('content')} has confidence: {vendor_address_recipient.get('confidence')}"
                    )
                customer_name = invoice.fields.get("CustomerName")
                if customer_name:
                    st.write(
                        f"Customer Name: {customer_name.get('content')} has confidence: {customer_name.get('confidence')}"
                    )
                customer_id = invoice.fields.get("CustomerId")
                if customer_id:
                    st.write(f"Customer Id: {customer_id.get('content')} has confidence: {customer_id.get('confidence')}")
                customer_address = invoice.fields.get("CustomerAddress")
                if customer_address:
                    st.write(
                        f"Customer Address: {customer_address.get('content')} has confidence: {customer_address.get('confidence')}"
                    )
                customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
                if customer_address_recipient:
                    st.write(
                        f"Customer Address Recipient: {customer_address_recipient.get('content')} has confidence: {customer_address_recipient.get('confidence')}"
                    )
                invoice_id = invoice.fields.get("InvoiceId")
                if invoice_id:
                    st.write(f"Invoice Id: {invoice_id.get('content')} has confidence: {invoice_id.get('confidence')}")
                invoice_date = invoice.fields.get("InvoiceDate")
                if invoice_date:
                    st.write(
                        f"Invoice Date: {invoice_date.get('content')} has confidence: {invoice_date.get('confidence')}"
                    )
                invoice_total = invoice.fields.get("InvoiceTotal")
                if invoice_total:
                    st.write(
                        f"Invoice Total: {invoice_total.get('content')} has confidence: {invoice_total.get('confidence')}"
                    )
                due_date = invoice.fields.get("DueDate")
                if due_date:
                    st.write(f"Due Date: {due_date.get('content')} has confidence: {due_date.get('confidence')}")
                purchase_order = invoice.fields.get("PurchaseOrder")
                if purchase_order:
                    st.write(
                        f"Purchase Order: {purchase_order.get('content')} has confidence: {purchase_order.get('confidence')}"
                    )
                billing_address = invoice.fields.get("BillingAddress")
                if billing_address:
                    st.write(
                        f"Billing Address: {billing_address.get('content')} has confidence: {billing_address.get('confidence')}"
                    )
                billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
                if billing_address_recipient:
                    st.write(
                        f"Billing Address Recipient: {billing_address_recipient.get('content')} has confidence: {billing_address_recipient.get('confidence')}"
                    )
                shipping_address = invoice.fields.get("ShippingAddress")
                if shipping_address:
                    st.write(
                        f"Shipping Address: {shipping_address.get('content')} has confidence: {shipping_address.get('confidence')}"
                    )
                shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
                if shipping_address_recipient:
                    st.write(
                        f"Shipping Address Recipient: {shipping_address_recipient.get('content')} has confidence: {shipping_address_recipient.get('confidence')}"
                    )
                st.write("Invoice items:")
                items = invoice.fields.get("Items")
                if items:
                    for idx, item in enumerate(items.get("valueArray")):
                        st.write(f"...Item #{idx + 1}")
                        item_description = item.get("valueObject").get("Description")
                        if item_description:
                            st.write(
                                f"......Description: {item_description.get('content')} has confidence: {item_description.get('confidence')}"
                            )
                        item_quantity = item.get("valueObject").get("Quantity")
                        if item_quantity:
                            st.write(
                                f"......Quantity: {item_quantity.get('content')} has confidence: {item_quantity.get('confidence')}"
                            )
                        unit = item.get("valueObject").get("Unit")
                        if unit:
                            st.write(f"......Unit: {unit.get('content')} has confidence: {unit.get('confidence')}")
                        unit_price = item.get("valueObject").get("UnitPrice")
                        if unit_price:
                            unit_price_code = (
                                unit_price.get("valueCurrency").get("currencyCode")
                                if unit_price.get("valueCurrency").get("currencyCode")
                                else ""
                            )
                            st.write(
                                f"......Unit Price: {unit_price.get('content')}{unit_price_code} has confidence: {unit_price.get('confidence')}"
                            )
                        product_code = item.get("valueObject").get("ProductCode")
                        if product_code:
                            st.write(
                                f"......Product Code: {product_code.get('content')} has confidence: {product_code.get('confidence')}"
                            )
                        item_date = item.get("valueObject").get("Date")
                        if item_date:
                            st.write(
                                f"......Date: {item_date.get('content')} has confidence: {item_date.get('confidence')}"
                            )
                        tax = item.get("valueObject").get("Tax")
                        if tax:
                            st.write(f"......Tax: {tax.get('content')} has confidence: {tax.get('confidence')}")
                        amount = item.get("valueObject").get("Amount")
                        if amount:
                            st.write(f"......Amount: {amount.get('content')} has confidence: {amount.get('confidence')}")
                subtotal = invoice.fields.get("SubTotal")
                if subtotal:
                    st.write(f"Subtotal: {subtotal.get('content')} has confidence: {subtotal.get('confidence')}")
                total_tax = invoice.fields.get("TotalTax")
                if total_tax:
                    st.write(f"Total Tax: {total_tax.get('content')} has confidence: {total_tax.get('confidence')}")
                previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
                if previous_unpaid_balance:
                    st.write(
                        f"Previous Unpaid Balance: {previous_unpaid_balance.get('content')} has confidence: {previous_unpaid_balance.get('confidence')}"
                    )
                amount_due = invoice.fields.get("AmountDue")
                if amount_due:
                    st.write(f"Amount Due: {amount_due.get('content')} has confidence: {amount_due.get('confidence')}")
                service_start_date = invoice.fields.get("ServiceStartDate")
                if service_start_date:
                    st.write(
                        f"Service Start Date: {service_start_date.get('content')} has confidence: {service_start_date.get('confidence')}"
                    )
                service_end_date = invoice.fields.get("ServiceEndDate")
                if service_end_date:
                    st.write(
                        f"Service End Date: {service_end_date.get('content')} has confidence: {service_end_date.get('confidence')}"
                    )
                service_address = invoice.fields.get("ServiceAddress")
                if service_address:
                    st.write(
                        f"Service Address: {service_address.get('content')} has confidence: {service_address.get('confidence')}"
                    )
                service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
                if service_address_recipient:
                    st.write(
                        f"Service Address Recipient: {service_address_recipient.get('content')} has confidence: {service_address_recipient.get('confidence')}"
                    )
                remittance_address = invoice.fields.get("RemittanceAddress")
                if remittance_address:
                    st.write(
                        f"Remittance Address: {remittance_address.get('content')} has confidence: {remittance_address.get('confidence')}"
                    )
                remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
                if remittance_address_recipient:
                    st.write(
                        f"Remittance Address Recipient: {remittance_address_recipient.get('content')} has confidence: {remittance_address_recipient.get('confidence')}"
                    )

if __name__ == "__main__":

    st.title("Invoice Analyzer")
    uploaded_file = st.file_uploader("Choose an invoice image...", type=["jpg", "jpeg", "png", "pdf"])
    
    if uploaded_file is not None:
        try:
            analyze_invoice(uploaded_file)
        except HttpResponseError as error:
            # Examples of how to check an HttpResponseError
            # Check by error code:
            if error.error is not None:
                if error.error.code == "InvalidImage":
                    st.error(f"Received an invalid image error: {error.error}")
                if error.error.code == "InvalidRequest":
                    st.error(f"Received an invalid request error: {error.error}")
                # Raise the error again after printing it
                raise
            # If the inner error is None and then it is possible to check the message to get more information:
            if "Invalid request".casefold() in error.message.casefold():
                st.error(f"Uh-oh! Seems there was an invalid request: {error}")
            # Raise the error again
            raise
